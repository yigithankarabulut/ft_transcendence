from django.urls import path
from .views import FriendsHandler

urlpatterns = [
    path('add', FriendsHandler.as_view({'post': 'add'})),
    path('accept', FriendsHandler.as_view({'post': 'accept'})),
    path('reject', FriendsHandler.as_view({'delete': 'reject'})),
    path('request', FriendsHandler.as_view({'get': 'request'})),
    path('list', FriendsHandler.as_view({'get': 'list'})),
    path('delete', FriendsHandler.as_view({'delete': 'delete'})),
]

