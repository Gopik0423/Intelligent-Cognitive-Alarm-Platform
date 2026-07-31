from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.habit_score import HabitScore
from schemas.habit_score import HabitScoreResponse, HabitScoreUpdateRequest, HabitMetrics
from services.habit_score import calculate_habit_score

router = APIRouter(prefix="/habit-score", tags=["Habit Score"])


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

    # Single source of truth for the weighted formula now lives in
    # services/habit_score.py (also used by routes/analytics.py).
    record.habit_score = calculate_habit_score(
        wakeup_consistency=metrics.wake_up_consistency,
        challenge_completion=metrics.challenge_completion,
        snooze_reduction=metrics.snooze_reduction,
        sleep_schedule_adherence=metrics.sleep_schedule_adherence,
    )

    db.commit()
    db.refresh(record)
    return record
