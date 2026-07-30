from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.alarm import Alarm
from models.alarm_event import AlarmEvent
from models.device_token import DeviceToken
from models.notification_log import NotificationLog
from models.user import User
from schemas.alarm import AlarmCreate, AlarmUpdate, AlarmOut, DeviceTokenCreate, SnoozeRequest
from auth import verify_token
from services.alarm_runtime import trigger_alarm
from services.notifications import send_alarm_notification

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
    values = alarm_in.model_dump()
    values["repeat_days"] = ",".join(map(str, values["repeat_days"])) if values["repeat_days"] else None
    alarm = Alarm(user_id=current_user.id, **values)
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

    updates = alarm_in.model_dump(exclude_unset=True)
    next_type = updates.get("alarm_type", alarm.alarm_type)
    next_date = updates.get("one_time_date", alarm.one_time_date)
    next_days = updates.get("repeat_days") if "repeat_days" in updates else ([int(day) for day in alarm.repeat_days.split(",") if day] if alarm.repeat_days else None)
    if next_type == "one_time" and not next_date:
        raise HTTPException(status_code=422, detail="one_time_date is required for one_time alarms")
    if next_type == "weekly" and not next_days:
        raise HTTPException(status_code=422, detail="repeat_days is required for weekly alarms")
    if "repeat_days" in updates:
        updates["repeat_days"] = ",".join(map(str, updates["repeat_days"])) if updates["repeat_days"] else None
    for field, value in updates.items():
        setattr(alarm, field, value)

    db.commit()
    db.refresh(alarm)
    return alarm


@router.post("/devices", status_code=201)
def register_device(device: DeviceTokenCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Register an FCM device token. Notification delivery falls back locally if FCM is not configured."""
    record = db.query(DeviceToken).filter(DeviceToken.token == device.token).first()
    if record and record.user_id != current_user.id:
        raise HTTPException(status_code=409, detail="Device token belongs to another user")
    if not record:
        record = DeviceToken(user_id=current_user.id, token=device.token, platform=device.platform)
        db.add(record)
    else:
        record.platform, record.is_active = device.platform, True
    db.commit()
    return {"id": record.id, "status": "registered"}


@router.get("/{alarm_id}", response_model=AlarmOut)
def get_alarm(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return alarm


@router.post("/{alarm_id}/trigger")
def trigger_alarm_now(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Trigger an alarm immediately; useful to bridge a mobile local alarm into the API workflow."""
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    event = trigger_alarm(db, alarm, current_user)
    db.commit()
    return {"event_id": event.id, "status": event.status, "verification_id": event.verification_id}


@router.post("/{alarm_id}/snooze")
def snooze_alarm(alarm_id: int, request: SnoozeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    event_query = db.query(AlarmEvent).filter(AlarmEvent.alarm_id == alarm_id, AlarmEvent.user_id == current_user.id)
    event = event_query.filter(AlarmEvent.id == request.event_id).first() if request.event_id else event_query.filter(AlarmEvent.status == "triggered").order_by(AlarmEvent.id.desc()).first()
    if not event or event.status != "triggered":
        raise HTTPException(status_code=409, detail="No active alarm event to snooze")
    if not alarm.snooze_enabled or event.snooze_count >= alarm.max_snooze_count:
        raise HTTPException(status_code=403, detail="Snooze limit reached; complete the challenge to dismiss")
    event.snooze_count += 1
    event.status = "snoozed"
    event.scheduled_for = datetime.utcnow() + timedelta(minutes=alarm.snooze_duration_minutes)
    db.commit()
    return {"event_id": event.id, "status": event.status, "snooze_count": event.snooze_count, "retrigger_at": event.scheduled_for}


@router.post("/{alarm_id}/dismiss")
def dismiss_alarm(alarm_id: int, event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(AlarmEvent).filter(AlarmEvent.id == event_id, AlarmEvent.alarm_id == alarm_id, AlarmEvent.user_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Alarm event not found")
    from models.verification import WakeupVerification
    verification = db.query(WakeupVerification).filter(WakeupVerification.id == event.verification_id).first()
    if not verification or verification.status != "success":
        raise HTTPException(status_code=403, detail="A successful cognitive challenge is required to dismiss this alarm")
    event.status, event.dismissed_at = "dismissed", datetime.utcnow()
    db.commit()
    return {"event_id": event.id, "status": event.status}


@router.get("/{alarm_id}/events")
def list_alarm_events(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(AlarmEvent).filter(AlarmEvent.alarm_id == alarm_id, AlarmEvent.user_id == current_user.id).order_by(AlarmEvent.id.desc()).limit(30).all()


@router.get("/{alarm_id}/notification-schedule")
def get_notification_schedule(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Client contract for scheduling its reliable OS-local alarm notification."""
    alarm = db.query(Alarm).filter(Alarm.id == alarm_id, Alarm.user_id == current_user.id).first()
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return {"alarm_id": alarm.id, "enabled": alarm.is_active, "time": alarm.alarm_time.isoformat(),
            "type": alarm.alarm_type, "repeat_days": [int(day) for day in alarm.repeat_days.split(",") if day] if alarm.repeat_days else [],
            "one_time_date": alarm.one_time_date, "notification": {"title": f"Alarm: {alarm.label}",
            "body": "Wake up and complete your cognitive challenge.", "channel": "alarm", "full_screen": True,
            "data": {"event": "alarm_triggered", "alarm_id": str(alarm.id)}}}


@router.get("/{alarm_id}/notifications")
def list_notification_history(alarm_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(NotificationLog).filter(NotificationLog.alarm_id == alarm_id, NotificationLog.user_id == current_user.id).order_by(NotificationLog.id.desc()).limit(50).all()


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
