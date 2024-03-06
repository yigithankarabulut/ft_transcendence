import pika
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
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._callback, auto_ack=True)

    def _callback(self, ch, method, properties, body):
        print(" [x] Received message:", body)
        payload = json.loads(body)
        mail_service = MailService()
        if payload['type'] != 'forgot_password':
            print("Invalid message type")
            return
        mail_service.send_email('yigithannkarabulutt@gmail.com', payload['body']['email'], payload['subject'], f"Please click the link to reset your password. Username: {payload['body']['username']}")
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Mesajın işlendiğini doğrulama

    def start_consuming(self):
        print("Waiting for messages...")
        self._channel.start_consuming()

    def close_connection(self):
        # Bağlantıyı kapatma
        self._connection.close()
        print("Connection closed")

if __name__ == "__main__":
    consumer = RabbitMQConsumer(amqp_url='amqp://guest:guest@localhost:5672/%2F', queue_name='mail_queue')
    consumer.connect()
    consumer.start_consuming()
