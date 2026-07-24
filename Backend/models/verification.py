from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from database.db import Base


class WakeupVerification(Base):
    __tablename__ = "wakeup_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alarm_id = Column(Integer, ForeignKey("alarms.id"), nullable=False)

    status = Column(String, default="pending")
    challenge_type = Column(String, nullable=True)
    challenge_id = Column(String, nullable=True)
    current_question = Column(String, nullable=True)

    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    consecutive_correct_required = Column(Integer, default=1)
    consecutive_correct_count = Column(Integer, default=0)

    time_limit_seconds = Column(Integer, default=60)

    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
