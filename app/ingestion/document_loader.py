from docling.document_converter import DocumentConverter
converter=DocumentConverter()
def load_document(file_path:str):
    result=converter.convert(file_path)
    return result


## this is a reusable script for any kind of document to parse the structure of the document followinng below code.
# python -c "from app.ingestion.document_loader import load_document;result=load_document('data/abreu_v._howard_university.pdf');print(type(result))"

# we will get the result <class 'docling.datamodel.document.ConversionResult'>

## very very important
# ConversionResult shows that the result contains in result.document