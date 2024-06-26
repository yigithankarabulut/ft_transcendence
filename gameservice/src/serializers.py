from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Game, Room, Player


class CreateRoomSerializer(serializers.Serializer):
    room_limit = serializers.IntegerField(required=True, min_value=2, max_value=4)
    game_score = serializers.IntegerField(required=True, min_value=4, max_value=20)
    players = serializers.ListField(child=serializers.CharField(), required=True, min_length=2, max_length=4)

