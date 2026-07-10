import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_challenge(challenge_type, difficulty):

    prompt = f"""
You are creating a cognitive challenge for a mobile alarm application.

Generate exactly ONE {difficulty} level {challenge_type} challenge.

Rules:
- The challenge must be solvable within 30 seconds.
- Use only basic arithmetic (+, -, *, /).
- Do not use powers, calculus, trigonometry, logarithms, or advanced mathematics.
- The challenge should be solvable mentally in under 30 seconds.
- Do NOT generate college-level mathematics.
- Do NOT generate calculus, trigonometry, differential equations or advanced algebra.
- Questions should be suitable for everyday users.
- If challenge_type is Math, generate simple arithmetic or mental math.
- If challenge_type is Memory, generate a short memory task.
- If challenge_type is Logic, generate a simple logical puzzle.
- If challenge_type is Pattern, generate a simple number or letter pattern.
- If challenge_type is Riddle, generate a short riddle.
- If challenge_type is Sequence, generate a sequence question.
- If challenge_type is Visual/Word, generate a word scramble or word puzzle.

Return ONLY a valid JSON object.

{{
    "question":"",
    "correct_answer":"",
    "difficulty":"{difficulty}",
    "points":10
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text) 