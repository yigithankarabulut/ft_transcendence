from rest_framework.response import Response
from rest_framework import viewsets
from .service import GameService
from .serializers import CreateRoomSerializer


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
        print("request data", req.validated_data)
        return Response("success", status=200)
        res, err = self.service.create_room(req.validated_data, user_id)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def update_game(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=400)
        res = self.service.get(user_id)
        return Response(res, status=200)
