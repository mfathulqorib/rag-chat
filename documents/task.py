from huey.contrib.djhuey import task

from documents.models import Document, DOC_STATUS_COMPLETE
from core.ai.mistral import mistral
from core.ai.prompt_manager import PromptManager
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from rich import print

from core.ai.chromadb import chroma, openai_ef
from core.utils import generate_id
from core.methods import send_notification

@task()
def process_document(document: Document):
    send_notification(notification_type="notification", content="Processing document...")
    uploaded_pdf = mistral.files.upload(
        file={
            'file_name': document.name,
            'content': open(f"media/{document.file.name}", "rb")
        },
        purpose="ocr"
    )

    signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_result = mistral.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url
        }
    ).model_dump()

    content = ""

    for page in ocr_result.get("pages", []):
        content += page["markdown"]

    send_notification(notification_type="notification", content="Summarizing document...")
    pm = PromptManager()
    pm.add_messages(role="system", content="Please summarize the provided text. Extract also the key points.")
    pm.add_messages(role="user", content=f"Content: {content}")

    ssummarize_content = pm.generate()

    document.raw_text = content
    document.summary = ssummarize_content
    document.status = DOC_STATUS_COMPLETE
    document.save()

    send_notification(notification_type="notification", content="Creating document...")

    splitter = SemanticChunker(OpenAIEmbeddings())
    documents = splitter.create_documents([content])

    collection = chroma.create_collection(name=document.id, embedding_function=openai_ef)

    collection.add(
        documents= [doc.model_dump()["page_content"] for doc in documents],
        ids= [generate_id() for _ in range(len(documents))]
    )

    send_notification(notification_type="done", content="Done")

