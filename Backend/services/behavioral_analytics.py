"""
behavioral_analytics.py

Behavioral Analytics.

Goes beyond simple averages (services/analytics.py) to detect patterns and
trends in a user's performance history:
  - Snooze pattern analysis: is snoozing trending up or down over time?
  - Wake-up behavior tracking: is accuracy/success trending up or down?
  - Productivity correlation: does higher snoozing line up with worse
    performance for this user?
  - Habit consistency monitoring: how stable (vs erratic) is their
    wake-up consistency score?

Requires at least 4 Performance records to detect a trend; with fewer,
returns "not_enough_data" rather than guessing.
"""

import pandas as pd

MIN_RECORDS_FOR_TREND = 4
TREND_THRESHOLD = 5.0  # minimum % point change for percentage-scale metrics (accuracy, consistency)
SNOOZE_TREND_THRESHOLD = 1.0  # snooze_count is a small raw number (0-6ish), not a percentage -- needs its own scale


def _trend_direction(before_avg: float, after_avg: float, lower_is_better: bool = False, threshold: float = TREND_THRESHOLD) -> str:
    diff = after_avg - before_avg
    if abs(diff) < threshold:
        return "stable"
    improving = diff < 0 if lower_is_better else diff > 0
    return "improving" if improving else "declining"


def analyze_behavior(performances) -> dict:
    if len(performances) < MIN_RECORDS_FOR_TREND:
        return {
            "status": "not_enough_data",
            "message": f"Need at least {MIN_RECORDS_FOR_TREND} attempts to detect behavioral trends.",
        }

    # Sort chronologically so "before" vs "after" actually means something
    ordered = sorted(performances, key=lambda p: p.completed_at)

    df = pd.DataFrame([
        {
            "accuracy": p.accuracy,
            "snooze_count": p.snooze_count or 0,
            "wakeup_consistency": p.wakeup_consistency or 0,
            "challenge_type": p.challenge_type,
        }
        for p in ordered
    ])

    midpoint = len(df) // 2
    earlier, later = df.iloc[:midpoint], df.iloc[midpoint:]

    snooze_trend = _trend_direction(
        earlier["snooze_count"].mean(), later["snooze_count"].mean(),
        lower_is_better=True, threshold=SNOOZE_TREND_THRESHOLD
    )
    accuracy_trend = _trend_direction(
        earlier["accuracy"].mean() * 100, later["accuracy"].mean() * 100
    )
    consistency_trend = _trend_direction(
        earlier["wakeup_consistency"].mean(), later["wakeup_consistency"].mean()
    )

    # Productivity correlation: do higher-snooze sessions line up with lower accuracy?
    correlation = None
    if df["snooze_count"].nunique() > 1 and df["accuracy"].nunique() > 1:
        correlation = round(float(df["snooze_count"].corr(df["accuracy"])), 2)

    most_common_type = df["challenge_type"].mode().iloc[0] if not df["challenge_type"].mode().empty else None

    return {
        "status": "ok",
        "records_analyzed": len(df),
        "snooze_trend": snooze_trend,
        "accuracy_trend": accuracy_trend,
        "wakeup_consistency_trend": consistency_trend,
        "snooze_accuracy_correlation": correlation,
        "correlation_note": (
            "Negative values mean more snoozing lines up with lower accuracy for this user."
            if correlation is not None else
            "Not enough variation in the data to compute a correlation yet."
        ),
        "most_common_challenge_type": most_common_type,
    }
