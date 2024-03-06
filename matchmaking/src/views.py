from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import JoinPlayerSerializer
from .service import QuickPlayService
from .repository import QuickPlayRepository

class QuickPlayHandlers(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = QuickPlayService(QuickPlayRepository())

    def join(self, request):
        req = JoinPlayerSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)
        player = req.bind(req.validated_data)
        res, err = self.service.join(player)
        if err:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)
        
        
    def leave(self, request):
        return Response({'status': 'ok'})

    def match(self, request):
        return Response({'status': 'ok'})