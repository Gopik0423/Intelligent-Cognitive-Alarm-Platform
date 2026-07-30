from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ai_generator import generate_challenge
from models.alarm import Alarm
from models.alarm_event import AlarmEvent
from models.challenge import Challenge
from models.verification import WakeupVerification
from puzzle_difficulty import calculate_age, difficulty_for_age
from services.notifications import send_alarm_notification


def trigger_alarm(db: Session, alarm: Alarm, user, scheduled_for: datetime | None = None) -> AlarmEvent:
    """Create one alarm occurrence and its cognitive challenge exactly once."""
    scheduled_for = scheduled_for or datetime.utcnow()
    existing = db.query(AlarmEvent).filter(
        AlarmEvent.alarm_id == alarm.id,
        AlarmEvent.status.in_(("triggered", "snoozed")),
    ).first()
    if existing:
        return existing

    difficulty = difficulty_for_age(user.date_of_birth)
    puzzle = generate_challenge(alarm.challenge_type or "math", difficulty, age=calculate_age(user.date_of_birth))
    challenge = Challenge(challenge_type=alarm.challenge_type, question=puzzle["question"],
                          correct_answer=puzzle["correct_answer"], difficulty=puzzle["difficulty"], points=puzzle["points"])
    db.add(challenge)
    db.flush()
    verification = WakeupVerification(user_id=user.id, alarm_id=alarm.id, status="pending",
        challenge_type=challenge.challenge_type, challenge_id=str(challenge.id), current_question=challenge.question,
        attempts=0, max_attempts=3, consecutive_correct_required=1, consecutive_correct_count=0,
        time_limit_seconds=alarm.challenge_time_limit_seconds or 60)
    db.add(verification)
    db.flush()
    event = AlarmEvent(alarm_id=alarm.id, user_id=user.id, scheduled_for=scheduled_for,
                       status="triggered", verification_id=verification.id)
    db.add(event)
    db.flush()
    send_alarm_notification(db, user.id, alarm.id, "Alarm: " + alarm.label,
                            "Wake up and complete your " + (alarm.challenge_type or "math") + " challenge.")
    return event


def is_due(alarm: Alarm, now: datetime) -> bool:
    if not alarm.is_active or alarm.alarm_time.hour != now.hour or alarm.alarm_time.minute != now.minute:
        return False
    if alarm.alarm_type == "one_time":
        return alarm.one_time_date == now.date()
    if alarm.alarm_type == "weekly":
        days = {int(day) for day in (alarm.repeat_days or "").split(",") if day}
        return now.weekday() in days
    return True  # daily and smart (the client selects the smart target time)


def process_due_alarms(db: Session, now: datetime | None = None) -> int:
    now = (now or datetime.utcnow()).replace(second=0, microsecond=0)
    count = 0
    from models.user import User
    # Snoozed occurrences re-trigger independently of the recurring schedule.
    for event in db.query(AlarmEvent).filter(AlarmEvent.status == "snoozed", AlarmEvent.scheduled_for <= now).all():
        alarm = db.query(Alarm).get(event.alarm_id)
        user = db.query(User).get(event.user_id)
        event.status, event.triggered_at = "triggered", now
        send_alarm_notification(db, user.id, alarm.id, "Alarm: " + alarm.label, "Snooze is over. Complete your challenge.")
        count += 1
    for alarm in db.query(Alarm).filter_by(is_active=True).all():
        if not is_due(alarm, now):
            continue
        already_fired = db.query(AlarmEvent).filter(
            AlarmEvent.alarm_id == alarm.id,
            AlarmEvent.scheduled_for == now,
        ).first()
        if not already_fired:
            trigger_alarm(db, alarm, db.query(User).get(alarm.user_id), now)
            if alarm.alarm_type == "one_time":
                alarm.is_active = False
            count += 1
    db.commit()
    return count
