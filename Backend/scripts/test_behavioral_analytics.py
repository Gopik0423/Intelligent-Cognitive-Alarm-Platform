"""
test_behavioral_analytics.py

Direct verification of Behavioral Analytics (services/behavioral_analytics.py).

The live app never actually populates snooze_count / wakeup_consistency on
Performance records (nothing in the current submit flow sets them), so every
trend came back "stable" by default -- not because the logic is broken, but
because it was never given data with real variation to detect. This script
manually creates Performance records with a deliberate improving trend
(snoozing less and scoring higher over time) and confirms the engine
actually detects it.

Run from inside Backend/:
    python -m scripts.test_behavioral_analytics
"""

from datetime import datetime, timedelta

from database.db import SessionLocal
from models.user import User
from models.performance import Performance
from services.behavioral_analytics import analyze_behavior


def run():
    db = SessionLocal()

    user = db.query(User).first()
    if not user:
        print("No user found. Register a user first.")
        return

    user_id = user.id
    print(f"Testing with user_id={user_id}")

    # Clear out any old test performance rows for a clean run
    db.query(Performance).filter(Performance.user_id == user_id).delete()
    db.commit()

    now = datetime.utcnow()
    # 3 "earlier" attempts: low accuracy, high snooze count
    # 3 "later" attempts: high accuracy, low snooze count
    # -> should detect accuracy "improving" and snooze "improving"
    rows = [
        # earlier (worse)
        Performance(user_id=user_id, challenge_type="math", attempts=1, accuracy=0.2, success=False,
                    completion_time=20, snooze_count=5, wakeup_consistency=30, completed_at=now - timedelta(days=6)),
        Performance(user_id=user_id, challenge_type="math", attempts=1, accuracy=0.3, success=False,
                    completion_time=22, snooze_count=6, wakeup_consistency=25, completed_at=now - timedelta(days=5)),
        Performance(user_id=user_id, challenge_type="math", attempts=1, accuracy=0.1, success=False,
                    completion_time=25, snooze_count=4, wakeup_consistency=35, completed_at=now - timedelta(days=4)),
        # later (better)
        Performance(user_id=user_id, challenge_type="math", attempts=1, accuracy=0.9, success=True,
                    completion_time=10, snooze_count=1, wakeup_consistency=80, completed_at=now - timedelta(days=2)),
        Performance(user_id=user_id, challenge_type="math", attempts=1, accuracy=1.0, success=True,
                    completion_time=8, snooze_count=0, wakeup_consistency=90, completed_at=now - timedelta(days=1)),
        Performance(user_id=user_id, challenge_type="math", attempts=1, accuracy=0.85, success=True,
                    completion_time=9, snooze_count=0, wakeup_consistency=85, completed_at=now),
    ]
    db.add_all(rows)
    db.commit()

    performances = db.query(Performance).filter(Performance.user_id == user_id).all()
    result = analyze_behavior(performances)

    print("\nResult:")
    for k, v in result.items():
        print(f"  {k}: {v}")

    checks = {
        "snooze_trend == 'improving'": result.get("snooze_trend") == "improving",
        "accuracy_trend == 'improving'": result.get("accuracy_trend") == "improving",
        "wakeup_consistency_trend == 'improving'": result.get("wakeup_consistency_trend") == "improving",
        "snooze_accuracy_correlation is negative": (result.get("snooze_accuracy_correlation") or 0) < 0,
    }
    print("\nChecks:")
    all_passed = True
    for label, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
        all_passed = all_passed and passed

    print("\nOVERALL:", "PASS" if all_passed else "FAIL")

    db.close()


if __name__ == "__main__":
    run()
