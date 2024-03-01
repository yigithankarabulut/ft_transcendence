from abc import ABC, abstractmethod
from .repository import IUserManagementRepository
from .models import UserManagement
from .serializers import ManagementSerializer
from usermanagement.settings import SERVICE_ROUTES
import requests
from django.core.paginator import Paginator, EmptyPage
from hashlib import sha256
from datetime import datetime, timedelta
from django.conf import settings


class BaseResponse:
    def __init__(self, err: bool, msg: str, data, pagination=None):
        self.err = err
        self.string = {"error": msg}
        self.data = {"message": msg, "data": data}
        self.pagination = pagination

    def res(self):
        if self.err:
            return self.string, self.err
        response_data = self.data
        if self.pagination:
            response_data['pagination'] = self.pagination
        return response_data, self.err


class IUserManagementService(ABC):
    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def register(self, user: UserManagement)-> BaseResponse:
        pass

    @abstractmethod
    def update(self, user: dict) -> BaseResponse:
        pass

    @abstractmethod
    def list(self, page, limit) -> BaseResponse:
        pass

    @abstractmethod
    def delete(self, id: int)-> BaseResponse:
        pass

    def register(self, user: UserManagement) -> BaseResponse:
        pass

    def login(self, req: UserManagement) -> BaseResponse:
        pass

    def forgot_password(self, req: UserManagement) -> BaseResponse:
        pass

    def change_password(self, req: UserManagement) -> BaseResponse:
        pass



class UserManagementService(IUserManagementService):
    def __init__(self, repository: IUserManagementRepository):
        self.repository = repository

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
        elif umail:
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

    def forgot_password(self, req: UserManagement) -> BaseResponse:
        # TODO: send email with a link to reset password
        pass
    
    def change_password(self, req) -> BaseResponse:
        user = self.repository.get_by_username(req.get("username"))
        if not user:
            return BaseResponse(True, "User not found", None).res()
        if user.password != sha256(req.get("old_password").encode()).hexdigest():
            return BaseResponse(True, "Invalid password", None).res()
        hashpwd = sha256(req.get("new_password").encode()).hexdigest()
        user.password = hashpwd
        res = self.repository.update(user)
        if not res:
            return BaseResponse(True, "Password change failed", None).res()
        return BaseResponse(False, "Password changed successfully", None).res()
