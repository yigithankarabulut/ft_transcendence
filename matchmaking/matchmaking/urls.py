from django.urls import path
from django.urls import include

urlpatterns = [
    path('matchmaking/', include('src.urls')),
]
