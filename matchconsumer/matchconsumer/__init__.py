from .consumer import RabbitMQConsumer

def start_consumer():
    consumer = RabbitMQConsumer(amqp_url='amqp://guest:guest@localhost:5672/%2F', queue_name='matchmaking')
    consumer.connect()
    consumer.start_consuming()

start_consumer()
