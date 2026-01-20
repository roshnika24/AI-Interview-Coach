from pydantic import BaseModel
from typing import Literal, List, Optional

class InterviewConfig(BaseModel):
    role: Literal["SDE", "Data Analyst", "SDET"]
    difficulty: Literal["Easy", "Medium", "Hard"]
    topic: Optional[str] = "General"

class InterviewQuestion(BaseModel):
    question: str
    context: Optional[str] = None
    expected_key_points: List[str]

class AnswerSubmission(BaseModel):
    question: str
    difficulty: str
    role: str
    user_answer: str

class EvaluationResult(BaseModel):
    score: int
    feedback: str
    model_answer: str
    missing_key_points: List[str]
    tips: List[str]
