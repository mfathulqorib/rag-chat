from documents.models import Document, DOC_STATUS_COMPLETE
from core.methods import send_notification
from core.ai.mistral import mistral
from core.ai.prompt_manager import PromptManager
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from core.ai.chromadb import chroma, openai_ef
from core.utils import generate_id


class DocumentProcessor:
    def __init__(self, document: Document):
        self.document = document
        self.extracted_text = ""

    def extract_text_via_ocr(self):
        uploaded_pdf = mistral.files.upload(
            file={
                'file_name': self.document.name,
                'content': open(f"media/{self.document.file.name}", "rb")
            },
            purpose="ocr"
        )

        signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)

        send_notification(notification_type="notification", content="Processing document...")

        ocr_response = mistral.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url.url
            }
        ).model_dump()

        for page in ocr_response.get("pages", []):
            self.extracted_text += page["markdown"]

    def generate_summary(self):
        send_notification(notification_type="notification", content="Summarizing document...")
        pm = PromptManager(model="gpt-4.1")
        pm.add_messages(role="system", content="Please summarize the provided text. Extract also the key points.")
        pm.add_messages(role="user", content=f"Content: {self.extracted_text}")

        ssummarize_content = pm.generate()

        self.document.raw_text = self.extracted_text
        self.document.summary = ssummarize_content
        self.document.status = DOC_STATUS_COMPLETE
        self.document.save()

    def create_vector_collection(self):
        send_notification(notification_type="notification", content="Creating collection...")

        splitter = SemanticChunker(OpenAIEmbeddings())
        chunks = splitter.create_documents([self.extracted_text])

        collection = chroma.create_collection(name=self.document.id, embedding_function=openai_ef)

        collection.add(
            documents= [chunk.model_dump()["page_content"] for chunk in chunks],
            ids= [generate_id() for _ in range(len(chunks))]
        )

        send_notification(
            notification_type="done", 
            content={
                'redirect_url': f"/query/{self.document.id}"
            }
        )