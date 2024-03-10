from django.urls import path, include
from .views import GamePlayHandler, TournamentHandler


tournamenturls = [
    path('create', TournamentHandler.as_view({'post': 'create'}), name='create'),
    path('invite', TournamentHandler.as_view({'post': 'invite'}), name='invite'),
    path('join', TournamentHandler.as_view({'post': 'join'}), name='join'),
    path('participants', TournamentHandler.as_view({'get': 'participants'}), name='participants'),
    path('start', TournamentHandler.as_view({'post': 'start'}), name='start'),
    path('details', TournamentHandler.as_view({'get': 'tournament_details'}), name='details'),
    path('play', TournamentHandler.as_view({'post': 'play'}), name='play'),
    path('update', TournamentHandler.as_view({'put': 'update'}), name='update'),
]


matchurls = [
    path('join', GamePlayHandler.as_view({'post': 'join'}), name='join'),
    path('cancel', GamePlayHandler.as_view({'post': 'cancel'}), name='leave'),
    path('check', GamePlayHandler.as_view({'get': 'check'}), name='check'),
    path('check-in', GamePlayHandler.as_view({'post': 'check_in'}), name='check-in'),
    path('start_match', GamePlayHandler.as_view({'post': 'start_match'}), name='start_match'),
    path('match_details', GamePlayHandler.as_view({'get': 'match_details'}), name='match_details'),
    path('match/update', GamePlayHandler.as_view({'put': 'update'}), name='update'),
]

urlpatterns = [
    path('match/', include(matchurls)),
    path('tournament/', include(tournamenturls)),
]

# path('api/tournaments/search/', TournamentSearchView.as_view(), name='tournament-search'),
# path('api/tournaments/', TournamentListView.as_view(), name='tournament-list'),
# path('api/tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),
# path('api/tournaments/create/', TournamentCreateView.as_view(), name='tournament-create'),
# path('api/tournaments/<int:pk>/update/', TournamentUpdateView.as_view(), name='tournament-update'),
# path('api/tournaments/<int:pk>/delete/', TournamentDeleteView.as_view(), name='tournament-delete'),
# path('api/tournaments/<int:pk>/participants/', ParticipantListView.as_view(), name='participant-list'),
# path('api/tournaments/<int:pk>/participants/add/', ParticipantCreateView.as_view(), name='participant-create'),
# path('api/tournaments/<int:pk>/participants/<int:player_id>/delete/', ParticipantDeleteView.as_view(), name='participant-delete'),
# path('api/tournaments/<int:pk>/winner/', WinnerSetView.as_view(), name='winner-set'),