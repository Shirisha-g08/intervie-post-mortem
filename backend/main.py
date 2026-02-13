from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import analysis_logic
import shutil
import os

app = FastAPI(title="Interview Post-Mortem API")

# Mount static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

# Ensure directories exist to prevent runtime errors
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=templates_dir)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResponse(BaseModel):
    match_score: int
    missing_skills: list[str]
    skill_gap_explanation: str
    clarity_score: int
    structure_feedback: list[str]
    confidence_rating: str
    confidence_feedback: list[str]
    rejection_reasons: list[dict]
    action_plan: dict

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_interview(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    interview_experience: str = Form(...)
):
    try:
        # Save resume temporarily to read it (or read in memory)
        # For pypdf, we can read from bytes stream usually, but saving to temp is safer for some libs
        # Here we will try to read bytes directly if possible, or save to temp
        
        # Read resume content
        resume_content = await resume.read()
        
        # Extract text from resume
        resume_text = analysis_logic.extract_text_from_pdf(resume_content)
        
        # Analyze Match
        match_analysis = analysis_logic.analyze_match(resume_text, job_description)
        
        # Analyze Interview Experience
        interview_analysis = analysis_logic.analyze_interview(interview_experience)
        
        # Synthesize final result
        result = analysis_logic.generate_feedback(match_analysis, interview_analysis)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
