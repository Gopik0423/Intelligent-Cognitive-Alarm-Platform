from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.alarm import Alarm
from schemas.alarm import AlarmCreate, AlarmUpdate, AlarmResponse

router = APIRouter(prefix="/alarms", tags=["Alarm"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/", response_model=AlarmResponse)
def create_alarm(alarm: AlarmCreate, db: Session = Depends(get_db)):
    new_alarm = Alarm(
        user_id=alarm.user_id,
        title=alarm.title,
        alarm_time=alarm.alarm_time,
        days=alarm.days,
        ringtone=alarm.ringtone,
        vibration=alarm.vibration,
    )

    db.add(new_alarm)
    db.commit()
    db.refresh(new_alarm)

    return new_alarm


# GET ALL
@router.get("/", response_model=list[AlarmResponse])
def get_alarms(db: Session = Depends(get_db)):
    return db.query(Alarm).all()


# GET ONE
@router.get("/{alarm_id}", response_model=AlarmResponse)
def get_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()

    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    return alarm


# UPDATE
@router.put("/{alarm_id}", response_model=AlarmResponse)
def update_alarm(
    alarm_id: int,
    alarm_update: AlarmUpdate,
    db: Session = Depends(get_db),
):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()

    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    update_data = alarm_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(alarm, key, value)

    db.commit()
    db.refresh(alarm)

    return alarm


# TOGGLE
@router.patch("/{alarm_id}/toggle", response_model=AlarmResponse)
def toggle_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()

    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    alarm.is_active = not alarm.is_active

    db.commit()
    db.refresh(alarm)

    return alarm


# DELETE
@router.delete("/{alarm_id}")
def delete_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()

    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")

    db.delete(alarm)
    db.commit()

    return {"message": "Alarm deleted successfully"}