import pika
from pymongo import MongoClient
import json
from datetime import datetime


def callback(ch, method, properties, body):  
    
    data_string = body.decode("utf-8")
    data = json.loads(data_string)
    data['timestamp'] = datetime.fromtimestamp(data['timestamp'])

    ##### Écrire ici #####

    # TODO : Récupérer les messages dans RabbitMQ et les insérer dans MongoDB

    # Exemple de code pour insérer dans MongoDB :
    # client = MongoClient('localhost', 27017)
    # db = client.test_database
    # collection = db.test_collection
    # data = {"foo": "bar"}
    # collection.insert_one(data)    

    ######################

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    print("Starting rabbit_to_mongo.py")

    # TODO : Indiquer la bonne url pour RabbitMQ
    rabbit_url = "TODO"

    connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
    channel = connection.channel()

    channel.queue_declare(queue='clics_to_mongo')
    channel.basic_consume(
        queue='clics_to_mongo',
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")

if __name__ == "__main__":
    main()