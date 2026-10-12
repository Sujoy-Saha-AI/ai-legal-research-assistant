from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_document
from app.ingestion.embedder import create_embedding
from app.ingestion.vector_store import store_chunk

from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_document
from app.ingestion.embedder import create_embedding
from app.ingestion.vector_store import store_chunk

def ingest_document(file_path: str):
    my_result = load_document(file_path)
    my_structured_document = my_result.document
    my_chunks = chunk_document(my_structured_document)

    for point_id, chunk in enumerate(my_chunks, start=1):  # Pair each chunk with a point ID starting from 1
        vector = create_embedding(chunk.text)
        store_chunk(point_id, vector, chunk.text)

    return len(my_chunks)


