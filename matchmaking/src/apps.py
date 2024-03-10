from django.apps import AppConfig
import signal
import sys


class SrcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'

    def ready(self):
        def signal_handler(sig, frame):
            print('Exiting...')
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        from .consumer import RabbitMQConsumer
        consumer = RabbitMQConsumer(amqp_url='amqp://guest:guest@localhost:5672/%2F', queue_name='quickplay')
        consumer.connect()
        consumer.start_consuming()
