# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        id = text_data_json.get("id")
        sender = text_data_json.get("sender")
        body = text_data_json.get("body")
        file = text_data_json.get("file")
        file_type = text_data_json.get("file_type")
        timestamp = text_data_json.get("timestamp")
        is_read = text_data_json.get("is_read")


        message = {
            "id": id,
            "sender": sender,
            "body": body,
            "file": file,
            "file_type": file_type,
            "timestamp": timestamp,
            "is_read": is_read,
        }
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))