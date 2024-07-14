from abc import ABC, abstractmethod
import logging
from .repository import IFriendsRepository
from django.core.paginator import Paginator
from .serializers import FriendsSerializer, FriendReqListSerializer


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
    def add_friend(self, sender_id, receiver_id) -> BaseResponse:
        pass

    @abstractmethod
    def delete_friend(self, sender_id, receiver_id) -> BaseResponse:
        pass

    @abstractmethod
    def accept_request(self, sender_id, receiver_id) -> BaseResponse:
        pass

    @abstractmethod
    def reject_request(self, sender_id, receiver_id) -> BaseResponse:
        pass

    @abstractmethod
    def get_requests(self, user_id, page, limit) -> BaseResponse:
        pass

    @abstractmethod
    def get_friends(self, user_id, page, limit) -> BaseResponse:
        pass


class FriendsService(IFriendsService):
    def __init__(self, repository: IFriendsRepository):
        self.repository = repository

    def add_friend(self, sender_id, receiver_id) -> BaseResponse:
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

    def delete_friend(self, sender_id, receiver_id) -> BaseResponse:
        fr = self.repository.get_double(sender_id, receiver_id)
        if not fr:
            return BaseResponse(True, "Friendship not found", None).res()
        if fr.state != 1:
            return BaseResponse(True, "Friendship not accepted", None).res()
        if not self.repository.delete(sender_id, receiver_id):
            return BaseResponse(True, "Failed to delete friendship", None).res()
        return BaseResponse(False, "Friendship deleted successfully", None).res()

    def accept_request(self, sender_id, receiver_id) -> BaseResponse:
        fr = self.repository.get_double(sender_id, receiver_id)
        if not fr:
            return BaseResponse(True, "Friendship not found", None).res()
        if fr.state != 0:
            return BaseResponse(True, "Friendship not requested", None).res()
        flag = self.repository.accept(fr.sender_id, fr.receiver_id)
        if flag is False:
            return BaseResponse(True, "Failed to accept friendship", None).res()
        return BaseResponse(False, "Friendship accepted successfully", None).res()

    def reject_request(self, sender_id, receiver_id) -> BaseResponse:
        fr = self.repository.get_double(sender_id, receiver_id)
        if not fr:
            return BaseResponse(True, "Friendship not found", None).res()
        if fr.state != 0:
            return BaseResponse(True, "Friendship not requested", None).res()
        flag = self.repository.reject(fr.sender_id, fr.receiver_id)
        if flag is False:
            return BaseResponse(True, "Failed to reject friendship", None).res()
        return BaseResponse(False, "Friendship rejected successfully", None).res()

    def get_requests(self, user_id, page, limit) -> BaseResponse:
        requests = self.repository.get_all_request(user_id)
        if requests is None:
            return BaseResponse(True, "Failed to get friend requests", None).res()
        paginator = Paginator(requests, limit)
        try:
            requests = paginator.page(page)
        except Exception as e:
            if e is Exception.EmptyPage:
                return BaseResponse(False, "No friend requests found in this page", None).res()
            return BaseResponse(True, "Failed to get friend requests", None).res()
        if not requests:
            return BaseResponse(False, "No friend requests found", None).res()
        res = FriendReqListSerializer.response(requests)
        paginate_data = {
            "current_page": page,
            "page_size": limit,
            "total_pages": paginator.num_pages,
            "total_records": paginator.count
        }
        return BaseResponse(False, "Friend requests found", res, paginate_data).res()

    def get_friends(self, user_id, page, limit) -> BaseResponse:
        friends = self.repository.get_all_friends(user_id)
        if friends is None:
            return BaseResponse(True, "Failed to get friends", None).res()
        paginator = Paginator(friends, limit)
        try:
            friends = paginator.page(page)
        except Exception as e:
            if e is Exception.EmptyPage:
                return BaseResponse(False, "No friends found in this page", None).res()
            return BaseResponse(True, "Failed to get friends", None).res()
        if not friends:
            return BaseResponse(False, "No friends found", None).res()
        res = FriendsSerializer.response(friends)
        paginate_data = {
            "current_page": page,
            "page_size": limit,
            "total_pages": paginator.num_pages,
            "total_records": paginator.count
        }
        return BaseResponse(False, "Friends found", res, paginate_data).res()
