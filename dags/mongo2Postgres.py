from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pymongo
from sqlalchemy import create_engine
import os
import json

# Airflow DAG 設定
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# 初始化 ETL 類別
mongo_uri = Variable.get("mongo_uri")
mongo_db_name = Variable.get("table_name")
postgres_uri = Variable.get("postgres_uri")


class MongoToPostgresETL:
    def __init__(self, mongo_uri, db_name, postgres_uri):
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.db_name = db_name
        self.postgres_engine = create_engine(postgres_uri)

    def extract_data(self, collection_name, **kwargs):
        print(f"Extracting data from MongoDB collection: {collection_name}")
        db = self.mongo_client[self.db_name]
        collection = db[collection_name]
        data = list(collection.find({}))
        print(f"Extracted {len(data)} records from {collection_name}")

        for record in data:
            # 將 _id 欄位格式化為 BSON 格式
            record['_id'] = {"$oid": str(record['_id'])}
            for key in record.keys():
                if isinstance(record[key], datetime):
                    record[key] = {"$date": record[key].isoformat()}

        df = pd.DataFrame(data)
        print(df.head())
        print(df.columns)
        kwargs['ti'].xcom_push(key='extracted_df', value=df.to_dict(orient='records'))

    def transform_users(self, **kwargs):
        extracted_data = kwargs['ti'].xcom_pull(key='extracted_df')
        df = pd.DataFrame(extracted_data)
        print(f"Transforming users data {df.columns}")

        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)

        json_columns = ['interestList', 'roleList', 'tagList', 'wantToDoList', 'contactList']
        for column in json_columns:
            df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, list) else None)

        df['isOpenLocation'] = df['isOpenLocation'].astype(bool)
        df['isOpenProfile'] = df['isOpenProfile'].astype(bool)
        df['isSubscribeEmail'] = df['isSubscribeEmail'].astype(bool)

        print("User transformation complete")
        kwargs['ti'].xcom_push(key='transform_users', value=df.to_dict(orient='records'))

    def transform_activities(self, **kwargs):
        extracted_data = kwargs['ti'].xcom_pull(key='extracted_df')
        df = pd.DataFrame(extracted_data)
        print(f"Transforming activities data {df.columns}")

        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)

        json_columns = ['category', 'area', 'partnerEducationStep', 'tagList']
        for column in json_columns:
            df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, list) else None)

        print("Activities transformation complete")
        kwargs['ti'].xcom_push(key='transform_activities', value=df.to_dict(orient='records'))

    def load_data(self, table_name, **kwargs):
        transform_data = kwargs['ti'].xcom_pull(key=f"transform_{table_name}")
        df = pd.DataFrame(transform_data)

        def parse_date(date_dict):
            if isinstance(date_dict, dict) and '$date' in date_dict:
                date_str = date_dict['$date']
                return datetime.fromisoformat(date_str[:-3])
            return pd.NaT

        df['createdDate'] = df['createdDate'].apply(parse_date)
        df['updatedDate'] = df['updatedDate'].apply(parse_date)

        df['createdDate'] = pd.to_datetime(df['createdDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updatedDate'] = pd.to_datetime(df['updatedDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

        df['created_at'] = pd.to_datetime('now')
        df['created_by'] = kwargs['task_instance'].task.owner
        df['updated_at'] = pd.to_datetime('now')
        df['updated_by'] = kwargs['task_instance'].task.owner

        try:
            df.to_sql(table_name, con=self.postgres_engine, if_exists='append', index=False, method='multi')
        except Exception as e:
            print(f"Failed to load data into {table_name}: {e}")


etl_process = MongoToPostgresETL(mongo_uri, mongo_db_name, postgres_uri)


# DAG for users
with DAG(
    dag_id="mongo_users_to_postgres",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:
    extract_task = PythonOperator(
        task_id="extract_users",
        python_callable=etl_process.extract_data,
        op_args=["users"],
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_users",
        python_callable=etl_process.transform_users,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_users",
        python_callable=etl_process.load_data,
        op_kwargs={"table_name": "users"},
        provide_context=True,
    )

    extract_task >> transform_task >> load_task

# DAG for activities
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
        op_args=["activities"],
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
        op_kwargs={"table_name": "activities"},
        provide_context=True,
    )

    extract_task >> transform_task >> load_task
