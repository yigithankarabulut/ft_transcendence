from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tournament/(?P<room_name>\w+)/$', consumers.Tournament.as_asgi()),
]
