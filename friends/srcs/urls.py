from django.urls import path
from .views import FriendsHandler

routes = [
    ('add', 'post', 'add'),
    ('accept', 'post', 'accept'),
    ('reject', 'delete', 'reject'),
    ('request', 'get', 'request'),
    ('list', 'get', 'list'),
    ('delete', 'delete', 'delete'),
]

urlpatterns = [path(route, FriendsHandler.as_view({method: action})) for route, method, action in routes]

# POST    /friends/add
# POST    /friends/accept
# DELETE  /friends/reject
# GET     /friends/request
# GET     /friends/list
# DELETE  /friends/delete
