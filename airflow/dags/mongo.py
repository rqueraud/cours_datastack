import pendulum
import logging
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import ExternalPythonOperator, PythonVirtualenvOperator, is_venv_installed
from datetime import timedelta

log = logging.getLogger(__name__)

MONGO_USERNAME = "admin"
MONGO_PASSWORD = "admin"
MONGO_HOST = "mongodb"
MONGO_PORT = 27017
MONGO_DB = "movies-stackexchange"
MONGO_COLLECTION = "post"
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

def mongo_to_bigquery():
    import pymongo

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

        def aggregate(self, pipeline):
            return self.collection.aggregate(pipeline)
    
    db = Database()

    pipeline = [
        {"$group": {"_id": "$@OwnerUserId", "count": {"$sum": 1}}},
    ]

    result = db.aggregate(pipeline)

    # TODO: terminer





def post():
    import random
    import os
    import json
    import pymongo

    data_filepath = "./data/movies-stackexchange/json/Posts.json"
    print(data_filepath)
    print(os.getcwd())
    with open(data_filepath, "r") as f:
        content = f.read()
        posts = json.loads(content)
        post = random.choice(posts)
        
    message = json.dumps(post, indent=4)

    connection = pika.BlockingConnection(pika.URLParameters("amqp://rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue='posts_to_minio')
    channel.basic_publish(
        exchange='',
        routing_key='posts_to_minio',
        body=message
    )

    channel.queue_declare(queue='posts_to_mongo')
    channel.basic_publish(
        exchange='',
        routing_key='posts_to_mongo',
        body=message
    )


with DAG(
    dag_id="DAG_mongo_to_bigquery",
    schedule=timedelta(seconds=60),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    is_paused_upon_creation=False,
    catchup=False,
    tags=[],
) as dag:
    
    if not is_venv_installed():
        log.warning("The virtalenv_python example task requires virtualenv, please install it.")

    virtual_classic = PythonVirtualenvOperator(
        task_id="mongo-to-bigquery",
        requirements="pymongo",
        python_callable=mongo_to_bigquery,
    )