from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from config import default_args, mongo_uri, mongo_db_name, postgres_uri
from etl.mongo2Postgres import MongoToPostgresETL

ORG_TABLE_NAME = "activities"
TABLE_NAME = "old_activities"
etl_process = MongoToPostgresETL(mongo_uri, mongo_db_name, postgres_uri)



with DAG(
    dag_id="mongo_activities_to_postgres",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag_activities:
    extract_task = PythonOperator(
        task_id="extract_activities",
        python_callable=etl_process.extract_data,
        op_args=[ORG_TABLE_NAME],
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_activities",
        python_callable=etl_process.transform_activities,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_activities",
        python_callable=etl_process.load_data,
        op_kwargs={"table_name": ORG_TABLE_NAME, "target_table_name": TABLE_NAME},
        provide_context=True,
    )

    extract_task >> transform_task >> load_task
