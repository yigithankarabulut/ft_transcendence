from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .service import MailService
from .serializers import EmailSerializer, PasswordResetSerializer

class SendEmailAPIView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        mail_service = MailService()
        mail_service.send_email(data['sender_email'], data['receiver_email'], data['subject'], data['body'])
        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)

class ProcessPasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        mail_service = MailService()
        #    def send_email(self, sender_email, receiver_email, subject, body):
        mail_service.send_email('[email protected]', data['email'], 'Password Reset', 'Please click the link to reset your password')
        return Response({'message': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
