import os
from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)


class PromptManager:
    def __init__(self, messages= [], model = "gpt-4.1-mini-2025-04-14"):
        self.messages = messages
        self.model = model

    def add_messages(self, role=str, content=str):
        self.messages.append({"role": role, "content": content})

    def set_messages(self, messages):
        self.messages = messages

    def generate(self):
        response = client.chat.completions.create(model=self.model, messages=self.messages)
        return response.choices[0].message.content
    
    def generate_structured(self, schema):
        response = client.beta.chat.completions.parse(model=self.model, messages=self.messages, response_format=schema)
        parsed = response.choices[0].message.parsed
        data = parsed.model_dump()

        return data