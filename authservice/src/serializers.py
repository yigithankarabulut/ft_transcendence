from rest_framework import serializers


class GenerateTokenSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)