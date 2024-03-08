from rest_framework import viewsets
from rest_framework.response import Response
from .service import UserManagementService
from .repository import UserManagementRepository, OAuthUserRepository
from .serializers import CreateManagementSerializer, GetUserByIdSerializer, PaginationSerializer, RegisterSerializer
from .serializers import LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, OauthCreateSerializer, ResetPasswordSerializer

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
        res, err = self.service.forgot_password(req.validated_data['email'])
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def reset_password(self, request): # TODO:  http://localhost:8004/user//user/reset-password/ ----> fix this
        req = ResetPasswordSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.errors, status=400)
        res, err = self.service.reset_password(req.validated_data, request)
        if err:
            return Response(res, status=400)
        return Response(res, status=200)

    def oauth_user_create(self, request):
        req = OauthCreateSerializer(data=request.data)
        if not req.is_valid():
            return Response(req.data, status=400)
        user_management = req.bind_user_management(req.validated_data)
        user_oauth = req.bind_oauth_user(req.validated_data)
        res, err = self.service.oauth_user_create(user_management, user_oauth)
        if err:
            return Response(res, status=400)
        return Response(res, status=201)
    