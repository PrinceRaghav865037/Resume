import uuid
from typing import List, Dict, Any, Tuple
from app.services.llm_service import generate_questions, evaluate_answer

# In-memory dictionary to maintain session-based memory for assessments
# Structure example:
# sessions = {
#     session_id: {
#         "skills": ["Python", "SQL"],
#         "current_skill_index": 0,
#         "current_skill": "Python",
#         "questions": ["Q1", "Q2", "Q3"],
#         "answers": [{"skill": "Python", "question": "Q1", "answer": "A1"}],
#         "scores": {"Python": {"total": 8, "count": 1}, "SQL": {"total": 0, "count": 0}},
#         "current_question_index": 1
#     }
# }
sessions: Dict[str, Dict[str, Any]] = {}

def start_assessment(skills: List[str]) -> Tuple[str, str]:
    """
    Initializes the session, picks the first skill, generates questions,
    and returns the session_id and the first question.
    """
    if not skills:
        raise ValueError("Skills list cannot be empty.")
        
    session_id = str(uuid.uuid4())
    
    sessions[session_id] = {
        "skills": skills,
        "current_skill_index": 0,
        "current_skill": skills[0],
        "questions": [], 
        "answers": [],
        "scores": {skill: {"total": 0, "count": 0} for skill in skills},
        "current_question_index": 0
    }
    
    # Generate 2-3 questions for the very first skill
    _generate_skill_questions(session_id)
    
    first_question = sessions[session_id]["questions"][0] if sessions[session_id]["questions"] else "No questions available."
    return session_id, first_question

def _generate_skill_questions(session_id: str) -> None:
    """
    Helper function to generate questions for the current skill via LLM.
    """
    session = sessions[session_id]
    skill = session["current_skill"]
    
    # Use llm_service to generate questions
    questions = generate_questions(skill)
    
    # Fallback in case LLM API fails or returns empty
    if not questions:
        questions = [f"Could you describe your experience and a complex problem you solved using {skill}?"]
        
    session["questions"] = questions
    session["current_question_index"] = 0

def get_next_question(session_id: str) -> str:
    """
    Returns the next question from the current skill.
    If no more questions, moves to the next skill.
    If all skills are done, returns 'assessment_complete'.
    """
    if session_id not in sessions:
        raise ValueError("Invalid session_id.")
        
    session = sessions[session_id]
    
    # Check if there are still questions left for the current skill
    if session["current_question_index"] < len(session["questions"]):
        return session["questions"][session["current_question_index"]]
    
    # Exhausted questions for current skill -> move to next skill
    session["current_skill_index"] += 1
    
    # Check if all skills are completed
    if session["current_skill_index"] >= len(session["skills"]):
        return "assessment_complete"
        
    # Set up the new skill and generate its questions
    session["current_skill"] = session["skills"][session["current_skill_index"]]
    _generate_skill_questions(session_id)
    
    # Return the first question of the new skill
    return session["questions"][session["current_question_index"]]

def submit_answer(session_id: str, answer: str) -> str:
    """
    Stores the user's answer, evaluates it using LLM, updates the score, 
    and returns the next question.
    """
    if session_id not in sessions:
        raise ValueError("Invalid session_id.")
        
    if not answer or not answer.strip():
        raise ValueError("Answer cannot be empty.")
        
    session = sessions[session_id]
    
    # Boundary check if someone tries to submit after completion
    if session["current_skill_index"] >= len(session["skills"]):
        return "assessment_complete"
        
    current_skill = session["current_skill"]
    current_question = session["questions"][session["current_question_index"]]
    
    # 1. Store answer
    session["answers"].append({
        "skill": current_skill,
        "question": current_question,
        "answer": answer
    })
    
    # 2. Evaluate answer using llm_service
    evaluation = evaluate_answer(current_question, answer)
    score = evaluation.get("score", 0)
    
    # 3. Update score
    session["scores"][current_skill]["total"] += score
    session["scores"][current_skill]["count"] += 1
    
    # Advance to the next question index
    session["current_question_index"] += 1
    
    # 4. Return next question
    return get_next_question(session_id)

def get_result(session_id: str) -> Dict[str, str]:
    """
    Calculates and returns the final proficiency level for each skill.
    """
    if session_id not in sessions:
        raise ValueError("Invalid session_id.")
        
    session = sessions[session_id]
    final_scores = {}
    
    for skill, stats in session["scores"].items():
        total = stats["total"]
        count = stats["count"]
        
        if count == 0:
            final_scores[skill] = "Not Evaluated"
            continue
            
        avg_score = total / count
        
        # Determine proficiency based on average score (0-10 scale)
        if avg_score >= 8:
            final_scores[skill] = "Advanced"
        elif avg_score >= 5:
            final_scores[skill] = "Intermediate"
        else:
            final_scores[skill] = "Beginner"
            
    return final_scores
