import json  
  
from channels.generic.websocket import AsyncWebsocketConsumer  
from chats.tasks import process_chat
from urllib.parse import parse_qs
  
class NotificationConsumer(AsyncWebsocketConsumer):  
    async def connect(self):  
        await self.accept()  
        await self.channel_layer.group_add("notifications", self.channel_name)  
  
    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard("notifications", self.channel_name)  
  
    async def send_notification(self, event):  
        message = event["message"]  
        await self.send(text_data=json.dumps({"message": message}))

class ChatConsumer(AsyncWebsocketConsumer):  
    async def connect(self):
        query_string = self.scope["query_string"].decode()  # bytes → string
        query_params = parse_qs(query_string)

        self.session_id = query_params.get("session_id", [None])[0]
        self.document_id = self.scope["url_route"]["kwargs"]["document_id"]
        self.group_name = f"chat_{self.session_id}"

        await self.accept()  
        await self.channel_layer.group_add(self.group_name, self.channel_name)  
  
    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard(self.group_name, self.channel_name)  
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        process_chat(message, self.document_id, self.session_id)

    async def send_message(self, event):  
        message = event["message"]  
        await self.send(text_data=json.dumps({"message": message}))