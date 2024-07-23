# Generated by Django 5.0.7 on 2024-07-23 06:47

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserManagement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('username', models.CharField(max_length=20, null=True, unique=True)),
                ('password', models.CharField(max_length=128, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('oauth_users', models.IntegerField(default=0)),
                ('email_verified', models.BooleanField(default=False)),
                ('twofa_code', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('email_verify_token', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('reset_password_token', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OAuthUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('provider', models.CharField(max_length=100)),
                ('provider_user_id', models.CharField(max_length=100)),
                ('access_token', models.CharField(max_length=100)),
                ('refresh_token', models.CharField(max_length=100)),
                ('expires_in', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.usermanagement')),
            ],
        ),
    ]
