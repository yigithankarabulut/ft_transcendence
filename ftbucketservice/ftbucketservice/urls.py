from django.urls import path, include

urlpatterns = [
    path('bucket/', include('src.urls')),
]
