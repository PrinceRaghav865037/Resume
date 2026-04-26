import os
import json
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Explicitly load .env from the project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize the Groq client.
client = Groq(api_key=api_key)

def _get_completion(prompt: str, system_prompt: str = "You are a helpful AI assistant.", temperature: float = 0.7) -> str:
    """
    A reusable wrapper function for the Groq ChatCompletion API.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with Groq API: {e}")
        return ""

def generate_questions(skill: str) -> List[str]:
    """
    Generates interview or assessment questions for a given skill.
    """
    system_prompt = "You are an expert technical interviewer. Return ONLY valid JSON. No explanation."
    prompt = f"Generate 3 diverse, intermediate-to-advanced interview questions to assess a candidate's proficiency in '{skill}'. Return an array of strings representing the questions."
    
    response = _get_completion(prompt, system_prompt, temperature=0.7)
    
    try:
        # Strip potential markdown formatting if the model disobeys instructions
        cleaned_response = response.strip("` \n").removeprefix("json\n").strip()
        questions = json.loads(cleaned_response, strict=False)
        if isinstance(questions, list):
            return questions
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for questions. Raw response: {response}")
        # Fallback if parsing fails
        return [q for q in response.split('\n') if q.strip()]
    
    return []

def evaluate_answer(question: str, answer: str) -> Dict[str, Any]:
    """
    Evaluates a candidate's answer to a question.
    Returns a score and constructive feedback.
    """
    system_prompt = "You are a strict but fair expert technical interviewer. Return ONLY valid JSON. No explanation."
    prompt = f"""
    Question: {question}
    Candidate's Answer: {answer}
    
    Evaluate the candidate's answer. Provide:
    1. A score from 0 to 10 (integer).
    2. Constructive feedback explaining the score and what could be improved.
    
    Return the result ONLY as a JSON object with exactly two keys: "score" (integer) and "feedback" (string).
    """
    
    response = _get_completion(prompt, system_prompt, temperature=0.2)
    
    try:
        cleaned_response = response.strip("` \n").removeprefix("json\n").strip()
        evaluation = json.loads(cleaned_response, strict=False)
        return evaluation
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for evaluation. Raw response: {response}")
        return {"score": 0, "feedback": "Evaluation failed due to API formatting error."}

def generate_learning_plan(gaps: List[str]) -> str:
    """
    Generates a personalized learning plan based on identified skill gaps.
    """
    system_prompt = "You are an expert technical mentor creating highly effective personalized learning plans. Return ONLY valid JSON. No explanation."
    gaps_str = ", ".join(gaps)
    prompt = f"""
    The candidate has the following skill gaps: {gaps_str}.
    
    Generate a concise, actionable, step-by-step learning plan to help them master these skills. 
    Include recommendations for resources.
    Structure the response as a JSON object.
    """
    
    response = _get_completion(prompt, system_prompt, temperature=0.6)
    return response
