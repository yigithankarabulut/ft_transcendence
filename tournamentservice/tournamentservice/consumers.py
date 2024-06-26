from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import asyncio

users = []
matches = []
usercount = 0
capacity = 0


class Tournament(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def connect(self):
        self.token = self.scope.get("query_string").decode("utf-8").split("=")[1]
        # TODO: verify token
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(self.room_name)
        self.room_group_name = f"game_{self.room_name}"
        global usercount
        global users
        if self.token != self.room_name:
            if users.count(self.token) == 0:
                await self.close()
            else:
                usercount += 1
        else:
            users.append(self.token)
            usercount += 1
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    
    async def disconnect(self, close_code):
        print('disconnect')

    async def receive(self, text_data):
        data = json.loads(text_data)
        global users
        global usercount
        if data['type'] == 'setlimit' and self.token == self.room_name:
            global capacity
            capacity = data['capacity']

        print(data)
        if data['type'] == 'adduser' and self.token == self.room_name:
            print('adduser')
            users.append(data['username'])
            print(users)
            #usercount += 1
            #if usercount == capacity:
            #    await self.matchmake()
        
        if data['type'] == 'getcount':
            self.send(text_data=json.dumps({'usercount': usercount}))
            #usercount -= 1

        if data['type'] == 'start' and self.token == self.room_name:
            if usercount != capacity:
                await self.send(text_data=json.dumps({'message': 'Not enough players'}))
                return
            await self.matchmake()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send.matches",
                    "matches": matches
                }
            )
            capacity = capacity / 2
            matches.clear()

        if data['type'] == 'addWinners':
            users.append(data['winner'])
            usercount += 1
            if usercount == capacity:
                await self.matchmake()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send.matches",
                        "matches": matches
                    }
                )
                capacity = capacity / 2
                if capacity == 1:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "send.winner",
                            "winner": matches[0][0]
                        }
                    )
                    await self.close()

    async def send_matches(self, event):
        matches = event['matches']
        await self.send(text_data=json.dumps({'matches': matches}))

    async def send_winner(self, event):
        winner = event['winner']
        await self.send(text_data=json.dumps({'winner': winner}))
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    async def matchmake(self):
        global usercount
        global users
        global matches
        if usercount >= capacity:
            while users:
                user1 = users.pop()
                user2 = users.pop()
                matches.append([user1, user2])
                usercount -= 2
                
