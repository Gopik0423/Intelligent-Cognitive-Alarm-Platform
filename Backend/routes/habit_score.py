from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.habit_score import HabitScore
from schemas.habit_score import HabitScoreResponse, HabitScoreUpdateRequest, HabitMetrics

router = APIRouter(prefix="/habit-score", tags=["Habit Score"])

WEIGHTS = {
    "wake_up_consistency": 0.35,
    "challenge_completion": 0.25,
    "snooze_reduction": 0.20,
    "sleep_schedule_adherence": 0.20,
}


def calculate_habit_score(metrics: HabitMetrics) -> float:
    score = (
        metrics.wake_up_consistency * WEIGHTS["wake_up_consistency"]
        + metrics.challenge_completion * WEIGHTS["challenge_completion"]
        + metrics.snooze_reduction * WEIGHTS["snooze_reduction"]
        + metrics.sleep_schedule_adherence * WEIGHTS["sleep_schedule_adherence"]
    )
    return round(score, 2)


@router.get("", response_model=HabitScoreResponse)
def get_habit_score(user_id: int, db: Session = Depends(get_db)):
    record = db.query(HabitScore).filter(HabitScore.user_id == user_id).first()
    if not record:
        record = HabitScore(user_id=user_id)
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


@router.post("", response_model=HabitScoreResponse)
def update_habit_score(payload: HabitScoreUpdateRequest, db: Session = Depends(get_db)):
    metrics = HabitMetrics(**payload.model_dump(exclude={"user_id"}))

    record = db.query(HabitScore).filter(HabitScore.user_id == payload.user_id).first()
    if not record:
        record = HabitScore(user_id=payload.user_id)
        db.add(record)

    record.wake_up_consistency = metrics.wake_up_consistency
    record.challenge_completion = metrics.challenge_completion
    record.snooze_reduction = metrics.snooze_reduction
    record.sleep_schedule_adherence = metrics.sleep_schedule_adherence
    record.habit_score = calculate_habit_score(metrics)

    db.commit()
    db.refresh(record)
    return record
