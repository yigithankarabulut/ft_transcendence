from django.urls import path
from rest_framework import viewsets
from .views import AuthHandler

urlpatterns = [
    path('token', AuthHandler.as_view({'post': 'generate_token'})),
    path('token/validate', AuthHandler.as_view({'post': 'validate_token'})),
    path('token/refresh', AuthHandler.as_view({'post': 'refresh_token'})),
]
