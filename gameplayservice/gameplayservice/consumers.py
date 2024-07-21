from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.utils import json
import json
import asyncio
import requests
import logging

rooms = {}
game_data = {str: dict}
width, height = 640, 320
canvas_width = 960
canvas_height = 480
padd_left = {
    'speed': 35,
    'positionX': 60,
    'positionY': canvas_height / 2 - 100,
    'sizeX': 24,
    'sizeY': 160,
}
padd_right = {
    'speed': 35,
    'positionX': canvas_width - 100,
    'positionY': canvas_height / 2 - 100,
    'sizeX': 24,
    'sizeY': 160,
}

GetUserByID_URL = "http://apigateway:8000/user/get/id"
CheckGame_URL = "http://apigateway:8000/game/check"
GameUpdate_URL = "http://gameservice:8010/game/update"


class Pong(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.access_token = None
        self.username = None

    async def connect(self):
        query_params = self.scope['query_string'].decode('utf-8')
        params = query_params.split('?')

        tmp_room_id = params[0].split('=')[1]
        access_token = params[1].split('=')[1]
        tmp_player_name = None

        try:
            response = requests.get(
                GetUserByID_URL,
                headers = {'Authorization': f'Bearer {access_token}'},
            )
            if response.status_code == 200:
                res = response.json()
                user = res['data'][0]
                tmp_player_name = user['username']
                self.access_token = access_token
        except Exception as e:
            logging.error("Error: %s", str(e))

        if tmp_player_name == None:
            await self.close()
            return

        try:
            response = requests.get(
                f'{CheckGame_URL}?game_id={tmp_room_id}',
                headers = {'Authorization': f'Bearer {access_token}'},
            )
            if response.status_code != 200:
                await self.close()
                return
            else:
                res = response.json()
                logging.error("check game response: %s", res)
        except Exception as e:
            logging.error("Error: %s", str(e))

        if tmp_room_id == "null":
            await self.close()
            return
        await self.accept()
        logging.error("Room: %s", tmp_room_id)
        logging.error("Player: %s", tmp_player_name)
        if tmp_room_id in rooms and 'padd_left' in rooms[tmp_room_id] and 'padd_right' in rooms[tmp_room_id]:
            await self.close()
            return
        else:
            self.room_id = tmp_room_id
            await self.channel_layer.group_add(
                self.room_id,
                self.channel_name
            )
            logging.error("Room id: %s", self.room_id)
            if self.room_id not in rooms:
                rooms[self.room_id] = {
                    'padd_left': {
                        'player': self.channel_name,
                        'info': padd_left.copy(),
                        'username': tmp_player_name
                    }
                }
                rooms[self.room_id]['game_status'] = 0
                self.username = tmp_player_name
                logging.error(rooms[self.room_id])
            elif len(rooms[self.room_id]) > 1:
                if tmp_player_name == rooms[self.room_id]['padd_left']['username']:
                    await self.close()
                    return
                rooms[self.room_id]['padd_right'] = {
                    'player': self.channel_name,
                    'info': padd_right.copy(),
                    'username': tmp_player_name
                }
                self.username = tmp_player_name
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
        rooms[room_id]['game_status'] = 1
        rooms[room_id]['user_count'] = 2
        tmp = rooms[room_id]['padd_left']
        rooms[room_id]['padd_left'] = rooms[room_id]['padd_right']
        rooms[room_id]['padd_right'] = tmp

    async def pong_message(self, event):
        if event['message'] == 'game_over':
            winner = rooms[self.room_id]['padd_left']['username']
            if rooms[self.room_id]['padd_right']['info']['score'] == 5:
                winner = rooms[self.room_id]['padd_right']['username']
            if self.username == winner:
                await self.send(text_data=json.dumps({
                    'message': 'game_over',
                    'winner': winner,
                    'newGame': event['newGame'],
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'message': 'game_over',
                    'winner': winner,
                    'newGame': "",
                    }))

            await self.channel_layer.group_discard(
                self.room_id,
                self.channel_name,
            )
            rooms[self.room_id]['user_count'] -= 1
            await self.close()
            return

        await self.send(text_data=json.dumps({
            'message': event['message'],
            'padd_left': rooms[self.room_id]['padd_left']['info'],
            'padd_right': rooms[self.room_id]['padd_right']['info'],
            'ball': rooms[self.room_id]['ball'],
            'padd_left_username': rooms[self.room_id]['padd_left']['username'],
            'padd_right_username': rooms[self.room_id]['padd_right']['username'],
            'padd_left_score': rooms[self.room_id]['padd_left']['info']['score'],
            'padd_right_score': rooms[self.room_id]['padd_right']['info']['score']
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
        logging.error(rooms[room_id]['ball'])
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
            rooms[self.room_id]['disconnected_username'] = self.username
            rooms[self.room_id]['game_status'] = 0
            if self.room_id in rooms and 'user_count' in rooms[self.room_id]:
                rooms[self.room_id]['user_count'] -= 1
            else:
                try:
                    body = {
                        'game_id': int(self.room_id),
                        'status': 3,
                        'player1_score': 0,
                        'player2_score': 0,
                    }
                    response = requests.put(
                        GameUpdate_URL,
                        data=json.dumps(body),
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {self.access_token}',
                        },
                    )
                    if response.status_code == 200:
                        res = response.json()
                        logging.error(res)
                except Exception as e:
                    logging.error(str(e))
                del rooms[self.room_id]
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        room_id = self.room_id
        if rooms[room_id]['game_status'] != 1:
            return
        if text_data == 'w':
            if self.username == rooms[room_id]['padd_left']['username']:
                rooms[room_id]['padd_left']['info']['positionY'] -= rooms[room_id]['padd_left']['info']['speed']
            elif self.username == rooms[room_id]['padd_right']['username']:
                rooms[room_id]['padd_right']['info']['positionY'] -= rooms[room_id]['padd_right']['info']['speed']
        elif text_data == 's':
            if self.username == rooms[room_id]['padd_left']['username']:
                rooms[room_id]['padd_left']['info']['positionY'] += rooms[room_id]['padd_left']['info']['speed']
            elif self.username == rooms[room_id]['padd_right']['username']:
                rooms[room_id]['padd_right']['info']['positionY'] += rooms[room_id]['padd_right']['info']['speed']
        self.paddleCollision(room_id)

    async def game_loop(self, room_id):
        while rooms[room_id]['game_status']:
            if room_id not in rooms:
                logging.error("Game over for: ", room_id)
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
                newGameId = None
                try:
                    body = {
                        'game_id': int(self.room_id),
                        'status': 2,
                        'player1_score': int(rooms[room_id]['padd_right']['info']['score']),
                        'player2_score': int(rooms[room_id]['padd_left']['info']['score']),
                    }
                    response = requests.put(
                        GameUpdate_URL,
                        data=json.dumps(body),
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {self.access_token}',
                        },
                    )
                    if response.status_code == 200:
                        res = response.json()
                        if res['data'] is not None and res['data']['game_id'] is not None:
                            newGameId = res['data']['game_id']
                except Exception as e:
                    logging.error(str(e))
                await self.channel_layer.group_send(
                    room_id,
                    {
                        'type': 'pong_message',
                        'message': 'game_over',
                        'newGame': newGameId,
                    }
                )
                break
            await asyncio.sleep(0.025)

        if rooms[room_id]['game_status'] == 0:
            try:
                disuser = rooms[room_id]["disconnected_username"]
                if disuser != rooms[room_id]["padd_left"]["username"]:
                    rooms[room_id]['padd_left']['info']['score'] = 5
                else:
                    rooms[room_id]['padd_right']['info']['score'] = 5
                body = {
                    'game_id': int(self.room_id),
                    'status': 2,
                    'player1_score': int(rooms[room_id]['padd_right']['info']['score']),
                    'player2_score': int(rooms[room_id]['padd_left']['info']['score']),
                }
                response = requests.put(
                    GameUpdate_URL,
                    data=json.dumps(body),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.access_token}',
                    },
                )
                if response.status_code == 200:
                    res = response.json()
                    logging.error(res)
            except Exception as e:
                logging.error(str(e))
            await self.channel_layer.group_send(
                room_id,
                {
                    'type': 'disconnect_message',
                    'message': room_id,
                }
            )
        else:
            pass
        while (1):
            if rooms[room_id]['user_count'] <= 0:
                del rooms[room_id]
                break
            await asyncio.sleep(0.025)
    async def disconnect_message(self, event):
        room_id = event['message']
        disconnected_user = rooms[room_id]['disconnected_username']
        winner = ""
        if rooms[room_id]['padd_left']['username'] != disconnected_user:
            winner = rooms[room_id]['padd_left']['username']
        else:
            winner = rooms[room_id]['padd_right']['username']
        await self.send(text_data=json.dumps({
            'message': 'game_over',
            'winner': winner
            }))
        await self.channel_layer.group_discard(
            room_id,
            self.channel_name,
        )
        rooms[room_id]['user_count'] -= 1
        await self.close()

