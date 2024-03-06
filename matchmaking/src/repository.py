from abc import ABC, abstractmethod
from .models import Player

class IQuickPlayRepository(ABC):
    @abstractmethod
    def insert(self, player: Player):
        pass

    def get_by_id(self, request):
        pass

    @abstractmethod
    def leave(self, request):
        pass

    @abstractmethod
    def match(self, request):
        pass


class QuickPlayRepository(IQuickPlayRepository):
    def insert(self, player: Player):
        pass

    def get_by_id(self, request):
        try:
            return Player.objects.get(id=request)
        except Player.DoesNotExist:
            return None

    def leave(self, request):
        pass

    def match(self, request):
        pass


class IMatchRepository(ABC):
    @abstractmethod
    def insert(self, match):
        pass

    @abstractmethod
    def get_by_id(self, request):
        pass

    @abstractmethod
    def save_state(self, request):
        pass

    @abstractmethod
    def add_player(self, request):
        pass

class MatchRepository(IMatchRepository):
    def insert(self, match):
        pass

    def get_by_id(self, request):
        pass

    def save_state(self, request):
        pass

    def add_player(self, request):
        pass