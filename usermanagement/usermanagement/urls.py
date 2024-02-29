from django.urls import path, include
from srcs.urls import auth_urlpatterns

urlpatterns = [
    path('user/', include('srcs.urls')),
    path('auth/', include(auth_urlpatterns)),
]
