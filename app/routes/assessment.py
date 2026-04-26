from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.services.assessment_service import start_assessment, submit_answer, get_result

router = APIRouter(tags=["Assessment"])

class StartAssessmentRequest(BaseModel):
    skills: List[str] = Field(..., min_items=1, description="List of skills to assess")

class SubmitAnswerRequest(BaseModel):
    session_id: str = Field(..., description="The ID of the active assessment session")
    answer: str = Field(..., min_length=1, description="The candidate's answer")

@router.post("/start-assessment")
async def api_start_assessment(request: StartAssessmentRequest):
    """
    Start a new conversational assessment session for the given skills.
    Returns the session ID and the first generated question.
    """
    try:
        session_id, first_question = start_assessment(request.skills)
        return {
            "session_id": session_id,
            "question": first_question
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred while starting assessment.")

@router.post("/submit-answer")
async def api_submit_answer(request: SubmitAnswerRequest):
    """
    Submit an answer to the current question.
    Returns the next question if there are more, or a completion message if done.
    """
    try:
        next_question = submit_answer(request.session_id, request.answer)
        
        if next_question == "assessment_complete":
            return {
                "message": "Assessment complete. You can now get your results.",
                "status": "completed"
            }
            
        return {
            "next_question": next_question,
            "status": "in_progress"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred while submitting answer.")

@router.get("/result/{session_id}")
async def api_get_result(session_id: str):
    """
    Get the final proficiency scores for all evaluated skills in a session.
    """
    try:
        results = get_result(session_id)
        return {
            "session_id": session_id,
            "results": results
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred while fetching results.")
