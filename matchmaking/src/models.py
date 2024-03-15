from django.db import models


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100)
    # 0 - not playing, 1 - in queue, 2 - in match
    is_playing = models.IntegerField(default=0)


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(Player, through='TournamentParticipant', related_name='tournament_participants')
    invites = models.ManyToManyField(Player, related_name='tournament_invites', blank=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, related_name='tournament_winner')
    creator = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournament_creator', null=True, blank=True)

class TournamentParticipant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    # 0 - not started, 1 - started, 2 - finished
    state = models.IntegerField(default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, blank=True)
    player1 = models.ForeignKey(Player, related_name='player1_matches', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2_matches', on_delete=models.CASCADE)
    player1_checkin = models.BooleanField(default=False)
    player2_checkin = models.BooleanField(default=False)
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
