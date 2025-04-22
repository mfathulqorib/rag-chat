from huey.contrib.djhuey import task

from documents.models import Document
from .methods import DocumentProcessor
# from core.ai.mistral import mistral
# from core.ai.prompt_manager import PromptManager
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai.embeddings import OpenAIEmbeddings
# from rich import print

# from core.ai.chromadb import chroma, openai_ef
# from core.utils import generate_id
# from core.methods import send_notification

@task()
def run_document_processing(document: Document):    
    processor = DocumentProcessor(document)
    processor.extract_text_via_ocr()
    processor.generate_summary()
    processor.create_vector_collection()