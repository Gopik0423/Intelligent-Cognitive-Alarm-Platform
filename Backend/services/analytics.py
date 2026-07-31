import pandas as pd


def _safe_mean(series, digits=2):
    """Round a pandas Series mean, safely handling all-None columns.

    Averaging a column that's entirely None/NaN (e.g. because a record
    never populated that field) produces NaN, which cannot be sent back
    as JSON. Fall back to 0 in that case, consistent with the "no data"
    default used elsewhere in this function.
    """
    value = series.mean()
    if pd.isna(value):
        return 0
    return round(float(value), digits)


def generate_analytics(performances):

    if not performances:
        return {
            "average_score": 0,
            "average_completion_time": 0,
            "success_rate": 0,
            "average_wakeup_consistency": 0,
            "average_challenge_completion": 0,
            "average_snooze_count": 0,
            "average_sleep_schedule_adherence": 0,
        }

    df = pd.DataFrame([
        {
            "score": p.score,
            "completion_time": p.completion_time,
            "success": p.success,
            "wakeup_consistency": p.wakeup_consistency,
            "challenge_completion": p.challenge_completion,
            "snooze_count": p.snooze_count,
            "sleep_schedule_adherence": p.sleep_schedule_adherence,
        }
        for p in performances
    ])

    return {
        "average_score": _safe_mean(df["score"]),
        "average_completion_time": _safe_mean(df["completion_time"]),
        "success_rate": _safe_mean(df["success"].astype(float) * 100),
        "average_wakeup_consistency": _safe_mean(df["wakeup_consistency"]),
        "average_challenge_completion": _safe_mean(df["challenge_completion"]),
        "average_snooze_count": _safe_mean(df["snooze_count"]),
        "average_sleep_schedule_adherence": _safe_mean(df["sleep_schedule_adherence"]),
    }
