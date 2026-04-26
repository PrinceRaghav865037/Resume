import re
from typing import List

# A predefined list of common technical and soft skills for matching.
# In a robust system, this could be loaded from a database or a trained spaCy NER model could be used.
COMMON_SKILLS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "react", "node.js", "angular", "vue",
    "html", "css", "sql", "nosql", "mongodb", "postgresql", "mysql", "aws",
    "azure", "gcp", "docker", "kubernetes", "git", "linux", "machine learning",
    "data science", "nlp", "artificial intelligence", "agile", "scrum", "leadership",
    "communication", "teamwork", "problem solving", "fastapi", "django", "flask",
    "rest api", "graphql", "ci/cd", "jenkins", "terraform", "pandas", "numpy", "pytorch",
    "tensorflow", "keras", "scikit-learn"
}

def preprocess_text(text: str) -> str:
    """
    Basic preprocessing of the job description text:
    - Lowercase
    - Remove special characters (keeping essential ones like +, -, .)
    - Remove extra whitespace
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep alphanumeric, spaces, and important symbols (+, -, ., /)
    text = re.sub(r'[^\w\s\.\,\-\+\/]', ' ', text)
    
    # Replace multiple consecutive spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_skills(text: str) -> List[str]:
    """
    Extracts skills from a raw job description using basic preprocessing 
    and keyword matching.
    """
    cleaned_text = preprocess_text(text)
    
    found_skills = set()
    
    # Simple word/phrase boundary matching
    for skill in COMMON_SKILLS:
        # Escape the skill to handle characters like '+', '.', '/'
        escaped_skill = re.escape(skill)
        
        # Word boundaries \b handle standard words well, but we need 
        # custom boundaries for terms with special characters (like c++ or node.js)
        # Using a regex that checks for space/boundary around the skill
        pattern = r'(?:\b|\s)' + escaped_skill + r'(?:\b|\s|\.|\,|$)'
        
        if re.search(pattern, cleaned_text):
            found_skills.add(skill)
            
    return sorted(list(found_skills))
