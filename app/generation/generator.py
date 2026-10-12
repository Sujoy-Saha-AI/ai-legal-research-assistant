from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def generate_answer(question: str, context: str):
    response = client.responses.create(
        model="gpt-5-mini",
        instructions="Answer the legal research question using only the provided context. If the context does not contain enough information to answer the question, clearly state that the available evidence is insufficient.",
        input=f"Question:\n{question}\n\nContext:\n{context}"
    )

    return response.output_text