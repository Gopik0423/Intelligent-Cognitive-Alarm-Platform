from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.challenge_selector import select_challenge
from services.answer_validation import validate_answer
from services.adaptive_engine import get_effective_difficulty_label, get_or_create_difficulty_record, apply_result
import random
from typing import Optional

from ai_generator import generate_challenge
from models.user import User
from database.db import SessionLocal
from models.challenge import Challenge
from models.performance import Performance
from schemas.challenge import ChallengeCreate, ChallengeAnswer
from scripts.challenge_engine import ChallengeEngine
from puzzle_difficulty import calculate_age, difficulty_for_age
from auth import verify_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
) -> User:
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_user_puzzle_settings(user_id: int, db: Session) -> tuple[str, int]:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return (
        difficulty_for_age(user.date_of_birth),
        calculate_age(user.date_of_birth),
    )


@router.post("/challenge")
def create_challenge(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    existing_challenge = db.query(Challenge).filter(
        Challenge.question == challenge.question
    ).first()

    if existing_challenge:
        return {"message": "Challenge already exists"}

    new_challenge = Challenge(
        challenge_type=challenge.challenge_type,
        question=challenge.question,
        correct_answer=challenge.correct_answer,
        difficulty=challenge.difficulty,
        points=challenge.points
    )

    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)

    return {
        "message": "Challenge created successfully",
        "challenge": new_challenge
    }


@router.get("/challenge/random/{challenge_type}")
def get_random_challenge(
    challenge_type: str,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if user_id is not None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        difficulty = get_effective_difficulty_label(db, user)
        selected = select_challenge(db, user_id=user_id, challenge_type=challenge_type, difficulty_label=difficulty)
        if selected is not None:
            return selected

        _, age = get_user_puzzle_settings(user_id, db)

        challenge_data = generate_challenge(
            challenge_type,
            difficulty,
            age=age
        )

        generated_challenge = Challenge(
            challenge_type=challenge_type,
            question=challenge_data["question"],
            correct_answer=challenge_data["correct_answer"],
            difficulty=challenge_data["difficulty"],
            points=challenge_data["points"],
        )

        db.add(generated_challenge)
        db.commit()
        db.refresh(generated_challenge)

        return generated_challenge

    challenges = db.query(Challenge).filter(
        Challenge.challenge_type == challenge_type
    ).all()

    if not challenges:
        challenge_data = generate_challenge(challenge_type, "Easy")

        generated_challenge = Challenge(
            challenge_type=challenge_type,
            question=challenge_data["question"],
            correct_answer=challenge_data["correct_answer"],
            difficulty=challenge_data["difficulty"],
            points=challenge_data["points"],
        )

        db.add(generated_challenge)
        db.commit()
        db.refresh(generated_challenge)

        return generated_challenge

    return random.choice(challenges)


@router.post("/challenge/{challenge_id}/submit")
def submit_answer(
    challenge_id: int,
    answer: ChallengeAnswer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not challenge:
        return {"message": "Challenge not found"}

    is_correct = validate_answer(answer.answer, challenge.correct_answer)

    new_performance = Performance(
        user_id=current_user.id,
        challenge_type=challenge.challenge_type,
        difficulty=challenge.difficulty,
        attempts=1,
        accuracy=1.0 if is_correct else 0.0,
        score=challenge.points if is_correct else 0,
        success=is_correct,
        completion_time=10,
    )

    db.add(new_performance)
    apply_result(get_or_create_difficulty_record(db, current_user), is_correct=is_correct)
    db.commit()

    if is_correct:
        return {
            "correct": True,
            "score": challenge.points
        }

    return {
        "correct": False,
        "score": 0
    }


@router.post("/challenge/start")
def start_challenge(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = current_user

    # Reconciled: uses the same earned, streak-based difficulty as
    # practice challenges and live alarm verification, instead of the
    # separate hybrid age+accuracy function that used to live in
    # routes/recommendation.py (calculate_next_difficulty -- now unused,
    # left in place but no longer called from anywhere; see that file's
    # docstring note).
    difficulty = get_effective_difficulty_label(db, user)

    age = calculate_age(user.date_of_birth)

    challenge_type = ChallengeEngine.select_random()

    challenge_data = generate_challenge(
        challenge_type,
        difficulty,
        age=age
    )

    new_challenge = Challenge(
        challenge_type=challenge_type,
        question=challenge_data["question"],
        correct_answer=challenge_data["correct_answer"],
        difficulty=challenge_data["difficulty"],
        points=challenge_data["points"]
    )

    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)

    return {
        "id": new_challenge.id,
        "challenge_type": new_challenge.challenge_type,
        "question": new_challenge.question,
        "difficulty": new_challenge.difficulty,
        "points": new_challenge.points
    }
