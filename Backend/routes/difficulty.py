from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from models.difficulty import DifficultyLevel
from schemas.difficulty import DifficultyResponse, DifficultyUpdateRequest
from services.adaptive_engine import apply_result, set_level

router = APIRouter(prefix="/difficulty", tags=["Difficulty"])


def _get_or_create(db: Session, user_id: int) -> DifficultyLevel:
    record = db.query(DifficultyLevel).filter(DifficultyLevel.user_id == user_id).first()
    if not record:
        record = DifficultyLevel(user_id=user_id)
        db.add(record)
        db.commit()
        db.refresh(record)
    return record


@router.get("/get", response_model=DifficultyResponse)
def get_difficulty(user_id: int, db: Session = Depends(get_db)):
    record = _get_or_create(db, user_id)
    return record


@router.post("/update", response_model=DifficultyResponse)
def update_difficulty(payload: DifficultyUpdateRequest, db: Session = Depends(get_db)):
    if payload.action == "set" and payload.level is None:
        raise HTTPException(status_code=400, detail="level is required when action='set'")

    record = _get_or_create(db, payload.user_id)

    if payload.action == "set":
        set_level(record, payload.level)
    elif payload.action == "correct":
        apply_result(record, is_correct=True)
    elif payload.action == "fail":
        apply_result(record, is_correct=False)

    db.commit()
    db.refresh(record)
    return record
