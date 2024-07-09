from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Game, Room, Player


class CreateRoomSerializer(serializers.Serializer):
    room_limit = serializers.IntegerField(required=True, min_value=2, max_value=4)
    players = serializers.ListField(child=serializers.CharField(), required=True, min_length=1, max_length=3)


class UpdateGameSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    status = serializers.IntegerField(required=True, min_value=0, max_value=3)
    player1_score = serializers.IntegerField(required=True)
    player2_score = serializers.IntegerField(required=True)

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, min_value=1, max_value=500)
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=500)
