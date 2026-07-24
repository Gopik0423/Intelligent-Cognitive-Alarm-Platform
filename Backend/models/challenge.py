from sqlalchemy import Column, Integer, String
from database.db import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    challenge_type = Column(String)
    question = Column(String)
    correct_answer = Column(String)
    difficulty = Column(String)
    points = Column(Integer)
