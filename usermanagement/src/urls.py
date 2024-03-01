from django.urls import path
from .views import UserManagementHandler, AuthHandler

urlpatterns = [
    path('details', UserManagementHandler.as_view({'get': 'get_user'})),
    path('update', UserManagementHandler.as_view({'put': 'update_user'})),
    path('delete', UserManagementHandler.as_view({'delete': 'delete_user'})),
    path('list', UserManagementHandler.as_view({'get': 'list_user'})),

    path('register', AuthHandler.as_view({'post': 'register'})),
    path('login', AuthHandler.as_view({'post': 'login'})),
    path('pwd/forgot', AuthHandler.as_view({'post': 'forgot_password'})),
    path('pwd/change', AuthHandler.as_view({'post': 'change_password'})),
]

# login_urlpatterns = [
#     path('register', AuthHandler.as_view({'post': 'register'})),
#     path('login', AuthHandler.as_view({'post': 'login'})),
#     path('pwd/forgot', AuthHandler.as_view({'post': 'forgot_password'})),
#     path('pwd/change', AuthHandler.as_view({'post': 'change_password'})),
# ]
