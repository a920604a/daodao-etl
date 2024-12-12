
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Users, Contact, BasicInfo, Location, Area, Store
from config import postgres_uri
import json
import uuid
import pandas as pd
from utils.code_enum import want_to_do_list_t, role_list_t
from utils.code import city_mapping
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import array, ARRAY
import logging

#設定日誌
logging.basicConfig(level=logging.INFO)

#設定DAG name和定義參數
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "delete_all_store_related_records",
     tags=['migrate', 'store'],
    default_args=default_args,
    description="Delete all records related to store from the database",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)




def delete_all_store_records():
    """
    刪除所有 Store 表中的紀錄。
    """
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        
        # 刪除 Store 表中的紀錄
        table_name_ids = session.query(Store.id).all()
        print(f"Deleting {len(table_name_ids)} store records.")
        session.query(Store).delete(synchronize_session=False)
        session.flush()

        # 提交事務
        session.commit()
        
    except Exception as e:
        print(f"Error occurred during deletion: {e}")
        session.rollback()
    finally:
        session.close()
    
delete_store_records_task = PythonOperator(
    task_id="delete_all_store_records",
    python_callable=delete_all_store_records,
    dag=dag,
)