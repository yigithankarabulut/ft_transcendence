from abc import ABC, abstractmethod
from src.models import UserManagement, OAuthUser
from src.utils import BaseResponse

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

    @abstractmethod
    def register(self, user: UserManagement) -> BaseResponse:
        pass

    @abstractmethod
    def login(self, req: UserManagement) -> BaseResponse:
        pass

    @abstractmethod
    def forgot_password(self, email) -> BaseResponse:
        pass

    @abstractmethod
    def change_password(self, req: UserManagement) -> BaseResponse:
        pass
    
    @abstractmethod
    def reset_password(self, req, uidb64, token) -> BaseResponse:
        pass

    @abstractmethod
    def oauth_user_create(self, user_management: UserManagement, oauth_user: OAuthUser) -> BaseResponse:
        pass

