from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import requests
import asyncio

users = []
active_games = {}

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
        if text_data == "cancel":
            if self.user_id in users:
                users.remove(self.user_id)
            await self.channel_layer.group_discard("quickplay", self.channel_name)
        elif text_data == "accept":
            await self.add_to_active_game()
        else:
            await self.add_group({
                "group_name": text_data,
                "user": self.user_id
            })

    async def add_group(self, event):
        group_name = event['group_name']
        if self.user_id != event['user']:
            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.channel_layer.group_discard("quickplay", self.channel_name)
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "send.group",
                    "message": "match found"
                }
            )

    async def send_group(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def matchmake(self):
        while len(users) >= 2:
            user1 = users.pop(0)
            user2 = users.pop(0)
            quickplay_group_name = f'quickplay_{user1}_{user2}'
            active_games[quickplay_group_name] = {'players': [user1, user2], 'accepted': []}
            await self.channel_layer.group_add(quickplay_group_name, self.channel_name)
            await self.channel_layer.group_send(
                "quickplay",
                {
                    "type": "add.group",
                    "group_name": quickplay_group_name,
                    "user": user1,
                }
            )
            await self.channel_layer.group_send(
                "quickplay",
                {
                    "type": "add.group",
                    "group_name": quickplay_group_name,
                    "user": user2,
                }
            )
            await self.channel_layer.group_send(
                quickplay_group_name,
                {
                    "type": "send.group",
                    "message": "match found"
                }
            )

    async def add_to_active_game(self):
        for group_name, game in active_games.items():
            if self.user_id in game['players'] and self.user_id not in game['accepted']:
                game['accepted'].append(self.user_id)
                if len(game['accepted']) == 2:
                    await self.channel_layer.group_send(
                        group_name,
                        {
                            "type": "send.group",
                            "message": "start game"
                        }
                    )
                break