from core.ai.prompt_manager import PromptManager
from huey.contrib.djhuey import task
from core.methods import send_chat_message
from core.ai.chromadb import chroma, openai_ef
from chats.models import Chat
from rich import print
from core.ai.tokenizer import count_token
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

    context = ""

    for doc in res["documents"][0]:
        context += doc

    messages = [{
        "role": "system",
        "content": SYSTEM_PROMPT_RAG.format(documents = context)
    }]
    
    chats = Chat.objects.filter(session_id = session_id)
    
    for chat in chats:
        messages.append({
            "role": chat.role,
            "content": chat.content
        })

    messages = messages[-20:]

    pm = PromptManager()
    pm.set_messages(messages[-20:])
    assistant_message = pm.generate()

    messages_token = count_token(json.dumps(messages))
    assistant_token = count_token(assistant_message)

    print("messages token: ", messages_token)
    print("assistant token: ", assistant_token)

    Chat.objects.create(role="assistant", content=assistant_message, document_id=document_id, session_id=session_id)

    send_chat_message(assistant_message, session_id)
