import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
from schemas import InterviewQuestion, EvaluationResult

load_dotenv()

# OpenRouter Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "mistralai/mistral-7b-instruct:free"

if not API_KEY:
    print("WARNING: OPENROUTER_API_KEY is not set. AI features will fail.")

# Set environment variables for OpenAI client to pick up
os.environ["OPENAI_API_KEY"] = API_KEY or "dummy"
os.environ["OPENAI_BASE_URL"] = BASE_URL

model = OpenAIModel(MODEL_NAME)

# Agent for generating questions
question_agent = Agent(
    model,
    output_type=InterviewQuestion,
    system_prompt="""
    You are an expert technical interviewer. 
    Your goal is to generate a realistic and challenging interview question based on the candidate's role and difficulty level.
    The output must strictly follow the InterviewQuestion schema.
    """
)

# Agent for evaluating answers
evaluation_agent = Agent(
    model,
    output_type=EvaluationResult,
    system_prompt="""
    You are a strict but helpful technical interview coach.
    Evaluate the candidate's answer based on the role, difficulty, and the specific question asked.
    Provide a score out of 10.
    List key points they missed.
    Provide a constructive model answer.
    Output must be structured as EvaluationResult.
    """
)

import random

async def generate_interview_question(role: str, difficulty: str) -> InterviewQuestion:
    if not API_KEY:
        # Fallback Mock Data with Variety
        mock_questions_pool = {
            "SDE": {
                "Easy": [
                    "Explain the difference between a process and a thread.",
                    "What is Polymorphism? Give a real-world example.",
                    "Explain the concept of a Hash Map and its time complexity."
                ],
                "Medium": [
                    "How would you design a URL shortening service like bit.ly?",
                    "Explain the difference between TCP and UDP.",
                    "What is a Deadlock and how can you prevent it?"
                ],
                "Hard": [
                    "Discuss the trade-offs between eventual consistency and strong consistency in distributed systems.",
                    "How would you design a rate limiter for a high-traffic API?",
                    "Explain the internal working of a Garbage Collector in your preferred language."
                ]
            },
            "Data Analyst": {
                "Easy": [
                    "What is the difference between WHERE and HAVING clauses in SQL?",
                    "Explain the difference between inner join, left join, and right join.",
                    "What are the different types of data visualization?"
                ],
                "Medium": [
                    "Explain how you would handle missing data in a dataset.",
                    "What is the difference between correlation and causation?",
                    "How do you detect outliers in a dataset?"
                ],
                "Hard": [
                    "Describe a time you found a significant insight in data that contradicted the business intuition.",
                    "How would you design an A/B test for a new feature?",
                    "Explain the concept of p-value to a non-technical audience."
                ]
            },
            "SDET": {
                "Easy": [
                    "What is the difference between black-box and white-box testing?",
                    "What is a regression test?",
                    "Explain the software testing life cycle (STLC)."
                ],
                "Medium": [
                    "How would you design an automated test suite for an e-commerce checkout flow?",
                    "What is the Page Object Model (POM) pattern?",
                    "Explain the difference between continuous integration and continuous deployment."
                ],
                "Hard": [
                    "Explain how you would test a distributed system for race conditions.",
                    "How do you handle flaky tests in your automation suite?",
                    "Design a performance testing strategy for a microservices architecture."
                ]
            }
        }
        
        questions = mock_questions_pool.get(role, {}).get(difficulty, [f"Tell me about a challenge you faced as a {role}."])
        question_text = random.choice(questions)
        
        return InterviewQuestion(
            question=question_text,
            context=f"Mock Question (AI key missing) - {difficulty} level - {role}",
            expected_key_points=["Key concept definition", "Real-world example", "Trade-off analysis"]
        )

    try:
        prompt = f"Generate a {difficulty} level interview question for a {role} position."
        result = await question_agent.run(prompt)
        return result.data
    except Exception as e:
        print(f"AI Generation failed: {e}")
        return InterviewQuestion(
            question=f"Describe the core responsibilities of a {role}.",
            context="Fallback Question (AI Error)",
            expected_key_points=["Responsibilities", "Skills", "Impact"]
        )

async def evaluate_interview_answer(question: str, role: str, difficulty: str, user_answer: str) -> EvaluationResult:
    if not API_KEY:
        # Dynamic Mock Evaluation
        word_count = len(user_answer.split())
        score = 0
        feedback = ""
        missing_points = []
        
        # Simple heuristic scoring
        if word_count < 10:
            score = 3
            feedback = "Your answer is too short. Please elaborate and provide more details."
            missing_points = ["Depth of explanation", "Examples", "Technical terminology"]
        elif word_count < 30:
            score = 6
            feedback = "Good start, but you could provide more specific examples to strengthen your point."
            missing_points = ["Concrete examples", "Trade-offs"]
        else:
            score = 8
            feedback = "Strong answer! You covered the main points well. To get a perfect score, mention edge cases."
            missing_points = ["Edge cases", "Scalability considerations"]

        # Keyword boost
        tech_keywords = ["scale", "latency", "consistency", "testing", "data", "optimization", "trade-off"]
        if any(k in user_answer.lower() for k in tech_keywords):
            score = min(10, score + 1)
            feedback += " Good use of technical vocabulary."

        return EvaluationResult(
            score=score,
            feedback=f"Mock Evaluation: {feedback} (Based on answer length & keywords)",
            model_answer=f"A great answer for '{question}' would involve defining the core concept, giving a concrete example, and discussing pros/cons. For example...",
            missing_key_points=missing_points,
            tips=["Use the STAR method", "Be concise but thorough", "Focus on impact"]
        )

    try:
        prompt = f"""
        Role: {role}
        Difficulty: {difficulty}
        Question: {question}
        Candidate Answer: {user_answer}
        
        Evaluate this answer.
        """
        result = await evaluation_agent.run(prompt)
        return result.data
    except Exception as e:
        print(f"AI Evaluation failed: {e}")
        return EvaluationResult(
            score=5,
            feedback="AI service unavailable. Please check backend logs.",
            model_answer="Unavailable",
            missing_key_points=[],
            tips=[]
        )
