from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
client= QdrantClient(":memory:")

client.create_collection(
    collection_name="legal_documents",
    vectors_config=VectorParams(
        size=3072,
        distance=Distance.COSINE
    )
)

# code explanation for above
# intially PointStruct class was not on above code to execute next code we will add it
# create_collection = Qdrant method , collection_name = parameter define by create_collection method, legal_document= file name that we chose
#

def store_chunk(point_id: int, vector: list, text: str):
    point = PointStruct(
        id=point_id,
        vector=vector,
        payload={"text":text}
        )
    client.upsert(
    collection_name="legal_documents",
    points=[point]
    )


# Qdrant terminology the object we store is called point and it contains id,vector,payload(chunk+metadata)
# store_chunk is our function name , PointStruct is the class and Point_id, vector,text is our defined parameter to link with id,vector,payload


# “This collection stores 3,072-dimensional vectors,
# and Qdrant should use cosine distance when comparing them for similarity.” 

# Execution 

# let's check Qdrant actually creates our legal_documents
# python -c "from app.ingestion.vector_store import client; print(client.get_collections())"

# it's result shows the file legal connection is stored 



# Things to remember:
# Qdrant-defined names: collection_name, points, and earlier id, vector, payload.
# Names we chose: legal_documents, point, point_id, text, and our function name store_chunk.
# And [point] means we're passing a Python list containing our one PointStruct object to Qdrant's points parameter.