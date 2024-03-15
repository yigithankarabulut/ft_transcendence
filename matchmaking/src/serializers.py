from rest_framework import serializers


class JoinWithNameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class PlayerRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)

class MatchCreateSerializer(serializers.Serializer):
    player1 = PlayerRequestSerializer()
    player2 = PlayerRequestSerializer()

class TournamentMatchSerializer(serializers.Serializer):
    player1 = PlayerRequestSerializer()
    player2 = PlayerRequestSerializer()
    tournament_id = serializers.IntegerField()
    match_id = serializers.IntegerField()
    player1_score = serializers.IntegerField()
    player2_score = serializers.IntegerField()
class MatchByIdSerializer(serializers.Serializer):
    match_id = serializers.IntegerField()

class CrateTournamentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class TournamentByIdSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField()

class TournamentInviteSerializer(serializers.Serializer):
    invited_user_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()


class GameFoundedSerializer(serializers.Serializer):

    def single_representation(self, data):
        return {
            "match_id": data.id,
            "player1_id": data.player1.id,
            "player2_id": data.player2.id,
            "tournament_id": data.tournament,
        }
    def response(self, data):
        return [self.single_representation(i) for i in data]


class MatchSerializer(serializers.Serializer):
    def single_representation(self, data):
        return {
            "match_id": data.id,
            "player1_id": data.player1.id,
            "player2_id": data.player2.id,
            "player1_state": data.player1_checkin,
            "player2_state": data.player2_checkin,
            "player1_score": data.player1_score,
            "player2_score": data.player2_score,
            "tournament_id": data.tournament,
        }
    def response(self, data):
        return [self.single_representation(i) for i in data]

class TournamentSerializer(serializers.Serializer):
    def single_representation(self, data):
        return {
            "tournament_id": data.id,
            "name": data.name,
            "creator_id": data.creator.id,
        }
    def response(self, data):
        return [self.single_representation(i) for i in data]
