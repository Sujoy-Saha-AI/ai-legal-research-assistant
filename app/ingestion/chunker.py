from docling.chunking import HybridChunker
chunker = HybridChunker()
def chunk_document(document):
    chunks=list(chunker.chunk(dl_doc=document))
    return chunks

