from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import ChallengeDifficulty, ChallengeType


class ChallengeBase(BaseModel):
    """Shared challenge fields."""

    type: ChallengeType = Field(..., description="Challenge category")
    difficulty: ChallengeDifficulty = Field(..., description="Difficulty level")
    question: str = Field(..., min_length=5, max_length=5000)
    answer: str = Field(..., min_length=1, max_length=5000)
    options: list[str] | None = Field(default=None)
    hint: str | None = Field(default=None, max_length=2000)
    explanation: str | None = Field(default=None, max_length=4000)
    time_limit: int = Field(..., ge=5, le=3600)
    points: int = Field(..., ge=1, le=1000)


class ChallengeCreate(ChallengeBase):
    """Payload for creating a new challenge."""


class ChallengeUpdate(BaseModel):
    """Payload for updating an existing challenge."""

    type: ChallengeType | None = None
    difficulty: ChallengeDifficulty | None = None
    question: str | None = Field(default=None, min_length=5, max_length=5000)
    answer: str | None = Field(default=None, min_length=1, max_length=5000)
    options: list[str] | None = None
    hint: str | None = Field(default=None, max_length=2000)
    explanation: str | None = Field(default=None, max_length=4000)
    time_limit: int | None = Field(default=None, ge=5, le=3600)
    points: int | None = Field(default=None, ge=1, le=1000)


class ChallengeRead(ChallengeBase):
    """Response model returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
