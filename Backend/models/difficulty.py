from sqlalchemy import Column, Integer
from database.db import Base


class DifficultyLevel(Base):
    __tablename__ = "difficulty_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)

    difficulty_level = Column(Integer, default=1)
    correct_streak = Column(Integer, default=0)
    fail_streak = Column(Integer, default=0)
