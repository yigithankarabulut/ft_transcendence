from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Online(AsyncWebsocketConsumer):
    online_users = set()

    async def connect(self):
        self.user_id = self.scope['query_string'].decode('utf-8').split('=')[1]
        if self.user_id is None:
            await self.close()
        else:
            Online.online_users.add(self.user_id)
            await self.channel_layer.group_add('online_users', self.channel_name)
            await self.accept()
            await self.channel_layer.group_send('online_users', {
                'type': 'broadcast_status',
                'user_id': self.user_id,
                'status': 'online'
            })

    async def disconnect(self, close_code):
        Online.online_users.discard(self.user_id)
        await self.channel_layer.group_discard('online_users', self.channel_name)
        await self.channel_layer.group_send('online_users', {
            'type': 'broadcast_status',
            'user_id': self.user_id,
            'status': 'offline'
        })

    async def broadcast_status(self, event):
        print("Online users: ", Online.online_users)
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'status': event['status']
        }))

    async def receive(self, text_data):
        pass
