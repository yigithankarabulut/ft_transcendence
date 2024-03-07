from rest_framework import viewsets
from .serializers import CreateManagementSerializer, GetUserByIdSerializer, PaginationSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, OauthCreateSerializer
# from . import serializers
from .repository import UserManagementRepository, OAuthUserRepository
from .service import UserManagementService
from django.http import response
from rest_framework.response import Response
from .models import UserManagement, OAuthUser
from datetime import datetime, timedelta

# GET     /user/details
# POST    /user/create
# PUT     /user/update
# DELETE  /user/delete
# GET     /user/list
class UserManagementHandler(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserManagementService(UserManagementRepository(), OAuthUserRepository())

    def get_user(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=400)
        res = self.service.get(user_id)
        return Response(res, status=200)

    def update_user(self, request):
        req = CreateManagementSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user = req.bind(req.validated_data)
        res = self.service.update(user)
        return Response(res, status=200)

    def list_user(self, request):
        req = PaginationSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res = self.service.list(req.validated_data['page'], req.validated_data['limit'])
        return Response(res, status=200)

    def delete_user(self, request):
        req = GetUserByIdSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res = self.service.delete(req.validated_data['id'])
        return Response(res, status=200)


class AuthHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserManagementService(UserManagementRepository(), OAuthUserRepository())

    def register(self, request):
        req = RegisterSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user = req.bind(req.validated_data)
        res, err = self.service.register(user)
        if err:
            return Response(res, status=400)
        return Response(res, status=201)

    def login(self, request):
        req = LoginSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user = req.bind(req.validated_data)
        res, err = self.service.login(user)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)        

    def change_password(self, request):
        req = ChangePasswordSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.change_password(req.validated_data)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def forgot_password(self, request):
        req = ForgotPasswordSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.forgot_password(req.validated_data['username'], req.validated_data['email'])
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def oauth_user_create(self, request):
        req = OauthCreateSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.data, status=400)
        user_management, user_oauth = self.mapper(req.validated_data)
        res, err = self.service.oauth_user_create(user_management, user_oauth)
        if err:
            return Response(res, status=400)
        return Response(res, status=201)
    
    def mapper(self, validated_data):
        seconds = int(validated_data['expires_in'])
        expires_in = datetime.now() + timedelta(seconds)
        user_management = UserManagement(
            username=validated_data['username'],
            password="oauth",
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone']
        )
        user_oauth = OAuthUser(
            provider=validated_data['provider'],
            provider_user_id=validated_data['provider_user_id'],
            access_token=validated_data['access_token'],
            refresh_token=validated_data['refresh_token'],
            expires_in=expires_in
        )
        return user_management, user_oauth