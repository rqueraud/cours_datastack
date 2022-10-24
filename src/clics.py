import pika
import random
import time
import json

def main():
    print("Starting clics.py")
    connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
    channel = connection.channel()

    while True:
        clic = {
            "id": int(time.time()*1000),  # milliseconds
            "timestamp": int(time.time()),  # seconds
            "visitor_id": random.randint(0, 4),
            "element": ["img", "text", "a", "iframe", "div"][random.randint(0, 4)]
        }
        message = json.dumps(clic, indent=4)

        channel.queue_declare(queue='clics_to_minio')
        channel.basic_publish(
            exchange='',
            routing_key='clics_to_minio',
            body=message
        )

        channel.queue_declare(queue='clics_to_redis')
        channel.basic_publish(
            exchange='',
            routing_key='clics_to_redis',
            body=message
        )

        time.sleep(0.1)  # seconds

if __name__ == "__main__":
    main()