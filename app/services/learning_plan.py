import json
from typing import List, Dict, Any
from app.services.llm_service import client

def generate_learning_plan(skill_gaps: List[str], user_level: str) -> List[Dict[str, Any]]:
    """
    Generates a structured, step-by-step learning roadmap for a candidate's skill gaps.
    
    Args:
        skill_gaps: A list of skills the user needs to learn or improve.
        user_level: The current overall level of the user (e.g., "Beginner", "Intermediate", "Advanced").
        
    Returns:
        A list of dictionaries containing the skill name, duration, step-by-step plan, and resources.
    """
    
    # 1. Error handling: Empty inputs
    if not skill_gaps:
        raise ValueError("The skill_gaps list cannot be empty.")
        
    if not user_level or not user_level.strip():
        raise ValueError("The user_level cannot be empty.")
        
    skills_str = ", ".join(skill_gaps)
    
    # 2. Prompt design
    system_prompt = (
        "You are an expert career coach and technical mentor. "
        "Your task is to generate a highly actionable, structured learning roadmap for a candidate "
        "to master a set of specific skills. You must strictly output ONLY valid JSON format. "
        "Do NOT wrap the output in markdown code blocks (e.g., do not use ```json). "
        "Do NOT include any explanations, preambles, or postscripts."
    )
    
    user_prompt = f"""
    The candidate's current overall level is: {user_level}.
    The candidate has gaps in the following skills: {skills_str}.
    
    Generate a learning roadmap for each skill.
    Return an array of JSON objects, where each object has EXACTLY this format:
    [
      {{
        "skill": "<skill name>",
        "duration": "<realistic estimated duration, e.g., '4 weeks'>",
        "plan": "<concise step-by-step learning plan>",
        "resources": [
          "<link to tutorial, docs, or course 1>",
          "<link to tutorial, docs, or course 2>",
          "<link to tutorial, docs, or course 3>"
        ]
      }}
    ]
    """
    
    try:
        # 3. Call OpenAI/Groq using the imported client
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        
        raw_response = response.choices[0].message.content
        if not raw_response:
            return []
            
        # Strip potential markdown formatting if the LLM disobeys "ONLY valid JSON"
        cleaned_response = raw_response.strip("` \n").removeprefix("json\n").strip()
        
        # 4. Parse the JSON string into a Python object
        parsed_json = json.loads(cleaned_response, strict=False)
        
        # Ensure the output is a list as expected
        if isinstance(parsed_json, list):
            return parsed_json
        elif isinstance(parsed_json, dict):
            # In case it wraps the array inside an object
            return [parsed_json]
        else:
            raise ValueError("LLM returned an unexpected JSON structure.")
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON. Error: {str(e)}\nRaw Response: {raw_response}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the learning plan: {str(e)}")
