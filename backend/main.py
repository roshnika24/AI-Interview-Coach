from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import InterviewConfig, InterviewQuestion, AnswerSubmission, EvaluationResult
from agent import generate_interview_question, evaluate_interview_answer
import os

app = FastAPI(title="AI Interview Coach")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Interview Coach API is running"}

@app.post("/generate-question", response_model=InterviewQuestion)
async def generate_question_endpoint(config: InterviewConfig):
    try:
        question = await generate_interview_question(config.role, config.difficulty)
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate-answer", response_model=EvaluationResult)
async def evaluate_answer_endpoint(submission: AnswerSubmission):
    try:
        evaluation = await evaluate_interview_answer(
            submission.question,
            submission.role,
            submission.difficulty,
            submission.user_answer
        )
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
