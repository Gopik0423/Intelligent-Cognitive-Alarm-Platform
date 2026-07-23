from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from Backend.database.db import Base


class Performance(Base):
    __tablename__ = "performance_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    challenge_type = Column(String, nullable=False)

    difficulty = Column(String)

    completion_time = Column(Float, nullable=False)

    attempts = Column(Integer, nullable=False)

    score = Column(Integer)

    accuracy = Column(Float, nullable=False)

    success = Column(Boolean, nullable=False)

    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Week 3 Metrics
    wakeup_consistency = Column(Float)

    challenge_completion = Column(Float)

    snooze_count = Column(Integer)

    sleep_schedule_adherence = Column(Float)