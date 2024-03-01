from django.core.mail import send_mail

class MailService:
    # Diğer metotlar burada
    def send_email(self, sender_email, receiver_email, subject, body):
        send_mail(
            subject,
            body,
            sender_email,
            [receiver_email],
            fail_silently=False,
        )
