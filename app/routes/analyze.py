import io
import os
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Dict, Any, List

from app.services.resume_parser import parse_resume
from app.services.jd_parser import extract_skills
from app.services.assessment_service import start_assessment, submit_answer, get_result
from app.services.gap_analyzer import analyze_gap
from app.services.learning_plan import generate_learning_plan

router = APIRouter(tags=["Pipeline"])

@router.post("/analyze")
async def analyze_pipeline(
    file: UploadFile = File(...),
    jd_text: str = Form(...)
):
    """
    Self-contained endpoint to run the entire AI Resume Analyzer pipeline.
    """
    temp_file_path = None
    try:
        # Basic Validation
        if not file.filename:
            raise ValueError("No file provided.")
        if not jd_text or not jd_text.strip():
            raise ValueError("Job description text cannot be empty.")
            
        # Step 1: Save uploaded resume temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # Step 2: Parse resume -> extract skills
        # parse_resume expects a BytesIO stream
        with open(temp_file_path, "rb") as f:
            file_stream = io.BytesIO(f.read())
            resume_data = parse_resume(file_stream, file.filename)
            
        resume_skills = resume_data.get("skills", [])
        
        # Step 3: Extract JD skills from jd_text
        jd_skills = extract_skills(jd_text)
        if not jd_skills:
            raise ValueError("No skills could be extracted from the provided job description.")
            
        # Step 4: Run assessment automatically (simulate answers)
        session_id, current_question = start_assessment(jd_skills)
        while current_question != "assessment_complete":
            current_question = submit_answer(session_id, "This is a simulated sample answer.")
            
        # Step 5: Get assessment scores
        assessment_scores = get_result(session_id)
        
        # Step 6: Run gap analysis
        gap_analysis = analyze_gap(jd_skills, assessment_scores, resume_skills)
        
        # Step 7: Generate learning plan
        missing = gap_analysis.get("missing_skills", [])
        weak = gap_analysis.get("weak_skills", [])
        skills_to_learn = list(set(missing + weak))
        
        learning_plan = []
        if skills_to_learn:
            learning_plan = generate_learning_plan(skills_to_learn, "Beginner")
            
        # Final JSON Output
        return {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "assessment_scores": assessment_scores,
            "gap_analysis": gap_analysis,
            "learning_plan": learning_plan
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")
    finally:
        # Cleanup temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_error:
                print(f"Failed to cleanup temp file: {cleanup_error}")
