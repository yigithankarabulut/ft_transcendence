import jwt
import requests
from datetime import datetime, timedelta, timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import GenerateTokenSerializer, RefreshTokenSerializer
from django.conf import settings
import logging


def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=1),
        'iat': datetime.now(tz=timezone.utc)
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    iat_seconds = payload['iat'].timestamp()
    logging.error("------------------------------->>>>>>>>> %s", iat_seconds)
    return access_token, iat_seconds


def generate_refresh_token(user_id, exp, iat, access_token_iat):
    if exp is None:
        exp = datetime.now(tz=timezone.utc) + timedelta(days=7)
    if iat is None:
        iat = datetime.now(tz=timezone.utc)
    payload = {
        'user_id': user_id,
        'acces_token_iat': access_token_iat,
        'exp': exp,
        'iat': iat,
    }

    refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return refresh_token


class AuthHandler(viewsets.ViewSet):
    SECRET_KEY = settings.SECRET_KEY
    verification_options = {"require": ["exp", "iat"], "verify_exp": True, "verify_iat": True, "verify_signature": True}

    def generate_tokens(self, request):
        req = GenerateTokenSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user_id = req.validated_data['user_id']
        access_token, acss_iat = generate_access_token(user_id)
        refresh_token = generate_refresh_token(user_id, None, None, acss_iat)
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
            decoded_token = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'], options=self.verification_options)
            return Response({'user_id': decoded_token['user_id']}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def refresh_token(self, request):
        access_token = request.headers.get('Authorization')
        if not access_token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        req = RefreshTokenSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = req.validated_data['refresh_token']

        try:
            decoded_access_token = jwt.decode(access_token.split(' ')[1], self.SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})
        except jwt.ExpiredSignatureError:
            try:
                accs_iat = decoded_access_token['iat']
                refresh_token = refresh_token.split(' ')[1]
                decoded_token = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=['HS256'], options=self.verification_options)
                refresh_accs_iat = decoded_token['acces_token_iat']
                if accs_iat != refresh_accs_iat:
                    return Response({'error': 'Access token and refresh token do not match'}, status=status.HTTP_400_BAD_REQUEST)
                user_id = decoded_token['user_id']
                new_access_token, access_iat = generate_access_token(user_id)
                new_refresh_token = generate_refresh_token(user_id, decoded_token['exp'], decoded_token['iat'], access_iat)
                return Response({
                    'access_token': new_access_token,
                    'refresh_token': new_refresh_token
                }, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalids token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        if user_creation_response.status_code != 201 and user_creation_response.status_code != 207:
            return Response(user_creation_response.json(), status=user_creation_response.status_code)

        response_data = user_creation_response.json().get('data')
        user_id = response_data[0].get('id')
        token, access_iat = generate_access_token(user_id)
        refresh_token = generate_refresh_token(user_id, None, None, access_iat)

        # 207 status code is for username already exist.
        # Redirect to frontend for update username. Otherwise, redirect to homepage
        if user_creation_response.status_code == 207:
            redirect_url = f"{settings.FRONTEND_URL}/uname?access_token={token}&refresh_token={refresh_token}"
        else:
            redirect_url = f"{settings.FRONTEND_URL}/auth?access_token={token}&refresh_token={refresh_token}"
        res = {
            "redirect_url": redirect_url
        }
        if user_creation_response.status_code == 207:
            return Response(res, status=status.HTTP_207_MULTI_STATUS)
        return Response(res, status=status.HTTP_200_OK)

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
