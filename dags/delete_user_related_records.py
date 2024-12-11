from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import postgres_uri
from models import Users, Contact, BasicInfo, Location, Area

# 設置 DAG 預設參數
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# 定義 DAG
dag = DAG(
    "delete_all_user_related_records",
    default_args=default_args,
    description="Delete all records related to users from the database",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)


def delete_related_records():
    """
    刪除所有與用戶相關的紀錄，包括 users, contact, basic_info, location, 和可能孤立的 area。
    """
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 刪除 Users 表中的紀錄
        user_ids = session.query(Users.id).all()
        print(f"Deleting {len(user_ids)} users.")
        session.query(Users).delete(synchronize_session=False)
        session.flush()

        # 刪除 Contact 表中的紀錄
        contact_ids = session.query(Contact.id).all()
        print(f"Deleting {len(contact_ids)} contacts.")
        session.query(Contact).delete(synchronize_session=False)
        session.flush()

        # 刪除 BasicInfo 表中的紀錄
        basic_info_ids = session.query(BasicInfo.id).all()
        print(f"Deleting {len(basic_info_ids)} basic_info records.")
        session.query(BasicInfo).delete(synchronize_session=False)
        session.flush()

        # 刪除 Location 表中的紀錄
        location_ids = session.query(Location.id).all()
        print(f"Deleting {len(location_ids)} locations.")
        session.query(Location).delete(synchronize_session=False)
        session.flush()

        # 刪除 Area 表中孤立的紀錄
        orphan_areas = session.query(Area).filter(~Area.id.in_(
            session.query(Location.area_id).distinct()
        )).all()
        print(f"Deleting {len(orphan_areas)} orphan areas.")
        session.query(Area).filter(
            ~Area.id.in_(session.query(Location.area_id).distinct())
        ).delete(synchronize_session=False)

        # 提交事務
        session.commit()
        print("All related records have been deleted successfully.")
    except Exception as e:
        print(f"Error occurred during deletion: {e}")
        session.rollback()
    finally:
        session.close()


# 定義 PythonOperator 執行刪除過程
delete_records_task = PythonOperator(
    task_id="delete_all_user_related_records",
    python_callable=delete_related_records,
    dag=dag,
)

delete_records_task
