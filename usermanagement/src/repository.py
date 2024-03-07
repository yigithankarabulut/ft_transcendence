from abc import ABC, abstractmethod
from .models import UserManagement, OAuthUser

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
    def delete(self, id: int)-> bool:
        pass


class UserManagementRepository(IUserManagementRepository):
    def get(self, id: int) -> UserManagement:
        try:
            model = UserManagement.objects.filter(id=id).first()
            return model
        except:
            return None            
    
    def get_by_username(self, username: str) -> UserManagement:
        try:
            model = UserManagement.objects.filter(username=username).first()
            return model
        except:
            return None

    def get_by_email(self, email: str) -> UserManagement:
        try:
            model = UserManagement.objects.filter(email=email).first()
            return model
        except:
            return None

    def create(self, user: UserManagement) -> UserManagement:
        try:
            user.save()
            return user
        except:
            return None

    def update(self, user: UserManagement) -> UserManagement:
        try:
            user.save()
            return user
        except Exception as e:
            print(e)
            return None

    def list(self) -> list:
        return UserManagement.objects.all()

    def delete(self, id: int) -> bool:
        try:
            model = UserManagement.objects.filter(id=id).first()
            model.delete()
            return True
        except:
            return False


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

class OAuthUserRepository(IOAuthUserRepository):
    def oauth_user_create(self, req: OAuthUser) -> OAuthUser:
        try:
            req.save()
            return req
        except:
            return None

    def get_oauth_user_with_provider_and_provider_user_id(self, provider: str, provider_user_id: str) -> OAuthUser:
        try:
            model = OAuthUser.objects.filter(provider=provider, provider_user_id=provider_user_id).first()
            return model
        except:
            return None

    def get_oauth_user_by_id(self, user_id: int) -> OAuthUser:
        try:
            model = OAuthUser.objects.filter(id=user_id).first()
            return model
        except:
            return None

    def update_oauth_user(self, oauth_user: OAuthUser) -> OAuthUser:
        try:
            oauth_user.save()
            return oauth_user
        except:
            return None

    def delete_oauth_user(self, id: int) -> bool:
        try:
            model = OAuthUser.objects.filter(id=id).first()
            model.delete()
            return True
        except:
            return False