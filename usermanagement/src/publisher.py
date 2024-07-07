import pika
import json

class PublisherBase:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, message):
        try:
            # Mesajı yayınlama
            self.channel.basic_publish(exchange='',
                                        routing_key=self.queue_name,
                                        body=json.dumps(message))
            print(" [x] Sent message:", message)
            return True
        except Exception as e:
            print("An error occurred while publishing message:", e)
            return False

    def close_connection(self):
        # Bağlantıyı kapatma
        self.connection.close()
        print("Connection closed")
