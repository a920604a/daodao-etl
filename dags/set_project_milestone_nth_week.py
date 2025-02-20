from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from migrate_marathon import default_args, set_project_milestone_nth_week


with DAG(
    "set_project_milestone_nth_week",
    tags=["migrate", "marathon", "project"],
    default_args=default_args,
    description="set all milestone nth week",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
) as dag:
    
    # --- DAG 定義 ---
    set_milestone_nth_week = PythonOperator(
        task_id="set_project_milestone_nth_week",
        python_callable=set_project_milestone_nth_week,
        dag=dag
    )

    set_milestone_nth_week 