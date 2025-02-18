from airflow.models import Variable
from datetime import timedelta

# Airflow DAG 設定
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# 初始化 ETL 類別
mongo_uri = Variable.get("MONGO_URI")
mongo_old_db_name = Variable.get("MONGO_OLD_DB_NAME")
mongo_db_name = Variable.get("MONGO_DB_NAME")
postgres_uri = Variable.get("POSTGRES_URI")
notion_api_key = Variable.get("NOTION_API_KEY")
