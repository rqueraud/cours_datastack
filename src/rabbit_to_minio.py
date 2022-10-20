import pika
from minio import Minio

client = Minio(
    endpoint="localhost:9000",
    access_key="rqueraud",
    secret_key="Catie515_",
    secure=False
)

def callback(ch, method, properties, body):
    string_body = "Received : %r" % body
    print(string_body)
    if not client.bucket_exists("clics"):
        client.make_bucket('clics')

    with open("/tmp/myfile.txt", "w") as f:
        f.write(string_body)
    client.fput_object("clics", "myfile.txt", '/tmp/myfile.txt')
    print("uploaded")

    # client.put_object("clics", "myfile.txt", str(string_body))

def main():
    print("Starting rabbit_to_minio.py")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clics_to_minio')
    channel.basic_consume(
        queue='clics_to_minio',
        auto_ack=True,
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")

if __name__ == "__main__":
    main()