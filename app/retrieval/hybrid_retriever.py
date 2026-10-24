from app.retrieval.retriever import retrieve_chunks
from app.retrieval.lexical_retriever import lexical_retrieve

def hybrid_retrieve(question: str, limit: int = 3):
    semantic_results = retrieve_chunks(question)
    lexical_results = lexical_retrieve(question, limit=limit)

    fused_results = reciprocal_rank_fusion(
        semantic_results,
        lexical_results
    )

    return fused_results[:limit]

def reciprocal_rank_fusion(semantic_results, lexical_results, k: int = 60):
    fused_scores = {}

    for rank, point in enumerate(semantic_results, start=1):
        fused_scores[point.id] = {
            "point": point,
            "score": 1 / (k + rank)
        }

    for rank, result in enumerate(lexical_results, start=1):
        point = result["point"]

        if point.id in fused_scores:
            fused_scores[point.id]["score"] += 1 / (k + rank)
        else:
            fused_scores[point.id] = {
                "point": point,
                "score": 1 / (k + rank)
            }

    ranked_results = sorted(
        fused_scores.values(),
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked_results