from core.ai.prompt_manager import PromptManager
from huey.contrib.djhuey import task
from core.methods import send_chat_message
from core.ai.chromadb import chroma, openai_ef
from chats.models import Chat
import json

SYSTEM_PROMPT_RAG = """
You are a helpful assistant.
Your task is to answer user question based on the provided document.

PROVIDED DOCUMENTS.
{documents}

ANSWER GUIDELINES:
- Always answer in bahasa Indonesia.
- Do not include any additional information either than provided document.
"""

@task()
def process_chat(message, document_id, session_id):
    Chat.objects.create(role="user", content=message, document_id=document_id, session_id=session_id)

    collection = chroma.get_collection(name=document_id, embedding_function=openai_ef)
    res = collection.query(query_texts=[message], n_results=3)
    
    pm = PromptManager()
    pm.add_messages(role="system", content=SYSTEM_PROMPT_RAG.format(documents=json.dumps(res)))
    pm.add_messages(role="user", content=message)

    assistant_message = pm.generate()
    send_chat_message(assistant_message, session_id)
