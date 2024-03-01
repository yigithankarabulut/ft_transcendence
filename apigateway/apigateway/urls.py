from django.urls import re_path

from src.views import APIGatewayView

urlpatterns = [
    re_path(r'^(?P<path>.*)$', APIGatewayView.as_view()),
]