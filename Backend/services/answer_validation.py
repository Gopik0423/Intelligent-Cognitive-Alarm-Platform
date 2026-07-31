"""
answer_validation.py

Answer Validation Logic.

Centralizes how a submitted answer is checked against a challenge's
correct_answer, so every challenge type is graded consistently and fairly
(instead of a single brittle exact-string-match).

Handles:
  - Case and whitespace differences ("Paris" == "paris " == " PARIS")
  - Trailing punctuation ("cold." == "cold")
  - Numeric answers, including "14" == "14.0"
  - Comma-separated list answers (Memory questions), order-sensitive but
    tolerant of spacing ("red, sun,tree" == "red,sun,tree")
  - Common yes/no/true/false shorthand ("y" == "yes", "t" == "true")
"""

_SYNONYMS = {
    "y": "yes",
    "n": "no",
    "t": "true",
    "f": "false",
}


def _normalize(text: str) -> str:
    return text.strip().lower().rstrip(".!? ")


def validate_answer(user_answer: str, correct_answer: str) -> bool:
    """Returns True if user_answer should be counted as correct."""
    if user_answer is None or correct_answer is None:
        return False

    user_norm = _normalize(user_answer)
    correct_norm = _normalize(correct_answer)

    # Comma-separated list answers (e.g. Memory questions)
    if "," in correct_norm:
        user_parts = [_normalize(p) for p in user_norm.split(",")]
        correct_parts = [_normalize(p) for p in correct_norm.split(",")]
        return user_parts == correct_parts

    # Numeric answers: "14" should match "14.0"
    try:
        return float(user_norm) == float(correct_norm)
    except ValueError:
        pass

    # yes/no/true/false shorthand
    user_norm = _SYNONYMS.get(user_norm, user_norm)
    correct_norm = _SYNONYMS.get(correct_norm, correct_norm)

    return user_norm == correct_norm
