import random

CHALLENGE_TYPES = [
    "Math",
    "Memory",
    "Logic",
    "Pattern",
    "Riddle",
    "Sequence",
    "Visual"
]

class ChallengeEngine:

    @staticmethod
    def select_random():
        return random.choice(CHALLENGE_TYPES)
