import random
import re
from typing import Dict, Any, List

# Vocabulary list for word games
WORD_BANK = [
    "HEALTH", "HABIT", "SLEEP", "ROUTINE", "COGNITIVE", 
    "ALARM", "INTELLIGE", "PRODUCTIVE", "WAKEUP", "CONSISTEN",
    "PROMPT", "PYTHON", "REACT", "CREATIVE", "FOCUS"
]

RIDDLES_BANK = [
    {
        "question": "What has keys but no locks, space but no room, and you can enter but can't go outside?",
        "answers": ["keyboard", "a keyboard"]
    },
    {
        "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "answers": ["echo", "an echo"]
    },
    {
        "question": "What has to be broken before you can use it?",
        "answers": ["egg", "an egg"]
    },
    {
        "question": "I am tall when I am young, and I am short when I am old. What am I?",
        "answers": ["candle", "a candle"]
    },
    {
        "question": "What is full of holes but still holds water?",
        "answers": ["sponge", "a sponge"]
    }
]

QUIZ_BANK = [
    {
        "question": "Which planet is closest to the Sun?",
        "options": ["Earth", "Mars", "Mercury", "Venus"],
        "answer": "Mercury"
    },
    {
        "question": "What is the capital city of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "answer": "Canberra"
    },
    {
        "question": "How many bones are there in an adult human body?",
        "options": ["106", "206", "306", "406"],
        "answer": "206"
    },
    {
        "question": "What is the primary gas found in Earth's atmosphere?",
        "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
        "answer": "Nitrogen"
    }
]

def generate_math_problem(difficulty: str) -> Dict[str, Any]:
    difficulty = difficulty.lower()
    if difficulty == "beginner":
        # 1-digit addition or subtraction
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])
        question = f"{a} {op} {b}"
        answer = str(eval(question))
        
    elif difficulty == "easy":
        # 2-digit + 1-digit or simple multiplication
        a = random.randint(10, 50)
        b = random.randint(2, 9)
        op = random.choice(["+", "-", "*"])
        question = f"{a} {op} {b}"
        answer = str(eval(question))
        
    elif difficulty == "medium":
        # 2-digit multiplication or 3-digit operations
        a = random.randint(10, 99)
        b = random.randint(3, 12)
        op = random.choice(["+", "-", "*"])
        if op == "*":
            question = f"{a} * {b}"
        else:
            question = f"{random.randint(100, 999)} {op} {random.randint(50, 499)}"
        answer = str(eval(question))
        
    elif difficulty == "hard":
        # Linear algebra: a * x + b = c, solve x
        x = random.randint(2, 12)
        a = random.choice([2, 3, 4, 5, 10])
        b = random.randint(1, 20)
        c = a * x + b
        sign = "+" if b >= 0 else "-"
        question = f"Solve for x: {a}x {sign} {abs(b)} = {c}"
        answer = str(x)
        
    else: # expert
        # Order of operations / multiple terms
        a = random.randint(10, 50)
        b = random.randint(2, 8)
        c = random.randint(5, 25)
        d = random.randint(2, 5)
        question = f"({a} * {b}) - ({c} * {d})"
        answer = str(eval(question))
        
    return {
        "question": f"Solve: {question}",
        "answer": answer,
        "type": "Math"
    }

def generate_logic_puzzle(difficulty: str) -> Dict[str, Any]:
    difficulty = difficulty.lower()
    if difficulty in ["beginner", "easy"]:
        # Logic patterns / sequence matching
        start = random.randint(1, 10)
        step = random.randint(2, 6)
        seq = [start + i * step for i in range(5)]
        question = f"Identify the next number in sequence: {', '.join(map(str, seq[:4]))}, ?"
        answer = str(seq[4])
        
    elif difficulty in ["medium", "hard"]:
        # Simple symbol puzzle: A + B = 10, A - B = 4. What is A?
        # A + B = S, A - B = D. S+D = 2A. S-D = 2B
        a = random.randint(5, 15)
        b = random.randint(1, a - 1)
        s = a + b
        d = a - b
        question = f"If A + B = {s} and A - B = {d}, what is the value of A?"
        answer = str(a)
        
    else: # expert
        # Multi-variable riddle
        # A = 2B, B = C + 5, C = 3. What is A?
        c = random.randint(1, 10)
        b = c + random.randint(2, 8)
        a = random.randint(2, 4) * b
        multiplier = a // b
        question = f"If A = {multiplier}B, B = C + {b - c}, and C = {c}, what is the value of A?"
        answer = str(a)
        
    return {
        "question": question,
        "answer": answer,
        "type": "Logic"
    }

def generate_memory_challenge(difficulty: str) -> Dict[str, Any]:
    # Memory challenges are sequence repetition based.
    # Level increases sequence length
    difficulty = difficulty.lower()
    lengths = {"beginner": 4, "easy": 5, "medium": 6, "hard": 8, "expert": 10}
    length = lengths.get(difficulty, 6)
    
    digits = [str(random.randint(0, 9)) for _ in range(length)]
    sequence = "".join(digits)
    
    return {
        "question": f"Memorize this sequence: {sequence}",
        "answer": sequence,
        "type": "Memory"
    }

def generate_word_game(difficulty: str) -> Dict[str, Any]:
    # Select word and either scramble (anagram) or reverse it
    word = random.choice(WORD_BANK)
    difficulty = difficulty.lower()
    
    if difficulty in ["beginner", "easy"]:
        # Reverse spelling
        question = f"Spell the word '{word}' in reverse order"
        answer = word[::-1]
    else:
        # Anagram
        scrambled_list = list(word)
        while "".join(scrambled_list) == word:
            random.shuffle(scrambled_list)
        scrambled = "".join(scrambled_list)
        question = f"Unscramble the word: '{scrambled}'"
        answer = word
        
    return {
        "question": question,
        "answer": answer.upper(),
        "type": "Word Games"
    }

def generate_pattern_recognition(difficulty: str) -> Dict[str, Any]:
    # Finding the odd visual item / missing code in grid
    difficulty = difficulty.lower()
    if difficulty in ["beginner", "easy"]:
        # Visual/symbol patterns
        row = "XO"
        grid = [row for _ in range(3)]
        # Make one item odd
        options = ["OOX", "OXO", "XOO", "XXX"]
        correct = random.choice(options)
        question = f"Which pattern is the odd one out? A: XOX, B: XOX, C: {correct}, D: XOX"
        answer = "C"
    else:
        # Find the missing matrix value
        # Simple multiplication matrix
        factor = random.randint(2, 5)
        question = f"Complete the grid pattern logic: [2, 4], [{factor}, ?]. What is the missing number?"
        answer = str(2 * factor)
        
    return {
        "question": question,
        "answer": answer,
        "type": "Pattern"
    }

def generate_riddle() -> Dict[str, Any]:
    item = random.choice(RIDDLES_BANK)
    return {
        "question": item["question"],
        "answer": item["answers"][0],  # Return first as standard answer
        "answers": item["answers"],    # Store all options for validation
        "type": "Riddles"
    }

def generate_quiz() -> Dict[str, Any]:
    quiz = random.choice(QUIZ_BANK)
    return {
        "question": quiz["question"],
        "options": quiz["options"],
        "answer": quiz["answer"],
        "type": "Quick Quizzes"
    }

def create_challenge(challenge_type: str, difficulty: str) -> Dict[str, Any]:
    """Factory to generate the challenge dictionary based on type and difficulty"""
    challenge_type = challenge_type.lower()
    
    if "math" in challenge_type:
        return generate_math_problem(difficulty)
    elif "logic" in challenge_type:
        return generate_logic_puzzle(difficulty)
    elif "memory" in challenge_type:
        return generate_memory_challenge(difficulty)
    elif "word" in challenge_type:
        return generate_word_game(difficulty)
    elif "pattern" in challenge_type:
        return generate_pattern_recognition(difficulty)
    elif "riddle" in challenge_type:
        return generate_riddle()
    elif "quiz" in challenge_type or "quick" in challenge_type:
        return generate_quiz()
    else:
        # Default fallback
        return generate_math_problem(difficulty)

def validate_answer(answer: str, challenge: Dict[str, Any]) -> bool:
    """Verifies user input against challenge answers with fuzzy string adjustments"""
    user_ans = answer.strip().lower()
    correct_ans = str(challenge.get("answer")).strip().lower()
    
    # Check if a custom options list was provided (e.g. Riddles)
    if "answers" in challenge:
        for possible in challenge["answers"]:
            if user_ans == str(possible).strip().lower():
                return True
        return False
        
    # Regular matching
    # Remove leading articles for word/riddle puzzles
    user_ans = re.sub(r'^(a|an|the)\s+', '', user_ans)
    correct_ans = re.sub(r'^(a|an|the)\s+', '', correct_ans)
    
    return user_ans == correct_ans
