"""
challenge_selector.py

Challenge Selection Logic.

Given a user and a challenge type, picks an appropriate question from the
question bank (challenges table), taking into account:
  1. The user's current adaptive difficulty level (from DifficultyLevel).
  2. Recently-served questions for that user, to reduce immediate repeats.

Difficulty level mapping (DifficultyLevel.difficulty_level is 1-4, but the
question bank only has Easy / Medium / Hard):
    1, 2 -> Easy
    3    -> Medium
    4    -> Hard
"""

import random
from sqlalchemy.orm import Session

from models.challenge import Challenge
from models.difficulty import DifficultyLevel
from models.verification import WakeupVerification

RECENT_HISTORY_LIMIT = 5  # how many recent challenge_ids to avoid repeating


def map_level_to_difficulty(level: int) -> str:
    if level <= 2:
        return "Easy"
    if level == 3:
        return "Medium"
    return "Hard"


def _recent_challenge_ids(db: Session, user_id: int) -> set[int]:
    """Recent challenge_ids this user was served, from their verification history."""
    rows = (
        db.query(WakeupVerification.challenge_id)
        .filter(WakeupVerification.user_id == user_id)
        .filter(WakeupVerification.challenge_id.isnot(None))
        .order_by(WakeupVerification.started_at.desc())
        .limit(RECENT_HISTORY_LIMIT)
        .all()
    )
    ids = set()
    for (cid,) in rows:
        try:
            ids.add(int(cid))
        except (TypeError, ValueError):
            continue
    return ids


def select_challenge(db: Session, user_id: int, challenge_type: str, difficulty_label: str | None = None) -> Challenge | None:
    """
    Select a challenge for this user and type, adapted to their difficulty
    level and avoiding recently-seen questions where possible.

    Returns None if no challenge of this type exists at all.
    """
    difficulty_record = (
        db.query(DifficultyLevel)
        .filter(DifficultyLevel.user_id == user_id)
        .first()
    )
    target_difficulty = difficulty_label or map_level_to_difficulty(
        difficulty_record.difficulty_level if difficulty_record else 1
    )

    recent_ids = _recent_challenge_ids(db, user_id)

    # 1st choice: matching type + matching difficulty, excluding recent repeats
    pool = (
        db.query(Challenge)
        .filter(Challenge.challenge_type == challenge_type)
        .filter(Challenge.difficulty == target_difficulty)
        .all()
    )
    candidates = [c for c in pool if c.id not in recent_ids]
    if candidates:
        return random.choice(candidates)

    # 2nd choice: matching type + matching difficulty, repeats allowed
    # (the user has seen everything at this difficulty recently)
    if pool:
        return random.choice(pool)

    # 3rd choice: matching type, any difficulty, excluding recent repeats
    all_of_type = db.query(Challenge).filter(Challenge.challenge_type == challenge_type).all()
    candidates = [c for c in all_of_type if c.id not in recent_ids]
    if candidates:
        return random.choice(candidates)

    # last resort: matching type, any difficulty, repeats allowed
    if all_of_type:
        return random.choice(all_of_type)

    return None
