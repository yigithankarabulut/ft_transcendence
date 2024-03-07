import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

class OAuthUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    provider = models.CharField(max_length=100)
    provider_user_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    expires_in = models.DateTimeField()
    user = models.ForeignKey(UserManagement, on_delete=models.CASCADE, related_name='oauth_users')
