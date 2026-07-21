from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backend.database.db import SessionLocal
from Backend.models.analytics import Analytics

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}")
def get_recommendation(
    user_id: int,
    db: Session = Depends(get_db)
):

    latest = (
        db.query(Analytics)
        .filter(Analytics.user_id == user_id)
        .order_by(Analytics.id.desc())
        .first()
    )

    if latest is None:
        return {
            "message": "No analytics found"
        }

    recommendations = []

    if latest.snooze_count >= 3:
        recommendations.append("Reduce snoozing.")

    if latest.completion_time > 30:
        recommendations.append("Try easier challenges.")

    if latest.success:
        recommendations.append("Excellent consistency! Keep it up.")

    if not recommendations:
        recommendations.append("Maintain your current routine.")

    return {
        "user_id": user_id,
        "recommendations": recommendations
    }