import io
from fastapi import APIRouter, UploadFile, File
from app.services.resume_parser import parse_resume

router = APIRouter(tags=["Resume"])

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a candidate's resume for analysis.
    """
    content = await file.read()
    file_stream = io.BytesIO(content)
    
    result = parse_resume(file_stream, file.filename)
    
    return result
