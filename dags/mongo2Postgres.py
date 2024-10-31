from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pymongo
from sqlalchemy import create_engine
import os
import numpy as np
import json

# MongoDB 設定
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo-daodao:27017")
mongo_client = pymongo.MongoClient(MONGO_URI)

# PostgreSQL 設定
POSTGRES_URI ="postgresql+psycopg2://daodao:daodao@postgres-daodao:5432/daodao"
postgres_engine = create_engine(POSTGRES_URI)

# 提取 MongoDB 資料
def extract_data(collection_name, **kwargs):
    print(f"Extracting data from MongoDB collection: {collection_name}")
    db = mongo_client["prod"]  # 替換為您的資料庫名稱
    collection = db[collection_name]
    data = list(collection.find({}))  # 將 collection 轉成 list
    print(f"Extracted {len(data)} records from {collection_name}")
    for record in data:
        # 將 _id 欄位格式化為 BSON 格式
        record['_id'] = {"$oid": str(record['_id'])}
        
        # 轉換日期欄位為 BSON 格式
        for key in record.keys():
            if isinstance(record[key], datetime):
                record[key] = {"$date": record[key].isoformat()}

    df = pd.DataFrame(data)
    print(df.head())
    print(df.columns)
    kwargs['ti'].xcom_push(key='extracted_df', value=df.to_dict(orient='records'))

# 轉換資料 - users
def transform_users( **kwargs):

    extracted_data = kwargs['ti'].xcom_pull(key='extracted_df')  # 獲取提取的資料
    df = pd.DataFrame(extracted_data)
    print(f"Transforming users data {df.columns}")
    
    # 處理 _id
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)

    def parse_date(date_dict):
        if isinstance(date_dict, dict) and '$date' in date_dict:
            date_str = date_dict['$date']
            return datetime.fromisoformat(date_str[:-3])  # 去掉微秒部分的 'Z'
        return pd.NaT



    # JSON 處理
    json_columns = ['interestList', 'roleList', 'tagList', 'wantToDoList', 'contactList']
    for column in json_columns:
        df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, list) else None)

    # 處理布林值
    df['isOpenLocation'] = df['isOpenLocation'].astype(bool)
    df['isOpenProfile'] = df['isOpenProfile'].astype(bool)
    df['isSubscribeEmail'] = df['isSubscribeEmail'].astype(bool)

    print("User transformation complete")
    kwargs['ti'].xcom_push(key='transform_users', value=df.to_dict(orient='records'))

# 轉換資料 - activities
def transform_activities(**kwargs):

    extracted_data = kwargs['ti'].xcom_pull(key='extracted_df')  # 獲取提取的資料
    df = pd.DataFrame(extracted_data)
    print(f"Transforming activities data {df.columns}")

    # 處理 _id
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)

    
       # JSON 處理
    json_columns = ['category', 'area', 'partnerEducationStep', 'tagList']

    for column in json_columns:
        df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, list) else None)



    print("Activities transformation complete")

    kwargs['ti'].xcom_push(key='transform_activities', value=df.to_dict(orient='records'))


# 載入到 PostgreSQL
def load_data(**kwargs):
    table_name = kwargs['table_name']

    transform_data = kwargs['ti'].xcom_pull(key=f"transform_{table_name}")  # 獲取提取的資料
    df = pd.DataFrame(transform_data)

    
    def parse_date(date_dict):
        if isinstance(date_dict, dict) and '$date' in date_dict:
            date_str = date_dict['$date']
            return datetime.fromisoformat(date_str[:-3])  # 去掉微秒部分的 'Z'
        return pd.NaT
    
    df['createdDate'] = df['createdDate'].apply(parse_date)
    df['updatedDate'] = df['updatedDate'].apply(parse_date)

    df['createdDate'] = pd.to_datetime(df['createdDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    df['updatedDate'] = pd.to_datetime(df['updatedDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    df['created_at'] = pd.to_datetime('now')
    df['created_by'] = kwargs['task_instance'].task.owner
    df['updated_at'] = pd.to_datetime('now')
    df['updated_by'] = kwargs['task_instance'].task.owner


    # 將資料寫入 PostgreSQL
    try:
        df.to_sql(table_name, con=postgres_engine, if_exists='append', index=False, method='multi')
    except Exception as e:
        print(f"Failed to load data into {table_name}: {e}")

# Airflow DAG 設定
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# DAG for users
with DAG(
    dag_id="mongo_users_to_postgres",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag_users:
    extract_task = PythonOperator(
        task_id="extract_users",
        python_callable=extract_data,
        op_args=["users"],
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_users",
        python_callable=transform_users,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_users",
        python_callable=load_data,
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
        python_callable=extract_data,
        op_args=["activities"],
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_activities",
        python_callable=transform_activities,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_activities",
        python_callable=load_data,
        op_kwargs={"table_name": "activities"},
        provide_context=True,
    )

    extract_task >> transform_task >> load_task
