from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.research import router as research_router
from app.ingestion.ingestion_pipeline import ingest_document

@asynccontextmanager
async def lifespan(app: FastAPI):
    ingest_document("data/abreu_v._howard_university.pdf")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(research_router)

@app.get("/")
def root():
    return {"message": "AI legal Research Assistant API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}