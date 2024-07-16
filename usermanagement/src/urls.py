from django.urls import path
from .views import UserManagementHandler, AuthHandler


urlpatterns = [
    path('details', UserManagementHandler.as_view({'get': 'get_user'})),
    path('update', UserManagementHandler.as_view({'put': 'update_user'})),
    path('username', UserManagementHandler.as_view({'patch': 'update_username'})),
    path('get', UserManagementHandler.as_view({'get': 'get_user_by_username'})),
    path('get/id', UserManagementHandler.as_view({'get': 'get_user_by_id'})),
    path('delete', UserManagementHandler.as_view({'delete': 'delete_user'})),
    path('list', UserManagementHandler.as_view({'get': 'list_user'})),
    path('search', UserManagementHandler.as_view({'get': 'search_user'})),
    path('pwd/update', AuthHandler.as_view({'post': 'change_password'})),

    path('login', AuthHandler.as_view({'post': 'login'})),
    path('2fa', AuthHandler.as_view({'post': 'two_factor_auth'})),

    path('register', AuthHandler.as_view({'post': 'register'})),
    path('oauth/create', AuthHandler.as_view({'post': 'oauth_user_create'})),

    path('pwd/forgot', AuthHandler.as_view({'post': 'forgot_password'})),
    path('reset-password/<uidb64>/<token>/', AuthHandler.as_view({'get': 'redirect_reset_password'}), name='reset_password'),
    path('pwd/change/<uidb64>/<token>/', AuthHandler.as_view({'post': 'reset_password'}), name='change_password'),
    path('email_verify/<uidb64>/<token>/', AuthHandler.as_view({'get': 'email_verify'}), name='email_verify'),
]
