import uuid
from django.db import models

class UserManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    username = models.CharField(null=True, max_length=20, unique=True)
    password = models.CharField(null=True, max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100)
    oauth_users = models.IntegerField(default=0)


class OAuthUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserManagement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    provider = models.CharField(max_length=100)
    provider_user_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    expires_in = models.DateTimeField()
