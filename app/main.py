from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.research import router as research_router
# from app.ingestion.ingestion_pipeline import ingest_document   # we had it till working on the memory and ingest_document("data/abreu_v._howard_university.pdf") used below 

@asynccontextmanager
async def lifespan(app: FastAPI):
                                        # until the we are working on memory there was line here as ingest_document("data/abreu_v._howard_university.pdf").after ingesting the chunk into qdrant cloud we deleted this line
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(research_router)

@app.get("/")
def root():
    return {"message": "AI legal Research Assistant API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}