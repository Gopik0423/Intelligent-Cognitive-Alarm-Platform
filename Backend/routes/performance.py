from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import require_role
from database.db import SessionLocal
from models.performance import Performance
from schemas.performance import PerformanceCreate, PerformanceOut

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/performance/log", response_model=PerformanceOut)
def log_performance(
    perf: PerformanceCreate,
    db: Session = Depends(get_db)
):
    new = Performance(
        user_id=perf.user_id,
        challenge_type=perf.challenge_type,
        difficulty="Easy",
        attempts=perf.attempts,
        accuracy=perf.accuracy,
        score=perf.score,
        success=perf.success,
        completion_time=perf.completion_time,

        wakeup_consistency=perf.wakeup_consistency,
        challenge_completion=perf.challenge_completion,
        snooze_count=perf.snooze_count,
        sleep_schedule_adherence=perf.sleep_schedule_adherence,
    )

    db.add(new)
    db.commit()
    db.refresh(new)

    return new


@router.get("/performance/user/{user_id}", response_model=list[PerformanceOut])
def get_user_performance(
    user_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Performance)
        .filter(Performance.user_id == user_id)
        .all()
    )


@router.get("/admin/performance", response_model=list[PerformanceOut])
def get_all_performance(
    payload=Depends(require_role("Admin")),
    db: Session = Depends(get_db),
):
    return db.query(Performance).all()
