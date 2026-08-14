from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.alarm import Alarm
from models.user import User
from models.challenge import Challenge
from models.verification import WakeupVerification
from models.performance import Performance
from auth import verify_token
from ai_generator import generate_challenge
from puzzle_difficulty import calculate_age
from services.adaptive_engine import get_effective_difficulty_label, get_or_create_difficulty_record, apply_result

router = APIRouter(prefix="/verification", tags=["Wake-up Verification"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(payload=Depends(verify_token), db: Session = Depends(get_db)) -> User:
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def _generate_challenge(db: Session, challenge_type: str, difficulty: str, age=None) -> Challenge:
    """Create and persist one on-demand puzzle for an alarm verification."""
    puzzle = generate_challenge(challenge_type or "math", difficulty or "Easy", age=age)
    challenge = Challenge(
        challenge_type=challenge_type or "math",
        question=puzzle["question"],
        correct_answer=puzzle["correct_answer"],
        difficulty=puzzle["difficulty"],
        points=puzzle["points"],
    )
    db.add(challenge)
    db.flush()
    return challenge


def _pick_challenge(db: Session, challenge_type: str, difficulty: str, age=None) -> Challenge:
    """Generate a fresh age-appropriate puzzle for each verification attempt."""
    return _generate_challenge(db, challenge_type or "math", difficulty, age)


@router.post("/start/{alarm_id}")
def start_verification(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    # Reconciled: this now uses the same earned, streak-based difficulty
    # system as practice challenges and the /difficulty endpoints, instead
    # of an age-only lookup that ignored a user's actual performance.
    difficulty = get_effective_difficulty_label(db, current_user)
    challenge = _pick_challenge(db, alarm.challenge_type, difficulty, calculate_age(current_user.date_of_birth))

    verification = WakeupVerification(
        user_id=current_user.id,
        alarm_id=alarm.id,
        status="pending",
        challenge_type=challenge.challenge_type,
        challenge_id=str(challenge.id),
        current_question=challenge.question,
        attempts=0,
        max_attempts=3,
        consecutive_correct_required=1,
        consecutive_correct_count=0,
        time_limit_seconds=alarm.challenge_time_limit_seconds or 60,
    )
    db.add(verification)
    db.commit()
    db.refresh(verification)

    return {
        "verification_id": verification.id,
        "alarm_id": verification.alarm_id,
        "status": verification.status,
        "challenge_type": verification.challenge_type,
        "challenge_id": verification.challenge_id,
        "question": verification.current_question,
        "attempts": verification.attempts,
        "max_attempts": verification.max_attempts,
        "time_limit_seconds": verification.time_limit_seconds,
        "deadline": verification.started_at + timedelta(seconds=verification.time_limit_seconds),
    }


@router.post("/{verification_id}/submit")
def submit_answer(verification_id: int, answer: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verification = db.query(WakeupVerification).filter(WakeupVerification.id == verification_id, WakeupVerification.user_id == current_user.id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification session not found")
    if verification.status != "pending":
        raise HTTPException(status_code=400, detail=f"Already ended: {verification.status}")
    deadline = verification.started_at + timedelta(seconds=verification.time_limit_seconds)
    if datetime.utcnow() >= deadline:
        verification.status = "timed_out"
        verification.completed_at = datetime.utcnow()
        db.commit()
        return {"status": "timed_out", "message": "Challenge time expired. Alarm will continue."}

    challenge = db.query(Challenge).filter(Challenge.id == int(verification.challenge_id)).first()
    is_correct = challenge and answer.strip().lower() == challenge.correct_answer.strip().lower()
    verification.attempts += 1

    # Reconciled: every real answer during an actual alarm now feeds the
    # same streak-based DifficultyLevel used everywhere else. Previously
    # this never happened, so a user's earned difficulty level had no
    # effect on their real alarm at all.
    difficulty_record = get_or_create_difficulty_record(db, current_user)
    apply_result(difficulty_record, is_correct=bool(is_correct))
    db.add(Performance(
        user_id=current_user.id,
        challenge_type=challenge.challenge_type if challenge else verification.challenge_type,
        difficulty=challenge.difficulty if challenge else get_effective_difficulty_label(db, current_user),
        attempts=1,
        accuracy=1.0 if is_correct else 0.0,
        score=challenge.points if is_correct and challenge else 0,
        success=bool(is_correct),
        completion_time=max(0, (datetime.utcnow() - verification.started_at).total_seconds()),
    ))

    if is_correct:
        verification.consecutive_correct_count += 1
        if verification.consecutive_correct_count >= verification.consecutive_correct_required:
            verification.status = "success"
            verification.completed_at = datetime.utcnow()
            db.commit()
            return {"status": "success", "message": "Verified! Alarm can be dismissed."}
        difficulty = get_effective_difficulty_label(db, current_user)
        next_challenge = _pick_challenge(db, verification.challenge_type, difficulty, calculate_age(current_user.date_of_birth))
        verification.challenge_id = str(next_challenge.id)
        verification.current_question = next_challenge.question
        db.commit()
        return {"status": "pending", "correct": True, "next_question": next_challenge.question}

    verification.consecutive_correct_count = 0
    if verification.attempts >= verification.max_attempts:
        verification.status = "failed"
        verification.completed_at = datetime.utcnow()
        db.commit()
        return {"status": "failed", "message": "Verification failed. Alarm will re-trigger."}

    difficulty = get_effective_difficulty_label(db, current_user)
    next_challenge = _pick_challenge(db, verification.challenge_type, difficulty, calculate_age(current_user.date_of_birth))
    verification.challenge_id = str(next_challenge.id)
    verification.current_question = next_challenge.question
    db.commit()
    return {"status": "pending", "correct": False, "next_question": next_challenge.question}


@router.get("/{verification_id}")
def get_verification_status(verification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verification = db.query(WakeupVerification).filter(WakeupVerification.id == verification_id, WakeupVerification.user_id == current_user.id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification session not found")
    if verification.status == "pending" and datetime.utcnow() >= verification.started_at + timedelta(seconds=verification.time_limit_seconds):
        verification.status, verification.completed_at = "timed_out", datetime.utcnow()
        db.commit()
    remaining = max(0, int((verification.started_at + timedelta(seconds=verification.time_limit_seconds) - datetime.utcnow()).total_seconds()))
    return {"id": verification.id, "alarm_id": verification.alarm_id, "status": verification.status,
            "question": verification.current_question, "attempts": verification.attempts,
            "max_attempts": verification.max_attempts, "time_limit_seconds": verification.time_limit_seconds,
            "seconds_remaining": remaining}
