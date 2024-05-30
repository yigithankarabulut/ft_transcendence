from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import requests
import asyncio

users = []

class QuickPlay(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def connect(self):
        token = self.scope['path_remaining'].split('/')[1]
        request = requests.post(f'http://localhost:8000/auth/token/validate', headers={'Authorization': 'Bearer ' + token})
        if request.status_code != 200:
            await self.close()
        print("--------------------")
        print(request.json())
        print("--------------------")
        self.user_id = request.json()['user_id']
        await self.channel_layer.group_add(
            "quickplay",
            self.channel_name
        )
        users.append(self.user_id)
        await self.accept()
        await self.matchmake()
    
    async def disconnect(self, close_code):
        print('disconnect')

    async def receive(self, text_data):
        print('recive')

    async def add_group(self, event):
        data = event['group_name']
        if self.user_id != event['user']:
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
            print("match found")
            print(user1)
            print("vs")
            print(user2)
            quickplay_group_name = f'quickplay_{user1}_{user2}'
            await self.channel_layer.group_add(quickplay_group_name, self.channel_name)
            await self.channel_layer.group_send(
                "quickplay",
                {
                    "type": "add.group",
                    "group_name": quickplay_group_name,
                    "user": self.user_id,
                }
            )
            