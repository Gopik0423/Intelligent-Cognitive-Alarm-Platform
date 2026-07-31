from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.performance import Performance
from services.analytics import generate_analytics
from services.habit_score import calculate_habit_score
from services.behavioral_analytics import analyze_behavior
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
@router.get("/{user_id}/behavior")
def get_behavioral_analytics(user_id: int, db: Session = Depends(get_db)):
    performances = (
        db.query(Performance)
        .filter(Performance.user_id == user_id)
        .all()
    )
    if not performances:
        return {"message": "No performance found"}
    return analyze_behavior(performances)
