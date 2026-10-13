from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_document
from app.ingestion.embedder import create_embedding
from app.ingestion.vector_store import store_chunk

def ingest_document(file_path: str):
    my_result = load_document(file_path)
    my_structured_document = my_result.document
    my_chunks = chunk_document(my_structured_document)

    for point_id, chunk in enumerate(my_chunks, start=1):  # (chunk is a variable) Pair each chunk with a point ID starting from 1.intially it was [chunk A, chunk B, Chunk C] later it became 1 chunkA , 2 chunk B 3 chunkC
        vector = create_embedding(chunk.text)
        filename=chunk.meta.origin.filename # we need to call the metadata before store the chunk. this step came when we decided to store the metadata.
        page = chunk.meta.doc_items[0].prov[0].page_no # from the chunk result doc_items is the collection of doclingitem prov means the provinance in the chunk result.
        heading=chunk.meta.headings # in metadata result we have the output like headings=['I.'] thats why we write "headings" in the source
        store_chunk(point_id, vector, chunk.text,filename,page,heading) # since we have to store the chunk and vector both that's why we mentioned the chunk.text in the store_chunk

    return len(my_chunks)



# ============================================================
# INGESTION PIPELINE — TESTING COMMANDS
# ============================================================

# ------------------------------------------------------------
# TEST 1: Check whether ingestion_pipeline.py loads successfully
# ------------------------------------------------------------

# python -c "from app.ingestion.ingestion_pipeline import ingest_document; print('Ingestion Pipeline loaded successfully')"

# Purpose:
# Checks whether Python can import ingestion_pipeline.py
# and find the ingest_document() function without syntax/import errors.


# ------------------------------------------------------------
# TEST 2: Directly verify that ingest_document() exists
# ------------------------------------------------------------

# python -c "from app.ingestion.ingestion_pipeline import ingest_document; print(ingest_document)"

# Expected output approximately:
# <function ingest_document at 0x...>

# Purpose:
# Confirms that Python successfully finds and imports
# the ingest_document() function from ingestion_pipeline.py.


# ------------------------------------------------------------
# TEST 3: Run the COMPLETE ingestion pipeline
# and verify all chunks are stored in Qdrant
# ------------------------------------------------------------

# python -c "from app.ingestion.ingestion_pipeline import ingest_document; from app.ingestion.vector_store import client; total=ingest_document('data/abreu_v._howard_university.pdf'); print('Chunks processed:', total); result=client.count(collection_name='legal_documents'); print('Points stored in Qdrant:', result.count)"

# Our actual result:
# Chunks processed: 15
# Points stored in Qdrant: 15

# Purpose:
# 1. Loads the Abreu PDF
# 2. Converts it into a Docling structured document
# 3. Creates chunks using HybridChunker
# 4. Loops through all chunks
# 5. Creates an embedding for each chunk
# 6. Stores each chunk as a Qdrant Point
# 7. Returns the total number of chunks processed
# 8. Asks Qdrant how many Points were actually stored


# ------------------------------------------------------------
# IMPORTANT: What happens inside ingest_document()
# ------------------------------------------------------------

# PDF file path
#       ↓
# load_document(file_path)
#       ↓
# ConversionResult
#       ↓
# my_result.document
#       ↓
# Structured Docling document
#       ↓
# chunk_document(my_structured_document)
#       ↓
# my_chunks
#       ↓
# 15 chunks
#       ↓
# for point_id, chunk in enumerate(my_chunks, start=1):
#       ↓
# create_embedding(chunk.text)
#       ↓
# 3072-dimensional vector for current chunk
#       ↓
# store_chunk(point_id, vector, chunk.text)
#       ↓
# Qdrant Point


# ------------------------------------------------------------
# QDRANT POINT CREATED FOR EACH CHUNK
# ------------------------------------------------------------

# Point 1:
# id      = 1
# vector  = embedding of Chunk 1
# payload = text of Chunk 1

# Point 2:
# id      = 2
# vector  = embedding of Chunk 2
# payload = text of Chunk 2

# ...

# Point 15:
# id      = 15
# vector  = embedding of Chunk 15
# payload = text of Chunk 15


# ------------------------------------------------------------
# IMPORTANT CURRENT LIMITATION
# ------------------------------------------------------------

# Our vector_store.py currently uses:
# QdrantClient(":memory:")

# Therefore Qdrant is currently an IN-MEMORY database.
# The 15 Points exist only while that Python process is running.
# When the process terminates, those Points disappear.

# This is why our final testing command performs:
# ingest_document(...)
# AND
# client.count(...)
# within the SAME Python process.
