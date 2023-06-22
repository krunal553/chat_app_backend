# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = "user_%s" % self.room_name

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
        message = {
            "id": "user consumer",
        }
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "user_message", 
                "message": text_data
            }
        )

    # Receive message from room group
    async def user_message(self, event):
        message = event["message"]
        await self.send(text_data=event["message"])