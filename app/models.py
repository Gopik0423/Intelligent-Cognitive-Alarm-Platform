from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import CheckConstraint, DateTime, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ChallengeType(StrEnum):
    """Supported cognitive challenge categories."""

    math_problems = "Math Problems"
    logic_puzzles = "Logic Puzzles"
    memory_challenges = "Memory Challenges"
    word_games = "Word Games"
    pattern_recognition = "Pattern Recognition"
    riddles = "Riddles"
    quick_quizzes = "Quick Quizzes"


class ChallengeDifficulty(StrEnum):
    """Supported difficulty levels."""

    beginner = "Beginner"
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    expert = "Expert"


class Challenge(Base):
    """ORM model for cognitive challenges."""

    __tablename__ = "challenges"
    __table_args__ = (
        CheckConstraint(
            "type IN ('Math Problems', 'Logic Puzzles', 'Memory Challenges', 'Word Games', 'Pattern Recognition', 'Riddles', 'Quick Quizzes')",
            name="ck_challenges_type",
        ),
        CheckConstraint(
            "difficulty IN ('Beginner', 'Easy', 'Medium', 'Hard', 'Expert')",
            name="ck_challenges_difficulty",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    time_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
