from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Backend.database.db import SessionLocal
from Backend.models.alarm import Alarm
from Backend.models.user import User
from Backend.schemas.alarm import AlarmCreate, AlarmUpdate, AlarmOut
from Backend.auth import verify_token

router = APIRouter(prefix="/alarms", tags=["Alarms"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(payload=Depends(verify_token), db: Session = Depends(get_db)) -> User:
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/", response_model=AlarmOut)
def create_alarm(
    alarm_in: AlarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if alarm_in.alarm_type == "one_time" and not alarm_in.one_time_date:
        raise HTTPException(
            status_code=400, detail="one_time_date is required for one_time alarms"
        )

    alarm = Alarm(user_id=current_user.id, **alarm_in.dict())
    db.add(alarm)
    db.commit()
    db.refresh(alarm)
    return alarm


@router.get("/", response_model=List[AlarmOut])
def list_alarms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Alarm)
        .filter(Alarm.user_id == current_user.id)
        .order_by(Alarm.alarm_time.asc())
        .all()
    )


@router.get("/{alarm_id}", response_model=AlarmOut)
def get_alarm(
    alarm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alarm = (
        db.query(Alarm)
        .filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id)
        .first()
    )
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return alarm


@router.put("/{alarm_id}", response_model=AlarmOut)
def update_alarm(
    alarm_id: int,
    alarm_in: AlarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alarm = (
        db.query(Alarm)
        .filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id)
        .first()
    )
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    updates = alarm_in.dict(exclude_unset=True)
    for field, value in updates.items():
        setattr(alarm, field, value)

    db.commit()
    db.refresh(alarm)
    return alarm


@router.delete("/{alarm_id}")
def delete_alarm(
    alarm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alarm = (
        db.query(Alarm)
        .filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id)
        .first()
    )
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    db.delete(alarm)
    db.commit()
    return {"message": "Alarm deleted successfully"}


@router.patch("/{alarm_id}/toggle", response_model=AlarmOut)
def toggle_alarm(
    alarm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alarm = (
        db.query(Alarm)
        .filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id)
        .first()
    )
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    alarm.is_active = not alarm.is_active
    db.commit()
    db.refresh(alarm)
    return alarm