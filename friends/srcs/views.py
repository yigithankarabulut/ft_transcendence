from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import BaseSerializer
from .service import FriendsService
from .repository import FriendsRepository

class FriendsHandler(viewsets.ViewSet):
    def __init__(self):
        self.service = FriendsService(FriendsRepository())

    def add(self, request) -> Response:
        serializer = BaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        sender_id = serializer.validated_data.get('sender_id')
        receiver_id = serializer.validated_data.get('receiver_id')
        response, err = self.service.add_friend(sender_id, receiver_id)
        if err:
            return Response(response, status=400)
        return Response(response, status=201)

    def accept(self, request) -> Response:
        serializer = BaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        sender_id = serializer.validated_data.get('sender_id')
        receiver_id = serializer.validated_data.get('receiver_id')
        response, err = self.service.accept_request(sender_id, receiver_id)
        if err:
            return Response(response, status=400)
        return Response(response, status=201)

    def reject(self, request) -> Response:
        pass

    def request(self, request) -> Response:
        pass

    def list(self, request) -> Response:
        pass

    def delete(self, request) -> Response:
        serializer = BaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        sender_id = serializer.validated_data.get('sender_id')
        receiver_id = serializer.validated_data.get('receiver_id')
        response, err = self.service.delete_friend(sender_id, receiver_id)
        if err:
            return Response(response, status=400)
        return Response(response, status=201)
