from django.core.mail import send_mail

class MailService:

    def send_email(self, sender_email, receiver_email, subject, body):
        send_mail(
            subject,
            body,
            sender_email,
            [receiver_email],
            fail_silently=False,
        )
