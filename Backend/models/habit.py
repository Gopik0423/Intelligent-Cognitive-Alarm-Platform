from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    habit_name = Column(String, nullable=False)

    productivity_type = Column(String, nullable=False)
