from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json

# Online kullanıcıları tutmak için global bir liste
online_users = {}

class Online(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        # URL'den kullanıcı ID'sini al
        query_params = self.scope['query_string'].decode('utf-8')
        params = query_params.split('?')

        user_id = None
        for param in params:
            if param.startswith('user_id='):
                user_id = param.split('=')[1]
                print(user_id)
                break

        if user_id:
            online_users[user_id] = self.channel_name
            await self.channel_layer.group_add("online_users", self.channel_name)
            await self.notify_status_change(user_id, True)

    async def disconnect(self, close_code):
        # Kullanıcı disconnect olduğunda online listesinden çıkar
        print(online_users)
        for user_id, channel_name in online_users.items():
            if channel_name == self.channel_name:
                del online_users[user_id]
                await self.channel_layer.group_discard("online_users", self.channel_name)
                await self.notify_status_change(user_id, False)
                break

    async def receive(self, text_data=None, bytes_data=None):
        # Mesaj alma işlemi (isteğe bağlı)
        pass

    async def notify_status_change(self, user_id, status):
        # Kullanıcı durumu değişikliğini frontend'e bildir
        await self.channel_layer.group_send(
            "online_users",
            {
                'type': 'status_change',
                'user_id': user_id,
                'status': 'online' if status else 'offline'
            }
        )

    async def status_change(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'status': event['status']
        }))
