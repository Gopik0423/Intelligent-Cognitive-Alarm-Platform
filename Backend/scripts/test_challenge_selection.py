"""
test_challenge_selection.py

Direct verification of Challenge Selection Logic (services/challenge_selector.py):
  1. Difficulty-awareness: does it pick from the right difficulty pool?
  2. Repeat-avoidance: does it actually exclude recently-served challenge_ids?

This bypasses the full alarm/verification UI flow (which uses a separate,
age-based difficulty system) and tests select_challenge() directly against
manually-crafted WakeupVerification history, so the two concerns don't get
tangled together.

Run from inside Backend/:
    python -m scripts.test_challenge_selection
"""

from database.db import SessionLocal
from models.challenge import Challenge
from models.difficulty import DifficultyLevel
from models.verification import WakeupVerification
from models.user import User
from models.alarm import Alarm  # noqa: F401 -- needed so SQLAlchemy can resolve the alarm_id FK
from services.challenge_selector import select_challenge


def run():
    db = SessionLocal()

    user = db.query(User).first()
    if not user:
        print("No user found. Register a user first.")
        return

    user_id = user.id
    print(f"Testing with user_id={user_id}")

    # --- Set up: force this user to Easy difficulty (level 1) ---
    record = db.query(DifficultyLevel).filter(DifficultyLevel.user_id == user_id).first()
    if not record:
        record = DifficultyLevel(user_id=user_id)
        db.add(record)
    record.difficulty_level = 1
    record.correct_streak = 0
    record.fail_streak = 0
    db.commit()

    # --- Test 1: difficulty-awareness ---
    easy_math_ids = {
        c.id for c in db.query(Challenge)
        .filter(Challenge.challenge_type == "math", Challenge.difficulty == "Easy")
        .all()
    }
    print(f"\nEasy math question IDs in bank: {sorted(easy_math_ids)}")

    picks = [select_challenge(db, user_id, "math") for _ in range(10)]
    picked_ids = {p.id for p in picks if p is not None}
    all_easy = all(p.difficulty == "Easy" for p in picks if p is not None)
    print(f"10 picks at Easy level -> all returned Easy difficulty: {all_easy}")
    print(f"Picked IDs: {sorted(picked_ids)} (should all be within the Easy math set above)")

    # --- Test 2: repeat-avoidance ---
    # Manually create WakeupVerification rows marking 2 of the 3 Easy math
    # questions as "recently served" to this user.
    to_exclude = sorted(easy_math_ids)[:2]
    print(f"\nMarking as recently served (should be excluded next): {to_exclude}")

    dummy_alarm_id = 1  # only used as a foreign key value here; not validated by this test
    for cid in to_exclude:
        db.add(WakeupVerification(
            user_id=user_id,
            alarm_id=dummy_alarm_id,
            status="success",
            challenge_type="math",
            challenge_id=str(cid),
        ))
    db.commit()

    picks_after = [select_challenge(db, user_id, "math") for _ in range(10)]
    picked_ids_after = {p.id for p in picks_after if p is not None}
    excluded_leaked = picked_ids_after & set(to_exclude)

    print(f"10 picks after marking 2 as recent -> picked IDs: {sorted(picked_ids_after)}")
    if excluded_leaked:
        print(f"FAIL: these recently-served IDs were picked anyway: {sorted(excluded_leaked)}")
    else:
        print("PASS: none of the recently-served IDs were picked again.")

    db.close()


if __name__ == "__main__":
    run()
