from fastapi import APIRouter
from pydantic import BaseModel
class ResearchRequest(BaseModel):
    question:str

router = APIRouter()

@router.post("/research")
def research_Assistant(request:ResearchRequest):
    return{"question_received":request.question}