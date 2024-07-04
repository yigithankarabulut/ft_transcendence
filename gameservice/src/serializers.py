from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Game, Room, Player


class CreateRoomSerializer(serializers.Serializer):
    room_limit = serializers.IntegerField(required=True, min_value=2, max_value=4)
    players = serializers.ListField(child=serializers.CharField(), required=True, min_length=2, max_length=4)


class UpdateGameSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    player1_score = serializers.IntegerField(required=True)
    player2_score = serializers.IntegerField(required=True)
    winner = serializers.CharField(required=True)
    loser = serializers.CharField(required=True)


class JoinRoomSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(required=True)


class ListInviteSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
