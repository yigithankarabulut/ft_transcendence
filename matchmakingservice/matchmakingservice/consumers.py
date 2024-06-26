from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import asyncio

users = []

class QuickPlay(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def connect(self):
        
        self.username = self.scope['path_remaining'].split('/')[1]
        await self.channel_layer.group_add(
            "quickplay",
            self.channel_name
        )
        users.append(self.username)
        await self.accept()
        await self.matchmake()
    
    async def disconnect(self, close_code):
        print('disconnect')

    async def receive(self, text_data):
        print('recive')

    async def add_group(self, event):
        data = event['group_name']
        if self.username != event['user']:
            await self.channel_layer.group_add(data, self.channel_name)
            await self.channel_layer.group_discard("quickplay", self.channel_name)
            await self.channel_layer.group_send(
                data,
                {
                    "type": "send.group",
                    "message": "match found"
                }
            )

    async def send_group(self, event):
        data = event['message']
        await self.send(text_data=json.dumps(data))

    async def matchmake(self):
        if len(users) >= 2:
            user1 = users.pop()
            user2 = users.pop()
            quickplay_group_name = f'quickplay_{user1}_{user2}'
            await self.channel_layer.group_add(quickplay_group_name, self.channel_name)
            await self.channel_layer.group_send(
                "quickplay",
                {
                    "type": "add.group",
                    "group_name": quickplay_group_name,
                    "user": self.username,
                }
            )
            