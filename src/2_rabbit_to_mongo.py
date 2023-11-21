import pymongo
import pika
import json
import time

MONGO_USERNAME = "admin"
MONGO_PASSWORD = "admin"
MONGO_HOST = "mongodb"
MONGO_PORT = 27017
MONGO_DB = "movies-stackexchange"
MONGO_COLLECTION = "post"
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def create_collection(self):
        # If the collection is empty, create the indexes and the validator
        if self.collection.count_documents({}) == 0:
            print("Creating indexes...")

            # Delete previous indexes
            self.collection.drop_indexes()

            # Create new indexes
            self.collection.create_index([("@Id", 1)], unique=True)

    def insert(self, document):
        return self.collection.insert_one(document)

# Create a new connection to the database
db = Database()
db.create_collection()

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
    try:
        result = db.insert(data)

        print(f"Uploaded message with id {result.inserted_id}")
    except pymongo.errors.DuplicateKeyError:
        print(f"Message with id {data['@Id']} already exists")

if __name__ == "__main__":
    print("Starting rabbit_to_db.py")

    channel = safe_connect_rabbitmq()

    channel.queue_declare(queue='posts_to_mongo')
    channel.basic_consume(
        queue='posts_to_mongo',
        on_message_callback=callback
    )
    channel.start_consuming()
    print("Done")
