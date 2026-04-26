from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, resume, jd, assessment, gap, learning, rag, analyze
from app.services.llm_service import _get_completion

app = FastAPI(
    title="AI Resume Analyzer API",
    description="API for conversational skill assessment and personalized learning plans",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from the routes module
app.include_router(health.router)
app.include_router(resume.router)
app.include_router(jd.router)
app.include_router(assessment.router)
app.include_router(gap.router)
app.include_router(learning.router)
app.include_router(rag.router)
app.include_router(analyze.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Resume Analyzer API. Go to /docs for the Swagger UI."}

@app.get("/test-openai")
def test_openai():
    """
    Test endpoint to verify OpenAI API integration.
    """
    try:
        # A simple prompt to verify the key and connection
        response = _get_completion("Say exactly: 'OpenAI integration is working!'", temperature=0.0)
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
