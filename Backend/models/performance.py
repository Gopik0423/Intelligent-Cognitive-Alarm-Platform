from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base


class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    challenge_type = Column(String)
    difficulty = Column(String)
    completion_time = Column(Integer)
    attempts = Column(Integer)
    score = Column(Integer)
    success = Column(Boolean)