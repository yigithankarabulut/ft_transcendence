from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import BaseSerializer, GetByIdSerializer, PaginationSerializer
from .service import FriendsService
from .repository import FriendsRepository


class FriendsHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        serializer = BaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        sender_id = serializer.validated_data.get('sender_id')
        receiver_id = serializer.validated_data.get('receiver_id')
        response, err = self.service.reject_request(sender_id, receiver_id)
        if err:
            return Response(response, status=400)
        return Response(response, status=201)


    def request(self, request) -> Response:
        serializer = GetByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user_id = serializer.validated_data.get('id')
        response, err = self.service.get_requests(user_id)
        if err:
            return Response(response, status=400)
        return Response(response, status=200)

    def list(self, request) -> Response:
        serializer = GetByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        page = PaginationSerializer(data=request.query_params)
        if not page.is_valid():
            return Response(page.errors, status=400)
        response, err = self.service.get_friends(
            serializer.validated_data.get('id'),
            page.validated_data.get('page'),
            page.validated_data.get('limit'),
        )
        if err:
            return Response(response, status=400)
        return Response(response, status=200)
        

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
