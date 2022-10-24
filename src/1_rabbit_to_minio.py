import pika
from minio import Minio
import json
import os

##### Écrire ici #####

# TODO : Indiquer les bons credentials tels que renseignés dans l'interface web de MinIO
client = Minio(
    endpoint="localhost:9000",
    access_key="test",
    secret_key="password",
    secure=False
)
######################
def callback(ch, method, properties, body):
    data_string = body.decode("utf-8")
    data = json.loads(data_string)
    if not client.bucket_exists("clics"):
        client.make_bucket('clics')

    filepath = f"/tmp/{data['id']}.json"
    with open(filepath, "w") as f:
        f.write(data_string)
    client.fput_object("clics", os.path.basename(filepath), filepath)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    os.remove(filepath)

    print(f"Uploaded message with id {data['id']}")

def main():
    print("Starting rabbit_to_minio.py")

    # TODO : Indiquer la bonne url pour RabbitMQ
    rabbit_url = "TODO"

    connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
    channel = connection.channel()

    channel.queue_declare(queue='clics_to_minio')
    channel.basic_consume(
        queue='clics_to_minio',
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")

if __name__ == "__main__":
    main()