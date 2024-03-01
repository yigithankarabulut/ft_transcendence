from django.urls import path, include
# from src.urls import login_urlpatterns

urlpatterns = [
    path('user/', include('src.urls')),
    # path('/', include(login_urlpatterns)),
]
