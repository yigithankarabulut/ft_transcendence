from rest_framework import viewsets, status
from rest_framework.response import Response
from .service import GamePlayService
from .repository import PlayerRepository, MatchRepository, TournamentParticipantRepository
from .serializers import JoinWithNameSerializer, MatchCreateSerializer, MatchByIdSerializer, TournamentByIdSerializer

def get_user_id(request):
    return request.headers.get('id')


class GamePlayHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = GamePlayService(player_repository=PlayerRepository(), match_repository=MatchRepository())

    def join(self, request):
        serializer = JoinWithNameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data['username']
        id = get_user_id(request)
        if not id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        res, err = self.service.join_game(id, username)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def cancel(self, request):
        return Response(self.service.cancel(request.data), status=status.HTTP_200_OK)

    def check(self, request):
        id = get_user_id(request)
        if not id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        res, err = self.service.is_game_found(id)
        if err:
            return Response(res, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_200_OK)

    def check_in(self, request):
        serializer = MatchByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        match_id = serializer.validated_data['match_id']
        id = get_user_id(request)
        if not id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        res, err = self.service.check_in(match_id, id)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def start_match(self, request):
        serializer = MatchCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        p1, p2 = serializer.validated_data['player1'], serializer.validated_data['player2']
        res, err = self.service.start_match(p1, p2)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def match_details(self, request):
        serializer = MatchByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        match_id = serializer.validated_data['match_id']
        res, err = self.service.get_match_details(match_id)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def update(self, request):
        return Response(self.service.update(request.data), status=status.HTTP_200_OK)

from .service import TournamentService
from .repository import TournamentRepository
from .serializers import CrateTournamentSerializer, TournamentInviteSerializer, TournamentMatchSerializer

class TournamentHandler(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TournamentService(tournament_repository=TournamentRepository(), player_repository=PlayerRepository(), match_repository=MatchRepository(), tournament_participant_repository=TournamentParticipantRepository())

    def create(self, request):
        serializer = CrateTournamentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        id = get_user_id(request)
        if not id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        res, err = self.service.create_tournament(serializer.validated_data['name'], id)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def join(self, request):
        serializer = TournamentByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        id = get_user_id(request)
        if not id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        res, err = self.service.join_tournament(serializer.validated_data['tournament_id'], id)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def tournament_details(self, request):
        serializer = TournamentByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        res, err = self.service.tournament_details(serializer.validated_data['tournament_id'])
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def invite(self, request):
        serializer = TournamentInviteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        creator_id = get_user_id(request)
        if not creator_id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        res, err = self.service.invite_participant(serializer.validated_data['tournament_id'], creator_id, serializer.validated_data['invited_user_id'])
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def start(self, request):
        serializer = TournamentByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        creator_id = get_user_id(request)
        if not creator_id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        res, err = self.service.start_tournament(serializer.validated_data['tournament_id'], creator_id)
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def play(self, request):
        serializer = TournamentMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        p1, p2 = serializer.validated_data['player1'], serializer.validated_data['player2']
        res, err = self.service.play_tournament_match(p1, p2, serializer.validated_data['tournament_id'])
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"","ok"}, status=status.HTTP_200_OK)

    def update(self, request):
        serializer = TournamentMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        p1, p2 = serializer.validated_data['player1'], serializer.validated_data['player2']
        p1_score, p2_score = serializer.validated_data['player1_score'], serializer.validated_data['player2_score']
        res, err = self.service.update_match(p1, p2, p1_score, p2_score, serializer.validated_data['tournament_id'], serializer.validated_data['match_id'])
        if err:
            return Response({"error": res}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"","ok"}, status=status.HTTP_200_OK)
