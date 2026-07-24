"""
audit_week2_data.py

Audits the performance_logs and analytics tables for data quality issues:
- missing/blank required fields
- out-of-range values
- duplicate rows
- orphaned user_id references

This script only REPORTS problems. It does not change any data.
Run from the project root:
    python -m Backend.scripts.audit_week2_data
"""

from collections import defaultdict

from database.db import SessionLocal
from models.performance import Performance
from models.analytics import Analytics
from models.user import User


def audit():
    db = SessionLocal()

    valid_user_ids = {u.id for u in db.query(User).all()}

    performance_rows = db.query(Performance).all()
    analytics_rows = db.query(Analytics).all()

    issues = defaultdict(list)

    # ---------- Audit Performance ----------
    seen_perf = set()
    for row in performance_rows:
        problems = []

        if not row.challenge_type or not row.challenge_type.strip():
            problems.append("blank challenge_type")

        if row.accuracy is None or not (0.0 <= row.accuracy <= 1.0):
            problems.append(f"accuracy out of range ({row.accuracy})")

        if row.completion_time is None or row.completion_time < 0:
            problems.append(f"negative/invalid completion_time ({row.completion_time})")

        if row.attempts is None or row.attempts < 1:
            problems.append(f"invalid attempts ({row.attempts})")

        if row.user_id not in valid_user_ids:
            problems.append(f"orphaned user_id ({row.user_id}, no matching user)")

        dup_key = (row.user_id, row.challenge_type, row.accuracy, row.completion_time, row.attempts)
        if dup_key in seen_perf:
            problems.append("duplicate of another Performance row")
        seen_perf.add(dup_key)

        if problems:
            issues["performance_logs"].append((row.id, problems))

    # ---------- Audit Analytics ----------
    seen_analytics = set()
    for row in analytics_rows:
        problems = []

        if not row.challenge_type or not row.challenge_type.strip():
            problems.append("blank challenge_type")

        if row.completion_time is None or row.completion_time < 0:
            problems.append(f"negative/invalid completion_time ({row.completion_time})")

        if row.snooze_count is None or row.snooze_count < 0:
            problems.append(f"negative/invalid snooze_count ({row.snooze_count})")

        if row.user_id not in valid_user_ids:
            problems.append(f"orphaned user_id ({row.user_id}, no matching user)")

        dup_key = (row.user_id, row.challenge_type, row.completion_time, row.snooze_count, row.success)
        if dup_key in seen_analytics:
            problems.append("duplicate of another Analytics row")
        seen_analytics.add(dup_key)

        if problems:
            issues["analytics"].append((row.id, problems))

    # ---------- Report ----------
    print("=" * 60)
    print("WEEK 2 ATTEMPT-LOG DATA AUDIT REPORT")
    print("=" * 60)
    print(f"Total Performance rows checked: {len(performance_rows)}")
    print(f"Total Analytics rows checked:   {len(analytics_rows)}")
    print()

    for table_name in ("performance_logs", "analytics"):
        rows = issues.get(table_name, [])
        print(f"--- {table_name}: {len(rows)} row(s) with issues ---")
        for row_id, problems in rows:
            print(f"  Row id={row_id}: {'; '.join(problems)}")
        print()

    total_issues = len(issues.get("performance_logs", [])) + len(issues.get("analytics", []))
    total_rows = len(performance_rows) + len(analytics_rows)
    print(f"Summary: {total_issues} / {total_rows} rows flagged with issues "
          f"({(total_issues / total_rows * 100) if total_rows else 0:.1f}%).")

    db.close()


if __name__ == "__main__":
    audit()
