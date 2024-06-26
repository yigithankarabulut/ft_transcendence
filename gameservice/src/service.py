import requests
import json
from abc import ABC, abstractmethod
from django.utils.timezone import now
from .models import Room, Game, Player
from .utils import BaseResponse


class IGameService(ABC):

    @abstractmethod
    def create_room(self, request, user_id) -> BaseResponse:
        pass
    #
    # @abstractmethod
    # def register(self, user: UserManagement) -> BaseResponse:
    #     pass


class GameService(IGameService):

    def create_room(self, request, user_id) -> BaseResponse:
        room = Room.objects.create(room_limit=request['room_limit'])
        players = request['players']
        for player in players:
            Player.objects.create(room=room, user_id=player)
        game = Game.objects.create(room=room, player1=players[0], player2=players[1])
        return BaseResponse(False, "Room created successfully", None)


