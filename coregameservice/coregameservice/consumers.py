# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Bağlantıyı kapatın
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         # Gelen veriyi işleyin ve istemcilere geri gönderin
#         await self.send(text_data=json.dumps({
#             'message': 'Oyun durumu güncellendi',
#             # İşlenmiş veri buraya eklenebilir
#         }))


import json
import asyncio
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Kullanıcı kimliği ve oda adını al
        self.user_id = self.scope['query_string'].decode("utf-8").split("=")[1]
        self.room_id = self.scope['query_string'].decode("utf-8").split("=")[3]

        # Kullanıcıyı odasına kat
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # Python'dan gelen JSON verisini al
        text_data_json = json.loads(text_data)

        # # Tüm istemcileri al ama channel layer in memory olduğu için sadece bir istemci olacak
        total_clients = self.channel_layer.group_channels("game_group")

        # # Eğer sadece bir istemci varsa, veriyi geri gönder ve güncelle
        if len(total_clients) == 1:
            self.send(text_data=json.dumps({
                'player1': text_data_json['player1'],
                'player2': text_data_json['player2'],
                'ball': text_data_json['ball'],
            }))
            return 

        asyncio.sleep(1)

        # İstemcilere güncel oyun durumunu gönder
        self.channel_layer.group_send(
            "game_group",
            {
                "type": "game_update",
                "message": text_data,
            }
        )

    # İstemciye güncel oyun durumunu gönder
    def game_update(self, event):
        self.send(text_data=event["message"])
