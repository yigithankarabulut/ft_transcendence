import pika
import json

from requests import request


class RabbitMQConsumer:
    def __init__(self, amqp_url, queue_name):
        self._amqp_url = amqp_url
        self._queue_name = queue_name
        self._matchlist = []
        self._tournamentlist = {int: list}

    def connect(self):
        self._connection = pika.BlockingConnection(pika.URLParameters(self._amqp_url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._callback)

    def _callback(self, ch, method, properties, body):
        payload = json.loads(body)

        if payload['type'] == 'tournament':
            tournament_id = payload['subject']
            if tournament_id not in self._tournamentlist:
                self._tournamentlist[tournament_id] = []
                self._tournamentlist[tournament_id].append(payload['body'])
            else:
                self._tournamentlist[tournament_id].append(payload['body'])
                if len(self._tournamentlist[tournament_id]) == 2:
                    req = {
                        'tournament_id': tournament_id,
                        'player1': self._tournamentlist[tournament_id][0],
                        'player2': self._tournamentlist[tournament_id][1]
                    }
                    print(req)
                    response = request("POST", "http://localhost:8005/game/tournament/play", json=req)
                    print("Tournament match has been created:", req)
                    self._tournamentlist[tournament_id] = []


        else:
            self._matchlist.append(payload['body'])
            if len(self._matchlist) == 2:
                req = {
                    'player1': self._matchlist[0],
                    'player2': self._matchlist[1]
                }
                response = request("POST", "http://localhost:8005/game/match/start_match", json=req)
                print("Match has been created:", req)
                self._matchlist = []

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        print("Waiting for messages...")
        self._channel.start_consuming()

    def close_connection(self):
        self._connection.close()
        print("Connection closed")
