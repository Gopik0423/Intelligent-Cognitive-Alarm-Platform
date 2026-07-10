from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Challenge
from app.schemas import ChallengeCreate, ChallengeUpdate


def get_challenges(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    challenge_type: str | None = None,
    difficulty: str | None = None,
) -> list[Challenge]:
    """Return a filtered, paginated list of challenges."""

    statement = select(Challenge)

    if challenge_type is not None:
        statement = statement.where(Challenge.type == challenge_type)
    if difficulty is not None:
        statement = statement.where(Challenge.difficulty == difficulty)

    statement = statement.order_by(Challenge.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def get_challenge(db: Session, challenge_id: int) -> Challenge | None:
    """Fetch a single challenge by primary key."""

    return db.get(Challenge, challenge_id)


def get_random_challenge(db: Session) -> Challenge | None:
    """Fetch one random challenge."""

    statement = select(Challenge).order_by(Challenge.id)
    challenges = list(db.scalars(statement).all())
    if not challenges:
        return None

    from random import choice

    return choice(challenges)


def create_challenge(db: Session, challenge_in: ChallengeCreate) -> Challenge:
    """Create a challenge and persist it."""

    challenge = Challenge(
        type=challenge_in.type.value,
        difficulty=challenge_in.difficulty.value,
        question=challenge_in.question,
        answer=challenge_in.answer,
        options=challenge_in.options,
        hint=challenge_in.hint,
        explanation=challenge_in.explanation,
        time_limit=challenge_in.time_limit,
        points=challenge_in.points,
    )
    db.add(challenge)
    try:
        db.commit()
        db.refresh(challenge)
    except SQLAlchemyError:
        db.rollback()
        raise
    return challenge


def update_challenge(
    db: Session,
    challenge: Challenge,
    challenge_in: ChallengeUpdate,
) -> Challenge:
    """Apply partial updates to an existing challenge."""

    update_data = challenge_in.model_dump(exclude_unset=True)
    for field_name, value in update_data.items():
        if field_name in {"type", "difficulty"} and value is not None:
            setattr(challenge, field_name, value.value)
        else:
            setattr(challenge, field_name, value)

    try:
        db.commit()
        db.refresh(challenge)
    except SQLAlchemyError:
        db.rollback()
        raise
    return challenge


def delete_challenge(db: Session, challenge: Challenge) -> None:
    """Delete a challenge from the database."""

    db.delete(challenge)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
