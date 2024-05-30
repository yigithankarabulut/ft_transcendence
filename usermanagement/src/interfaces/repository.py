from abc import ABC, abstractmethod
from ..models import UserManagement, OAuthUser


class IUserManagementRepository(ABC):

    @abstractmethod
    def get(self, id: int) -> UserManagement:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> UserManagement:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserManagement:
        pass

    @abstractmethod
    def create(self, user: UserManagement) -> UserManagement:
        pass

    @abstractmethod
    def update(self, user: UserManagement) -> UserManagement:
        pass

    @abstractmethod
    def list(self) -> list:
        pass

    @abstractmethod
    def search(self, key: str) -> list:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class IOAuthUserRepository(ABC):

    @abstractmethod
    def oauth_user_create(self, req: OAuthUser) -> OAuthUser:
        pass

    @abstractmethod
    def get_oauth_user_with_provider_and_provider_user_id(self, provider: str, provider_user_id: str) -> OAuthUser:
        pass

    @abstractmethod
    def get_oauth_user_by_id(self, user_id: int) -> OAuthUser:
        pass

    @abstractmethod
    def update_oauth_user(self, oauth_user: OAuthUser) -> OAuthUser:
        pass

    @abstractmethod
    def delete_oauth_user(self, id: int) -> bool:
        pass
