import pandas as pd


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
        "average_score": round(df["score"].mean(), 2),
        "average_completion_time": round(df["completion_time"].mean(), 2),
        "success_rate": round(df["success"].mean() * 100, 2),
        "average_wakeup_consistency": round(df["wakeup_consistency"].mean(), 2),
        "average_challenge_completion": round(df["challenge_completion"].mean(), 2),
        "average_snooze_count": round(df["snooze_count"].mean(), 2),
        "average_sleep_schedule_adherence": round(df["sleep_schedule_adherence"].mean(), 2),
    }
