from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from database.db import Base


class AlarmEvent(Base):
    """An auditable wake-up occurrence, separate from the recurring alarm rule."""

    __tablename__ = "alarm_events"

    id = Column(Integer, primary_key=True, index=True)
    alarm_id = Column(Integer, ForeignKey("alarms.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="triggered")
    scheduled_for = Column(DateTime, nullable=False)
    triggered_at = Column(DateTime, server_default=func.now(), nullable=False)
    snooze_count = Column(Integer, nullable=False, default=0)
    verification_id = Column(Integer, ForeignKey("wakeup_verifications.id"), nullable=True)
    dismissed_at = Column(DateTime, nullable=True)
