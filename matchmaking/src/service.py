from abc import ABC, abstractmethod
from .serializers import GameFoundedSerializer, MatchSerializer

from .repository import IPlayerRepository, IMatchRepository
from .publisher import PublisherBase
from .models import Player, Match

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


class IGamePlayService(ABC):
    @abstractmethod
    def join_game(self, user_id: int, username: str):
        pass

    @abstractmethod
    def start_match(self, player1, player2):
        pass

    @abstractmethod
    def is_game_found(self, player_id: int):
        pass

    @abstractmethod
    def get_match_details(self, match_id):
        pass

    @abstractmethod
    def check_in(self, match_id, player_id):
        pass

class GamePlayService(IGamePlayService):
    def __init__(self, player_repository: IPlayerRepository, match_repository: IMatchRepository):
        self.player_repository = player_repository
        self.match_repository = match_repository

    def join_game(self, user_id: int, username: str):
        player = self.player_repository.get_by_user_id(user_id)
        if not player:
            player = self.player_repository.create(user_id, username)
            if not player:
                return True, "Error creating player"
        if player.is_playing != 0:
            return True, "Already in queue or in match"
        message = {
            'subject': 'Matchmaking',
            'body': {'id': player.id, 'user_id': int(player.user_id), 'username': player.username},
            'type': 'matchmaking'
        }
        publisher = PublisherBase('matchmaking')
        res = publisher.publish_message(message)
        if not res:
            return BaseResponse(True, "Matchmaking failed", None).res()
        err = self.player_repository.set_state_by_user_id(player.user_id, 1)
        if err:
            return BaseResponse(True, "Error setting state", None).res()
        publisher.close_connection()
        return BaseResponse(False, "Matchmaking started", None).res()

    def start_match(self, player1, player2):
        p1 = Player(id=player1['id'], user_id=player1['user_id'], username=player1['username'])
        p2 = Player(id=player2['id'], user_id=player2['user_id'], username=player2['username'])
        match = self.match_repository.create(p1, p2, None)
        if match is None:
            return BaseResponse(True, "Error creating match", None).res()
        return BaseResponse(False, "Match started", None).res()

    def is_game_found(self, player_id: int):
        pk = self.player_repository.get_by_user_id(player_id).id
        match = self.match_repository.get_match_by_match_state_depends_on_id(pk)
        if match is None:
            return BaseResponse(True, "Still in queue", None).res()
        res = GameFoundedSerializer().response([match])
        return BaseResponse(False, "Match found", res).res()

    def get_match_details(self, match_id):
        match = self.match_repository.get_by_match_id(match_id)
        if match is None:
            return BaseResponse(True, "Match not found", None).res()
        res = MatchSerializer().response([match])
        return BaseResponse(False, "Match found", res).res()

    def check_in(self, match_id, player_id):
        match = self.match_repository.get_by_match_id(match_id)
        id = self.player_repository.get_by_user_id(player_id).id
        if match is None:
            return BaseResponse(True, "Match not found", None).res()
        if match.player1.id == id:
            match.player1_checkin = True
        elif match.player2.id == id:
            match.player2_checkin = True
        else:
            return BaseResponse(True, "Not in match", None).res()
        err = self.match_repository.update(match)
        if err:
            return BaseResponse(True, "Error updating match", None).res()
        return BaseResponse(False, "Checked in", None).res()

class ITournamentService(ABC):
    @abstractmethod
    def create_tournament(self, name, creater_id):
        pass

    @abstractmethod
    def invite_participant(self, tournament_id, creator_id, invited_user_id):
        pass

    @abstractmethod
    def join_tournament(self, tournament_id, user_id):
        pass

    @abstractmethod
    def start_tournament(self, tournament_id: int, creator_id: int):
        pass

    @abstractmethod
    def tournament_details(self, tournament_id):
        pass

    @abstractmethod
    def play_tournament_match(self, player1, player2, tournament_id):
        pass

    @abstractmethod
    def update_match(self, player1, player2, player1_score, player2_score, tournament_id, match_id):
        pass


from .repository import ITournamentRepository, ITournamentParticipantRepository, IPlayerRepository, IMatchRepository
from .serializers import TournamentSerializer
class TournamentService(ITournamentService):
    def __init__(self, player_repository: IPlayerRepository, match_repository: IMatchRepository, tournament_repository: ITournamentRepository, tournament_participant_repository: ITournamentParticipantRepository):
        self.player_repository = player_repository
        self.match_repository = match_repository
        self.tournament_repository = tournament_repository
        self.tournament_participant_repository = tournament_participant_repository

    def create_tournament(self, name, creator_id):
        player = self.player_repository.get_by_user_id(user_id=creator_id)
        if player is None:
            return BaseResponse(True, "Player not found", None).res()
        tournament = self.tournament_repository.create(name, player)
        if tournament is None:
            return BaseResponse(True, "Error creating tournament", None).res()
        err = self.tournament_participant_repository.create(player, tournament.id)
        if err:
            return BaseResponse(True, "Creating participant", None).res()
        err = self.tournament_repository.add_participant(tournament, player)
        if err:
            return BaseResponse(True, "Error adding participant", None).res()
        return BaseResponse(False, "Tournament created", None).res()

    def tournament_details(self, tournament_id):
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is None:
            return BaseResponse(True, "Tournament not found", None).res()
        participants = self.tournament_repository.get_participants(tournament_id)
        if participants is None:
            return BaseResponse(True, "Error getting participants", None).res()
        invites = self.tournament_repository.get_invites(tournament_id)
        if invites is False:
            return BaseResponse(True, "Error getting invites", None).res()
        res = {
            "tournament": TournamentSerializer().response([tournament]),
            "participants": participants,
            "invites": invites,
        }
        return BaseResponse(False, "Tournament details", res).res()

    def invite_participant(self, tournament_id, creator_id, invited_user_id):
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is None:
            return BaseResponse(True, "Tournament not found", None).res()
        player = self.player_repository.get_by_user_id(creator_id)
        if player is None:
            return BaseResponse(True, "Player not found", None).res()
        if tournament.creator != player:
            return BaseResponse(True, "Not creator", None).res()
        invited = self.player_repository.get_by_user_id(invited_user_id)
        if invited is None:
            return BaseResponse(True, "Invited player not found", None).res()
        err = self.tournament_repository.invite(tournament, invited)
        if err:
            return BaseResponse(True, "Error inviting player", None).res()
        return BaseResponse(False, "Invited player", None).res()


    def join_tournament(self, tournament_id, user_id):
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is None:
            return BaseResponse(True, "Tournament not found", None).res()
        player = self.player_repository.get_by_user_id(user_id)
        if player is None:
            return BaseResponse(True, "Player not found", None).res()
        if player in tournament.participants.all():
            return BaseResponse(True, "Already in tournament", None).res()
        if player not in tournament.invites.all():
            return BaseResponse(True, "Not invited", None).res()
        err = self.tournament_participant_repository.create(player, tournament.id)
        if err:
            return BaseResponse(True, "Error creating participant", None).res()
        err = self.tournament_repository.add_participant(tournament, player)
        if err:
            return BaseResponse(True, "Error adding participant", None).res()
        return BaseResponse(False, "Joined tournament", None).res()

    def start_tournament(self, tournament_id: int, creator_id: int):
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is None:
            return BaseResponse(True, "Tournament not found", None).res()
        creator = self.player_repository.get_by_user_id(creator_id)
        if creator is None:
            return BaseResponse(True, "Creator not found", None).res()
        if tournament.creator != creator:
            return BaseResponse(True, "Not creator", None).res()
        if tournament.participants.count() < 2:
            return BaseResponse(True, "Not enough participants", None).res()
        for participant in tournament.participants.all():
            message = {
                'subject': tournament.id,
                'body': {'id': participant.id, 'user_id': int(participant.user_id), 'username': participant.username},
                'type': 'tournament'
            }
            publisher = PublisherBase('matchmaking')
            res = publisher.publish_message(message)
            if not res:
                return BaseResponse(True, "Matchmaking failed", None).res()
            err = self.player_repository.set_state_by_user_id(participant.user_id, 1)
            if err:
                return BaseResponse(True, "Error setting state", None).res()
            publisher.close_connection()
        return BaseResponse(False, "Tournament started", None).res()

    def play_tournament_match(self, player1, player2, tournament_id):
        p1 = Player(id=player1['id'], user_id=player1['user_id'], username=player1['username'])
        p2 = Player(id=player2['id'], user_id=player2['user_id'], username=player2['username'])
        match = self.match_repository.create(p1, p2, tournament_id)
        if match is None:
            return BaseResponse(True, "Error creating match", None).res()
        return BaseResponse(False, "Match started", None).res()


    def update_match(self, player1, player2, player1_score, player2_score, tournament_id, match_id):
        match = self.match_repository.get_by_match_id(match_id)
        if match is None:
            return BaseResponse(True, "Match not found", None).res()
        match.player1_score = player1_score
        match.player2_score = player2_score
        if player1_score > player2_score:
            match.winner = match.player1
        else:
            match.winner = match.player2
        match.state = 2
        err = self.match_repository.update(match)
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if match is None:
            return BaseResponse(True, "Tournament not found", None).res()
        all_matches = self.match_repository.get_all_matches_with_tournament_id(tournament_id)
        print(all_matches)
        if all_matches is None:
            return BaseResponse(True, "Error getting matches", None).res()
        all_finished_matches = [m for m in all_matches if m.get('state') == 2]
        if len(all_finished_matches) == len(all_matches):
            return BaseResponse(False, "Tournament finished", None).res()
        print()
        message = {
            'subject': tournament.id,
            'body': {'id': match.winner.id, 'user_id': int(match.winner.user_id), 'username': match.winner.username},
            'type': 'tournament'
        }
        publisher = PublisherBase('matchmaking')
        res = publisher.publish_message(message)
        if not res:
            return BaseResponse(True, "Matchmaking failed", None).res()
        err = self.player_repository.set_state_by_user_id(match.winner.user_id, 1)
        if err:
            return BaseResponse(True, "Error setting state", None).res()
        publisher.close_connection()
        if err:
            return BaseResponse(True, "Error updating match", None).res()
        return BaseResponse(False, "Match updated", None).res()
