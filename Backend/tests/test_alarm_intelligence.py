from datetime import datetime, timedelta
from types import SimpleNamespace

from services.adaptive_engine import apply_result
from services.alarm_intelligence import build_alarm_intelligence


def _performance(index, success, snoozes, accuracy):
    return SimpleNamespace(
        success=success,
        snooze_count=snoozes,
        accuracy=accuracy,
        wakeup_consistency=70,
        challenge_type="math",
        completed_at=datetime(2026, 1, 1) + timedelta(minutes=index),
    )


def test_three_correct_results_raise_difficulty():
    record = SimpleNamespace(difficulty_level=1, correct_streak=0, fail_streak=0)
    for _ in range(3):
        apply_result(record, True)
    assert (record.difficulty_level, record.correct_streak, record.fail_streak) == (2, 0, 0)


def test_two_failed_results_lower_difficulty():
    record = SimpleNamespace(difficulty_level=3, correct_streak=0, fail_streak=0)
    apply_result(record, False)
    apply_result(record, False)
    assert (record.difficulty_level, record.correct_streak, record.fail_streak) == (2, 0, 0)


def test_alarm_recommendation_uses_behavior_and_has_one_difficulty_action():
    performances = [
        _performance(0, True, 0, 1.0),
        _performance(1, True, 0, 1.0),
        _performance(2, True, 3, 1.0),
        _performance(3, True, 4, 1.0),
    ]
    intelligence = build_alarm_intelligence(
        performances, SimpleNamespace(difficulty_level=2, correct_streak=0, fail_streak=0)
    )
    actions = [item["action"] for item in intelligence["recommendations"]]
    assert intelligence["validated"] is True
    assert intelligence["behavior"]["snooze_trend"] == "declining"
    assert sum(action in {"increase_difficulty", "decrease_difficulty", "maintain_difficulty"} for action in actions) == 1
    assert "reduce_snoozing" in actions
