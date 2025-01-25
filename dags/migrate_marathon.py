from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Group, Users, UserJoinGroup, Area  # 假設模型已經更新
from config import postgres_uri
import pandas as pd
import logging
from utils.code import partnerEducationStep_mapping, group_type_mapping

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 設定DAG name和定義參數
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "migrate_old_activities_to_groups",
    tags=['migrate', 'marathon', 'project'],
    default_args=default_args,
    description="Migrate data from old_marathon table to marathon, project task tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)



def transform_and_load_data(**kwargs):
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    
    try:
        # 查詢舊表的所有資料
        old_records = session.query(OldMarathons).all()

        for record in old_records:
            # 插入到新表的 ProjectMarathon 中
            project_marathon = ProjectMarathon(
                project_id=record.userId,  # 假設 userId 是對應的 project_id
                marathon_id=record.eventId,  # 假設 eventId 是對應的 marathon_id
                project_registration_date=parse_date(record.registrationDate),
                status=record.registrationStatus or "Pending",
                feedback=record.description,  # 假設 feedback 來自 description
            )
            session.add(project_marathon)

            # 處理 milestones
            if record.milestones:
                milestones = record.milestones.split(",")  # 假設以逗號分隔的字串
                for milestone_name in milestones:
                    milestone = Milestone(
                        project_id=record.userId,
                        start_date=None,  # 若無法從舊資料中得知，設為 None
                        end_date=None,
                        interval=1,  # 預設為 1 週
                    )
                    session.add(milestone)

            # 處理 tasks
            if record.goals:
                tasks = record.goals.split(",")  # 假設以逗號分隔的字串
                for task_name in tasks:
                    task = Task(
                        milestone_id=None,  # 需匹配對應的 milestone
                        name=task_name,
                        description=record.content,
                        start_date=None,
                        end_date=None,
                        is_completed=False,
                        is_deleted=False,
                    )
                    session.add(task)

        # 提交事務
        session.commit()

    except Exception as e:
        print(f"資料轉移過程中發生錯誤: {e}")
        session.rollback()
    finally:
        session.close()