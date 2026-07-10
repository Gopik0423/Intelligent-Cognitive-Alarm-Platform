from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import require_role
from database.db import SessionLocal
from models.performance import Performance
from schemas.performance import PerformanceCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/performance")
def save_performance(
    performance: PerformanceCreate,
    db: Session = Depends(get_db)
):

    new_record = Performance(
        user_id=performance.user_id,
        challenge_type=performance.challenge_type,
        difficulty=performance.difficulty,
        completion_time=performance.completion_time,
        attempts=performance.attempts,
        score=performance.score,
        success=performance.success
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "Performance saved successfully",
        "data": new_record
    }
@router.get("/admin/performance")
def get_all_performance(
    payload=Depends(require_role("Admin")),
    db: Session = Depends(get_db)
):
    return db.query(Performance).all()