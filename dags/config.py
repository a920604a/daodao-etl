from airflow.models import Variable
from datetime import timedelta

# Airflow DAG 設定
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# 初始化 ETL 類別
mongo_uri = Variable.get("mongo_uri")
mongo_db_name = Variable.get("table_name")
postgres_uri = Variable.get("postgres_uri")