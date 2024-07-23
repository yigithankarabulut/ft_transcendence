from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import requests
import aiohttp
import logging

class PongGame:
    def __init__(self, canvas_width=960, canvas_height=480):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.padd_left = self.create_paddle(60)
        self.padd_right = self.create_paddle(canvas_width - 100)
        self.ball = self.create_ball()
        self.game_status = 0
        self.user_count = 0
        self.players = {'left': None, 'right': None}

    def create_paddle(self, x):
        return {
            'speed': 35,
            'positionX': x,
            'positionY': self.canvas_height / 2 - 100,
            'sizeX': 24,
            'sizeY': 160,
            'score': 0
        }

    def create_ball(self):
        return {
            'speedX': 10,
            'speedY': 10,
            'positionX': self.canvas_width / 2,
            'positionY': self.canvas_height / 2,
            'size': 20,
            'dir': True
        }

    def reset_ball(self):
        self.ball['positionX'] = self.canvas_width / 2
        self.ball['positionY'] = self.canvas_height / 2
        self.ball['speedX'] = 10 if self.ball['speedX'] > 0 else -10
        self.ball['speedY'] = -10 if self.ball['dir'] else 10
        self.ball['dir'] = not self.ball['dir']

    def update_ball(self):
        self.ball['positionX'] += self.ball['speedX']
        self.ball['positionY'] += self.ball['speedY']

    def check_collisions(self):
        self.check_wall_collision()
        self.check_paddle_collision()

    def check_wall_collision(self):
        if self.ball['positionX'] + self.ball['size'] >= self.canvas_width or self.ball['positionX'] - self.ball['size'] <= 0:
            self.update_score()
            self.reset_ball()
        if self.ball['positionY'] + self.ball['size'] >= self.canvas_height or self.ball['positionY'] - self.ball['size'] <= 0:
            self.ball['speedY'] *= -1

    def check_paddle_collision(self):
        for paddle in [self.padd_left, self.padd_right]:
            if (abs(self.ball['positionX'] - (paddle['positionX'] + paddle['sizeX']/2)) <= self.ball['size'] + paddle['sizeX']/2 and
                    abs(self.ball['positionY'] - (paddle['positionY'] + paddle['sizeY']/2)) <= self.ball['size'] + paddle['sizeY']/2):
                self.ball['speedX'] *= -1

    def update_score(self):
        if self.ball['speedX'] > 0:
            self.padd_right['score'] += 1
        else:
            self.padd_left['score'] += 1

    def move_paddle(self, player, direction):
        paddle = self.padd_left if player == 'left' else self.padd_right
        paddle['positionY'] += paddle['speed'] * direction
        paddle['positionY'] = max(0, min(self.canvas_height - paddle['sizeY'], paddle['positionY']))

    def is_game_over(self):
        return self.padd_left['score'] == 5 or self.padd_right['score'] == 5

    def get_winner(self):
        winner = 'left' if self.padd_left['score'] == 5 else 'right'
        winner_username = self.players[winner]
        return winner

    def add_player(self, username):
        if not self.players['left']:
            self.players['left'] = username
            return 'left'
        elif not self.players['right']:
            self.players['right'] = username
            return 'right'
        return None

    def is_full(self):
        return self.players['left'] and self.players['right']


class Pong(AsyncWebsocketConsumer):
    games = {}
    API_URLS = {
        'get_user': "http://apigateway:8000/user/get/id",
        'check_game': "http://apigateway:8000/game/check",
        'update_game': "http://gameservice:8010/game/update"
    }

    async def connect(self):
        self.room_id, self.access_token = self.parse_query_string()
        self.username = await self.get_username()

        if not self.username or not await self.check_game():
            await self.close()
            return

        await self.accept()
        await self.join_game()

    async def disconnect(self, close_code):
        if self.room_id in self.games:
            game = self.games[self.room_id]
            game.game_status = 0
            game.user_count -= 1
            if game.user_count <= 0:
                await self.update_game_status(3, 0, 0)
                del self.games[self.room_id]
            else:
                await self.group_send('disconnect_message', {'disconnected_user': self.username})

    async def receive(self, text_data):
        game = self.games.get(self.room_id)
        if not game or game.game_status != 1:
            return

        direction = -1 if text_data == 'w' else 1 if text_data == 's' else 0
        if direction != 0:
            game.move_paddle(self.player_side, direction)

    async def game_loop(self):
        game = self.games[self.room_id]
        while game.game_status:
            game.update_ball()
            game.check_collisions()
            await self.group_send('pong_message', {'message': 'game_run'})

            if game.is_game_over():
                await self.handle_game_over()
                break

            await asyncio.sleep(0.025)

    async def handle_game_over(self):
        game = self.games[self.room_id]
        winner = game.get_winner()
        new_game_id = await self.update_game_status(2, game.padd_right['score'], game.padd_left['score'])
        logging.error("winner: %s new_game_id: %s", winner, new_game_id)
        await self.group_send('pong_message', {
            'message': 'game_over',
            'winner': winner,
            'newGame': new_game_id
        })

    async def join_game(self):
        if self.room_id not in self.games:
            self.games[self.room_id] = PongGame()

        game = self.games[self.room_id]
        player_side = game.add_player(self.username)

        if player_side is None:
            await self.close()
            return

        self.player_side = player_side
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        game.user_count += 1

        if game.is_full():
            await self.start_game()

    async def start_game(self):
        game = self.games[self.room_id]
        game.game_status = 1
        game.user_count = 2
        asyncio.create_task(self.game_loop())

    async def pong_message(self, event):
        if event['message'] == 'game_over':
            if self.username == event['winner']:
                await self.send(text_data=json.dumps({
                    'message': 'game_over',
                    'winner': event['winner'],
                    'newGame': event['newGame']
                }))
            else:
                await self.send(text_data=json.dumps({
                    'message': 'game_over',
                    'winner': event['winner'],
                    'newGame': "",
                }))
            await self.close()
            return

        game = self.games[self.room_id]
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'padd_left': game.padd_left,
            'padd_right': game.padd_right,
            'ball': game.ball,
            'padd_left_username': game.players['left'],
            'padd_right_username': game.players['right'],
            'padd_left_score': game.padd_left['score'],
            'padd_right_score': game.padd_right['score']
        }))

    async def disconnect_message(self, event):
        game = self.games[self.room_id]
        disconnected_user = event['disconnected_user']
        winner = game.padd_left['username'] if game.padd_left['username'] != disconnected_user else game.padd_right['username']
        await self.send(text_data=json.dumps({
            'message': 'game_over',
            'winner': winner
        }))
        await self.close()

    async def group_send(self, message_type, message):
        await self.channel_layer.group_send(self.room_id, {
            'type': message_type,
            **message
        })

    def parse_query_string(self):
        query_params = self.scope['query_string'].decode('utf-8').split('?')
        room_id = query_params[0].split('=')[1]
        access_token = query_params[1].split('=')[1]
        logging.error("room_id: %s access_token: %s", room_id, access_token)
        return room_id, access_token

    async def get_username(self):
        try:
            response = await self.make_request('get', self.API_URLS['get_user'])
            logging.error("response: %s", response)

            return response['data']['data'][0]['username'] if response['status_code'] == 200 else None
        except Exception as e:
            logging.error(f"Error getting username: {str(e)}")
            return None

    async def check_game(self):
        try:
            response = await self.make_request('get', f"{self.API_URLS['check_game']}?game_id={self.room_id}")
            return response['status_code'] == 200
        except Exception as e:
            logging.error(f"Error checking game: {str(e)}")
            return False

    async def update_game_status(self, status, player1_score, player2_score):
        try:
            body = {
                'game_id': int(self.room_id),
                'status': status,
                'player1_score': player1_score,
                'player2_score': player2_score,
            }
            response = await self.make_request('put', self.API_URLS['update_game'], json.dumps(body))
            if response['status_code'] == 200 and 'data' in response and 'game_id' in response['data']:
                return response['data']['game_id']
            return None
        except Exception as e:
            logging.error(f"Error updating game status: {str(e)}")
            return None

    async def make_request(self, method, url, data=None):
        logging.error("access_token: %s method: %s url: %s data: %s", self.access_token, method, url, data)
        headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=data) as response:
                return {'status_code': response.status, 'data': await response.json()}



# --------------------------------- consumer.py -----------------------

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
        logging.error("User %s is line 64 ", tmp_player_name)

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
                logging.error("check game responses: %s", res)
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
            elif len(rooms[self.room_id]) > 1: # *
                logging.error("User %s is line 108 ", tmp_player_name)
                if tmp_player_name == rooms[self.room_id]['padd_left']['username']:
                    await self.close()
                    return
                rooms[self.room_id]['padd_right'] = {
                    'player': self.channel_name,
                    'info': padd_right.copy(),
                    'username': tmp_player_name
                }
                logging.error("User %s is line 117  ", tmp_player_name)
                logging.error(rooms[self.room_id])
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
        if room_id not in rooms:
            return
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
