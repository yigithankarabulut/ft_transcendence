import pika
import json
import logging
import os

class PublisherBase:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        if self.queue_name == "mail-service":
            self.queue_name = os.environ.get('RABBITMQ_QUEUE_NAME')
        rabbitmq_host = os.environ.get('RABBITMQ_HOST')
        rabbitmq_port = os.environ.get('RABBITMQ_PORT')
        rabbitmq_user = os.environ.get('RABBITMQ_DEFAULT_USER')
        rabbitmq_pass = os.environ.get('RABBITMQ_DEFAULT_PASS')
        rabbitmq_vhost = os.environ.get('RABBITMQ_DEFAULT_VHOST')
        logging.error("->>>>>>>>>>> host: %s, port: %s, user: %s, pass: %s, vhost: %s", rabbitmq_host, rabbitmq_port, rabbitmq_user, rabbitmq_pass, rabbitmq_vhost)

        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
        parameters = pika.ConnectionParameters(rabbitmq_host,
                                               rabbitmq_port,
                                               rabbitmq_vhost,
                                               credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        logging.info("RabbitMQ connection established")

    def publish_message(self, message):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                )
            logging.info(" [x] Sent message:", message)
            return True
        except Exception as e:
            logging.error("An error occurred while publishing message: %s", e)
            return False

    def close_connection(self):
        self.connection.close()
        logging.info("RabbitMQ connection closed")
