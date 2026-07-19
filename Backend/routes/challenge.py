from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random
from Backend.ai_generator import generate_challenge
from Backend.models.performance import Performance
from Backend.database.db import SessionLocal
from Backend.models.challenge import Challenge
from Backend.schemas.challenge import ChallengeCreate, ChallengeAnswer
from Backend.schemas.challenge import StartChallenge
from Backend.scripts.challenge_engine import ChallengeEngine
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_difficulty(user_id: int, db: Session):

    latest = (
        db.query(Performance)
        .filter(Performance.user_id == user_id)
        .order_by(Performance.id.desc())
        .first()
    )

    if latest is None:
        return "Easy"

    if latest.completion_time < 15:
        return "Hard"

    elif latest.completion_time < 30:
        return "Medium"

    else:
        return "Easy"

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
def get_random_challenge(challenge_type: str, db: Session = Depends(get_db)):

    challenges = db.query(Challenge).filter(
        Challenge.challenge_type == challenge_type
    ).all()

    if not challenges:
        return {"message": "No challenges found"}

    return random.choice(challenges)


@router.post("/challenge/{challenge_id}/submit")
def submit_answer(
    challenge_id: int,
    answer: ChallengeAnswer,
    db: Session = Depends(get_db)
):

    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not challenge:
        return {"message": "Challenge not found"}

    user_answer = answer.answer.strip().lower()

    correct_answer = challenge.correct_answer.strip().lower()
    is_correct = user_answer == correct_answer

    new_performance = Performance(
    user_id=1,
    challenge_type=challenge.challenge_type,
    difficulty=challenge.difficulty,
    completion_time=10,
    attempts=1,
    score=challenge.points if is_correct else 0,
    success=is_correct
    )

    db.add(new_performance)
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
    request: StartChallenge,
    db: Session = Depends(get_db)
):

    difficulty = get_user_difficulty(
        request.user_id,
        db
    )
    challenge_type = ChallengeEngine.select_random()

    challenge_data = generate_challenge(
        challenge_type,
        difficulty
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
        "question": new_challenge.question,
        "difficulty": new_challenge.difficulty,
        "points": new_challenge.points
    }
