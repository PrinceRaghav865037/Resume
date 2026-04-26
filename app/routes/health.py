from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    Check if the application is healthy.
    """
    return {"status": "ok"}
