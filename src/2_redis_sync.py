from genericpath import exists
import pika
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def callback(ch, method, properties, body):  
    data_string = body.decode("utf-8")
    data = json.loads(data_string)

    ##### Écrire ici #####

    # TODO : Récupérer les messages dans une queue RabbitMQ et n'en pousser qu'un par seconde dans une seconde queue en utilisant Redis pour se synchroniser 

    # Exemple de code pour écrire dans Redis :

    # r = redis.Redis(host='localhost', port=6379, db=0)
    # r.set('foo', '{"key": "value"}')
    # r.get('foo')

    ######################

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    print("Starting redis_sync.py")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clics_to_redis')
    channel.basic_consume(
        queue='clics_to_redis',
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")

if __name__ == "__main__":
    main()