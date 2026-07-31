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
"""

MIN_LEVEL = 1
MAX_LEVEL = 4

CORRECT_STREAK_TO_LEVEL_UP = 3
FAIL_STREAK_TO_LEVEL_DOWN = 2


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

    if accuracy >= 80:
        return "Hard"
    elif accuracy >= 50:
        return "Medium"
    else:
        return "Easy"
