import pendulum
import logging
from airflow import DAG
from airflow.operators.python import ExternalPythonOperator
from datetime import timedelta

log = logging.getLogger(__name__)

def user():
    import random
    import os
    import json
    import pika
    import pymongo

    MONGO_USERNAME = "admin"
    MONGO_PASSWORD = "admin"
    MONGO_HOST = "mongodb"
    MONGO_PORT = 27017
    MONGO_DB = "movies-stackexchange"
    MONGO_COLLECTION = "user"
    MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    data_filepath = "./data/movies-stackexchange/json/Users.json"
    print(data_filepath)
    print(os.getcwd())
    with open(data_filepath, "r") as f:
        content = f.read()
        users = json.loads(content)

    if collection.count_documents({}) == 0:
        print("Creating indexes...")
        # Delete previous indexes
        collection.drop_indexes()
        # Create new indexes
        collection.create_index([("@Id", 1)], unique=True)
    
    collection.insert_many(users)




with DAG(
    dag_id="DAG_ingest_users",
    schedule="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    is_paused_upon_creation=False,
    catchup=False,
    tags=[],
) as dag:
    ingest_users = ExternalPythonOperator(
        task_id="user",
        python="/usr/local/bin/python",
        python_callable=user
    )

    ingest_users