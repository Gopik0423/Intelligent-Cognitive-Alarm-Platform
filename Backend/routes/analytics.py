from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backend.database.db import SessionLocal
from Backend.models.performance import Performance
from Backend.services.analytics import generate_analytics
from Backend.services.habit_score import calculate_habit_score

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}")
def get_analytics(user_id: int, db: Session = Depends(get_db)):

    performances = (
        db.query(Performance)
        .filter(Performance.user_id == user_id)
        .all()
    )

    if not performances:
        return {"message": "No performance found"}

    analytics = generate_analytics(performances)

    habit_score = calculate_habit_score(
        wakeup_consistency=analytics["average_wakeup_consistency"],
        challenge_completion=analytics["average_challenge_completion"],
        snooze_reduction=max(
            0, 100 - analytics["average_snooze_count"] * 20
        ),
        sleep_schedule_adherence=analytics["average_sleep_schedule_adherence"],
    )

    analytics["habit_score"] = habit_score

    return analytics