from abc import ABC, abstractmethod
from .models import Friends


class IFriendsRepository(ABC):
    @abstractmethod
    def insert(self, sender_id, receiver_id):
        pass

    @abstractmethod
    def delete(self, sender_id, receiver_id):
        pass

    @abstractmethod
    def accept(self, sender_id, receiver_id):
        pass

    @abstractmethod
    def reject(self, sender_id, receiver_id):
        pass

    @abstractmethod
    def get(self, sender_id, receiver_id):
        pass

    @abstractmethod
    def get_all_friends(self, user_id):
        pass

    @abstractmethod
    def get_all_request(self, user_id):
        pass

    @abstractmethod
    def set_state(self, sender_id, receiver_id, state):
        pass

    @abstractmethod
    def get_double(self, sender_id, receiver_id):
        pass

    @abstractmethod
    def get_state_by_id(self, owner_id, friend_id):
        pass


class FriendsRepository(IFriendsRepository):
    def insert(self, sender_id, receiver_id):
        try:
            if Friends.objects.create(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None, state=0):
                return True
        except:
            return False
        return False

    def delete(self, sender_id, receiver_id):
        try:
            fr = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).first()
            if fr is None:
                return False
            fr.soft_delete()
        except:
            return False
        return True

    def accept(self, sender_id, receiver_id):
        try:
            if Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).update(state=1):
                return True
        except:
            return False
        return False

    def reject(self, sender_id, receiver_id):
        try:
            fr = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).first()
            if fr is None:
                return False
            fr.soft_delete()
        except:
            return False
        return True

    def get(self, sender_id, receiver_id):
        try:
            fr = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id).first()
            if not fr:
                return False
        except:
            return False
        return True

    def get_all_friends(self, user_id):
        try:
            senders = Friends.objects.filter(sender_id=user_id, state=1, deleted_at=None).values('receiver_id')
            receivers = Friends.objects.filter(receiver_id=user_id, state=1, deleted_at=None).values('sender_id')
        except:
            return set()
        return senders.union(receivers)

    def get_all_request(self, user_id):
        try:
            res = Friends.objects.filter(receiver_id=user_id, state=0, deleted_at=None).all().values('sender_id')
        except:
            return ""
        res = res.order_by('-created_at')
        return res

    def set_state(self, sender_id, receiver_id, state):
        try:
            if Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id).update(state=state):
                return True
        except:
            return False
        return False

    def get_double(self, sender_id, receiver_id):
        try:
            fr1 = Friends.objects.filter(sender_id=sender_id, receiver_id=receiver_id, deleted_at=None).first()
            fr2 = Friends.objects.filter(sender_id=receiver_id, receiver_id=sender_id, deleted_at=None).first()
        except:
            return None
        if fr1:
            return fr1
        if fr2:
            return fr2
        return None

    def get_state_by_id(self, owner_id, friend_id):
        try:
            fr = Friends.objects.filter(sender_id=owner_id, receiver_id=friend_id).first()
            fr2 = Friends.objects.filter(sender_id=friend_id, receiver_id=owner_id).first()
        except:
            return -1
        if fr:
            return fr.state
        if fr2:
            return fr2.state
        return 5
