"""
adaptive_engine.py

Adaptive Difficulty Engine (consolidated).

This is the single source of truth for difficulty adjustment logic.
Previously this logic was duplicated: a streak-based version lived inline
in routes/difficulty.py (and was the one actually wired up and used), and
a separate, unused accuracy-threshold version lived here. This file now
owns the real logic; routes/difficulty.py just calls into it.

Primary mechanism -- streak-based (per attempt, live-updating):
    3 correct answers in a row -> difficulty increases by 1 (max level 4)
    2 wrong answers in a row   -> difficulty decreases by 1 (min level 1)

Secondary signal -- accuracy-based (used for analytics / recommendations,
not for directly changing a user's live difficulty level): given a batch
of past Performance records, estimate what difficulty level their overall
accuracy would suggest. Useful for spotting when the streak-based level
has drifted from a user's actual longer-term performance.

--- Reconciliation note (previously 3 separate, disconnected difficulty
systems existed in this codebase) ---
Before this change:
  - routes/verification.py (the live alarm-ringing flow) used ONLY
    puzzle_difficulty.difficulty_for_age(), and never updated a user's
    streak, so a user's earned difficulty level had zero effect on their
    actual alarm.
  - routes/difficulty.py / services/challenge_selector.py used ONLY the
    streak-based DifficultyLevel system.
  - routes/challenge.py's start_challenge used a third, hybrid
    age+accuracy function (routes.recommendation.calculate_next_difficulty).

get_or_create_difficulty_record() and get_effective_difficulty_label()
below are now the single entry point all three should use: a brand-new
user's streak record is seeded from their age (so age still matters for a
first impression), and every attempt after that -- including ones made
during a real alarm-ringing verification -- feeds the same streak system.
"""

from models.difficulty import DifficultyLevel
from puzzle_difficulty import difficulty_for_age
from services.tuning_config import (
    DIFFICULTY_MIN_LEVEL,
    DIFFICULTY_MAX_LEVEL,
    CORRECT_STREAK_TO_LEVEL_UP,
    FAIL_STREAK_TO_LEVEL_DOWN,
    ACCURACY_HARD_THRESHOLD,
    ACCURACY_MEDIUM_THRESHOLD,
)

# Kept as module-level names too, for backwards compatibility with any
# existing code importing these directly from this file.
MIN_LEVEL = DIFFICULTY_MIN_LEVEL
MAX_LEVEL = DIFFICULTY_MAX_LEVEL

_AGE_DIFFICULTY_TO_STARTING_LEVEL = {"Easy": 1, "Medium": 3, "Hard": 4}


def apply_result(record, is_correct: bool):
    """
    Update a DifficultyLevel record in place based on a single answer result.
    `record` needs: difficulty_level, correct_streak, fail_streak attributes.
    Returns the same record, mutated.
    """
    if is_correct:
        record.correct_streak += 1
        record.fail_streak = 0
        if record.correct_streak >= CORRECT_STREAK_TO_LEVEL_UP and record.difficulty_level < MAX_LEVEL:
            record.difficulty_level += 1
            record.correct_streak = 0
    else:
        record.fail_streak += 1
        record.correct_streak = 0
        if record.fail_streak >= FAIL_STREAK_TO_LEVEL_DOWN and record.difficulty_level > MIN_LEVEL:
            record.difficulty_level -= 1
            record.fail_streak = 0

    return record


def set_level(record, level: int):
    """Directly set a difficulty level (e.g. an explicit user/admin override)."""
    record.difficulty_level = level
    record.correct_streak = 0
    record.fail_streak = 0
    return record


def estimate_accuracy_level(performances) -> str:
    """
    Secondary signal: given a list of Performance records, estimate what
    difficulty label ("Easy" / "Medium" / "Hard") the user's overall
    accuracy would suggest. This is informational -- used by analytics /
    recommendations -- and does not directly move a user's live streak-based
    difficulty_level.
    """
    if not performances:
        return "Easy"

    total = len(performances)
    correct = sum(1 for p in performances if p.success)
    accuracy = (correct / total) * 100

    if accuracy >= ACCURACY_HARD_THRESHOLD:
        return "Hard"
    elif accuracy >= ACCURACY_MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "Easy"


def get_or_create_difficulty_record(db, user) -> DifficultyLevel:
    """
    The one place a DifficultyLevel record should be fetched or created from.
    New users are seeded from age (via difficulty_for_age), so a first-time
    user still gets an age-appropriate starting point; every attempt after
    that updates via apply_result(), regardless of whether it happened
    through practice challenges or a live alarm verification.
    """
    record = db.query(DifficultyLevel).filter(DifficultyLevel.user_id == user.id).first()
    if record:
        return record

    age_label = difficulty_for_age(user.date_of_birth)
    starting_level = _AGE_DIFFICULTY_TO_STARTING_LEVEL.get(age_label, DIFFICULTY_MIN_LEVEL)

    record = DifficultyLevel(user_id=user.id, difficulty_level=starting_level)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_effective_difficulty_label(db, user) -> str:
    """
    The single function every part of the app (practice challenges,
    /difficulty endpoints, and live alarm verification) should call to get
    a user's current difficulty as an "Easy"/"Medium"/"Hard" label.
    """
    from services.challenge_selector import map_level_to_difficulty
    record = get_or_create_difficulty_record(db, user)
    return map_level_to_difficulty(record.difficulty_level)
