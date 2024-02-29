from abc import ABC, abstractmethod
from .models import Friends


class IFriendsRepository(ABC):
    @abstractmethod
    def insert(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def delete(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def accept(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def reject(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def get(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def get_all_friends(self, user_id: int):
        pass

    @abstractmethod
    def get_all_request(self, user_id: int):
        pass

    @abstractmethod
    def set_state(self, sender_id: int, receiver_id: int, state: int):
        pass

    @abstractmethod
    def get_double(self, sender_id: int, receiver_id: int):
        pass


class FriendsRepository(IFriendsRepository):
    def insert(self, sender_id: int, receiver_id: int):
        if Friends.objects.create(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None, state=0):
            return True
        return False
        
    def delete(self, sender_id: int, receiver_id: int):
        fr = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).first()
        if fr is None:
            return False
        fr.soft_delete()
        return True

    def accept(self, sender_id: int, receiver_id: int):
        if Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).update(state=1):
            return True
        return False

    def reject(self, sender_id: int, receiver_id: int):
        pass

    def get(self, sender_id: int, receiver_id: int):
        fr = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id).first()
        if not fr:
            return False 
        return True
        
    def get_all_friends(self, user_id: int):
        pass

    def get_all_request(self, user_id: int):
        pass

    def set_state(self, sender_id: int, receiver_id: int, state: int):
        if Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id).update(state=state):
            return True
        return False

    def get_double(self, sender_id: int, receiver_id: int):
        fr1 = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).first()
        fr2 = Friends.objects.filter(sender_id=receiver_id, receiver_id=sender_id, deleted_at=None).first()
        if fr1:
            return fr1
        if fr2:
            return fr2
        return None
