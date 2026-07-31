"""
question_bank.py

Static seed question bank for the Cognitive Challenge Engine.
Covers all 7 challenge types (Math, Logic, Memory, Word, Pattern, Riddle, Quiz)
across 3 difficulty levels (Easy, Medium, Hard).

Each entry: {"question": str, "correct_answer": str, "points": int}

Answer matching convention (used by validate_answer in answer_validation.py):
- case-insensitive, surrounding whitespace stripped
- comma-separated list answers (e.g. Memory) are also order-sensitive but
  ignore spacing around commas
"""

QUESTION_BANK = {
    "math": {
        "Easy": [
            {"question": "7 + 5", "correct_answer": "12", "points": 5},
            {"question": "9 - 4", "correct_answer": "5", "points": 5},
            {"question": "6 + 8", "correct_answer": "14", "points": 5},
        ],
        "Medium": [
            {"question": "14 * 3", "correct_answer": "42", "points": 10},
            {"question": "56 / 8", "correct_answer": "7", "points": 10},
            {"question": "23 + 19", "correct_answer": "42", "points": 10},
        ],
        "Hard": [
            {"question": "12 * 7 - 15", "correct_answer": "69", "points": 15},
            {"question": "144 / 12 + 9", "correct_answer": "21", "points": 15},
            {"question": "8 * 8 - 3 * 4", "correct_answer": "52", "points": 15},
        ],
    },
    "logic": {
        "Easy": [
            {"question": "True or False: All squares are rectangles.", "correct_answer": "true", "points": 5},
            {"question": "If it is raining, the ground is wet. It is raining. Is the ground wet? (yes/no)", "correct_answer": "yes", "points": 5},
            {"question": "True or False: A triangle has four sides.", "correct_answer": "false", "points": 5},
        ],
        "Medium": [
            {"question": "All cats are animals. All animals need food. Do cats need food? (yes/no)", "correct_answer": "yes", "points": 10},
            {"question": "If today is Monday, what day is it in 3 days?", "correct_answer": "thursday", "points": 10},
            {"question": "Sam is older than Alex. Alex is older than Jo. Who is the oldest?", "correct_answer": "sam", "points": 10},
        ],
        "Hard": [
            {"question": "Five friends sit in a row. Ana is left of Ben. Ben is left of Cal. Who is in the middle?", "correct_answer": "ben", "points": 15},
            {"question": "If no fish can fly, and a salmon is a fish, can a salmon fly? (yes/no)", "correct_answer": "no", "points": 15},
            {"question": "A is taller than B. C is shorter than B. Who is the shortest?", "correct_answer": "c", "points": 15},
        ],
    },
    "memory": {
        "Easy": [
            {"question": "Remember these words in order: red, sun, tree", "correct_answer": "red,sun,tree", "points": 5},
            {"question": "Remember these numbers in order: 3, 7, 1", "correct_answer": "3,7,1", "points": 5},
            {"question": "Remember these words in order: cat, book, lamp", "correct_answer": "cat,book,lamp", "points": 5},
        ],
        "Medium": [
            {"question": "Remember these words in order: apple, chair, cloud, river", "correct_answer": "apple,chair,cloud,river", "points": 10},
            {"question": "Remember these numbers in order: 9, 2, 6, 4", "correct_answer": "9,2,6,4", "points": 10},
            {"question": "Remember these words in order: moon, glass, tiger, frost", "correct_answer": "moon,glass,tiger,frost", "points": 10},
        ],
        "Hard": [
            {"question": "Remember these words in order: pencil, ocean, whistle, garden, spark", "correct_answer": "pencil,ocean,whistle,garden,spark", "points": 15},
            {"question": "Remember these numbers in order: 5, 8, 1, 9, 3", "correct_answer": "5,8,1,9,3", "points": 15},
            {"question": "Remember these words in order: quartz, ladder, ember, coast, plume", "correct_answer": "quartz,ladder,ember,coast,plume", "points": 15},
        ],
    },
    "word": {
        "Easy": [
            {"question": "What is the opposite of 'hot'?", "correct_answer": "cold", "points": 5},
            {"question": "Unscramble this word: OGD (an animal)", "correct_answer": "dog", "points": 5},
            {"question": "What is the opposite of 'up'?", "correct_answer": "down", "points": 5},
        ],
        "Medium": [
            {"question": "Unscramble this word: ELPAP (a fruit)", "correct_answer": "apple", "points": 10},
            {"question": "What word means the same as 'happy'?", "correct_answer": "joyful", "points": 10},
            {"question": "Unscramble this word: RVEIR (a body of water)", "correct_answer": "river", "points": 10},
        ],
        "Hard": [
            {"question": "Unscramble this word: LAIRBRY (a place with books)", "correct_answer": "library", "points": 15},
            {"question": "What 7-letter word means 'to think deeply'? (hint: starts with P)", "correct_answer": "ponder", "points": 15},
            {"question": "Unscramble this word: OMOUNTNIA (a large landform)", "correct_answer": "mountain", "points": 15},
        ],
    },
    "pattern": {
        "Easy": [
            {"question": "What comes next: 2, 4, 6, 8, ?", "correct_answer": "10", "points": 5},
            {"question": "What comes next: A, B, C, D, ?", "correct_answer": "e", "points": 5},
            {"question": "What comes next: 1, 2, 3, 4, ?", "correct_answer": "5", "points": 5},
        ],
        "Medium": [
            {"question": "What comes next: 3, 6, 9, 12, ?", "correct_answer": "15", "points": 10},
            {"question": "What comes next: 1, 4, 9, 16, ?", "correct_answer": "25", "points": 10},
            {"question": "What comes next: Z, Y, X, W, ?", "correct_answer": "v", "points": 10},
        ],
        "Hard": [
            {"question": "What comes next: 2, 6, 18, 54, ?", "correct_answer": "162", "points": 15},
            {"question": "What comes next: 1, 1, 2, 3, 5, 8, ?", "correct_answer": "13", "points": 15},
            {"question": "What comes next: 100, 90, 72, 45, ?", "correct_answer": "0", "points": 15},
        ],
    },
    "riddle": {
        "Easy": [
            {"question": "What has keys but can't open locks?", "correct_answer": "piano", "points": 5},
            {"question": "What gets wetter as it dries?", "correct_answer": "towel", "points": 5},
            {"question": "What has a face but no eyes?", "correct_answer": "clock", "points": 5},
        ],
        "Medium": [
            {"question": "What has hands but cannot clap?", "correct_answer": "clock", "points": 10},
            {"question": "What can travel around the world while staying in a corner?", "correct_answer": "stamp", "points": 10},
            {"question": "What has a neck but no head?", "correct_answer": "bottle", "points": 10},
        ],
        "Hard": [
            {"question": "The more you take, the more you leave behind. What am I?", "correct_answer": "footsteps", "points": 15},
            {"question": "I speak without a mouth and hear without ears. What am I?", "correct_answer": "echo", "points": 15},
            {"question": "What has cities but no houses, forests but no trees, and water but no fish?", "correct_answer": "map", "points": 15},
        ],
    },
    "quiz": {
        "Easy": [
            {"question": "What planet do we live on?", "correct_answer": "earth", "points": 5},
            {"question": "How many days are in a week?", "correct_answer": "7", "points": 5},
            {"question": "What color do you get by mixing blue and yellow?", "correct_answer": "green", "points": 5},
        ],
        "Medium": [
            {"question": "What is the capital of France?", "correct_answer": "paris", "points": 10},
            {"question": "How many continents are there on Earth?", "correct_answer": "7", "points": 10},
            {"question": "What gas do plants absorb from the air?", "correct_answer": "carbon dioxide", "points": 10},
        ],
        "Hard": [
            {"question": "What is the largest planet in our solar system?", "correct_answer": "jupiter", "points": 15},
            {"question": "In what year did World War II end?", "correct_answer": "1945", "points": 15},
            {"question": "What is the chemical symbol for gold?", "correct_answer": "au", "points": 15},
        ],
    },
}