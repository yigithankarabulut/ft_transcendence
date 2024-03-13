from rest_framework.response import Response
from rest_framework import viewsets
from .service import UserManagementService
from .repository import UserManagementRepository, OAuthUserRepository
from .serializers import RegisterSerializer, OauthCreateSerializer, ResetPasswordSerializer
from .serializers import LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from .serializers import CreateManagementSerializer, GetUserByIdSerializer, PaginationSerializer
from .serializers import TwoFactorAuthSerializer


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
            print(res)
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
        res, err = self.service.change_password(req.validated_data)
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

    def email_verify(self, request, uidb64=None, token=None):
        if not uidb64 or not token:
            return Response({'error': 'invalid url'}, status=400)
        res, err = self.service.email_verify(request, uidb64, token)
        if err:
            return Response(res, status=500)
        return Response(res, status=200)

    def oauth_user_create(self, request):
        req = OauthCreateSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.data, status=400)
        user_management = req.bind_user_management(req.validated_data)
        user_oauth = req.bind_oauth_user(req.validated_data)
        res, err = self.service.oauth_user_create(user_management, user_oauth)
        if err:
            return Response(res, status=500)
        return Response(res, status=201)
