from django.urls import path
from .views import QuickPlayHandlers


urlpatterns = [
    path('join', QuickPlayHandlers.as_view({'post': 'join'})),
    path('leave', QuickPlayHandlers.as_view({'post': 'leave'})),
    path('match', QuickPlayHandlers.as_view({'get': 'match'})),
]