from abc import ABC, abstractmethod
from .repository import IQuickPlayRepository, IMatchRepository
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
    def get_by_id(self, request):
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

    def get_by_id(self, request):
        return self.repository.get_by_id(request)

    def leave(self, request):
        pass

    def match(self, request):
        pass


class IMatchService(ABC):
    @abstractmethod
    def create(self, request):
        pass

    @abstractmethod
    def save_state(self, request):
        pass
    
    @abstractmethod
    def get_by_id(self, request):
        pass

    @abstractmethod
    def add_player(self, request):
        pass


class MatchService(IMatchService):
    def __init__(self, repository: IMatchRepository):
        self.repository = repository

    def create(self, request):
        pass

    def save_state(self, request):
        pass

    def get_by_id(self, request):
        pass

    def add_player(self, request):
        pass