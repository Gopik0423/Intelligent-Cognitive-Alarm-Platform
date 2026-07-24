from pydantic import BaseModel


class ChallengeCreate(BaseModel):
    challenge_type: str
    question: str
    correct_answer: str
    difficulty: str
    points: int


class ChallengeAnswer(BaseModel):
    answer: str

class StartChallenge(BaseModel):
    user_id: int
    challenge_type: str
