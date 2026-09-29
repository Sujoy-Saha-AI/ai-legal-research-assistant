from fastapi import APIRouter
from app.services.research_service import process_research_question
from pydantic import BaseModel
class ResearchRequest(BaseModel):
    question:str

router = APIRouter()

@router.post("/research")
def research_Assistant(request:ResearchRequest):
    return process_research_question(request.question)