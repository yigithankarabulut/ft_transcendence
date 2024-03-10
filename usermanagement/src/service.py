import requests
from hashlib import sha256

from django.utils.timezone import now
from .utils import BaseResponse, make_hash_value, check_token_validity
from .publisher import PublisherBase
from .serializers import ManagementSerializer
from .models import UserManagement, OAuthUser
from usermanagement.settings import SERVICE_ROUTES
from django.core.paginator import Paginator, EmptyPage
from .interfaces.service import IUserManagementService
from .interfaces.repository import IUserManagementRepository, IOAuthUserRepository

from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# TODO: All queries should be made email because email is unique. username sometimes can be null.

class UserManagementService(IUserManagementService):
    def __init__(self, repository: IUserManagementRepository, oauth_repository = IOAuthUserRepository):
        self.repository = repository
        self.oauth_repository = oauth_repository

    def get(self, id: int) -> BaseResponse:
        user = self.repository.get(id)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        res = ManagementSerializer().response([user])
        return BaseResponse(False, "User found", res).res()

    def update(self, user: UserManagement) -> BaseResponse: # TODO: verifying email and phone 
        uname = self.repository.get_by_username(user.username)
        uemail = self.repository.get_by_email(user.email)
        if uname and uname.id != user.id:
            return BaseResponse(True, "Username already exists", None).res()
        elif uname and uname.id == user.id:
            return BaseResponse(True, "Please provide a different username", None).res()
        if uemail and uemail.id != user.id:
            return BaseResponse(True, "Email already exists", None).res()

        elif uemail and uemail.id == user.id:
            return BaseResponse(True, "Please provide a different email", None).res()

        new_user = self.repository.update(user)
        if not new_user:
            return BaseResponse(True, "User update failed", None).res()
        res = ManagementSerializer().response([new_user])
        return BaseResponse(False, "User updated successfully", res).res()

    def list(self, page, limit) -> BaseResponse:
        users = self.repository.list()
        if not users:
            return BaseResponse(True, "No users found", None).res()
        paginator = Paginator(users, limit)
        try:
            pagineted_users = paginator.page(page)
        except EmptyPage:
            return BaseResponse(True, "There is no data on this page", None).res()

        if not pagineted_users:
            return BaseResponse(False, "No users found", None).res()

        res = ManagementSerializer().response(pagineted_users)
        paginate_data = {
            "current_page": page,
            "page_size": limit,
            "total_pages": paginator.num_pages,
            "total_records": paginator.count
        }
        return BaseResponse(False, "Users found", res, paginate_data).res()

    def delete(self, id: int)-> BaseResponse:
        user = self.repository.get(id)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        res = self.repository.delete(id)
        if not res:
            return BaseResponse(True, "User deletion failed", None).res()
        return BaseResponse(False, "User deleted successfully", None).res()

    def register(self, user: UserManagement) -> BaseResponse:
        uname = self.repository.get_by_username(user.username)
        umail = self.repository.get_by_email(user.email)
        if uname:
            return BaseResponse(True, "Username already exists", None).res()
        if umail:
            return BaseResponse(True, "Email already exists", None).res()
        hashpwd = sha256(user.password.encode()).hexdigest()
        user.password = hashpwd
        user = self.repository.create(user)
        if not user:
            return BaseResponse(True, "User creation failed", None).res()
        res = ManagementSerializer().response([user])
        return BaseResponse(False, "User created successfully", res).res()

    def login(self, req: UserManagement) -> BaseResponse:
        user = self.repository.get_by_username(req.username)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if user.password != sha256(req.password.encode()).hexdigest():
            return BaseResponse(True, "Invalid password", None).res()
        # request to auth service add query params user_id and get token
        response = requests.post(f"{SERVICE_ROUTES['/auth']}/auth/token", params={"user_id": user.id})
        if response.status_code != 200:
            return BaseResponse(True, "Token generation failed", None).res()
        token = response.json().get('token')
        return BaseResponse(False, "Login successful", {"token": token}).res()

    def forgot_password(self, email) -> BaseResponse:
        user = self.repository.get_by_email(email)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if user.reset_password_token:
            err = check_token_validity(user.reset_password_token)
            if err is None:
                return BaseResponse(True, "Password reset link already sent", None).res()

        encoded_token = urlsafe_base64_encode(
            force_bytes(
                make_hash_value(
                    user,
                    now().timestamp(),
                )
            )
        )
        uid = urlsafe_base64_encode(force_bytes(email))
        reset_path = reverse(
            'reset_password',
            kwargs={'uidb64': uid, 'token': encoded_token},
        )

        user.reset_password_token = encoded_token
        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "Unknow error. Please try again later!", None).res()

        # TODO: Fix the front back communication this situation
        # TODO: Change this url with frontend url
        reset_url = f"http://localhost:8004{reset_path}"
        message = {
            'subject': 'Transcendence Password Reset Email',
            'body': {'email': email, 'reset_url': reset_url},
            'type': 'forgot_password'
        }

        publisher = PublisherBase('mail-service')
        res = publisher.publish_message(message)
        publisher.close_connection()
        if not res:
            return BaseResponse(True, "Password sending failed", None).res()
        return BaseResponse(False, "Password sent to your email", None).res()

    def change_password(self, req) -> BaseResponse:
        user = self.repository.get_by_username(req.get("username"))
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if user.password != sha256(req.get("old_password").encode()).hexdigest():
            return BaseResponse(True, "Invalid password", None).res()
        hash_password = sha256(req.get("new_password").encode()).hexdigest()
        user.password = hash_password
        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "Password change failed", None).res()
        return BaseResponse(False, "Password changed successfully", None).res()

    def reset_password(self, req, uid, token) -> BaseResponse:
        email = force_str(urlsafe_base64_decode(uid))
        if not email:
            return BaseResponse(True, "Invalid token", None).res()
        user = self.repository.get_by_email(email)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if not user.reset_password_token:
            return BaseResponse(True, "This link is already used", None).res()
        if user.reset_password_token != token:
            return BaseResponse(True, "Invalid token", None).res()

        err = check_token_validity(token)
        if err is not None:
            return BaseResponse(True, err, None).res()

        hash_password = sha256(req.get("new_password").encode()).hexdigest()
        user.password = hash_password
        user.reset_password_token = None

        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "Password reset failed", None).res()
        return BaseResponse(False, "Password reset successfully", None).res()

    def oauth_user_create(self, user_management: UserManagement, oauth_user: OAuthUser) -> BaseResponse:
        uname = self.repository.get_by_username(user_management.username)
        umail = self.repository.get_by_email(user_management.email)
        flag = False
        if uname:
            flag = True
            user_management.username = None
        if umail:
            return BaseResponse(True, "Email already exist.Please login with your Email", None).res()
        user_management.oauth_users = 1
        user_management = self.repository.create(user_management)
        if not user_management:
            return BaseResponse(True, "User creation failed", None).res()
        oauth_user.user = user_management
        oauth_user = self.oauth_repository.oauth_user_create(oauth_user)
        if not oauth_user:
            return BaseResponse(True, "OAuth user creation failed", None).res()
        res = ManagementSerializer().response([user_management])
        if flag:
            return BaseResponse(
                False,
                "User created successfully but your intra username is already exist."
                "Please visit your profile and update your username",
                res
            ).res()
        return BaseResponse(False, "User created successfully", res).res()
