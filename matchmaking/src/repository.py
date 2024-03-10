from abc import ABC, abstractmethod
from .models import Player, Match


class IPlayerRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, username: str):
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def set_state_by_user_id(self, user_id: int, state: int):
        pass


class PlayerRepository(IPlayerRepository):
    def create(self, user_id: int, username: str):
        try:
            player = Player(user_id=user_id, username=username)
            player.save()
            return player
        except:
            return None

    def get_by_user_id(self, user_id: int):
        try:
            player = Player.objects.filter(user_id=user_id).first()
            return player
        except:
            return None

    def get_by_id(self, id: int):
        try:
            player = Player.objects.filter(id=id).first()
            return player
        except:
            return None

    def set_state_by_user_id(self, user_id: int, state: int):
        try:
            player = Player.objects.filter(user_id=user_id).first()
            player.is_playing = state
            player.save()
            return False
        except:
            return True


class IMatchRepository(ABC):
    @abstractmethod
    def create(self, player1: Player, player2: Player, tournament_id: int = None):
        pass

    @abstractmethod
    def update(self, match: Match):
        pass

    @abstractmethod
    def get_match_by_match_state_depends_on_id(self, id: int):
        pass

    @abstractmethod
    def get_all_by_player_id(self, player_id: int):
        pass

    @abstractmethod
    def get_by_match_id(self, match_id: int):
        pass


class MatchRepository(IMatchRepository):
    def create(self, player1: Player, player2: Player, tournament_id: int = None):
        try:
            match = Match(player1=player1, player2=player2, player1_score=0, player2_score=0, tournament_id=tournament_id)
            match.save()
            return match
        except:
            return None

    def update(self, match: Match):
        try:
            match.save()
            return False
        except:
            return True

    def get_match_by_match_state_depends_on_id(self, id: int):
        try:
            matches_for_player = Match.objects.filter(player1_id=id) | Match.objects.filter(player2_id=id)
            matches_with_state_0 = matches_for_player.filter(state=0).first()
            return matches_with_state_0
        except:
            return None

    def get_all_by_player_id(self, player_id: int):
        pass

    def get_by_match_id(self, match_id: int):
        try:
            match = Match.objects.filter(id=match_id).first()
            return match
        except:
            return None

from .models import Tournament
class ITournamentRepository(ABC):
    @abstractmethod
    def create(self, name: str, creator : Player):
        pass

    @abstractmethod
    def invite(self, tournament: Tournament, invited_player: Player):
        pass

    @abstractmethod
    def get_invites(self, tournament_id: int):
        pass

    @abstractmethod
    def get_by_id(self, tournament_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add_participant(self, tournament: Tournament, player_id: int):
        pass

    @abstractmethod
    def set_winner(self, tournament_id: int, player_id: int):
        pass

    @abstractmethod
    def get_participants(self, tournament_id: int):
        pass

    @abstractmethod
    def get_winner(self, tournament_id: int):
        pass

from .models import Tournament, TournamentParticipant

class TournamentRepository(ITournamentRepository):
    def create(self, name: str, creator: Player):
        try:
            tournament = Tournament(name=name, creator=creator)
            tournament.save()
            return tournament
        except Exception as e:
            return None

    def invite(self, tournament: Tournament, invited_player: Player):
        try:
            tournament.invites.add(invited_player)
            return False
        except:
            return True

    def get_invites(self, tournament_id: int):
        try:
            tournament = Tournament.objects.filter(id=tournament_id).first()
            invites = list(tournament.invites.all().values())
            return invites
        except:
            return False

    def get_by_id(self, tournament_id: int):
        try:
            tournament = Tournament.objects.filter(id=tournament_id).first()
            return tournament
        except:
            return None

    def get_all(self):
        pass

    def add_participant(self, tournament: Tournament, participant: TournamentParticipant):
        try:
            tournament.participants.add(participant)
            return False
        except:
            return True


    def set_winner(self, tournament_id: int, player_id: int):
        pass

    def get_participants(self, tournament_id: int):
        try:
            tournament = Tournament.objects.filter(id=tournament_id).first()
            participants = list(tournament.participants.all().values())
            print(participants)
            return participants
        except:
            return None

    def get_winner(self, tournament_id: int):
        pass


class ITournamentParticipantRepository(ABC):
    @abstractmethod
    def create(self, player_id: int, tournament_id: int):
        pass

    @abstractmethod
    def get_by_tournament_id(self, tournament_id: int):
        pass

    @abstractmethod
    def get_by_player_id(self, player_id: int):
        pass


class TournamentParticipantRepository(ITournamentParticipantRepository):
    def create(self, player_id: int, tournament_id: int):
        try:
            tournament_participant = TournamentParticipant(player_id=player_id, tournament_id=tournament_id)
            tournament_participant.save()
            return tournament_participant
        except:
            return None

    def get_by_tournament_id(self, tournament_id: int):
        pass

    def get_by_player_id(self, player_id: int):
        pass
