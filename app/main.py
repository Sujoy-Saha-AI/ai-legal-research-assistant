from fastapi import FastAPI
from app.api.research import router as research_router

app=FastAPI()
app.include_router(research_router)
@app.get("/")
def root():
    return {"message": "AI legal Research Assistnat API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
