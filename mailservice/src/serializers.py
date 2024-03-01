# serializers.py
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    sender_email = serializers.EmailField()
    receiver_email = serializers.EmailField()
    subject = serializers.CharField()
    body = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
