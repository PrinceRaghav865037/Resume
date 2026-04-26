from fastapi import APIRouter
from pydantic import BaseModel
from app.services.jd_parser import extract_skills

router = APIRouter(tags=["Job Description"])

class JDRequest(BaseModel):
    text: str

@router.post("/upload-jd")
async def upload_jd(request: JDRequest):
    """
    Upload a Job Description for analysis.
    Accepts raw text and extracts relevant skills.
    """
    skills = extract_skills(request.text)
    
    return {
        "message": "JD processed successfully",
        "skills": skills
    }
