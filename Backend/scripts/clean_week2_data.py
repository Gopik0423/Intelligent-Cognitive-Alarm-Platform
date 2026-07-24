"""
clean_week2_data.py

Reads performance_logs and analytics from the database, applies cleaning
rules to the issues found by audit_week2_data.py, and exports two clean
CSV files (the 'Clean dataset' deliverable). Does NOT modify the database.

Cleaning rules:
- blank challenge_type          -> row dropped (unfixable, no reliable value)
- accuracy outside 0.0-1.0      -> clamped into range (fixed)
- negative completion_time      -> converted to absolute value (fixed)
- orphaned user_id              -> row dropped (unfixable, no matching user)
- duplicate row                 -> extra copies dropped, first kept
- negative snooze_count         -> clamped to 0 (fixed)

Run from the project root:
    python -m Backend.scripts.clean_week2_data
"""

import csv
import os

from database.db import SessionLocal
from models.performance import Performance
from models.analytics import Analytics
from models.user import User

OUTPUT_DIR = "clean_data_export"


def clean():
    db = SessionLocal()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    valid_user_ids = {u.id for u in db.query(User).all()}

    performance_rows = db.query(Performance).all()
    analytics_rows = db.query(Analytics).all()

    dropped = {"performance_logs": 0, "analytics": 0}
    fixed = {"performance_logs": 0, "analytics": 0}

    # ---------- Clean Performance ----------
    clean_performance = []
    seen_perf = set()

    for row in performance_rows:
        was_fixed = False

        if not row.challenge_type or not row.challenge_type.strip():
            dropped["performance_logs"] += 1
            continue

        if row.user_id not in valid_user_ids:
            dropped["performance_logs"] += 1
            continue

        accuracy = row.accuracy
        if accuracy is None:
            dropped["performance_logs"] += 1
            continue
        if accuracy > 1.0:
            accuracy = 1.0
            was_fixed = True
        elif accuracy < 0.0:
            accuracy = 0.0
            was_fixed = True

        completion_time = row.completion_time
        if completion_time is None:
            dropped["performance_logs"] += 1
            continue
        if completion_time < 0:
            completion_time = abs(completion_time)
            was_fixed = True

        dup_key = (row.user_id, row.challenge_type, row.accuracy, row.completion_time, row.attempts)
        if dup_key in seen_perf:
            dropped["performance_logs"] += 1
            continue
        seen_perf.add(dup_key)

        if was_fixed:
            fixed["performance_logs"] += 1

        clean_performance.append({
            "id": row.id,
            "user_id": row.user_id,
            "challenge_type": row.challenge_type,
            "attempts": row.attempts,
            "accuracy": accuracy,
            "success": row.success,
            "completion_time": completion_time,
            "completed_at": row.completed_at,
        })

    # ---------- Clean Analytics ----------
    clean_analytics = []
    seen_analytics = set()

    for row in analytics_rows:
        was_fixed = False

        if not row.challenge_type or not row.challenge_type.strip():
            dropped["analytics"] += 1
            continue

        if row.user_id not in valid_user_ids:
            dropped["analytics"] += 1
            continue

        completion_time = row.completion_time
        if completion_time is None:
            dropped["analytics"] += 1
            continue
        if completion_time < 0:
            completion_time = abs(completion_time)
            was_fixed = True

        snooze_count = row.snooze_count
        if snooze_count is None:
            snooze_count = 0
            was_fixed = True
        elif snooze_count < 0:
            snooze_count = 0
            was_fixed = True

        dup_key = (row.user_id, row.challenge_type, row.completion_time, row.snooze_count, row.success)
        if dup_key in seen_analytics:
            dropped["analytics"] += 1
            continue
        seen_analytics.add(dup_key)

        if was_fixed:
            fixed["analytics"] += 1

        clean_analytics.append({
            "id": row.id,
            "user_id": row.user_id,
            "challenge_type": row.challenge_type,
            "completion_time": completion_time,
            "snooze_count": snooze_count,
            "success": row.success,
        })

    # ---------- Export ----------
    perf_path = os.path.join(OUTPUT_DIR, "performance_logs_clean.csv")
    with open(perf_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "user_id", "challenge_type", "attempts",
            "accuracy", "success", "completion_time", "completed_at"
        ])
        writer.writeheader()
        writer.writerows(clean_performance)

    analytics_path = os.path.join(OUTPUT_DIR, "analytics_clean.csv")
    with open(analytics_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "user_id", "challenge_type",
            "completion_time", "snooze_count", "success"
        ])
        writer.writeheader()
        writer.writerows(clean_analytics)

    # ---------- Report ----------
    print("=" * 60)
    print("WEEK 2 ATTEMPT-LOG DATA CLEANING REPORT")
    print("=" * 60)
    print(f"Performance: {len(performance_rows)} original -> {len(clean_performance)} clean "
          f"({fixed['performance_logs']} fixed, {dropped['performance_logs']} dropped)")
    print(f"Analytics:   {len(analytics_rows)} original -> {len(clean_analytics)} clean "
          f"({fixed['analytics']} fixed, {dropped['analytics']} dropped)")
    print()
    print(f"Clean data exported to:")
    print(f"  {perf_path}")
    print(f"  {analytics_path}")

    db.close()


if __name__ == "__main__":
    clean()
