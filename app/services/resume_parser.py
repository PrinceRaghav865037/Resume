import os
import io
import pdfplumber
import docx
from typing import Dict, Any, Union

def extract_text_from_pdf(file_path: Union[str, io.BytesIO]) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_path: Union[str, io.BytesIO]) -> str:
    """Extracts text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def parse_resume(file_stream: io.BytesIO, filename: str) -> Dict[str, Any]:
    """
    Parses a resume (PDF or DOCX) and extracts skills, education, and experience.
    Returns a structured JSON-serializable dictionary.
    """
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.pdf':
        text = extract_text_from_pdf(file_stream)
    elif ext in ['.doc', '.docx']:
        text = extract_text_from_docx(file_stream)
    else:
        return {"error": "Unsupported file format. Please provide a PDF or DOCX file."}

    # Basic heuristic parsing to extract sections
    skills = []
    education = []
    experience = []
    
    lines = text.split('\n')
    current_section = None
    
    # Simple keywords to identify sections (can be expanded)
    skills_keywords = ['skills', 'technologies', 'technical skills', 'core competencies']
    edu_keywords = ['education', 'academic background', 'qualifications', 'academic history']
    exp_keywords = ['experience', 'work history', 'employment history', 'professional experience']
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
            
        lower_line = cleaned_line.lower()
        
        # Check for section headers (heuristics: line is short and matches keywords)
        words_count = len(lower_line.split())
        if words_count <= 4 and any(keyword in lower_line for keyword in skills_keywords):
            current_section = 'skills'
            continue
        elif words_count <= 4 and any(keyword in lower_line for keyword in edu_keywords):
            current_section = 'education'
            continue
        elif words_count <= 4 and any(keyword in lower_line for keyword in exp_keywords):
            current_section = 'experience'
            continue
            
        # Append to current section
        if current_section == 'skills':
            # Simple list extraction: split by commas if present
            if ',' in cleaned_line:
                skills.extend([s.strip() for s in cleaned_line.split(',') if s.strip() and len(s) > 1])
            else:
                # Omit very long lines from skills to avoid picking up paragraphs
                if len(cleaned_line.split()) <= 5:
                    skills.append(cleaned_line.lstrip('-•* '))
        elif current_section == 'education':
            education.append(cleaned_line)
        elif current_section == 'experience':
            experience.append(cleaned_line)
            
    # Clean up and structure the result
    return {
        "skills": list(set(skills)),  # Remove duplicates
        "education": education,
        "experience": experience,
        "raw_text_extracted": bool(text.strip())
    }
