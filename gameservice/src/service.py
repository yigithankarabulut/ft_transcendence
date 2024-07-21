import requests
import json
from abc import ABC, abstractmethod
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage
from .models import Room, Game, Player
from .utils import BaseResponse
from gameservice.settings import SERVICE_ROUTES
import logging


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
            if user['id'] == user_id:
                return BaseResponse(True, 'You cannot invite yourself', None).res()
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
        
        other_players = []
        players = Player.objects.filter(room=room)
        for player in players:
            if player.user_id != game.player1 and player.user_id != game.player2:
                other_players.append(player.user_id)

        other_game1 = Game.objects.filter(room=room).filter(player1=other_players[0]).filter(player2=other_players[1]).first()
        other_game2 = Game.objects.filter(room=room).filter(player1=other_players[1]).filter(player2=other_players[0]).first()
        other_game = None
        if other_game1:
            other_game = other_game1
        elif other_game2:
            other_game = other_game2
        
        if other_game.status != 0 or other_game.status != 3:
            other_game = None

        if game.player1_score > game.player2_score:
            new_game = Game.objects.create(room=room, status=0, player1=game.player1)
            new_game.save()
        else:
            new_game = Game.objects.create(room=room, status=0, player1=game.player2)
            new_game.save()
        if other_game is not None:
            other_game.status = 3
            other_game.save()
            new_game.player1_score = 5
            new_game.player2_score = 0
            new_game.status = 3
            new_game.player2 = "Cancelled"
            new_game.save()
            return BaseResponse(False, 'Other game not played yet', None).res()
        res = {
                "game_id": new_game.id,
        }
        return BaseResponse(False, 'Game updated successfully', res).res()

    def list_invite(self, user_id, page, limit) -> BaseResponse:
        games = Game.objects.filter(player1=user_id, status=0)
        games2 = Game.objects.filter(player2=user_id, status=0)
        games = games | games2
        games = games.order_by('-created_at')
        paginator = Paginator(games, limit)
        try:
            games = paginator.page(page)
        except Exception as e:
            if e is EmptyPage:
                return BaseResponse(False, 'No invites found', None).res()
            return BaseResponse(True, str(e), None).res()
        if not games:
            return BaseResponse(False, 'No invites found', None).res()
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
        owner = user['id']

        games1 = Game.objects.filter(status=2).filter(player1=user['id'])
        games2 = Game.objects.filter(status=2).filter(player2=user['id'])
        games = games1 | games2
        games = games.order_by('-updated_at')
        paginator = Paginator(games, limit)
        try:
            games = paginator.page(page)
        except Exception as e:
            if e is EmptyPage:
                return BaseResponse(False, 'No games found', None).res()
            return BaseResponse(True, str(e), None).res()
        if not games:
            return BaseResponse(False, 'No games found', None).res()
        game1 = []
        game2 = []
        for game in games:
            if game.player1 == user['id']:
                game1.append(game)
            else:
                game2.append(game)
        resp = []
        win_count = 0
        lose_count = 0
        for game in game1:
            player2 = game.player2
            try:
                response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get/id?id={player2}")
            except Exception as e:
                return BaseResponse(True, str(e), None).res()
            if response.status_code != 200:
                return BaseResponse(True, response.json()['error'], None).res()
            res = response.json()
            user = res['data'][0]
            if game.player1_score > game.player2_score:
                win_count += 1
            else:
                lose_count += 1
            resp.append({
                "player1": username,
                "player2": user['username'],
                "player1_score": game.player1_score,
                "player2_score": game.player2_score,
                "date": game.updated_at,
            })
        for game in game2:
            player1 = game.player1
            try:
                response = requests.get(f"{SERVICE_ROUTES['/user']}/user/get/id?id={player1}")
            except Exception as e:
                return BaseResponse(True, str(e), None).res()
            if response.status_code != 200:
                return BaseResponse(True, response.json()['error'], None).res()
            res = response.json()
            user = res['data'][0]
            if game.player2_score > game.player1_score:
                win_count += 1
            else:
                lose_count += 1
            resp.append({
                "player1": user['username'],
                "player2": username,
                "player1_score": game.player1_score,
                "player2_score": game.player2_score,
                "date": game.updated_at,
            })
        stats = self.games_stats(owner)

        resp = sorted(resp, key=lambda x: x['date'], reverse=True)
        
        paginate_data = {
            "current_page": page,
            "page_size": limit,
            "total_pages": paginator.num_pages,
            "total_records": paginator.count
        }
        return BaseResponse(False, 'List of games', resp, paginate_data, stats).res()

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

    def games_stats(self, user_id):
        game = Game.objects.filter(status=2).filter(player1=user_id)
        game2 = Game.objects.filter(status=2).filter(player2=user_id)
        game = game | game2
        win_count = 0
        lose_count = 0
        for g in game:
            if g.player1 == user_id:
                if g.player1_score > g.player2_score:
                    win_count += 1
                else:
                    lose_count += 1
            else:
                if g.player2_score > g.player1_score:
                    win_count += 1
                else:
                    lose_count += 1
        stats = {
            "total_games": game.count(),
            "win_count": win_count,
            "lose_count": lose_count,
        }
        return stats
