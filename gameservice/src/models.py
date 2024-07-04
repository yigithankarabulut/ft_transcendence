from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    room_limit = models.IntegerField(default=2)  # room_limit


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)  # 0 = Waiting, 1 = Playing, 2 = Finished
    player1 = models.CharField(max_length=100) # player1 (user_id)
    player2 = models.CharField(max_length=100) # player2 (user_id)
    player1_score = models.IntegerField(default=0) # player1_score
    player2_score = models.IntegerField(default=0) # player2_score
    winner = models.CharField(max_length=100, blank=True, null=True)  # winner (user_id)
    loser = models.CharField(max_length=100, blank=True, null=True)  # loser (user_id)


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='players')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user_id = models.CharField(max_length=100)
    is_owner = models.BooleanField(default=False)
