from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import asyncio


class Notification(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "notifications"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "message": "Notification"
            }
        )
