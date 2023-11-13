from genericpath import exists
import pika
import redis
import json
import time

r = redis.Redis(host='redis-cours', port=6379, db=0)

def safe_connect_rabbitmq():
    channel = None
    while not channel:
        try:
            connection = pika.BlockingConnection(pika.URLParameters("amqp://rabbitmq"))
            channel = connection.channel()
        except pika.exceptions.AMQPConnectionError:
            time.sleep(1)
    return channel

def callback(ch, method, properties, body):  
    data_string = body.decode("utf-8")
    data = json.loads(data_string)

    ##### Écrire ici #####

    # TODO : Récupérer les posts dans la queue RabbitMQ et vérifier que le post n'a pas déjà été rencontré avant de le pousser vers la queue suivante
    # TODO 2: Pousser le message dans une nouvelle queue posts_to_bigquery
    # Exemple de code pour écrire dans Redis :

    # r = redis.Redis(host='localhost', port=6379, db=0)
    # r.set('foo', '{"key": "value"}')
    # r.get('foo')

    ######################

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    print("Starting redis_sync.py")

    channel = safe_connect_rabbitmq()

    channel.queue_declare(queue='posts_to_redis')
    channel.basic_consume(
        queue='posts_to_redis',
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")

if __name__ == "__main__":
    main()