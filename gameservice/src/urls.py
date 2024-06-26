from django.urls import path
from .views import GameHandler

urlpatterns = [
    path('room', GameHandler.as_view({'post': 'create_room'})),
    path('update', GameHandler.as_view({'post': 'update_game'})),

]
