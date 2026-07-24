from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Time
from Backend.database.db import Base


class WakeGoal(Base):
    __tablename__ = "wake_goals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    goal_time = Column(Time, nullable=False)

    description = Column(String, nullable=False)

    is_enabled = Column(Boolean, default=True)