import requests
from hashlib import sha256
from django.utils.timezone import now
from .utils import BaseResponse, req_to_auth_service_for_generate_token
from .utils import check_token_validity, make_hash_value, generate_2fa_code
from .publisher import PublisherBase
from .serializers import ManagementSerializer
from .models import UserManagement, OAuthUser
from usermanagement.settings import SERVICE_ROUTES, FRONTEND_URL
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from .interfaces.service import IUserManagementService
from .interfaces.repository import IUserManagementRepository, IOAuthUserRepository
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class UserManagementService(IUserManagementService):
    def __init__(self, repository: IUserManagementRepository, oauth_repository: IOAuthUserRepository):
        self.repository = repository
        self.oauth_repository = oauth_repository

    def get(self, id) -> BaseResponse:
        user = self.repository.get(id)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        res = ManagementSerializer().response([user])
        return BaseResponse(False, "User found", res).res()

    def update(self, user, id) -> BaseResponse:
        data = self.repository.get_by_id(id)
        if not data:
            return BaseResponse(True, "User not found", None).res()
        if data.username != user.username:
            new_user = self.repository.get_by_username(user.username)
            if new_user:
                return BaseResponse(True, "Username already exists", None).res()
        if data.phone != user.phone:
            new_user = self.repository.get_by_phone(user.phone)
            if new_user:
                return BaseResponse(True, "Phone already exists", None).res()
        data.first_name = user.first_name
        data.last_name = user.last_name
        data.username = user.username
        data.phone = user.phone
        new_user = self.repository.update(data)
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

    def get_by_username(self, username: str) -> BaseResponse:
        user = self.repository.get_by_username(username)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        res = ManagementSerializer().response([user])
        return BaseResponse(False, "User found", res).res()

    def get_by_id(self, id: str) -> BaseResponse:
        user = self.repository.get_by_id(id)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        res = ManagementSerializer().response([user])
        return BaseResponse(False, "User found", res).res()
    
    def update_username(self, username, id) -> BaseResponse:
        user = self.repository.get_by_id(id)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        new_user = self.repository.get_by_username(username)
        if new_user:
            return BaseResponse(True, "Username already exists", None).res()
        user.username = username
        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "Username update failed", None).res()
        return BaseResponse(False, "Username updated successfully", None).res()

    def search(self, key, page, limit) -> BaseResponse:
        users = self.repository.search(key)
        if not users:
            return BaseResponse(True, "No users found", None).res()
        paginator = Paginator(users, limit)
        try:
            pagineted_users = paginator.page(page)
        except Exception as e:
            if e is EmptyPage:
                return BaseResponse(False, "There is no data on this page", None).res()
            return BaseResponse(True, "Failed to get users", None).res()

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

    def delete(self, id: int) -> BaseResponse:
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
        hash_password = sha256(user.password.encode()).hexdigest()
        user.password = hash_password
        try:
            with transaction.atomic():
                user = self.repository.create(user)
                if not user:
                    raise Exception("User creation failed")
                res = ManagementSerializer().response([user])
        except Exception as e:
            err = str(e)
            return BaseResponse(True, err, None).res()
        # This step user created but email verification is not done yet.
        # Create email verification token and send email.
        encoded_token = urlsafe_base64_encode(
            force_bytes(
                make_hash_value(
                    user,
                    now().timestamp(),
                )
            )
        )
        user.email_verify_token = encoded_token
        updated_user = self.repository.update(user)
        if not updated_user:
            return BaseResponse(True, "Email verification token creation failed", None).res()
        uid = urlsafe_base64_encode(force_bytes(user.email))
        verify_url = reverse(
            'email_verify',
            kwargs={'uidb64': uid, 'token': encoded_token},
        )

        verify_url = f"{FRONTEND_URL}/api{verify_url}"
        message = {
            'subject': 'Transcendence Email Verification',
            'body': {'email': user.email, 'verify_url': verify_url},
            'type': 'email_verify'
        }
        publisher = PublisherBase('mail-service')
        err = publisher.publish_message(message)
        if err is not True:
            return BaseResponse(True, "Email verification mail sending failed, but registration successfuly.", None).res()
        publisher.close_connection()
        return BaseResponse(False, "User created successfully", res).res()

    def login(self, req: UserManagement) -> BaseResponse:
        user = self.repository.get_by_email(req.email)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if user.oauth_users > 0:
            return BaseResponse(True, "User logged in with oauth provider", None).res()
        if user.password != sha256(req.password.encode()).hexdigest():
            return BaseResponse(True, "Invalid password", None).res()
        if not user.email_verified:
            return BaseResponse(True, "Email not verified. Please check your mailbox and verify your email", None).res()

        code, db_code = generate_2fa_code()
        user.twofa_code = db_code
        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "2FA code generation failed", None).res()

        message = {
            'subject': 'Transcendence 2FA Code',
            'body': {'email': user.email, 'code': code},
            'type': '2fa_code'
        }
        publisher = PublisherBase('mail-service')
        res = publisher.publish_message(message)
        publisher.close_connection()
        if not res:
            return BaseResponse(True, "2FA code sending failed", None).res()
        return BaseResponse(False, "2FA code sent to your email", None).res()

    def two_factor_auth(self, req: UserManagement) -> BaseResponse:
        user = self.repository.get_by_email(req.email)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if not user.email_verified:
            return BaseResponse(True, "Email not verified. Please check your mailbox and verify your email", None).res()
        if not user.twofa_code:
            return BaseResponse(True, "You are not requested 2FA code", None).res()

        code = user.twofa_code.split("-")[0]
        if code != req.twofa_code:
            return BaseResponse(True, "Invalid 2FA code", None).res()
        code_timestamp = user.twofa_code.split("-")[1]
        if now().timestamp() - float(code_timestamp) > 100:
            return BaseResponse(True, "2FA code expired", None).res()

        access_token, refresh_token = req_to_auth_service_for_generate_token(user.id)
        if not access_token or not refresh_token:
            return BaseResponse(True, "Token generation failed", None).res()
        return BaseResponse(False, "Login successful", {"access_token": access_token, "refresh_token": refresh_token}).res()

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

        reset_url = f"{FRONTEND_URL}/api{reset_path}"
        message = {
            'subject': 'Transcendence Password Reset Email',
            'body': {'email': email, 'reset_url': reset_url},
            'type': 'forgot_password'
        }
        publisher = PublisherBase('mail-service')
        res = publisher.publish_message(message)
        publisher.close_connection()
        if not res:
            return BaseResponse(True, "Password reset link sending failed", None).res()
        return BaseResponse(False, "Password reset link sent to your email", None).res()

    def change_password(self, req, id) -> BaseResponse:
        user = self.repository.get_by_id(id)
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

    def redirect_reset_password(self, uid, token) -> BaseResponse:
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
        return BaseResponse(False, "Reset password", None).res()

    def email_verify(self, req, uid, token) -> BaseResponse:
        email = force_str(urlsafe_base64_decode(uid))
        if not email:
            return BaseResponse(True, "Invalid token", None).res()
        user = self.repository.get_by_email(email)
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if not user.email_verify_token:
            return BaseResponse(True, "This link is already used", None).res()
        if user.email_verify_token != token:
            return BaseResponse(True, "Invalid token", None).res()

        err = check_token_validity(token)
        if err is not None:
            return BaseResponse(True, err, None).res()
        user.email_verify_token = None
        user.email_verified = True
        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "Email verification failed", None).res()
        return BaseResponse(False, "Email verified successfully. You can login now", None).res()

    def oauth_user_create(self, user_management: UserManagement, oauth_user: OAuthUser) -> BaseResponse:
        # If user already logged in with oauth provider, update the user with new data, but username should be unique.
        user = self.oauth_repository.get_oauth_user_with_provider_and_provider_user_id(oauth_user.provider, oauth_user.provider_user_id)
        if user:
            user.access_token = oauth_user.access_token
            user.refresh_token = oauth_user.refresh_token
            user.expires_in = oauth_user.expires_in
            if self.oauth_repository.update_oauth_user(user) is None:
                return BaseResponse(True, "OAuth user update failed", None).res()
            if user.user.username:
                res = ManagementSerializer().response([user.user])
                return BaseResponse(False, "Login successfully", res).res()
            else:
                res = ManagementSerializer().response([user.user])
                return BaseResponse(False, "Login successfully but your username is not set. Please update your username", res).res()

        uname = self.repository.get_by_username(user_management.username)
        umail = self.repository.get_by_email(user_management.email)
        flag = False
        if uname:
            flag = True
            user_management.username = None
        if umail:
            res = ManagementSerializer().response([umail])
            return BaseResponse(True, "Email already exists", res).res()

        try:
            with transaction.atomic():
                user_management.oauth_users = 1
                user_management.email_verified = True
                user_management = self.repository.create(user_management)
                if not user_management:
                    raise Exception("User creation failed")
                oauth_user.user = user_management
                oauth_user = self.oauth_repository.oauth_user_create(oauth_user)
                if not oauth_user:
                    raise Exception("OAuth user creation failed")
                res = ManagementSerializer().response([user_management])
        except Exception as e:
            err = str(e)
            return BaseResponse(True, err, None).res()

        if flag:
            return BaseResponse(
                False,
                "User created successfully but your intra username is already exist."
                "Please update your username",
                res
            ).res()
        return BaseResponse(False, "User created successfully", res).res()
