from django.urls import path
from .views import UserManagementHandler, AuthHandler

urlpatterns = [
    path('details', UserManagementHandler.as_view({'get': 'get_user'})),
    path('update', UserManagementHandler.as_view({'put': 'update_user'})),
    # TODO: Create endpoint update username. if intra login name is already exist.
    path('delete', UserManagementHandler.as_view({'delete': 'delete_user'})),
    path('list', UserManagementHandler.as_view({'get': 'list_user'})),
    path('pwd/change', AuthHandler.as_view({'post': 'change_password'})),
    
    path('login', AuthHandler.as_view({'post': 'login'})),
    path('register', AuthHandler.as_view({'post': 'register'})),
    path('pwd/forgot', AuthHandler.as_view({'post': 'forgot_password'})),
    path('oauth/create', AuthHandler.as_view({'post': 'oauth_user_create'})),

    # TODO: Frontend must receive the reset url we sent but now we send this url to queue.
    path('reset-password/<uidb64>/<token>/', AuthHandler.as_view({'post': 'reset_password'}), name='reset_password'),
]
