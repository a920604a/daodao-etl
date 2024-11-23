from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
import pandas as pd
from sqlalchemy import create_engine
import json

# Airflow DAG 設定
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


# 初始化 ETL 類別
class NotionToPostgresETL:
    def __init__(self, notion_database_id, postgres_table_name):
        self.notion_api_key = Variable.get("NOTION_API_KEY")
        self.postgres_uri = Variable.get("postgres_uri")
        self.postgres_engine = create_engine(self.postgres_uri)
        self.notion_database_id = notion_database_id
        self.postgres_table_name = postgres_table_name

        # 請求標頭設定
        self.headers = {
            "Authorization": f"Bearer {self.notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def read_and_save_json(self, database_id, headers, output_json_path):
        read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        data = []
        has_more = True
        next_cursor = None

        while has_more:
            payload = {"start_cursor": next_cursor} if next_cursor else {}

            response = requests.post(read_url, headers=headers, json=payload)
            if response.status_code != 200:
                raise Exception(f"Error: {response.status_code}, {response.text}")

            response_data = response.json()
            data.extend(response_data.get("results", []))
            has_more = response_data.get("has_more", False)
            next_cursor = response_data.get("next_cursor")

        # 儲存 JSON 數據
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return output_json_path

    def process_and_save_csv(self, input_json_path, output_csv_path):
        with open(input_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        properties_list = []
        for item in data:
            if "properties" in item:
                properties = item["properties"]
                properties_dict = {}
                for key, value in properties.items():
                    properties_dict[key] = self.extract_property_value(value)
                properties_list.append(properties_dict)

        df = pd.DataFrame(properties_list)
        df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        return output_csv_path

    def extract_property_value(self, value):
        if value["type"] == "rich_text":
            return "".join([v["plain_text"] for v in value["rich_text"]])
        elif value["type"] == "multi_select":
            return ", ".join([v["name"] for v in value["multi_select"]])
        elif value["type"] == "select":
            return value["select"]["name"] if value["select"] else None
        elif value["type"] == "url":
            return value["url"]
        elif value["type"] == "files":
            return ", ".join(
                [
                    f.get("external", {}).get("url", "無法獲取 URL")
                    for f in value["files"]
                ]
            )
        elif value["type"] == "created_time":
            return value["created_time"]
        elif value["type"] == "title":
            return "".join([v["plain_text"] for v in value["title"]])
        return None

    def save_to_postgresql(self, csv_path):
        df = pd.read_csv(csv_path)
        df.to_sql(
            self.postgres_table_name,
            self.postgres_engine,
            if_exists="append",
            index=False,
        )


def create_etl_tasks(etl_instance, database_id, dag):
    output_json_path = f"/opt/airflow/data/{database_id}.json"
    output_csv_path = f"/opt/airflow/data/{database_id}.csv"
    transformed_csv_path = f"/opt/airflow/data/{database_id}_transformed.csv"

    save_json_task = PythonOperator(
        task_id=f"save_json_{database_id}",
        python_callable=etl_instance.read_and_save_json,
        op_kwargs={
            "database_id": etl_instance.notion_database_id,
            "headers": etl_instance.headers,
            "output_json_path": output_json_path,
        },
        dag=dag,
    )

    save_csv_task = PythonOperator(
        task_id=f"process_and_save_csv_{database_id}",
        python_callable=etl_instance.process_and_save_csv,
        op_kwargs={
            "input_json_path": output_json_path,
            "output_csv_path": output_csv_path,
        },
        dag=dag,
    )

    load_task = PythonOperator(
        task_id=f"load_{database_id}_data_to_postgres",
        python_callable=etl_instance.save_to_postgresql,
        op_kwargs={"csv_path": output_csv_path},
        dag=dag,
    )

    save_json_task >> save_csv_task >> load_task


with DAG(
    dag_id="notion_resource_to_postgresql",
    start_date=days_ago(1),
    schedule_interval="@monthly",
    catchup=False,
    default_args=default_args,
) as dag:
    notion_resource_etl = NotionToPostgresETL(
        Variable.get("NOTION_DATABASE_RESOURCE_ID"), "resource"
    )

    # 建立資源 ETL 任務
    create_etl_tasks(notion_resource_etl, "resource", dag)


with DAG(
    dag_id="notion_store_to_postgresql",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:
    notion_store_etl = NotionToPostgresETL(
        Variable.get("NOTION_DATABASE_STORE_ID"), "store"
    )

    # 建立商店 ETL 任務
    create_etl_tasks(notion_store_etl, "store", dag)
