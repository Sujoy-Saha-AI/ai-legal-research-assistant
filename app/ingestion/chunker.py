from docling.chunking import HybridChunker
chunker = HybridChunker()
def chunk_document(document):
    chunks=list(chunker.chunk(dl_doc=document))
    return chunks

# This is also a reusble code/script
# here document is our own choiced parameter and
# dl_doc(not our invented) means docling documents and parameter name expected by Docling chunk()

# list been used to make the created chunk in a list group like [chunk 1, chunnk 2 ] etc otherwise it could make inferate chunk like sentence or one after one

## now using both the script document_loader.py and chunker.py we will check the chunk type
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document;result=load_document('data/abreu_v._howard_university.pdf');chunks=chunk_document(result.document);print(type(chunks))"

## Result => <class 'list'> means the chunks are listed 


## now ask how many chunks are created 

# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document;result=load_document('data/abreu_v._howard_university.pdf');chunks=chunk_document(result.document);print('Number of chunks:',len(chunks))"

## now we can see that 15 chunking has been created
# but we are not sure if the chunking quality is good or not 
## inspect the first chunk 
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.
# chunker import chunk_document; result=load_document('data/abreu_v._howard_university.pdf'); chunks=chunk_document(result.document); print(chunks[0])"


## Step to be taken for chunking AND Evaluation

## DOCUMENT INGESTION + CHUNKING TESTING WORKFLOW


# STEP 1 — Parse the PDF document
# Purpose: Verify that Docling can successfully parse the PDF.

# python -c "from app.ingestion.document_loader import load_document; my_document=load_document('data/abreu_v._howard_university.pdf'); print('Parsing completed')"


# STEP 2 — Check the type returned by load_document()
# Expected: docling.datamodel.document.ConversionResult

# python -c "from app.ingestion.document_loader import load_document; my_document=load_document('data/abreu_v._howard_university.pdf'); print(type(my_document))"


# STEP 3 — Extract the structured Docling document
# my_document = ConversionResult
# my_document.document = structured Docling document

# python -c "from app.ingestion.document_loader import load_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; print(type(structured_document))"


# STEP 4 — Inspect the structured document as Markdown
# [:2000] means display only the first 2,000 characters.
# It DOES NOT control chunk size.

# python -c "from app.ingestion.document_loader import load_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; print(structured_document.export_to_markdown()[:2000])"


# STEP 5 — Perform chunking
# chunk_document() uses the chunking implementation defined in chunker.py.

# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; chunks=chunk_document(structured_document); print('Chunking completed')"


# STEP 6 — Check the type of the chunk collection
# Expected: list

# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(type(my_chunks))"


# STEP 7 — Count the number of chunks

# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print('Number of chunks:', len(my_chunks))"


# STEP 8 — Inspect chunk text
# Python list indexing starts at 0.

# First chunk
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(my_chunks[0].text)"

# Second chunk
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(my_chunks[1].text)"

# Third chunk
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(my_chunks[2].text)"


# CHUNK QUALITY EVALUATION
#
# Inspect representative chunks from different parts of the document.
#
# Evaluate whether chunks:
# - contain coherent legal information
# - contain sufficient standalone context
# - preserve important legal reasoning
# - contain unnecessary layout/page-number noise
#
# If systematic problems are found:
# 1. Consider tuning the current HybridChunker configuration.
# 2. Consider filtering/post-processing low-value chunks.
# 3. If necessary, evaluate another chunking strategy/implementation.
#
# Do NOT change the chunking strategy simply because one isolated chunk is weak.


# STEP 9 — Inspect chunk metadata

# First chunk metadata
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(my_chunks[0].meta)"

# Second chunk metadata
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(my_chunks[1].meta)"

# Third chunk metadata
# python -c "from app.ingestion.document_loader import load_document; from app.ingestion.chunker import chunk_document; my_document=load_document('data/abreu_v._howard_university.pdf'); structured_document=my_document.document; my_chunks=chunk_document(structured_document); print(my_chunks[2].meta)"

# STEP 9 — Inspect Chunk Metadata
#
# Each chunk contains:
#   1. text  -> the actual content of the chunk
#   2. meta  -> information describing where the chunk came from
#
# schema_name = 'DocMeta'
#   -> Shows that Docling is using its DocMeta metadata structure/schema.
#
# doc_items
#   -> Shows the original document element(s) from which the chunk was created.
#
# label
#   -> Describes the type of document element.
#      Example: TEXT, TABLE, etc.
#      IMPORTANT: label=TEXT means the source ELEMENT is text;
#      it does not mean the entire document type is "text".
#
# prov (provenance)
#   -> Shows where the source element appeared in the original document.
#      It can include:
#         - page_no
#         - bounding box/location on the page
#         - character span
#
# headings
#   -> Shows the heading/section associated with the chunk.
#      Example: ['I.'], ['IV.']
#
# origin
#   -> Shows information about the original source document.
#      It can include:
#         - filename
#         - MIME type
#         - binary hash
#         - URI (if available)
#
# Therefore, useful metadata for our Legal RAG system may include:
#   - element_type / document element label
#   - page_number
#   - heading / section
#   - source_filename
#   - source URL / URI (when available)
#
# For legal retrieval, we will eventually enrich this with our own
# legal metadata such as:
#   - case_name
#   - court
#   - jurisdiction
#   - decision_date
#   - citation / docket number
#   - document_type
#   - source_url
#
# This metadata can later be stored with each chunk in Qdrant
# to support provenance, filtering, and citations.