from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import GenerateTokenSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import requests


def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=600),  # Access token expiration
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),  # Refresh token expiration
        'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return refresh_token


class AuthHandler(viewsets.ViewSet):
    SECRET_KEY = settings.SECRET_KEY

    def generate_tokens(self, request):
        req = GenerateTokenSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user_id = req.validated_data['user_id']
        access_token = generate_access_token(user_id)
        refresh_token = generate_refresh_token(user_id)
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)

    def validate_token(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = token.split(' ')[1]
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
            token = token.split(' ')[1]
            decoded_token = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            if 'exp' in decoded_token:
                if decoded_token['exp'] < datetime.utcnow():
                    return Response({'error': 'Refresh token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            new_access_token = generate_access_token(decoded_token['user_id'])
            return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    def intra_oauth(self, request):
        return Response({'url': settings.INTRA_REDIRECT_URL}, status=status.HTTP_200_OK)

    def intra_oauth_callback(self, request):
        code = request.query_params['code']
        url = f"{settings.INTRA_API_URL}/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.INTRA_UID,
            "client_secret": settings.INTRA_SECRET,
            "code": code,
            "redirect_uri": settings.INTRA_CALLBACK_URL
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            return Response({'error': 'Failed to retrieve OAuth token'}, status=response.status_code)

        oauth_token = response.json()

        user_creation_response = self.create_user(oauth_token)
        if user_creation_response.status_code != 201:
            return Response(user_creation_response.json(), status=user_creation_response.status_code)
        response_data = user_creation_response.json().get('data')
        user_id = response_data[0].get('id')
        token = generate_access_token(user_id)
        res = {
            'message': user_creation_response.json().get('message'),
            'data': [{'token': token, 'user_id': user_id}]
        }
        return Response(res, status=status.HTTP_201_CREATED)
    

    def create_user(self, oauth_token):
        user_info = self.get_user_info(oauth_token)
        user_creation_url = f"{settings.USER_MANAGEMENT_URL}/user/oauth/create"
        user_creation_data = {
            'username': user_info.get('login'),
            'email': user_info.get('email'),
            'first_name': user_info.get('first_name'),
            'last_name': user_info.get('last_name'),
            'phone': user_info.get('phone'),
            'provider': 'intra',
            'provider_user_id': user_info.get('id'),
            'access_token': oauth_token.get('access_token'),
            'refresh_token': oauth_token.get('refresh_token'),
            'expires_in': oauth_token.get('expires_in')
        }
        response = requests.post(user_creation_url, data=user_creation_data)

        return response

    def get_user_info(self, oauth_token):
        user_info_url = f"{settings.INTRA_API_URL}/v2/me"
        headers = {'Authorization': f"Bearer {oauth_token.get('access_token')}"}
        response = requests.get(user_info_url, headers=headers)

        return response.json()
