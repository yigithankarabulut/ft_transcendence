import pika, pika.exceptions
import json
from .service import MailService


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
        print(" [x] Received message:", body)
        payload = json.loads(body)
        mail_service = MailService()
        if payload['type'] != 'forgot_password':
            print("Invalid message type")
            return
        mail_service.send_email('yigithannkarabulutt@gmail.com', payload['body']['email'], payload['subject'],
                                f"Please click the link to reset your password. Link: {payload['body']['reset_url']}")
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        print("Waiting for messages...")
        try:
            self._channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker as e:
            print("Connection closed by broker")
            self.connect()
            self.start_consuming()
        except Exception as e:
            print("Error:", e)

    def close_connection(self):
        try:
            self._connection.close()
        except Exception as e:
            print("Error:", e)
        print("Connection closed")
