from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from migrate_marathon import migrate_old_marathons, get_date_flag, default_args
from config import mongo_db_name



with DAG(
    "migrate_old_marathon_v2_to_marathons",
    tags=["migrate", "marathon", "project"],
    default_args=default_args,
    description="Migrate data from old_marathon_v2 table to marathon, project task tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
) as dag:
    date_flag = get_date_flag(mongo_db_name)
    
    # --- DAG 定義 ---
    migrate_marathon_task = PythonOperator(
        task_id="migrate_old_marathon_v2_to_marathons",
        python_callable=migrate_old_marathons,
        op_kwargs={'date_flag': date_flag},  # 傳遞 date_flag 參數
        dag=dag
    )

    migrate_marathon_task 