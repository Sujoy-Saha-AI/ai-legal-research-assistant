from app.evaluation.test_cases import TEST_CASES
from app.retrieval.hybrid_retriever import hybrid_retrieve

def evaluate_test_case(test_case):
    question = test_case["question"]
    relevant_point_ids = test_case["relevant_point_ids"]

    results = hybrid_retrieve(question)

    retrieved_point_ids = [
        result["point"].id
        for result in results
    ]

    hit_at_k = any(
        point_id in relevant_point_ids
        for point_id in retrieved_point_ids
    )
    reciprocal_rank = 0.0

    for rank, point_id in enumerate(retrieved_point_ids, start=1):
        if point_id in relevant_point_ids:
            reciprocal_rank = 1 / rank
            break

    return {
    "question": question,
    "relevant_point_ids": relevant_point_ids,
    "retrieved_point_ids": retrieved_point_ids,
    "hit_at_k": hit_at_k,
    "reciprocal_rank":reciprocal_rank
}

question = "What did the court ultimately decide regarding Howard University's motion to dismiss?"

results = hybrid_retrieve(question, limit=10)

print([
    (result["point"].id, round(result["score"], 6))
    for result in results
])