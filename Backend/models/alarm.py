from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base


class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    title = Column(String, nullable=False)

    alarm_time = Column(String, nullable=False)

    days = Column(String, nullable=True)

    ringtone = Column(String, default="Default")

    vibration = Column(Boolean, default=True)

    is_active = Column(Boolean, default=True)