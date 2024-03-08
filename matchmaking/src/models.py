from django.db import models

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    match_id = models.IntegerField()
    match_state = False
    match_name = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    match_time = models.TimeField()
    match_location = models.CharField(max_length=100)
    match_players = models.ManyToManyField(Player)
