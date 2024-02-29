from abc import ABC, abstractmethod
from .models import UserManagement

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
