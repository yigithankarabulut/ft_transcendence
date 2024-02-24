from abc import ABC, abstractmethod
from .repository import IFriendsRepository

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


class IFriendsService(ABC):
    @abstractmethod
    def add_friend(self, sender_id: int, receiver_id: int) -> BaseResponse:
        pass

    @abstractmethod
    def delete_friend(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def accept_request(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def reject_request(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def get_friends(self, user_id: int):
        pass

class FriendsService(IFriendsService):
    def __init__(self, repository: IFriendsRepository):
        self.repository = repository
    def add_friend(self, sender_id: int, receiver_id: int) -> BaseResponse:
        if sender_id == receiver_id:
            return BaseResponse(True, "Cannot add yourself as a friend", None).res()

        friendship = self.repository.get_double(sender_id, receiver_id)
        if friendship:
            print(friendship.deleted_at)
            match friendship.state:
                case 0:
                    return BaseResponse(True, "Friend request already sent", None).res()
                case 1:
                    return BaseResponse(True, "Already friends with this user", None).res()
                case 2:
                    if not self.repository.set_state(sender_id, receiver_id, 0):
                        return BaseResponse(True, "Failed to update friend request status", None).res()
                    return BaseResponse(False, "Friend request sent successfully", None).res()
                case _:
                    return BaseResponse(True, "Failed to process friend request", None).res()

        if not self.repository.insert(sender_id, receiver_id):
            return BaseResponse(True, "Failed to send friend request", None).res()

        return BaseResponse(False, "Friend request sent successfully", None).res()
    
    def delete_friend(self, sender_id: int, receiver_id: int):
        fr = self.repository.get_double(sender_id, receiver_id)
        if not fr:
            return BaseResponse(True, "Friendship not found", None).res()
        if fr.state != 1:
            return BaseResponse(True, "Friendship not accepted", None).res()
        if not self.repository.delete(sender_id, receiver_id):
            return BaseResponse(True, "Failed to delete friendship", None).res()
        return BaseResponse(False, "Friendship deleted successfully", None).res()
        

    def accept_request(self, sender_id: int, receiver_id: int):
        fr = self.repository.get_double(sender_id, receiver_id)
        if not fr:
            return BaseResponse(True, "Friendship not found", None).res()
        if fr.state != 0:
            return BaseResponse(True, "Friendship not requested", None).res()
        if not self.repository.accept(sender_id, receiver_id):
            return BaseResponse(True, "Failed to accept friendship", None).res()
        return BaseResponse(False, "Friendship accepted successfully", None).res()
        

    def reject_request(self, sender_id: int, receiver_id: int):
        pass

    def get_friends(self, user_id: int):
        pass
