import pika
import json
from .models import Player, Match


class RabbitMQConsumer:
    def __init__(self, amqp_url, queue_name):
        self._amqp_url = amqp_url
        self._queue_name = queue_name
        self._current_match = None

    def connect(self):
        self._connection = pika.BlockingConnection(pika.URLParameters(self._amqp_url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._callback)

    def _callback(self, ch, method, properties, body):
        payload = json.loads(body)
        player_id = payload['player_id']

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            print("Player not found")
            return

        if not self._current_match:
            self._current_match = Match.objects.create()

        self._current_match.match_players.add(player)
        self._current_match.save()

        # İki oyuncu geldikten sonra mevcut maçı sıfırla
        if self._current_match.match_players.count() == 2:
            self._current_match = None

        # Mesajı işleme doğrulama
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        print("Waiting for messages...")
        self._channel.start_consuming()

    def close_connection(self):
        # Bağlantıyı kapatma
        self._connection.close()
        print("Connection closed")
