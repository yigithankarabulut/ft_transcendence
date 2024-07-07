from django.urls import path
from .views import GameHandler

urlpatterns = [
    path('room', GameHandler.as_view({'post': 'create_room'})),
    path('update', GameHandler.as_view({'put': 'update_game'})),
    path('join', GameHandler.as_view({'post': 'join_room'})),
    path('list', GameHandler.as_view({'get': 'list_invite'})),
    path('history', GameHandler.as_view({'get': 'list_history'})),
    path('check', GameHandler.as_view({'get': 'check_game'}))
]