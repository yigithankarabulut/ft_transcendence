# serializers.py
from rest_framework import serializers
from .models import Player, Match

class JoinPlayerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)

    def bind(self, validated_data):
        return Player(**validated_data)