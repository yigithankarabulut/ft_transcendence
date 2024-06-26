import uuid
from django.db import models


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    games = models.ManyToManyField('Game', related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    room_name = models.CharField(max_length=100)  # room_name
    room_limit = models.IntegerField(default=2)  # size of the room (2/4 players)
    room_owner = models.CharField(max_length=100)  # room_owner (user_id)


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)  # 0 = Waiting, 1 = Playing, 2 = Finished
    player1 = models.CharField(max_length=100) # player1 (user_id)
    player2 = models.CharField(max_length=100) # player2 (user_id)
    player1_score = models.IntegerField(default=0) # player1_score
    player2_score = models.IntegerField(default=0) # player2_score
    # **
    player1_ready = models.BooleanField(default=False) # player1_ready
    player2_ready = models.BooleanField(default=False) # player2_ready
    # **
    winner = models.CharField(max_length=100)  # winner (user_id)
    loser = models.CharField(max_length=100)  # loser (user_id)

