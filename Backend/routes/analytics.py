from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backend.database.db import SessionLocal
from Backend.models.analytics import Analytics
from Backend.schemas.analytics import AnalyticsCreate

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_analytics(
    analytics: AnalyticsCreate,
    db: Session = Depends(get_db)
):

    new_record = Analytics(
        user_id=analytics.user_id,
        challenge_type=analytics.challenge_type,
        completion_time=analytics.completion_time,
        snooze_count=analytics.snooze_count,
        success=analytics.success
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "Analytics saved successfully",
        "data": new_record
    }