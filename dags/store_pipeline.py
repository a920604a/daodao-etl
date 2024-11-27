from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from config import default_args, mongo_uri, mongo_db_name, postgres_uri
from etl.notion2Postgresql import NotionToPostgresETL, create_etl_tasks
from airflow.utils.dates import days_ago
from airflow.models import Variable

TABLE_NAME = "old_store"



with DAG(
    dag_id="notion_store_to_postgresql",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:
    notion_store_etl = NotionToPostgresETL(
        Variable.get("NOTION_DATABASE_STORE_ID"), TABLE_NAME
    )

    # 建立商店 ETL 任務
    create_etl_tasks(notion_store_etl, TABLE_NAME, dag)
