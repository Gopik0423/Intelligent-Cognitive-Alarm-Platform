"""
seed_question_bank.py

Loads QUESTION_BANK (services/question_bank.py) into the challenges table.
Safe to re-run: skips any question that already exists (matched by question text).

Run from inside the Backend/ folder:
    python -m scripts.seed_question_bank
"""

from database.db import SessionLocal
from models.challenge import Challenge
from services.question_bank import QUESTION_BANK


def seed():
    db = SessionLocal()

    inserted = 0
    skipped = 0

    for challenge_type, difficulties in QUESTION_BANK.items():
        for difficulty, questions in difficulties.items():
            for q in questions:
                existing = (
                    db.query(Challenge)
                    .filter(Challenge.question == q["question"])
                    .first()
                )
                if existing:
                    skipped += 1
                    continue

                new_challenge = Challenge(
                    challenge_type=challenge_type,
                    question=q["question"],
                    correct_answer=q["correct_answer"],
                    difficulty=difficulty,
                    points=q["points"],
                )
                db.add(new_challenge)
                inserted += 1

    db.commit()
    print(f"Seeded {inserted} new questions ({skipped} already existed, skipped).")

    total = db.query(Challenge).count()
    print(f"Total questions now in challenges table: {total}")

    db.close()


if __name__ == "__main__":
    seed()