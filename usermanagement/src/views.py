from rest_framework.response import Response
from rest_framework import viewsets
import logging
from django.conf import settings
from .service import UserManagementService
from .repository import UserManagementRepository, OAuthUserRepository
from .serializers import RegisterSerializer, OauthCreateSerializer, ResetPasswordSerializer
from .serializers import LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from .serializers import CreateManagementSerializer, GetUserByIdSerializer, PaginationSerializer, SearchUserToPaginationSerializer
from .serializers import TwoFactorAuthSerializer, UpdateUsernameSerializer


class UserManagementHandler(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserManagementService(UserManagementRepository(), OAuthUserRepository())

    def get_user(self, request):
        user_id = request.headers.get('id')
        if not user_id:
            return Response({'error': 'User id is required'}, status=400)
        res, err = self.service.get(user_id)
        if err:
            return Response(res, status=401)
        return Response(res, status=200)

    def get_user_by_username(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=400)
        res, err = self.service.get_by_username(username)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def get_user_by_id(self, request):
        id = request.query_params.get('id')
        uid = request.headers.get('id')
        if not id and not uid:
            return Response({'error': 'Id is required'}, status=400)
        if not id:
            id = uid
        res, err = self.service.get_by_id(id)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def update_user(self, request):
        req = CreateManagementSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        id = request.headers.get('id')
        if not id:
            return Response({'error': 'Id is required'}, status=400)
        user = req.bind(req.validated_data)
        res, err = self.service.update(user, id)
        if err:
            return Response(res, status=500)
        if res.get('message') == 'User updated successfully. Email verification mail sent to your email':
            return Response(res, status=207)
        return Response(res, status=200)

    def update_username(self, request):
        req = UpdateUsernameSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        username = request.data.get('username')
        id = request.headers.get('id')
        if not id:
            return Response({'error': 'Unauthorized'}, status=401)
        res, err = self.service.update_username(username, id)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def list_user(self, request):
        req = PaginationSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res = self.service.list(req.validated_data['page'], req.validated_data['limit'])
        return Response(res, status=200)

    def search_user(self, request):
        req = SearchUserToPaginationSerializer(data=request.query_params)
        if not req.is_valid():
            return Response(req.errors, status=400)
        id = request.headers.get('id')
        if not id:
            return Response({'error': 'Id is required'}, status=400)
        res, err = self.service.search(
            req.validated_data['key'],
            req.validated_data['page'],
            req.validated_data['limit'],
            id,
        )
        if err:
            return Response(res, status=500)
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
        print(request.data)
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
            return Response(res, status=500)
        return Response(res, status=200)

    def two_factor_auth(self, request):
        print(request.data)
        req = TwoFactorAuthSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        user = req.bind(req.validated_data)
        res, err = self.service.two_factor_auth(user)
        if err:
            logging.error(res)
            return Response(res, status=500)
        return Response(res, status=200)

    def forgot_password(self, request):
        req = ForgotPasswordSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.forgot_password(req.validated_data['email'])
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def change_password(self, request):
        req = ChangePasswordSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        id = request.headers.get('id')
        if not id:
            return Response({'error': 'Id is required'}, status=400)
        res, err = self.service.change_password(req.validated_data, id)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def reset_password(self, request, uidb64=None, token=None):
        if not uidb64 or not token:
            return Response({'error': 'invalid url'}, status=400)
        req = ResetPasswordSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.reset_password(req.validated_data, uidb64, token)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)
    
    def redirect_reset_password(self, request, uidb64=None, token=None):
        if not uidb64 or not token:
            return Response({'error': 'invalid url'}, status=400)
        res, err = self.service.redirect_reset_password(uidb64, token)
        if err:
            return Response(res, status=500)
        redirect_url = f"{settings.FRONTEND_URL}/reset-password?uidb64={uidb64}&token={token}"
        resp = {
            "redirect_url": redirect_url,
        }
        return Response(resp, status=200)

    def email_verify(self, request, uidb64=None, token=None):
        if not uidb64 or not token:
            return Response({'error': 'invalid url'}, status=400)
        res, err = self.service.email_verify(request, uidb64, token)
        if err:
            logging.error("Email verification failed %s", res)
            return Response(res, status=500)
        logging.info('Email verified successfully')
        redirect_url = f"{settings.FRONTEND_URL}/login"
        resp = {
            "redirect_url": redirect_url,
        }
        return Response(resp, status=200)

    def oauth_user_create(self, request):
        req = OauthCreateSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.data, status=400)
        user_management = req.bind_user_management(req.validated_data)
        user_oauth = req.bind_oauth_user(req.validated_data)
        res, err = self.service.oauth_user_create(user_management, user_oauth)
        if err:
            return Response(res, status=500)
        # 207 status code is for username already exist. Redirect to frontend to update username
        if res.get('message') == 'User created successfully' or res.get('message') == 'Login successfully':
            return Response(res, status=201)
        return Response(res, status=207)
