"""
seed_week2_data.py

Generates realistic sample 'Week 2 attempt-log' data into the
performance_logs and analytics tables, for auditing/cleaning practice.

Intentionally includes some messy/bad records (nulls, out-of-range values,
duplicates, an orphaned user_id) since a real Week 2 log would have these too.

Run from the project root:
    python -m Backend.scripts.seed_week2_data
"""

import random
from datetime import datetime, timedelta

from database.db import SessionLocal
from models.performance import Performance
from models.analytics import Analytics
from models.user import User

CHALLENGE_TYPES = ["math", "logic", "memory", "pattern", "riddle"]


def seed():
    db = SessionLocal()

    existing_users = db.query(User).all()
    if not existing_users:
        print("No users found. Register at least one user before running this script.")
        db.close()
        return

    user_ids = [u.id for u in existing_users]
    print(f"Found {len(user_ids)} existing user(s): {user_ids}")

    performance_rows = []
    analytics_rows = []

    # --- Generate ~40 mostly realistic Performance rows ---
    for i in range(40):
        uid = random.choice(user_ids)
        completed_at = datetime.now() - timedelta(days=random.randint(0, 13), hours=random.randint(0, 23))
        performance_rows.append(Performance(
            user_id=uid,
            challenge_type=random.choice(CHALLENGE_TYPES),
            attempts=random.randint(1, 3),
            accuracy=round(random.uniform(0.3, 1.0), 2),
            success=random.choice([True, True, True, False]),
            completion_time=round(random.uniform(5, 45), 1),
            completed_at=completed_at,
        ))

    # --- Generate ~30 mostly realistic Analytics rows ---
    for i in range(30):
        uid = random.choice(user_ids)
        analytics_rows.append(Analytics(
            user_id=uid,
            challenge_type=random.choice(CHALLENGE_TYPES),
            completion_time=random.randint(5, 45),
            snooze_count=random.randint(0, 5),
            success=random.choice([True, True, False]),
        ))

    # --- Intentionally messy records for the audit exercise ---

    # 1. Empty/blank challenge_type (invalid but passes DB NOT NULL constraint)
    performance_rows.append(Performance(
        user_id=user_ids[0], challenge_type="", attempts=1,
        accuracy=0.7, success=True, completion_time=20.0,
        completed_at=datetime.now(),
    ))

    # 2. Out-of-range accuracy (>1.0)
    performance_rows.append(Performance(
        user_id=user_ids[0], challenge_type="math", attempts=1,
        accuracy=1.4, success=True, completion_time=15.0,
        completed_at=datetime.now(),
    ))

    # 3. Negative completion time
    performance_rows.append(Performance(
        user_id=user_ids[0], challenge_type="logic", attempts=1,
        accuracy=0.5, success=False, completion_time=-10.0,
        completed_at=datetime.now(),
    ))

    # 4. Orphaned user_id (references a user that doesn't exist)
    performance_rows.append(Performance(
        user_id=99999, challenge_type="riddle", attempts=1,
        accuracy=0.6, success=True, completion_time=25.0,
        completed_at=datetime.now(),
    ))

    # 5. Duplicate Analytics row (will add the same one twice)
    dup = Analytics(
        user_id=user_ids[0], challenge_type="pattern",
        completion_time=12, snooze_count=1, success=True,
    )
    analytics_rows.append(dup)
    analytics_rows.append(Analytics(
        user_id=user_ids[0], challenge_type="pattern",
        completion_time=12, snooze_count=1, success=True,
    ))

    # 6. Negative snooze_count (invalid)
    analytics_rows.append(Analytics(
        user_id=user_ids[0], challenge_type="math",
        completion_time=20, snooze_count=-2, success=False,
    ))

    db.add_all(performance_rows)
    db.add_all(analytics_rows)
    db.commit()

    print(f"Inserted {len(performance_rows)} Performance rows "
          f"({len(performance_rows) - 4} clean + 4 messy).")
    print(f"Inserted {len(analytics_rows)} Analytics rows "
          f"({len(analytics_rows) - 3} clean + 3 messy, incl. 1 duplicate pair).")
    db.close()


if __name__ == "__main__":
    seed()
