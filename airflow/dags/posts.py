import pendulum
import logging
from airflow import DAG
from airflow.operators.python import ExternalPythonOperator
from datetime import timedelta

log = logging.getLogger(__name__)

def post():
    import random
    import os
    import json
    import pika

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
    dag_id="DAG_stackexchange_posts",
    schedule=timedelta(seconds=60),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    is_paused_upon_creation=False,
    catchup=False,
    tags=[],
) as dag:
    external_classic = ExternalPythonOperator(
        task_id="post",
        python="/usr/local/bin/python",
        python_callable=post
    )

    external_classic