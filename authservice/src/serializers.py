from rest_framework import serializers


class GenerateTokenSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)


class RefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)