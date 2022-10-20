import pika
import redis

def callback(ch, method, properties, body):
    string_body = "Received : %r" % body
    print(string_body)
    
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', string_body)

    print("uploaded")


def main():
    print("Starting redis_to_minio.py")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clics_to_redis')
    channel.basic_consume(
        queue='clics_to_redis',
        auto_ack=True,
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")

if __name__ == "__main__":
    main()