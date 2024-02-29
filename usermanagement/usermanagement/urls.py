from django.urls import path, include
from src.urls import login_urlpatterns

urlpatterns = [
    path('user/', include('srcs.urls')),
    path('/', include(login_urlpatterns)),
]
