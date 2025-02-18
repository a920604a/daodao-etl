from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from migrate_marathon import migrate_old_marathons, set_player_role, set_mentor_role, get_date_flag
from config import mongo_old_db_name

# DAG 設定
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}



with DAG(
    "migrate_old_marathon_v1_to_marathons",
    tags=["migrate", "marathon", "project"],
    default_args=default_args,
    description="Migrate data from old_marathon_v1 table to marathon, project task tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
) as dag:
    date_flag = get_date_flag(mongo_old_db_name)
    # --- DAG 定義 ---
    migrate_marathon_task = PythonOperator(
        task_id="migrate_old_marathons_v1_to_projects",
        python_callable=migrate_old_marathons,
        op_kwargs={'date_flag': date_flag},  # 傳遞 date_flag 參數
        dag=dag
    )
    set_player_role_task = PythonOperator(
            task_id="set_player_the_right_role_id",
            python_callable=set_player_role,
            dag=dag
        )
    set_mentor_role_task =  PythonOperator(
        task_id="set_mentor_the_right_role_id",
        python_callable=set_mentor_role,
        dag=dag
    )
    
    migrate_marathon_task >> set_player_role_task >> set_mentor_role_task
 