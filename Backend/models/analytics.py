from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from Backend.database.db import Base


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    challenge_type = Column(String)

    completion_time = Column(Integer)

    snooze_count = Column(Integer)

    success = Column(Boolean)

    created_at = Column(DateTime, server_default=func.now())