from chromadb import HttpClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
chroma = HttpClient(host="localhost", port=8010)

openai_ef = OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)