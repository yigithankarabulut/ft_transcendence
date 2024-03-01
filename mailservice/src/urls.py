from django.urls import path, include
from .views import SendEmailAPIView, ProcessPasswordResetAPIView

urlpatterns = [
    path('send', SendEmailAPIView.as_view(), name='send-email'),
    path('reset/password', ProcessPasswordResetAPIView.as_view(), name='process-password-reset'),
]
