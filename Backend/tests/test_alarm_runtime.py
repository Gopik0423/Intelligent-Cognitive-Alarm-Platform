from datetime import date, datetime, time, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db import Base
from models.alarm import Alarm
from models.alarm_event import AlarmEvent
from models.notification_log import NotificationLog
from models.user import User
from models.verification import WakeupVerification
from services.alarm_runtime import is_due, process_due_alarms, trigger_alarm


def test_alarm_trigger_snooze_retrigger_and_notification_audit():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    user = User(name="Demo", email="demo@example.com", password="hash", role="User", date_of_birth=date(2000, 1, 1))
    session.add(user)
    session.flush()
    alarm = Alarm(user_id=user.id, label="Morning", alarm_time=time(7, 0), alarm_type="weekly", repeat_days="0,1,2,3,4",
                  challenge_type="math", challenge_time_limit_seconds=30, is_active=True)
    session.add(alarm)
    session.commit()

    event = trigger_alarm(session, alarm, user, datetime(2026, 7, 27, 7, 0))
    session.commit()
    assert event.status == "triggered"
    assert session.query(WakeupVerification).one().time_limit_seconds == 30
    assert session.query(NotificationLog).one().channel == "local"
    assert is_due(alarm, datetime(2026, 7, 27, 7, 0))

    event.status = "snoozed"
    event.scheduled_for = datetime.utcnow() - timedelta(minutes=1)
    session.commit()
    assert process_due_alarms(session) == 1
    assert session.query(AlarmEvent).one().status == "triggered"
