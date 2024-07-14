## game/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/status', consumers.Online.as_asgi()),
]
