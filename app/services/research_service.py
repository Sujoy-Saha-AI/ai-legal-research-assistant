# initially in the FasAPI service layer creation the function was like 
#def process_research_question(question:str):
   # return {"processed question":question}
# later we used below whenever the retriever.py and generator.py  file is done

from app.retrieval.retriever import retrieve_chunks
from app.generation.generator import generate_answer
def process_research_question(question:str):
    retrieved_points = retrieve_chunks(question)
    context_parts = [point.payload["text"] for point in retrieved_points]
    context = "\n\n".join(context_parts)
    answer = generate_answer(question, context)

    return {"answer": answer}