from docling.document_converter import DocumentConverter
converter=DocumentConverter()
def load_document(file_path:str):
    result=converter.convert(file_path)
    return result

    