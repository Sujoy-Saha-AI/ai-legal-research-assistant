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



# ============================================================
# RETRIEVAL PIPELINE — TESTING EXPERIMENTS
# AI Legal Research Assistant
# ============================================================


# ------------------------------------------------------------
# TEST 1 — Verify retriever.py can be imported
# ------------------------------------------------------------

# Purpose:
# Check whether Python can successfully import the retrieve_chunks()
# function from app/retrieval/retriever.py.

# Terminal command:
# python -c "from app.retrieval.retriever import retrieve_chunks; print(retrieve_chunks)"

# Expected output:
# <function retrieve_chunks at 0x...>

# Actual result:
# SUCCESS

# Meaning:
# - retriever.py has no blocking syntax/import error.
# - Python recognizes retrieve_chunks as a function.
# - This test does NOT perform an actual Qdrant search.


# ------------------------------------------------------------
# TEST 2 — Full ingestion + first semantic retrieval
# ------------------------------------------------------------

# Purpose:
# Test the complete flow:
# PDF -> parsing -> chunking -> embedding -> Qdrant storage
# -> question embedding -> semantic search -> Top-3 results.

# Important:
# Qdrant currently uses ":memory:".
# Therefore ingestion and retrieval must happen in the SAME
# Python process. Otherwise the stored points disappear.

# Terminal command:
# python -c "from app.ingestion.ingestion_pipeline import ingest_document; from app.retrieval.retriever import retrieve_chunks; ingest_document('data/abreu_v._howard_university.pdf'); results=retrieve_chunks('What claims did Abreu bring against Howard University?'); print(results)"

# Test question:
# What claims did Abreu bring against Howard University?

# Qdrant returned Top-3 results:
# Point 9  -> score approximately 0.6725
# Point 2  -> score approximately 0.6668
# Point 10 -> score approximately 0.6482

# Actual result:
# SUCCESS

# Important observation:
# Point 2 contained the most direct answer to the question.

# Point 2 stated that Abreu brought:
# 1. breach of contract
# 2. failure to accommodate under Title III of the ADA
# 3. failure to accommodate under Section 504
#    of the Rehabilitation Act

# This confirms that semantic retrieval is working.


# ------------------------------------------------------------
# TEST 3 — Understand the similarity score
# ------------------------------------------------------------

# Example result:
# ScoredPoint(
#     id=9,
#     score=0.6725154765658727,
#     payload={...}
# )

# Meaning:
# Qdrant compares the lawyer's query vector with the stored
# document vectors.

# Current collection uses:
# Distance.COSINE

# Therefore Qdrant ranks the stored points according to
# cosine similarity.

# Higher-ranked results are treated as more similar to the query
# under the current embedding/retrieval configuration.

# Important:
# The highest-scoring chunk is not automatically the best
# evidence for answering the legal question.

# In our experiment:
# Point 9 ranked first,
# but Point 2 was arguably the most directly responsive chunk.

# This demonstrates why later stages such as retrieval evaluation
# and reranking can be important.


# ------------------------------------------------------------
# TEST 4 — Change retriever to return points directly
# ------------------------------------------------------------

# Originally:
# return results

# Changed to:
# return results.points

# Purpose:
# client.query_points() returns a Qdrant response object
# containing the retrieved points.

# Returning results.points gives the caller the actual
# ScoredPoint objects directly.

# Conceptually:
# Qdrant response object
#       ->
# results.points
#       ->
# [ScoredPoint, ScoredPoint, ScoredPoint]


# ------------------------------------------------------------
# TEST 5 — Verify results.points change
# ------------------------------------------------------------

# Terminal command:
# python -c "from app.ingestion.ingestion_pipeline import ingest_document; from app.retrieval.retriever import retrieve_chunks; ingest_document('data/abreu_v._howard_university.pdf'); results=retrieve_chunks('What claims did Abreu bring against Howard University?'); print(results[0])"

# Actual output started with:
# id=9
# score=0.672515...
# payload={'text': "Abreu's First Amended Complaint..."}

# Actual result:
# SUCCESS

# Meaning:
# results is now directly a collection/list-like sequence
# of retrieved ScoredPoint objects.

# results[0]
# means:
# retrieve the first/highest-ranked point.


# ------------------------------------------------------------
# TEST 6 — Understand vector=None
# ------------------------------------------------------------

# Retrieved Qdrant result displayed:
# vector=None

# This does NOT mean the vector was missing from Qdrant.

# We only need the retrieved payload/evidence for this stage,
# and the query response did not return the full stored vector.

# The stored vector was still used internally by Qdrant
# for similarity comparison.


# ------------------------------------------------------------
# TEST 7 — Extract text from the highest-ranked point
# ------------------------------------------------------------

# Terminal command:
# python -c "from app.ingestion.ingestion_pipeline import ingest_document; from app.retrieval.retriever import retrieve_chunks; ingest_document('data/abreu_v._howard_university.pdf'); results=retrieve_chunks('What claims did Abreu bring against Howard University?'); print(results[0].payload['text'])"

# Actual result:
# SUCCESS

# Important expression:
# results[0].payload["text"]

# Breakdown:
# results
#   -> retrieved points
#
# results[0]
#   -> first/highest-ranked ScoredPoint
#
# results[0].payload
#   -> payload dictionary attached to that point
#
# results[0].payload["text"]
#   -> original legal chunk text stored in the payload

# This confirmed that we can move from:
# Qdrant retrieval object
# ->
# actual legal evidence text.


# ------------------------------------------------------------
# TEST 8 — Extract text from ALL Top-3 retrieved points
# ------------------------------------------------------------

# Terminal command:
# python -c "from app.ingestion.ingestion_pipeline import ingest_document; from app.retrieval.retriever import retrieve_chunks; ingest_document('data/abreu_v._howard_university.pdf'); results=retrieve_chunks('What claims did Abreu bring against Howard University?'); print([point.payload['text'] for point in results])"

# Actual result:
# SUCCESS

# Important expression:
# [point.payload["text"] for point in results]

# This is a Python list comprehension.

# Conceptually:
# for each point in results
#       ->
# access point.payload
#       ->
# extract ["text"]
#       ->
# put the text into a new list

# Result conceptually:
# [
#     "retrieved legal chunk 1",
#     "retrieved legal chunk 2",
#     "retrieved legal chunk 3"
# ]


# ------------------------------------------------------------
# TEST 9 — Why retrieve multiple chunks?
# ------------------------------------------------------------

# Our experiment demonstrated an important RAG principle.

# Top result:
# Point 9
# Mainly discussed Abreu's breach-of-contract claim.

# Second result:
# Point 2
# Directly identified all three claims brought by Abreu.

# Therefore:
# We should not assume that results[0] alone contains
# all evidence needed to answer the question.

# Instead, multiple Top-K chunks can be supplied as context
# to the generation stage.

# Current baseline:
# limit=3

# Therefore:
# Top-K = 3

# This value is currently an initial configuration.
# It can later be evaluated and tuned.


# ------------------------------------------------------------
# CURRENT retriever.py LOGIC
# ------------------------------------------------------------

# from app.ingestion.embedder import create_embedding
# from app.ingestion.vector_store import client

# def retrieve_chunks(question: str):
#     query_vector = create_embedding(question)

#     results = client.query_points(
#         collection_name="legal_documents",
#         query=query_vector,
#         limit=3
#     )

#     return results.points


# ------------------------------------------------------------
# RETRIEVAL FUNCTION BREAKDOWN
# ------------------------------------------------------------

# question
# -> function parameter containing lawyer's question

# query_vector
# -> variable we created

# create_embedding(question)
# -> converts the lawyer's question into an embedding vector

# The same embedding model is used for:
# document chunks
# and
# lawyer's query

# This places both in the same embedding/vector space.


# client
# -> QdrantClient object imported from vector_store.py

# client.query_points(...)
# -> Qdrant method used to perform vector similarity retrieval

# collection_name="legal_documents"
# -> tells Qdrant which collection to search

# query=query_vector
# -> supplies the lawyer's question embedding to Qdrant

# limit=3
# -> asks Qdrant for the Top-3 results

# results
# -> our variable holding the Qdrant query response

# results.points
# -> actual retrieved ScoredPoint objects


# ------------------------------------------------------------
# COMPLETE RETRIEVAL FLOW
# ------------------------------------------------------------

# Lawyer's question
#       |
#       v
# retrieve_chunks(question)
#       |
#       v
# create_embedding(question)
#       |
#       v
# 3072-dimensional query vector
#       |
#       v
# Qdrant legal_documents collection
#       |
#       v
# Compare query vector against stored chunk vectors
#       |
#       v
# Cosine similarity
#       |
#       v
# Rank candidate chunks
#       |
#       v
# Top-3 ScoredPoints
#       |
#       v
# point.payload["text"]
#       |
#       v
# Retrieved legal evidence


# ------------------------------------------------------------
# END-TO-END PIPELINE COMPLETED SO FAR
# ------------------------------------------------------------

# Legal PDF
#       |
#       v
# Docling parsing
#       |
#       v
# Structured document
#       |
#       v
# HybridChunker
#       |
#       v
# 15 chunks
#       |
#       v
# text-embedding-3-large
#       |
#       v
# 3072-dimensional vectors
#       |
#       v
# Qdrant points
#       |
#       v
# Lawyer's question
#       |
#       v
# Query embedding
#       |
#       v
# Qdrant semantic retrieval
#       |
#       v
# Top-3 relevant chunks
#       |
#       v
# Extract payload["text"]
#       |
#       v
# Retrieved legal evidence
#       |
#       v
# NEXT: LLM GENERATION


# ------------------------------------------------------------
# IMPORTANT CURRENT LIMITATION
# ------------------------------------------------------------

# Qdrant is currently configured as:
# QdrantClient(":memory:")

# Therefore:
# Data exists only while the Python process is running.

# When the process ends:
# stored Qdrant points disappear.

# This is why our current tests perform:
# ingestion + retrieval
# inside the SAME Python process.

# Later we will replace this testing configuration with
# persistent/local or cloud Qdrant storage.


# ------------------------------------------------------------
# RETRIEVAL QUALITY OBSERVATION
# ------------------------------------------------------------

# Baseline semantic retrieval works successfully.

# However:
# highest similarity score != automatically best legal evidence.

# Example:
# Point 9 score ≈ 0.6725
# Point 2 score ≈ 0.6668

# Point 2 was more directly responsive to our specific question.

# This gives us a concrete reason for later implementing/testing:
# - Top-K tuning
# - reranking
# - metadata filtering
# - retrieval evaluation
# - hybrid semantic + lexical retrieval

# We should NOT change the retrieval strategy based on this
# single experiment yet.

# First establish the complete baseline RAG pipeline,
# then evaluate retrieval systematically.


# ------------------------------------------------------------
# CURRENT PROJECT POSITION
# ------------------------------------------------------------

# COMPLETED:
# PDF loading/parsing
# Structured document extraction
# Chunking
# Chunk inspection
# Embeddings
# Qdrant collection
# Vector storage
# Full 15-chunk ingestion pipeline
# Query embedding
# Semantic similarity retrieval
# Top-K retrieval
# Qdrant payload extraction

# NEXT:
# Generation layer
# -> provide retrieved evidence to an LLM
# -> generate an answer grounded in retrieved evidence
# -> later add source/citation handling