from app.ingestion.embedder import create_embedding
from app.ingestion.vector_store import client

def retrieve_chunks(question: str):
    query_vector = create_embedding(question)

    results = client.query_points(
        collection_name="legal_documents",
        query=query_vector,
        limit=3
    )

    return results.points

