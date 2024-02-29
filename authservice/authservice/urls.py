from django.urls import path, include
from src.urls import urlpatterns

urlpatterns = [
    path('auth/', include('src.urls')),
]
