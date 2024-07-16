from django.urls import path, include

urlpatterns = [
    path('friends/', include('srcs.urls')),
]
