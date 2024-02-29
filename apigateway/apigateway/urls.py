from django.urls import path
from src.views import APIGatewayViewSet

urlpatterns = [
    path('/', APIGatewayViewSet.as_view({'get': 'dispatch', 'post': 'dispatch', 'put': 'dispatch', 'delete': 'dispatch'})),
]
