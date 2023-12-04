import pendulum
import logging
from airflow import DAG
from airflow.operators.python import ExternalPythonOperator
from datetime import timedelta

log = logging.getLogger(__name__)

def mongo_to_bigquery_user():
    import pymongo
    from google.cloud import bigquery
    from google.oauth2 import service_account

    MONGO_USERNAME = "admin"
    MONGO_PASSWORD = "admin"
    MONGO_HOST = "mongodb"
    MONGO_PORT = 27017
    MONGO_DB = "movies-stackexchange"
    MONGO_COLLECTION = "user"
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

        def aggregate(self, pipeline):
            return self.collection.aggregate(pipeline)
    
    db = Database()

    pipeline = [
        { "$match": {"@Id": "11"}},
        { "$lookup": { "from": "post", "localField": "@Id", "foreignField": "@OwnerUserId", "as": "userPosts"}},
        { "$unwind": { "path": "$userPosts"}},
        { "$sort": { "userPosts.@CreationDate": -1}}, 
        { "$group": {"_id": "$@DisplayName", "latestPostDate": { "$max": "$userPosts.@CreationDate" }}}
    ]

    result = db.aggregate(pipeline)

    latest_post = list(map(lambda p : {"UserId": None if p["_id"] == None else p["_id"],"latestPostDate": p["latestPostDate"]}, list(result)))

    #project_id = "bigquery-404409"
    project_id = "tp-bigquery"
    dataset_id = "users"
    table_id = "users_latest_post"

    # Set up credentials (replace 'path/to/your/credentials.json' with your service account key file)
    credentials = service_account.Credentials.from_service_account_file(
        "./config/service-account.json",
    )

    # Create a BigQuery client
    client = bigquery.Client(project=project_id, credentials=credentials)

    # Delete the dataset if it already exists and create a new one
    client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
    client.create_dataset(dataset_id)

    # Specify the dataset and table to which you want to upload the data
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    job = client.load_table_from_json(latest_post, table_ref)
    job.result()  # Wait for the job to complete
    print(f"Loaded {job.output_rows} rows into {table_id}")

with DAG(
    dag_id="DAG_mongo_to_bigquery_user",
    schedule=timedelta(seconds=60),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    is_paused_upon_creation=False,
    catchup=False,
    tags=[],
) as dag:
    external_classic = ExternalPythonOperator(
        task_id="mongo-to-bigquery-user",
        python="/usr/local/bin/python",
        python_callable=mongo_to_bigquery_user
    )

    external_classic