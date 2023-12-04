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

    data_filepath = "./data/movies-stackexchange/json/Users.json"
    print(data_filepath)
    print(os.getcwd())
    with open(data_filepath, "r") as f:
        content = f.read()
        users = json.loads(content)
        # user = random.choice(users)
        
    message = json.dumps(users, indent=4)

    connection = pika.BlockingConnection(pika.URLParameters("amqp://rabbitmq"))
    channel = connection.channel()

    # channel.queue_declare(queue='users_to_minio')
    # channel.basic_publish(
    #     exchange='',
    #     routing_key='users_to_minio',
    #     body=message
    # )

    channel.queue_declare(queue='users_to_mongo')
    channel.basic_publish(
        exchange='',
        routing_key='users_to_mongo',
        body=message
    )



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