from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import GenerateTokenSerializer, ValidateTokenSerializer, RefreshTokenSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings

class AuthHandler(viewsets.ViewSet):
    SECRET_KEY = settings.SECRET_KEY

    def generate_token(self, request):
        req= GenerateTokenSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user_id = req.validated_data['user_id']
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
        return Response({'token': token}, status=status.HTTP_200_OK)

    def validate_token(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return Response({'user_id': decoded_token['user_id']}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    def refresh_token(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            new_token = self.generate_token(decoded_token['user_id'])
            return Response({'token': new_token}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
