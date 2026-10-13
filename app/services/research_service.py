# initially in the FasAPI service layer creation the function was like 
#def process_research_question(question:str):
   # return {"processed question":question}
# later we used below whenever the retriever.py and generator.py  file is done

from app.retrieval.retriever import retrieve_chunks
from app.generation.generator import generate_answer

def process_research_question(question: str):
    retrieved_points = retrieve_chunks(question)

    context_parts = [] # before adding the metadata to LLM it was context_parts = [point.payload["text"] for point in retrieved_points] # below that text = point.payload["text"]
    sources=[]    

    for point in retrieved_points:
        text = point.payload["text"]
        filename = point.payload["filename"]
        page = point.payload["page"]
        heading = point.payload["heading"]
        context_part = f"""Source: {filename}
Page: {page}
Heading: {heading}
Text: {text}"""

        context_parts.append(context_part) 
        source = {
    "filename": filename,
    "page": page,
    "heading": heading
}
        sources.append(source)
     

    context = "\n\n".join(context_parts)
    answer = generate_answer(question, context)

    return {
    "answer": answer,
    "sources": sources
}