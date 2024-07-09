import requests
import json
from abc import ABC, abstractmethod
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage
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
    def update_game(self, request) -> BaseResponse:
        pass

    @abstractmethod
    def list_invite(self, user_id, page, limit) -> BaseResponse:
        pass

    @abstractmethod
    def list_history(self, username, page, limit) -> BaseResponse:
        pass

    @abstractmethod
    def check_game(self, user_id, game_id) -> BaseResponse:
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

    def update_game(self, request) -> BaseResponse:
        game = Game.objects.get(id=request['game_id'])
        game.player1_score = request['player1_score']
        game.player2_score = request['player2_score']
        game.status = request['status']
        game.save()
        if game.status != 2:
            return BaseResponse(False, 'Game updated successfully', None).res()
        room = Room.objects.get(id=game.room_id)
        if room.room_limit == 2:
            return BaseResponse(False, 'Game updated successfully', None).res()
        games = Game.objects.filter(room=room, status=2)
        if games.count() == 3:
            return BaseResponse(False, 'Game updated successfully', None).res()
        active_game = Game.objects.filter(room=room, status=0).filter(player2="").first()
        if active_game:
            if game.player1_score > game.player2_score:
                active_game.player2 = game.player1
            else:
                active_game.player2 = game.player2
            active_game.save()
            res = {
                "game_id": active_game.id,
            }
            return BaseResponse(False, 'Game updated successfully', res).res()
        if game.player1_score > game.player2_score:
            new_game = Game.objects.create(room=room, status=0, player1=game.player1)
            new_game.save()
        else:
            new_game = Game.objects.create(room=room, status=0, player1=game.player2)
            new_game.save()
        res = {
            "game_id": new_game.id,
        }
        return BaseResponse(False, 'Game updated successfully', res).res()

    def list_invite(self, user_id, page, limit) -> BaseResponse:
        games = Game.objects.filter(player1=user_id, status=0) | Game.objects.filter(player2=user_id, status=0)
        paginator = Paginator(games, limit)
        try:
            games = paginator.page(page)
        except EmptyPage:
            return BaseResponse(False, 'There is no data in this page', None).res()
        if not games:
            return BaseResponse(False, 'Invite list is empty', None).res()
        resp = []
        for game in games:
            room = Room.objects.get(id=game.room_id)
            players = Player.objects.filter(room=room)
            player1 = players[0].user_id
            try:
                response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get/id?id={player1}", headers={'Authorization': f'Bearer {user_id}'})
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
        paginate_data = {
            "current_page": page,
            "page_size": limit,
            "total_pages": paginator.num_pages,
            "total_records": paginator.count
        }
        return BaseResponse(False, 'List of invites', resp, paginate_data).res()

    def list_history(self, username, page, limit) -> BaseResponse:
        try:
            response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get?username={username}")
        except Exception as e:
            return BaseResponse(True, str(e), None).res()
        if response.status_code != 200:
            return BaseResponse(True, response.json()['error'], None).res()
        res = response.json()
        user = res['data'][0]

        games = Game.objects.filter(status=2).filter(player1=user['id'])
        games2 = Game.objects.filter(status=2).filter(player2=user['id'])
        resp = []
        for game in games:
            room = Room.objects.get(id=game.room_id)
            players = Player.objects.filter(room=room)
            player2 = players[1].user_id
            try:
                response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get/id?id={player2}")
            except Exception as e:
                return BaseResponse(True, str(e), None).res()
            if response.status_code != 200:
                return BaseResponse(True, response.json()['error'], None).res()
            res = response.json()
            user = res['data'][0]
            resp.append({
                "player1": username,
                "player2": user['username'],
                "player1_score": game.player1_score,
                "player2_score": game.player2_score,
            })
        for game in games2:
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
                "player2": username,
                "player1_score": game.player1_score,
                "player2_score": game.player2_score,
            })
        return BaseResponse(False, 'List of games', resp).res()
    
    def check_game(self, user_id, game_id) -> BaseResponse:
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return BaseResponse(True, 'Game not found', None).res()
        if game.deleted_at:
            return BaseResponse(True, 'Game not found', None).res()
        if game.player1 == user_id or game.player2 == user_id:
            return BaseResponse(False, 'Game found', None).res()
        return BaseResponse(True, 'You are not part of this game', None).res()