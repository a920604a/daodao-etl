from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from config import default_args, mongo_uri, mongo_db_name, postgres_uri
from etl.notion2Postgresql import NotionToPostgresETL, create_etl_tasks
from airflow.utils.dates import days_ago
from airflow.models import Variable

TABLE_NAME = "old_resource"

with DAG(
    dag_id="notion_resource_to_postgresql",
    start_date=days_ago(1),
    schedule_interval="@monthly",
    catchup=False,
    default_args=default_args,
) as dag:
    notion_resource_etl = NotionToPostgresETL(
        Variable.get("NOTION_DATABASE_RESOURCE_ID"), TABLE_NAME
    )

    # 建立資源 ETL 任務
    create_etl_tasks(notion_resource_etl, TABLE_NAME, dag)

