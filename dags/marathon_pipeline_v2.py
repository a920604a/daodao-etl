from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from config import default_args, mongo_uri, mongo_old_db_name, mongo_db_name, postgres_uri
from etl.mongo2Postgres import MongoToPostgresETL

# 定义表名
ORG_TABLE_NAME = "marathons"
TABLE_NAME = "old_marathons_v2"

# 初始化 ETL 实例
etl_v2_process = MongoToPostgresETL(mongo_uri, mongo_db_name, postgres_uri)

    
with DAG(
    dag_id="mongo_marathons_v2_to_postgres",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag_marathons:

    # 提取任务
    extract_task = PythonOperator(
        task_id="extract_marathons_v2",
        python_callable=etl_v2_process.extract_marathon_data,
        op_args=[ORG_TABLE_NAME],
        provide_context=True,
    )

    # 转换任务
    transform_task = PythonOperator(
        task_id="transform_marathons_v2",
        python_callable=etl_v2_process.transform_marathons,
        provide_context=True,
    )

    # 加载任务
    load_task = PythonOperator(
        task_id="load_marathons_v2",
        python_callable=etl_v2_process.load_data,
        op_kwargs={"table_name": ORG_TABLE_NAME, "target_table_name": TABLE_NAME},
        provide_context=True,
    )

    # 定义任务依赖关系
    extract_task >> transform_task >> load_task
    
    