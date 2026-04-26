from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

from app.services.gap_analyzer import analyze_gap

router = APIRouter(tags=["Gap Analysis"])

class GapRequest(BaseModel):
    jd_skills: List[str] = Field(..., description="List of skills required by the job description")
    assessed_skills: Dict[str, str] = Field(..., description="Dictionary mapping skills to their assessed proficiency levels")

@router.post("/analyze-gap")
async def api_analyze_gap(request: GapRequest):
    """
    Analyze the skill gap between a job description and a candidate's assessed skills.
    Returns categorized lists of missing, weak, and strong skills.
    """
    try:
        # Basic validation for completely empty inputs
        if not request.jd_skills and not request.assessed_skills:
            raise ValueError("Both jd_skills and assessed_skills cannot be completely empty.")
            
        # Pydantic automatically handles the format validation.
        # Calling the service logic
        result = analyze_gap(request.jd_skills, request.assessed_skills)
        
        return result
        
    except ValueError as ve:
        # Client-side error (400 Bad Request)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Server-side error (500 Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
