from django.urls import path, include

urlpatterns = [
    path('game/', include('src.urls')),
]
