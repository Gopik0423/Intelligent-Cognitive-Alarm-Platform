from __future__ import annotations

from itertools import product

from app.database import SessionLocal
from app.models import Challenge, ChallengeDifficulty, ChallengeType


def _difficulty_profile(difficulty: ChallengeDifficulty) -> tuple[int, int, int]:
    """Return a time limit and point profile for a difficulty level."""

    profile_map = {
        ChallengeDifficulty.beginner: (30, 10, 1),
        ChallengeDifficulty.easy: (45, 20, 2),
        ChallengeDifficulty.medium: (60, 30, 3),
        ChallengeDifficulty.hard: (90, 50, 4),
        ChallengeDifficulty.expert: (120, 80, 5),
    }
    return profile_map[difficulty]


def _build_challenge(
    challenge_type: ChallengeType,
    difficulty: ChallengeDifficulty,
    variant: int,
) -> Challenge:
    """Create a deterministic sample challenge payload."""

    time_limit, points, scale = _difficulty_profile(difficulty)

    if challenge_type is ChallengeType.math_problems:
        left = scale * (variant + 2)
        right = scale + variant + 1
        question = f"What is {left} + {right}?"
        answer = str(left + right)
        options = [str(left + right - 1), answer, str(left + right + 1), str(left + right + 2)]
        hint = "Add the two numbers together."
        explanation = f"{left} plus {right} equals {left + right}."
    elif challenge_type is ChallengeType.logic_puzzles:
        question = (
            f"A hallway has {variant + 2} doors. If one door is open and the rest are closed, "
            "how many doors can you walk through without opening anything?"
        )
        answer = "1"
        options = ["0", "1", "2", str(variant + 2)]
        hint = "Think about the open door."
        explanation = "Only the already open door can be walked through without opening a door."
    elif challenge_type is ChallengeType.memory_challenges:
        sequence = [str(scale + i) for i in range(3)]
        question = f"Memorize this sequence: {' '.join(sequence)}. What was the second number?"
        answer = sequence[1]
        options = [sequence[0], sequence[1], sequence[2], str(scale + 10)]
        hint = "Focus on the middle number."
        explanation = f"The second number in the sequence is {sequence[1]}."
    elif challenge_type is ChallengeType.word_games:
        base_word = ["stream", "planet", "marker", "silver", "candle"][variant % 5]
        question = f"Unscramble this word: {''.join(sorted(base_word))}"
        answer = base_word
        options = [base_word, base_word[::-1], base_word.upper(), base_word.title()]
        hint = "Rearrange the letters into a common word."
        explanation = f"The scrambled letters form the word '{base_word}'."
    elif challenge_type is ChallengeType.pattern_recognition:
        start = scale + variant
        question = f"What comes next in the pattern: {start}, {start + 2}, {start + 4}, ?"
        answer = str(start + 6)
        options = [str(start + 5), str(start + 6), str(start + 7), str(start + 8)]
        hint = "The sequence increases by 2 each time."
        explanation = f"Each term increases by 2, so the next value is {start + 6}."
    elif challenge_type is ChallengeType.riddles:
        question = "I speak without a mouth and hear without ears. What am I?"
        answer = "Echo"
        options = ["Echo", "Shadow", "Wind", "Mirror"]
        hint = "It repeats what you say."
        explanation = "An echo reflects sound back, so it can speak and hear metaphorically."
    else:
        question = (
            f"Quick quiz: In a sequence of {variant + 3} steps, which step is the midpoint when the count is odd?"
        )
        answer = "The middle step"
        options = ["The first step", "The last step", "The middle step", "There is no midpoint"]
        hint = "Count the steps and find the center."
        explanation = "An odd-numbered sequence has one center element, which is the midpoint."

    return Challenge(
        type=challenge_type.value,
        difficulty=difficulty.value,
        question=question,
        answer=answer,
        options=options,
        hint=hint,
        explanation=explanation,
        time_limit=time_limit,
        points=points,
    )


def seed_database() -> int:
    """Seed the database with sample challenge content."""

    db = SessionLocal()
    try:
        existing_count = db.query(Challenge).count()
        if existing_count >= 100:
            return 0

        challenges_to_insert: list[Challenge] = []
        for index, (challenge_type, difficulty) in enumerate(product(ChallengeType, ChallengeDifficulty)):
            for variant in range(3):
                challenges_to_insert.append(
                    _build_challenge(challenge_type, difficulty, index + variant)
                )

        db.add_all(challenges_to_insert)
        db.commit()
        return len(challenges_to_insert)
    finally:
        db.close()


if __name__ == "__main__":
    inserted = seed_database()
    print(f"Inserted {inserted} sample challenges.")
