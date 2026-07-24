from sqlalchemy import Column, Integer, Time, ForeignKey
from database.db import Base


class Sleep(Base):
    __tablename__ = "sleep_schedule"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sleep_time = Column(Time, nullable=False)

    wake_time = Column(Time, nullable=False)
