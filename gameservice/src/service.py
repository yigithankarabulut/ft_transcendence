import requests
import json
from abc import ABC, abstractmethod
from django.utils.timezone import now
from .models import Room, Game, Player
from .utils import BaseResponse
from gameservice.settings import SERVICE_ROUTES


class IGameService(ABC):

    @abstractmethod
    def create_room(self, request, user_id) -> BaseResponse:
        pass

    @abstractmethod
    def join_room(self, room_id, user_id) -> BaseResponse:
        pass

    @abstractmethod
    def list_invite(self, user_id) -> BaseResponse:
        pass

    @abstractmethod
    def update_game(self, request) -> BaseResponse:
        pass


class GameService(IGameService):

    def create_room(self, request, user_id) -> BaseResponse:
        users = []
        users.append({'id': user_id})
        players = request['players']
        for player in players:
            try:
                response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get?username={player}")
            except Exception as e:
                return BaseResponse(True, str(e), None).res()
            if response.status_code != 200:
                return BaseResponse(True, response.json()['error'], None).res()
            res = response.json()
            user = res['data'][0]
            users.append(user)
        room = Room.objects.create(room_limit=request['room_limit'])
        count = 0
        for user in users:
            count += 1
            player = Player.objects.create(room=room, user_id=user['id'])
            if user['id'] == user_id:
                player.is_owner = True
            player.save()
        if count == 2:
            game = Game.objects.create(room=room, player1=users[0]['id'], player2=users[1]['id'])
            game.save()
        elif count == 4:
            game = Game.objects.create(room=room, player1=users[0]['id'], player2=users[1]['id'])
            game.save()
            game2 = Game.objects.create(room=room, player1=users[2]['id'], player2=users[3]['id'])
            game2.save()
        else:
            return BaseResponse(True, 'Invalid number of players', None).res()
        res = {
            "game_id": game.id,
        }
        return BaseResponse(False, 'Room created successfully', res).res()

    def join_room(self, room_id, user_id) -> BaseResponse:
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return BaseResponse(True, 'Room not found', None).res()
        if room.deleted_at:
            return BaseResponse(True, 'Room not found', None).res()
        players = Player.objects.filter(room=room)
        flag = False
        for player in players:
            if player.user_id == user_id:
                flag = True
                break
        if flag is False:
            return BaseResponse(True, 'You are not invited', None).res()
        game = Game.objects.filter(room=room, status=0).filter(player1=user_id).first()
        if not game:
            game = Game.objects.filter(room=room, status=0).filter(player2=user_id).first()
        if not game:
            return BaseResponse(True, 'Invalid room', None).res()
        res = {
            "game_id": game.id,
        }
        return BaseResponse(False, 'Room joined successfully', res).res()

    def list_invite(self, user_id) -> BaseResponse:
        games = Game.objects.filter(player2=user_id, status=0)
        resp = []
        for game in games:
            room = Room.objects.get(id=game.room_id)
            players = Player.objects.filter(room=room)
            player1 = players[0].user_id
            try:
                response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get/id?id={player1}")
            except Exception as e:
                return BaseResponse(True, str(e), None).res()
            if response.status_code != 200:
                return BaseResponse(True, response.json()['error'], None).res()
            res = response.json()
            user = res['data'][0]
            resp.append({
                "player1": user['username'],
                "room_id": room.id,
            })
        return BaseResponse(False, 'List of invites', resp).res()

    def update_game(self, request) -> BaseResponse:
        game_id = request['game_id']
        player1_score = request['player1_score']
        player2_score = request['player2_score']
        winner = request['winner']
        loser = request['loser']
        game = Game.objects.get(id=game_id)
        game.player1_score = player1_score
        game.player2_score = player2_score
        game.winner = winner
        game.loser = loser
        game.status = 2
        game.save()
        return BaseResponse(False, 'Game updated successfully', None).res()
