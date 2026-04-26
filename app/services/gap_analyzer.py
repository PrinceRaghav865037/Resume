from typing import List, Dict

def analyze_gap(jd_skills: List[str], assessed_skills: Dict[str, str], resume_skills: List[str] = None) -> Dict[str, List[str]]:
    """
    Analyzes the gap between the skills required in a job description 
    and the candidate's assessed skill levels, taking into account their resume.
    """
    result = {
        "missing_skills": set(),
        "weak_skills": set(),
        "strong_skills": set()
    }
    
    if not jd_skills:
        return {"missing_skills": [], "weak_skills": [], "strong_skills": []}
        
    if not assessed_skills:
        assessed_skills = {}
        
    # Edge Case: If resume_skills is not provided by older routes, fallback to assessed_skills keys
    if resume_skills is None:
        resume_skills = list(assessed_skills.keys())
        
    # Normalize inputs for case-insensitive matching
    normalized_resume = {s.lower().strip() for s in resume_skills if s and s.strip()}
    normalized_assessed = {
        k.lower().strip(): v.strip().title() if isinstance(v, str) else str(v)
        for k, v in assessed_skills.items()
    }
    
    for original_skill in jd_skills:
        if not original_skill or not original_skill.strip():
            continue
            
        clean_skill = original_skill.strip()
        normalized_skill = clean_skill.lower()
        
        # New Logic: Check if skill is on the resume first
        if normalized_skill not in normalized_resume:
            result["missing_skills"].add(clean_skill)
        else:
            level = normalized_assessed.get(normalized_skill, "Unknown")
            
            # Categorize based on new strict proficiency level rules
            if level in ["Beginner", "Intermediate"]:
                result["weak_skills"].add(clean_skill)
            elif level == "Advanced":
                result["strong_skills"].add(clean_skill)
            else:
                # Edge Case: On resume but assessment level unknown/missing
                # Treat as weak or missing. We'll default to missing to be safe.
                result["missing_skills"].add(clean_skill)
                
    return {
        "missing_skills": sorted(list(result["missing_skills"])),
        "weak_skills": sorted(list(result["weak_skills"])),
        "strong_skills": sorted(list(result["strong_skills"]))
    }
