from rank_bm25 import BM25Okapi
from app.ingestion.vector_store import client

def get_all_chunks():
    records, _ = client.scroll(
        collection_name="legal_documents",
        limit=100,
        with_payload=True
    )

    return records

def tokenize_chunks(records):
    tokenized_corpus = [
        record.payload["text"].lower().split()
        for record in records
    ]

    return tokenized_corpus

def build_bm25_index(records):
    tokenized_corpus = tokenize_chunks(records)
    bm25 = BM25Okapi(tokenized_corpus)

    return bm25

def lexical_retrieve(question: str, limit: int = 3):
    records = get_all_chunks()
    bm25 = build_bm25_index(records)

    tokenized_query = question.lower().split()
    scores = bm25.get_scores(tokenized_query)

    ranked_indices = scores.argsort()[::-1][:limit]

    results = [
        {
            "point": records[index],
            "score": float(scores[index])
        }
        for index in ranked_indices
    ]

    return results