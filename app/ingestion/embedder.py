from openai import OpenAI
from app.core.config import settings
client=OpenAI(api_key=settings.openai_api_key)
def create_embedding(text:str):
    response=client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding















# We convert our document chunks into vectors using an embedding model 
#and store the vectors together with their text and metadata in Qdrant/vector database. 
# #When a user submits a query, we convert that query into a vector using the same embedding model. 
# Qdrant compares the query vector with the stored chunk vectors and retrieves the most semantically relevant chunks.
#  Those retrieved chunks, together with the user's question, are then provided to the LLM, 
# then LLM generates the grounded answer.

 
# Question :Why did we initially choose text-embedding-3-large?

# 1. Our legal RAG system requires strong semantic retrieval.
# 2. Legal questions may use different wording from the source documents.
# 3. text-embedding-3-large is OpenAI's most capable current embedding model for English and non-English tasks.
# 4. It provides stronger benchmark retrieval performance than text-embedding-3-small.
# 5. Retrieval quality is initially more important to our legal MVP than minimizing embedding cost.
# 6. It supports up to 3072 dimensions and allows dimension reduction if we later need to optimize storage/cost.

# Important:
# We are selecting it as our BASELINE, not assuming it is automatically the best embedding model for our legal dataset.

# Later we should evaluate retrieval quality (e.g., Recall@K/MRR) and
# compare alternatives if necessary.need strong semantic retrieval,Retrieval quality is important.



