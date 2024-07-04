from rest_framework.response import Response
from rest_framework import viewsets
from .service import GameService
from .serializers import CreateRoomSerializer, UpdateGameSerializer


class GameHandler(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = GameService()

    def create_room(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'unauthorized'}, status=401)
        req = CreateRoomSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.create_room(req.validated_data, user_id)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def join_room(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'unauthorized'}, status=401)
        room_id = request.query_params.get('room')
        if not room_id:
            return Response({'error': 'Room id is required'}, status=400)
        res, err = self.service.join_room(room_id, user_id)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def list_invite(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=400)
        res, err = self.service.list_invite(user_id)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def update_game(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=400)
        req = UpdateGameSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.update_game(req.validated_data)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)
