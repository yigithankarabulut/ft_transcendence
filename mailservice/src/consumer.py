import pika
import pika.exceptions
import json
import logging
from .service import MailService
from mailservice.settings import EMAIL_HOST_USER


def send_reset_password_email(payload, mail_service):
    mail_service.send_email(EMAIL_HOST_USER,
                            payload['body']['email'],
                            payload['subject'],
                            f"Please click the link to reset your password. Link: {payload['body']['reset_url']}",
                            )
    logging.info(" [x] Done")

def send_email_verification_email(payload, mail_service):
    mail_service.send_email(EMAIL_HOST_USER,
                            payload['body']['email'],
                            payload['subject'],
                            f"Please click the link to verify your email. Link: {payload['body']['verify_url']}",
                            )
    logging.info(" [x] Done")

def send_2fa_email(payload, mail_service):
    mail_service.send_email(EMAIL_HOST_USER,
                            payload['body']['email'],
                            payload['subject'],
                            f"Your 2FA code is: {payload['body']['code']}",
                            )
    logging.info(" [x] Done")

class RabbitMQConsumer:
    def __init__(self, amqp_url, queue_name):
        self._amqp_url = amqp_url
        self._queue_name = queue_name

    def connect(self):
        self._connection = pika.BlockingConnection(pika.URLParameters(self._amqp_url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._callback, auto_ack=False)

    def _callback(self, ch, method, properties, body):
        logging.info(" [x] Received message:", body)
        payload = json.loads(body)
        mail_service = MailService()
        if payload['type'] == 'forgot_password':
            send_reset_password_email(payload, mail_service)
        elif payload['type'] == 'email_verify':
            send_email_verification_email(payload, mail_service)
        elif payload['type'] == '2fa_code':
            send_2fa_email(payload, mail_service)
        else:
            logging.info(" [x] Unknown message type")
            return
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        logging.info("Waiting for messages...")
        try:
            self._channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker as e:
            logging.error("Error occurred while consuming messages:", e)
            self.connect()
            self.start_consuming()
        except Exception as e:
            logging.error("Error:", e)

    def close_connection(self):
        try:
            self._connection.close()
        except Exception as e:
            logging.error("Error occurred while closing connection:", e)
        logging.info("Connection closed")
