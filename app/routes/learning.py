from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.services.learning_plan import generate_learning_plan

router = APIRouter(tags=["Learning Plan"])

class LearningPlanRequest(BaseModel):
    skill_gaps: List[str] = Field(..., description="List of skills the user needs to learn or improve")
    user_level: str = Field(..., description="The user's overall level (e.g., Beginner, Intermediate, Advanced)")

@router.post("/generate-learning-plan")
async def api_generate_learning_plan(request: LearningPlanRequest):
    """
    Generate a personalized, structured learning roadmap for the candidate's skill gaps.
    """
    try:
        # Basic validation
        if not request.skill_gaps:
            raise ValueError("The skill_gaps list cannot be empty.")
            
        valid_levels = ["beginner", "intermediate", "advanced"]
        if not request.user_level or request.user_level.strip().lower() not in valid_levels:
            raise ValueError(f"Invalid user_level '{request.user_level}'. Must be one of: Beginner, Intermediate, Advanced.")
            
        # Generate the plan
        plan = generate_learning_plan(request.skill_gaps, request.user_level)
        
        return {
            "message": "Learning plan generated successfully",
            "learning_plan": plan
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error occurred: {str(e)}")
