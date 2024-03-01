from django.urls import path, include

urlpatterns = [
    # apiview for mail service
    path('mail/', include('src.urls')),
]
