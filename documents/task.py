from huey.contrib.djhuey import task

from documents.models import Document
from .methods import DocumentProcessor

@task()
def run_document_processing(document: Document):    
    processor = DocumentProcessor(document)
    processor.extract_text_via_ocr()
    processor.generate_summary()
    processor.create_vector_collection()