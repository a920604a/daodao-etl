from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
import pandas as pd
import json
from sqlalchemy import create_engine
import os
import ast
# 環境變數設定
NOTION_API_KEY = Variable.get("NOTION_API_KEY")
NOTION_DATABASE_RESOURCE_ID = Variable.get("NOTION_DATABASE_RESOURCE_ID")
POSTGRES_URI = Variable.get("postgres_uri")
postgres_engine = create_engine(POSTGRES_URI)

# 請求標頭設定
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# 保存 Notion 整體 JSON 檔案
def read_and_save_json(database_id, headers, output_json_path):
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    data = []
    has_more = True
    next_cursor = None
    i = 0

    while has_more:
        # 如果有游標，則附加到請求的有效負載中
        payload = {
            "start_cursor": next_cursor
        } if next_cursor else {}

        response = requests.post(read_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}, {response.text}")

        response_data = response.json()
        data.extend(response_data.get("results", []))
        has_more = response_data.get("has_more", False)
        next_cursor = response_data.get("next_cursor")
        print(f"page : {i} parsed")
        i += 1

    # 儲存整個資料
    with open(output_json_path, 'w', encoding='utf8') as f:
        json.dump({"results": data}, f, ensure_ascii=False)
    
    print(f"Fetched {len(data)} items and saved to JSON file")


# 處理並返回 DataFrame 結果
def process_and_save_csv(input_json_path, output_csv_path):
    with open(input_json_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        
    results = data.get("results", [])
    print(f"process_and_save_csv 共 {len(results)} 筆資料" )
    properties_list = []
    
    for item in results:
        if 'properties' in item:
            properties = item['properties']
            properties_dict = {}
            for key, value in properties.items():
                properties_dict[key] = {
                    'id': value['id'],
                    'type': value['type'],
                    'value': None
                }
                # 根據類型提取對應的值
                if value['type'] == 'multi_select':
                    properties_dict[key]['value'] = ', '.join([v['name'] for v in value['multi_select']])
                elif value['type'] == 'select':
                    properties_dict[key]['value'] = value['select']['name'] if value['select'] else None
                elif value['type'] == 'url':
                    properties_dict[key]['value'] = value['url']
                elif value['type'] == 'rich_text':
                    properties_dict[key]['value'] = ''.join([v['plain_text'] for v in value['rich_text']])
                elif value['type'] == 'title':
                    properties_dict[key]['value'] = ''.join([v['plain_text'] for v in value['title']])
                elif value['type'] == 'files':
                    properties_dict[key]['value'] = ', '.join([f['external']['url'] for f in value['files']])

            properties_list.append(properties_dict)

    df = pd.DataFrame(properties_list)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"Processed data saved to CSV file: {output_csv_path}")


# 讀取與轉換資料
def parse_and_transform_data(input_csv_path, output_csv_path):
    # 讀取原始 CSV 文件
    df = pd.read_csv(input_csv_path)
    print("原始資料：")
    print(df.head())  # 打印原始 DataFrame 的前幾行

    # 創建一個新的 DataFrame，僅提取每列的 value
    transformed_data = {}

    for column in df.columns:
        # 對每一列進行處理，提取 'value' 鍵的內容
        transformed_data[column] = df[column].apply(
            lambda x: ast.literal_eval(x)['value'] if isinstance(x, str) and 'value' in ast.literal_eval(x) else None
        )

    transformed_df = pd.DataFrame(transformed_data)
    
    # 檢查是否有有效的轉換數據
    print("轉換後的資料：")
    print(transformed_df.head())  # 打印轉換後 DataFrame 的前幾行
    
    transformed_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"Transformed data saved to CSV file: {output_csv_path}")

# 儲存至 PostgreSQL
def save_to_postgresql(input_csv_path):
    df = pd.read_csv(input_csv_path)

    df.to_sql('resources', postgres_engine, if_exists='append', index=False)
    print("Data saved to PostgreSQL table 'resources'")

# Airflow DAG 設定
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="notion_resource_to_Postgresql",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    output_json_path = f"/opt/airflow/data/{NOTION_DATABASE_RESOURCE_ID}.json"
    output_csv_path = f"/opt/airflow/data/{NOTION_DATABASE_RESOURCE_ID}.csv"
    transformed_csv_path = f"/opt/airflow/data/{NOTION_DATABASE_RESOURCE_ID}_transformed.csv"

    save_json_task = PythonOperator(
        task_id="save_json",
        python_callable=read_and_save_json,
        op_kwargs={
            "database_id": NOTION_DATABASE_RESOURCE_ID, 
            "headers": headers, 
            "output_json_path": output_json_path,
        },
    )

    save_csv_task = PythonOperator(
        task_id="process_and_save_csv",
        python_callable=process_and_save_csv,
        op_kwargs={
            "input_json_path": output_json_path,
            "output_csv_path": output_csv_path
        },
    )

    parse_task = PythonOperator(
        task_id="parse_and_transform_data",
        python_callable=parse_and_transform_data,
        op_kwargs={
            "input_csv_path": output_csv_path,
            "output_csv_path": transformed_csv_path
        },
    )

    save_task = PythonOperator(
        task_id="save_to_postgresql",
        python_callable=save_to_postgresql,
        op_kwargs={"input_csv_path": transformed_csv_path},
    )

    save_json_task >> save_csv_task >> parse_task >> save_task
