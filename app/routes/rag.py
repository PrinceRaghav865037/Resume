from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict
from app.services.vector_store import retrieve_resources

router = APIRouter(tags=["RAG"])

@router.get("/test-rag", response_model=List[Dict[str, str]])
async def test_rag(
    skill: str = Query(..., description="The skill to search learning resources for")
):
    """
    Query the in-memory FAISS RAG system to find the top 5 learning resources 
    based on the semantic similarity of the skill.
    """
    # 1. Validate input
    if not skill or not skill.strip():
        raise HTTPException(status_code=400, detail="Skill query parameter cannot be empty.")
        
    try:
        # 2. Call the vector store
        results = retrieve_resources(skill)
        return results
        
    except ValueError:
        # Our vector_store throws a ValueError if no results are found.
        # To maintain the array return type constraint, we return an empty array.
        return []
        
    except Exception as e:
        # Generic error fallback
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
