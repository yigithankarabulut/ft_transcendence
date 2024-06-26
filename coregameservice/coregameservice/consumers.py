from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import asyncio

rooms = {}
game_data = {str: dict}
width, height = 800, 400
canvas_width = 1200
canvas_height = 600
padd_left = {
    'speed': 35,
    'positionX': 60,
    'positionY': canvas_height / 2 - 100,
    'sizeX': 30,
    'sizeY': 200,
}
padd_right = {
    'speed': 35,
    'positionX': canvas_width - 100,
    'positionY': canvas_height / 2 - 100,
    'sizeX': 30,
    'sizeY': 200,
}


class Pong(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None

    async def connect(self):
        await self.accept()
        query_params = self.scope['query_string'].decode('utf-8')
        tmp_room_id = query_params.split('=')[1]
        if tmp_room_id in rooms and 'padd_left' in rooms[tmp_room_id] and 'padd_right' in rooms[tmp_room_id]:
            await self.close()
        else:
            self.room_id = tmp_room_id
            await self.channel_layer.group_add(
                self.room_id,
                self.channel_name
            )
            print('Connected to: ', self.room_id)
            if self.room_id not in rooms:
                rooms[self.room_id] = {
                    'padd_left': {
                        'player': self.channel_name,
                        'info': padd_left.copy()
                    }
                }
                print(rooms[self.room_id])
            elif len(rooms[self.room_id]) == 1:
                rooms[self.room_id]['padd_right'] = {
                    'player': self.channel_name,
                    'info': padd_right.copy()
                }
                print('Starting game for: ', self.room_id)
                await self.start_game(self.room_id)

    def init_game(self, room_id):
        rooms[room_id]['ball'] = {
            'speedX': 10,
            'speedY': 10,
            'positionX': canvas_width / 2,
            'positionY': canvas_height / 2,
            'size': 20,
            'dir': True
        }
        rooms[room_id]['padd_left']['info']['score'] = 0
        rooms[room_id]['padd_right']['info']['score'] = 0

    async def pong_message(self, event):
        if event['message'] == 'game_over':
            winner = "Left"
            if rooms[self.room_id]['padd_left']['info']['score'] == 5:
                winner = "Right"
            await self.send(text_data=json.dumps({
                'message': 'game_over',
                'winner': winner    
                }))
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'padd_left': rooms[self.room_id]['padd_left']['info'],
            'padd_right': rooms[self.room_id]['padd_right']['info'],
            'ball': rooms[self.room_id]['ball']
        }))

    async def start_game(self, room_id):
        self.init_game(room_id)
        rooms[room_id]['ball']['positionX'] += rooms[room_id]['ball']['speedX']
        rooms[room_id]['ball']['positionY'] += rooms[room_id]['ball']['speedY']
        await self.channel_layer.group_send(
            room_id,
            {
                'type': 'pong_message',
                'message': 'ball',
            }
        )
        print(rooms[room_id]['ball'])
        if room_id in rooms:
            asyncio.create_task(self.game_loop(room_id))

    def BallPaddleCollision(self, room_id):
        sizeY = rooms[room_id]['padd_left']['info']['sizeY']
        sizeX = rooms[room_id]['padd_left']['info']['sizeX']
        leftX_center = self.get_padd_center(room_id, 'leftX')
        leftY_center = self.get_padd_center(room_id, 'leftY')
        rightX_center = self.get_padd_center(room_id, 'rightX')
        rightY_center = self.get_padd_center(room_id, 'rightY')
        left_dx = abs(rooms[room_id]['ball']['positionX'] - leftX_center)
        left_dy = abs(rooms[room_id]['ball']['positionY'] - leftY_center)
        right_dx = abs(rooms[room_id]['ball']['positionX'] - rightX_center)
        right_dy = abs(rooms[room_id]['ball']['positionY'] - rightY_center)
        if (left_dx <= rooms[room_id]['ball']['size'] + sizeX / 2 and
                left_dy <= rooms[room_id]['ball']['size'] + sizeY / 2):
            if (rooms[room_id]['ball']['positionX'] >=
                leftX_center and rooms[room_id]['ball']['speedX'] > 0) or (
                    rooms[room_id]['ball']['positionX'] <=
                    leftX_center and rooms[room_id]['ball']['speedX'] < 0):
                return
            rooms[room_id]['ball']['speedX'] *= -1
        elif (right_dx <= rooms[room_id]['ball']['size'] + sizeX / 2 and
              right_dy <= rooms[room_id]['ball']['size'] + sizeY / 2):
            if (rooms[room_id]['ball']['positionX'] >=
                rightX_center and rooms[room_id]['ball']['speedX'] > 0) or (
                    rooms[room_id]['ball']['positionX'] <=
                    rightX_center and rooms[room_id]['ball']['speedX'] < 0):
                return
            rooms[room_id]['ball']['speedX'] *= -1

    def paddleCollision(self, room_id):
        size = rooms[room_id]['padd_right']['info']['sizeY']
        pos_right = rooms[room_id]['padd_right']['info']['positionY']
        pos_left = rooms[room_id]['padd_left']['info']['positionY']
        if pos_right + size >= canvas_height:
            rooms[room_id]['padd_right']['info']['positionY'] \
                = canvas_height - size
        elif pos_right <= 0:
            rooms[room_id]['padd_right']['info']['positionY'] = 0
        if pos_left + size >= canvas_height:
            rooms[room_id]['padd_left']['info']['positionY'] \
                = canvas_height - size
        elif pos_left <= 0:
            rooms[room_id]['padd_left']['info']['positionY'] = 0

    def reset_game(self, room_id):
        if rooms[room_id]['ball']['speedX'] > 0:
            rooms[room_id]['padd_right']['info']['score'] += 1
            rooms[room_id]['ball']['speedX'] = 10
        else:
            rooms[room_id]['padd_left']['info']['score'] += 1
            rooms[room_id]['ball']['speedX'] = -10
        if rooms[room_id]['padd_left']['info']['score'] == 5 or rooms[room_id]['padd_right']['info']['score'] == 5:
            return
        rooms[room_id]['ball']['positionX'] = canvas_width / 2
        rooms[room_id]['ball']['positionY'] = canvas_height / 2
        if rooms[room_id]['ball']['dir']:
            rooms[room_id]['ball']['speedY'] = -10
            rooms[room_id]['ball']['dir'] = False
        else:
            rooms[room_id]['ball']['speedY'] = 10
            rooms[room_id]['ball']['dir'] = True
        rooms[room_id]['padd_left']['info']['positionX'] = 60
        rooms[room_id]['padd_left']['info']['positionY'] = canvas_height / 2 - 100
        rooms[room_id]['padd_right']['info']['positionX'] = canvas_width - 100
        rooms[room_id]['padd_right']['info']['positionY'] = canvas_height / 2 - 100
        


    def BallCollision(self, room_id):
        if ((rooms[room_id]['ball']['positionX'] +
             rooms[room_id]['ball']['size'] >= canvas_width) or
                (rooms[room_id]['ball']['positionX'] -
                 rooms[room_id]['ball']['size'] <= 0)):
            self.reset_game(room_id)
        if (rooms[room_id]['ball']['positionY'] +
                rooms[room_id]['ball']['size'] >= canvas_height):
            rooms[room_id]['ball']['speedY'] *= -1
        if (rooms[room_id]['ball']['positionY'] -
                rooms[room_id]['ball']['size'] <= 0):
            rooms[room_id]['ball']['speedY'] *= -1

    def get_padd_center(self, room_id, side):
        size_x = rooms[room_id]['padd_left']['info']['sizeX']
        size_y = rooms[room_id]['padd_left']['info']['sizeY']
        if side == 'leftX':
            return rooms[room_id]['padd_left']['info']['positionX'] + size_x / 2
        elif side == 'leftY':
            return rooms[room_id]['padd_left']['info']['positionY'] + size_y / 2
        elif side == 'rightX':
            return rooms[room_id]['padd_right']['info']['positionX'] + size_x / 2
        elif side == 'rightY':
            return rooms[room_id]['padd_right']['info']['positionY'] + size_y / 2

    async def disconnect(self, close_code):
        if self.room_id in rooms:
            await self.channel_layer.group_discard(
                self.room_id,
                self.channel_name,
            )
            del rooms[self.room_id]

    async def receive(self, text_data=None, bytes_data=None):
        room_id = self.room_id
        if text_data == 'w':
            if self.channel_name in rooms[room_id]['padd_left']['player']:
                rooms[room_id]['padd_left']['info']['positionY'] -= rooms[room_id]['padd_left']['info']['speed']
            elif self.channel_name in rooms[room_id]['padd_right']['player']:
                rooms[room_id]['padd_right']['info']['positionY'] -= rooms[room_id]['padd_right']['info']['speed']
        elif text_data == 's':
            if self.channel_name in rooms[room_id]['padd_left']['player']:
                rooms[room_id]['padd_left']['info']['positionY'] += rooms[room_id]['padd_left']['info']['speed']
            elif self.channel_name in rooms[room_id]['padd_right']['player']:
                rooms[room_id]['padd_right']['info']['positionY'] += rooms[room_id]['padd_right']['info']['speed']
        self.paddleCollision(room_id)

    async def game_loop(self, room_id):
        while True:
            if room_id not in rooms:
                print('Game over for: ', room_id)
                break
            rooms[room_id]['ball']['positionX'] += rooms[room_id]['ball']['speedX']
            rooms[room_id]['ball']['positionY'] += rooms[room_id]['ball']['speedY']
            self.BallCollision(room_id)
            self.paddleCollision(room_id)
            self.BallPaddleCollision(room_id)
            await self.channel_layer.group_send(
                room_id,
                {
                    'type': 'pong_message',
                    'message': 'game_run',
                }
            )
            if rooms[room_id]['ball']['speedX'] > 0:
                rooms[room_id]['ball']['speedX'] += 0.01
            else:
                rooms[room_id]['ball']['speedX'] -= 0.01
            if rooms[room_id]['ball']['speedY'] > 0:
                rooms[room_id]['ball']['speedY'] += 0.01
            else:
                rooms[room_id]['ball']['speedY'] -= 0.01
            if rooms[room_id]['padd_left']['info']['score'] == 5 or rooms[room_id]['padd_right']['info']['score'] == 5:
                await self.channel_layer.group_send(
                    room_id,
                    {
                        'type': 'pong_message',
                        'message': 'game_over',
                    }
                )
                break
            await asyncio.sleep(0.025)
