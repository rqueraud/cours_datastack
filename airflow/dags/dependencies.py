import pendulum
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="DAG_install_dependencies",
    schedule="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    is_paused_upon_creation=False,
    catchup=False,
    tags=[],
) as dag:
    install_dependencies = BashOperator(
        task_id='install_dependencies',
        bash_command='pip install pika pymongo google-cloud-bigquery',
        dag=dag,
    )

    ingest_users = TriggerDagRunOperator(
        task_id='ingest_users',
        trigger_dag_id="DAG_ingest_users",
        dag=dag,
    )

    install_dependencies >> ingest_users