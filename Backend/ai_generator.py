import os
import json
import random

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
    else:
        model = None
except Exception:
    genai = None
    model = None


def _fallback_math(difficulty: str):
    level = (difficulty or "Easy").lower()
    if level == "easy":
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(["+", "-"])
        result = a + b if op == "+" else a - b
        points = 5
    elif level == "medium":
        a, b = random.randint(10, 30), random.randint(2, 12)
        op = random.choice(["+", "-", "*"])
        result = a + b if op == "+" else a - b if op == "-" else a * b
        points = 10
    else:
        a, b, c = random.randint(20, 99), random.randint(3, 15), random.randint(2, 20)
        op = random.choice(["+", "-", "*"])
        first_result = a + b if op == "+" else a - b if op == "-" else a * b
        question = f"{a} {op} {b} + {c}"
        return {
            "question": question,
            "correct_answer": str(first_result + c),
            "difficulty": difficulty,
            "points": 15,
        }

    question = f"{a} {op} {b}"
    return {
        "question": question,
        "correct_answer": str(result),
        "difficulty": difficulty,
        "points": points,
    }


def generate_challenge(challenge_type: str, difficulty: str, age: int = None):
    """Generate a challenge. Uses Gemini if available, otherwise falls back to a simple generator."""
    if model is None:
        t = (challenge_type or "math").lower()
        if t == "math":
            return _fallback_math(difficulty)
        if t == "memory":
            items = ["red", "sun", "tree", "book", "cat"]
            q = "Remember these words: " + ", ".join(items[:4])
            return {"question": q, "correct_answer": ",".join(items[:4]), "difficulty": difficulty, "points": 8}
        if t == "logic":
            return {"question": "If all cats are animals and all animals breathe, do cats breathe? (yes/no)", "correct_answer": "yes", "difficulty": difficulty, "points": 5}
        if t == "pattern":
            return {"question": "What is the next number in the sequence: 2, 4, 6, 8, ?", "correct_answer": "10", "difficulty": difficulty, "points": 5}
        if t == "riddle":
            return {"question": "What has keys but can't open locks?", "correct_answer": "piano", "difficulty": difficulty, "points": 5}
        if t == "sequence":
            return {"question": "Complete the sequence: 3, 6, 12, 24, ?", "correct_answer": "48", "difficulty": difficulty, "points": 6}
        if t == "visual":
            return {"question": "Which shape has three sides: circle, triangle, or square?", "correct_answer": "triangle", "difficulty": difficulty, "points": 5}
        return _fallback_math(difficulty)

    # Use Gemini model when available. Keep the prompt concise and expect JSON output.
    prompt = f"""
Generate exactly one {difficulty} {challenge_type} challenge as a JSON object with keys: question, correct_answer, difficulty, points.
The user is {age if age is not None else "an unspecified age"} years old; make the wording and complexity age-appropriate.
Keep challenges short and solvable in under 30 seconds.
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception:
        return _fallback_math(difficulty)
