from abc import ABC, abstractmethod
from .models import Player

class IQuickPlayRepository(ABC):
    @abstractmethod
    def insert(self, player: Player):
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

    def leave(self, request):
        pass

    def match(self, request):
        pass