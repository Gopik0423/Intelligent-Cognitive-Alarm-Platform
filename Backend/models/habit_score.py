from sqlalchemy import Column, Integer, Float
from database.db import Base


class HabitScore(Base):
    __tablename__ = "habit_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)

    wake_up_consistency = Column(Float, default=0.0)
    challenge_completion = Column(Float, default=0.0)
    snooze_reduction = Column(Float, default=0.0)
    sleep_schedule_adherence = Column(Float, default=0.0)
    habit_score = Column(Float, default=0.0)
