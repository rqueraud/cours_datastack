import pika

def main():
    print("Starting clic.py")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    clic = {
        id: 0,
        visitor_id: 0,
        element: "image"
    }
    message = str(clic)

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

    print("Done")

if __name__ == "__main__":
    main()