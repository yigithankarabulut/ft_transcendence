from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import BaseSerializer, GetByIdSerializer, PaginationSerializer, ReceiverSerializer
from .service import FriendsService
from .repository import FriendsRepository


class FriendsHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = FriendsService(FriendsRepository())

    def add(self, request) -> Response:
        sender_id = request.headers.get('id')
        if not sender_id:
            return Response({"error": "User ID is required"}, status=400)
        req = ReceiverSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        receiver_id = req.validated_data.get('receiver_id')
        res, err = self.service.add_friend(sender_id, receiver_id)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def accept(self, request) -> Response:
        sender_id = request.headers.get('id')
        if not sender_id:
            return Response({"error": "User ID is required"}, status=400)
        req = ReceiverSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        receiver_id = req.validated_data.get('receiver_id')
        res, err = self.service.accept_request(sender_id, receiver_id)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def reject(self, request) -> Response:
        sender_id = request.headers.get('id')
        if not sender_id:
            return Response({"error": "User ID is required"}, status=400)
        req = ReceiverSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        receiver_id = req.validated_data.get('receiver_id')
        res, err = self.service.reject_request(sender_id, receiver_id)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def request(self, request) -> Response:
        id = request.headers.get('id')
        if not id:
            return Response({"error": "User ID is required"}, status=400)
        page = PaginationSerializer(data=request.query_params)
        if not page.is_valid():
            return Response(page.errors, status=400)
        res, err = self.service.get_requests(
            id,
            page.validated_data.get('page'),
            page.validated_data.get('limit'),
        )
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def list(self, request) -> Response:
        id = request.headers.get('id')
        if not id:
            return Response({"error": "User ID is required"}, status=400)
        page = PaginationSerializer(data=request.query_params)
        if not page.is_valid():
            return Response(page.errors, status=400)
        res, err = self.service.get_friends(
            id,
            page.validated_data.get('page'),
            page.validated_data.get('limit'),
        )
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def delete(self, request) -> Response:
        sender_id = request.headers.get('id')
        if not sender_id:
            return Response({"error": "User ID is required"}, status=400)
        req = ReceiverSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        receiver_id = req.validated_data.get('receiver_id')
        res, err = self.service.delete_friend(sender_id, receiver_id)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)