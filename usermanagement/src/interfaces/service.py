from abc import ABC, abstractmethod
from ..models import UserManagement, OAuthUser
from ..utils import BaseResponse


class IUserManagementService(ABC):

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def register(self, user: UserManagement) -> BaseResponse:
        pass

    @abstractmethod
    def update(self, user, id) -> BaseResponse:
        pass

    @abstractmethod
    def list(self, page, limit) -> BaseResponse:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> BaseResponse:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> BaseResponse:
        pass

    @abstractmethod
    def delete(self, id: int) -> BaseResponse:
        pass

    @abstractmethod
    def register(self, user: UserManagement) -> BaseResponse:
        pass

    @abstractmethod
    def login(self, req: UserManagement) -> BaseResponse:
        pass

    @abstractmethod
    def two_factor_auth(self, req: UserManagement) -> BaseResponse:
        pass

    @abstractmethod
    def forgot_password(self, email) -> BaseResponse:
        pass

    @abstractmethod
    def change_password(self, req, id) -> BaseResponse:
        pass
    
    @abstractmethod
    def reset_password(self, req, uidb64, token) -> BaseResponse:
        pass

    @abstractmethod
    def email_verify(self, req, uid, token) -> BaseResponse:
        pass

    @abstractmethod
    def oauth_user_create(self, user_management: UserManagement, oauth_user: OAuthUser) -> BaseResponse:
        pass
