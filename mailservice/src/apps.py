import sys
import signal
import threading
from django.apps import AppConfig
from .consumer import RabbitMQConsumer
import logging, os


def start_rabbitmq_consumer():
    logging.info('Starting RabbitMQ consumer...')
    rabbitmq_host = os.environ.get('RABBITMQ_HOST')
    rabbitmq_port = os.environ.get('RABBITMQ_PORT')
    rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER')
    rabbitmq_password = os.environ.get('RABBITMQ_DEFAULT_PASS')
    rabbitmq_vhost = os.environ.get('RABBITMQ_DEFAULT_VHOST')
    amqp_url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}{rabbitmq_vhost}"
    logging.error("->>>>>>>>>>> amqp_url: %s", amqp_url)
    
    queue_name = os.environ.get('RABBITMQ_QUEUE_NAME')
    try:
        consumers = RabbitMQConsumer(amqp_url, queue_name=queue_name)
        consumers.connect()
        consumers.start_consuming()
    except Exception as e:
        logging.error(f'Error starting RabbitMQ consumer: {e}')
        sys.exit(1)


class SrcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'

    def ready(self):
        def signal_handler(sig, frame):
            logging.info('Received shutdown signal. Gracefully shutting down...')
            sys.exit(0)

        consumer_thread = threading.Thread(target=start_rabbitmq_consumer)
        consumer_thread.daemon = True
        consumer_thread.start()

        signal.signal(signal.SIGINT, signal_handler)
