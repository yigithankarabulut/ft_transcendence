import sys
import signal
import threading
from django.apps import AppConfig
from .consumer import RabbitMQConsumer


def start_rabbitmq_consumer():
    print('Starting RabbitMQ consumer thread...')
    amqp_url = "amqp://guest:guest@localhost:5672/%2F"
    consumers = RabbitMQConsumer(amqp_url, queue_name='mail-service')
    consumers.connect()
    consumers.start_consuming()


class SrcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'

    def ready(self):
        def signal_handler(sig, frame):
            print('Exiting...')
            sys.exit(0)

        consumer_thread = threading.Thread(target=start_rabbitmq_consumer)
        consumer_thread.daemon = True
        consumer_thread.start()

        signal.signal(signal.SIGINT, signal_handler)
