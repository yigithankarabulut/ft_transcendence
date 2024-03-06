from abc import ABC, abstractmethod
from .repository import IQuickPlayRepository
from .models import Player
from .publisher import PublisherBase

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


class IQuickPlayService(ABC):
    @abstractmethod
    def join(self, request):
        pass

    @abstractmethod
    def quick_play_match(self, player: Player):
        pass

    @abstractmethod
    def leave(self, request):
        pass

    @abstractmethod
    def match(self, request):
        pass


class QuickPlayService(IQuickPlayService):
    def __init__(self, repository: IQuickPlayRepository):
        self.repository = repository

    def join(self, player: Player):
        # TODO: CHECK PLAYERS IS EXIST IN USERMANAGEMENT SERVICE
        
        err = self.repository.insert(player)
        if err:
            return BaseResponse(True, "Quick Play failed", None).res()
        message = {
            'subject': 'QuickPlayJoin',
            'body': {
                'user_id': player.user_id,
                'username': player.username,
            },
            'type': 'QuickPlay'
        }
        publisher = PublisherBase('quickplay')
        res = publisher.publish_message(message)
        if not res:
            return BaseResponse(True, "Quick Play failed", None).res()
        publisher.close_connection()
        return BaseResponse(False, "Quick play matchmaking has started", None).res()

    def quick_play_match(self, player: Player):
        pass

    def leave(self, request):
        pass

    def match(self, request):
        pass