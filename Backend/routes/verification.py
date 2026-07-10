import random
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database.db import SessionLocal
from Backend.models.alarm import Alarm
from Backend.models.user import User
from Backend.models.challenge import Challenge
from Backend.models.verification import WakeupVerification
from Backend.auth import verify_token

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


def _pick_challenge(db: Session, challenge_type: str = None) -> Challenge:
    q = db.query(Challenge)
    if challenge_type:
        q = q.filter(Challenge.challenge_type == challenge_type)
    challenges = q.all()
    if not challenges:
        raise HTTPException(status_code=404, detail="No challenges available for this type")
    return random.choice(challenges)


@router.post("/start/{alarm_id}")
def start_verification(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    challenge = _pick_challenge(db, alarm.challenge_type)

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
    }


@router.post("/{verification_id}/submit")
def submit_answer(verification_id: int, answer: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verification = db.query(WakeupVerification).filter(WakeupVerification.id == verification_id, WakeupVerification.user_id == current_user.id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification session not found")
    if verification.status != "pending":
        raise HTTPException(status_code=400, detail=f"Already ended: {verification.status}")

    challenge = db.query(Challenge).filter(Challenge.id == int(verification.challenge_id)).first()
    is_correct = challenge and answer.strip().lower() == challenge.correct_answer.strip().lower()
    verification.attempts += 1

    if is_correct:
        verification.consecutive_correct_count += 1
        if verification.consecutive_correct_count >= verification.consecutive_correct_required:
            verification.status = "success"
            verification.completed_at = datetime.utcnow()
            db.commit()
            return {"status": "success", "message": "Verified! Alarm can be dismissed."}
        next_challenge = _pick_challenge(db, verification.challenge_type)
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

    next_challenge = _pick_challenge(db, verification.challenge_type)
    verification.challenge_id = str(next_challenge.id)
    verification.current_question = next_challenge.question
    db.commit()
    return {"status": "pending", "correct": False, "next_question": next_challenge.question}


@router.get("/{verification_id}")
def get_verification_status(verification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verification = db.query(WakeupVerification).filter(WakeupVerification.id == verification_id, WakeupVerification.user_id == current_user.id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification session not found")
    return verification
