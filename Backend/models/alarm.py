from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Time,
    Date,
    DateTime,
    ForeignKey,
    func,
)
from database.db import Base


class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    label = Column(String, default="Alarm")
    alarm_time = Column(Time, nullable=False)

    alarm_type = Column(String, default="daily")

    # SQLite doesn't support ARRAY
    # Store repeat days as comma-separated string
    # Example: "1,2,3,4,5"
    repeat_days = Column(String, nullable=True)

    one_time_date = Column(Date, nullable=True)

    is_active = Column(Boolean, default=True)

    snooze_enabled = Column(Boolean, default=True)
    snooze_duration_minutes = Column(Integer, default=5)
    max_snooze_count = Column(Integer, default=3)

    challenge_type = Column(String, default="math")
    difficulty = Column(String, default="easy")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
