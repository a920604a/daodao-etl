from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Marathon, ProjectMarathon, Project, Milestone, Task, UserProject, Eligibility, FeePlan
from config import postgres_uri
import pandas as pd
import logging
import json
import re
from utils.code import qualifications_mapping,motivation_mapping, policy_mapping, presentation_mapping
from utils.code_enum import qualifications_t

# 設定日誌
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("migration_logger")

# DAG 設定
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "migrate_old_marathon_to_marathons",
    tags=["migrate", "marathon", "project"],
    default_args=default_args,
    description="Migrate data from old_marathon table to marathon, project task tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)

# --- 模組化方法 ---
def fetch_old_marathons(engine):
    logger.info("開始提取 old_marathons 資料...")
    query = "SELECT * FROM old_marathons"
    return pd.read_sql(query, engine)

def process_user(row, session):
    user = session.query(User).filter_by(mongo_id=row["userId"]).first()
    if not user:
        user = User(
            mongo_id=row["userId"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
        session.add(user)
        session.flush()
        logger.info(f"新增 User: {user.mongo_id}")
    return user

def process_eligibility(row, session):
    pricing = json.loads(row.get("pricing", "{}"))
    option_value = pricing.get("option", "")
    match = re.search(r"\d+", option_value)
    number = int(match.group()) if match else 0
    qualification_type = qualifications_mapping.get(option_value.split("：")[0], 'four')

    logger.info(qualification_type)

    fee_plan = session.query(FeePlan).filter_by(fee_plan_type=qualification_type).first()
    
    eligibility = Eligibility(
        partner_emails=pricing.get("email", []),
        fee_plans_id=fee_plan.id,
    )
    session.add(eligibility)
    session.flush()
    logger.info(f"新增 Eligibility ID: {eligibility.id}")
    return eligibility

def process_project(row, user, session):
    motivation_str = row.get("motivation", "{}") or "{}"
    strategies_str = row.get("strategies", "{}") or "{}"
    outcome_str = row.get("outcomes", "{}") or "{}"
    resources_str = row.get("resources", "[]") or "[]"

    # 處理可能是空字串或 None 的情況
    motivation = json.loads(motivation_str if motivation_str not in [None, ""] else "{}")
    strategies = json.loads(strategies_str if strategies_str not in [None, ""] else "{}")
    outcome = json.loads(outcome_str if outcome_str not in [None, ""] else "{}")
    resources = json.loads(resources_str if resources_str not in [None, ""] else "[]")

    # 使用映射表進行轉換
    motivation_tags = [
        motivation_mapping.get(tag[:2], tag[:2]) if tag.startswith("其他") else motivation_mapping.get(tag, tag)
        for tag in motivation.get("tags", [])
    ]
    policy_tags = [
        policy_mapping.get(tag[:2], tag[:2]) if tag.startswith("其他") else policy_mapping.get(tag, tag)
        for tag in strategies.get("tags", [])
    ]
    
    presentation_tags = [
        presentation_mapping.get(tag[:2], tag[:2]) if tag.startswith("其他") else presentation_mapping.get(tag, tag)
        for tag in outcome.get("tags", [])
    ]


    
    project = Project(
        user_id=user.id,
        topic=row.get("title"),
        description=row.get("description"),
        motivation=motivation_tags,
        motivation_description=motivation.get("description"),
        goal=row.get("goal", ""),
        content=row.get("content", ""),
        strategy=policy_tags,
        strategy_description=strategies.get("description"),
        resource_name=[res.get("name", "") for res in resources],
        resource_url=[res.get("url", "") for res in resources],
        outcome=presentation_tags,
        outcome_description=outcome.get("description"),
        is_public=row.get("isPublic", False),
        # start_date=
        # end_date=
        version = 1,
    )
    session.add(project)
    session.flush()
    logger.info(f"新增 Project ID: {project.id}")
    return project

def process_milestones(row, project, session):
    milestone_datas = json.loads(row.get("milestones", "[]"))
    # milestone = Milestone(project_id=project.id)
    for milestone_data in milestone_datas:
    
        milestone = Milestone(
            name=milestone_data.get("name"),
            project_id=project.id,
            start_date=milestone_data.get("startDate"),
            end_date=milestone_data.get("endDate"),
        )
        session.add(milestone)
        session.flush()
        logger.info(f"新增 Task ID: {milestone.id}")

        for task_data in milestone_data.get("subMilestones", []):
            logger.info(f"task_data {task_data}")
            task = Task(
                milestone_id=milestone.id,
                name=task_data.get("name"),
                description=task_data.get("description"),
            )
            session.add(task)
            logger.info(f"新增 Task ID: {task.id}")

    logger.info(f"關聯 Milestone ID: {milestone.id}")
        
def link_user_project(user, project, session):
    user_project = UserProject(user_external_id=user.external_id, project_id=project.id)
    session.add(user_project)
    session.flush()
    logger.info(f"新增 UserProject: User external_id {user.external_id}, Project ID {project.id}")

def link_project_marathon(project, marathon, session):
    project_marathon = ProjectMarathon(project_id=project.id, marathon_id=marathon.id)
    session.add(project_marathon)
    session.flush()
    logger.info(f"新增 ProjectMarathon: Project ID {project.id}, Marathon ID {marathon.id}")

def migrate_old_marathons(**kwargs):
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        old_marathons_df = fetch_old_marathons(engine)
        logger.info(f"共提取 {len(old_marathons_df)} 筆資料")

        for idx, row in old_marathons_df.iterrows():
            logger.info(f"處理第 {idx+1} 筆資料 (User ID: {row['userId']})")
            user = process_user(row, session)
            eligibility = process_eligibility(row, session)
            project = process_project(row, user, session)
            process_milestones(row, project, session)

            # 將 User 與 Project 連結
            link_user_project(user, project, session)

            # 將 Project 與 Marathon 連結
            marathon = session.query(Marathon).filter_by(event_id=row["eventId"]).first()
            if marathon:
                link_project_marathon(project, marathon, session)

        session.commit()
        logger.info("所有資料成功遷移至新表")
    except IntegrityError as e:
        session.rollback()
        logger.error(f"資料庫完整性錯誤: {e}")
    except Exception as e:
        session.rollback()
        logger.error(f"發生未預期錯誤: {e}")
    finally:
        session.close()

# --- DAG 定義 ---
migrate_marathon_task = PythonOperator(
    task_id="migrate_old_marathons_to_projects",
    python_callable=migrate_old_marathons,
    dag=dag,
)
