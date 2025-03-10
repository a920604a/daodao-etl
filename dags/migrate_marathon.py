from airflow.operators.python import PythonOperator
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Marathon, ProjectMarathon, Project, Milestone, Task, UserProject, Eligibility, FeePlan
from serivces import get_valid_contestants, set_player_role_id, set_mentor_role_id, get_marthon_user_list, get_mentor_info, get_mentor_map_dict, insert_participant_into_mentor
from config import postgres_uri
import pandas as pd
import logging
import json
import re
from utils.code import qualifications_mapping, motivation_mapping, strategy_mapping, outcome_mapping
from datetime import datetime
from serivces import fetch_project_milestones
from sqlalchemy import text, select, update, insert

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




def get_date_flag(mongo_db_name):
    try:
        if "-prod" not in mongo_db_name:
            raise ValueError("Input string must contain '-prod' delimiter.")
        date_part = mongo_db_name.split("-prod")[0]  # replace mongo_db_name, mongo_old_db_name
        date_obj = datetime.strptime(date_part, "%Y-%m-%d")
    except Exception as e:
        raise ValueError(f"Invalid mongo_db_name format: {mongo_db_name}") from e
    timestamp = int(date_obj.timestamp())  

    return datetime.fromtimestamp(timestamp).date() # 2025-01-30


# --- 模組化方法 ---
def fetch_old_marathons(engine):
    logger.info("開始提取 old_marathons_v1 資料...")
    query = "SELECT * FROM old_marathons_v1"
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

def process_project_version(session, date_flag):
    version = -1  # 預設值
    # 查询今天的马拉松记录
    today = date.today()
    marathon = session.query(Marathon).filter(
        and_(
            Marathon.start_date <= today,
            Marathon.end_date >= today
        )
    ).first()


    if not marathon:    
        logger.info(f"No marathon found for today's date: {today}")
        return version 
    else:
        logger.info(f"Found marathon: {marathon.title} (Event ID: {marathon.event_id})")
    
    today = date_flag

    if today < marathon.start_date:
        version = 1
    elif today < marathon.end_date:
        version = 2
    else:
        version = 3

    return version

def process_project(row, user, session, date_flag):
    
    version = process_project_version(session, date_flag)
    
    # 判斷是否重複專案新增
    if existing_project := session.query(Project).filter_by(user_id=user.id, title=row.get("title"), version=version).first():

        logger.info(f"專案已存在，跳過新增: {existing_project.id} {existing_project.title} {existing_project.version}")
        return None  # 直接回傳已存在的專案
    
    
    motivation_str = row.get("motivation", "{}") or "{}"
    strategies_str = row.get("strategies", "{}") or "{}"
    outcome_str = row.get("outcomes", "{}") or "{}"
    resources_str = row.get("resources", "")

    # 處理可能是空字串或 None 的情況
    motivation = json.loads(motivation_str if motivation_str not in [None, ""] else "{}")
    strategies = json.loads(strategies_str if strategies_str not in [None, ""] else "{}")
    outcome = json.loads(outcome_str if outcome_str not in [None, ""] else "{}")
    # resources = json.loads(resources_str if resources_str not in [None, ""] else "[]")

    # 使用映射表進行轉換
    motivation_tags = [
        motivation_mapping.get(tag[:2], tag[:2]) if tag.startswith("其他") else motivation_mapping.get(tag, tag)
        for tag in motivation.get("tags", [])
    ]
    policy_tags = [
        strategy_mapping.get(tag[:2], tag[:2]) if tag.startswith("其他") else strategy_mapping.get(tag, tag)
        for tag in strategies.get("tags", [])
    ]
    
    presentation_tags = [
        outcome_mapping.get(tag[:2], tag[:2]) if tag.startswith("其他") else outcome_mapping.get(tag, tag)
        for tag in outcome.get("tags", [])
    ]


    try:    
        project = Project(
            user_id=user.id,
            title=row.get("title"),
            description=row.get("description"),
            motivation=motivation_tags,
            motivation_description=motivation.get("description"),
            goal=row.get("goals", ""),
            content=row.get("content", ""),
            strategy=policy_tags,
            strategy_description=strategies.get("description"),
            # resource_name=[res.get("name", "") for res in resources],
            # resource_url=[res.get("url", "") for res in resources],
            resource = resources_str,
            outcome=presentation_tags,
            outcome_description=outcome.get("description"),
            is_public=row.get("isPublic", False),
            # start_date=
            # end_date=
            version = version, # depend on marathon 
        )
        session.add(project)
        session.flush()
        logger.info(f"新增 Project ID: {project.id}")
        return project
    except IntegrityError:
        session.rollback()  # 回滾變更
        logger.info(f"發現重複專案，跳過: {row.get('title')} (User ID: {user.id})")

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
    
    task_instance = kwargs['ti']  # 訪問 task_instance 來推送 XCom

    # 初始化統計數據
    statistics = {
        'total_processed': 0,
        'users_added': 0,
        'projects_added': 0,
        'milestones_added': 0,
        'tasks_added': 0,
        'errors': 0
    }
    

    try:
        old_marathons_df = fetch_old_marathons(engine)
        logger.info(f"共提取 {len(old_marathons_df)} 筆資料")

        for idx, row in old_marathons_df.iterrows():
            logger.info(f"處理第 {idx+1} 筆資料 (User ID: {row['userId']})")
            try:
                user = process_user(row, session)
                statistics['users_added'] += 1

                eligibility = process_eligibility(row, session)

                project = process_project(row, user, session, kwargs['date_flag'])
                statistics['projects_added'] += 1        
                if project is None:
                    continue   

                process_milestones(row, project, session)
                statistics['milestones_added'] += len(json.loads(row.get("milestones", "[]")))
                
                for milestone_data in json.loads(row.get("milestones", "[]")):
                    statistics['tasks_added'] += len(milestone_data.get("subMilestones", []))


                # 將 User 與 Project 連結
                # 目前 UserProject 一對多 所以不需要
                # link_user_project(user, project, session)

                # 將 Project 與 Marathon 連結
                marathon = session.query(Marathon).filter_by(event_id=row["eventId"]).first()
                if marathon:
                    link_project_marathon(project, marathon, session)
                    
                statistics['total_processed'] += 1
            except Exception as e:
                statistics['errors'] += 1
                logger.error(f"處理第 {idx+1} 筆資料時出錯: {e}")
                
        session.commit()
        logger.info("所有資料成功遷移至新表")
        

        # 推送統計數據到 XCom
        task_instance.xcom_push(key="statistics", value=statistics)
        logger.info(f"統計數據已推送至 XCom: {statistics}")
        
    except IntegrityError as e:
        session.rollback()
        logger.error(f"資料庫完整性錯誤: {e}")
    except Exception as e:
        session.rollback()
        logger.error(f"發生未預期錯誤: {e}")
    finally:
        session.close()



def set_project_milestone_nth_week():
    
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        try:
            project_ids = session.execute(
                text("SELECT DISTINCT project_id FROM public.milestone WHERE project_id IS NOT NULL")
            ).fetchall()
            
            for (project_id,) in project_ids:
                milestones = fetch_project_milestones(session, project_id)
                for milestone in milestones:
                    logger.info(f"milestones {milestone} in {project_id}")

                    existing = session.execute(
                        text("SELECT id FROM public.milestone WHERE id = :milestone_id"),
                        {"milestone_id": milestone["milestone_id"]}
                    ).fetchone()

                    if existing:
                        milestone_id = existing[0]
                        session.execute(
                            text("UPDATE public.milestone SET week = :week, updated_at = CURRENT_TIMESTAMP WHERE id = :id"),
                            {"week": milestone["week"], "id": milestone_id}
                        )
            
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating milestones: {e}")
            raise
        
    
def set_player_role():
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    valid_user_list = get_valid_contestants(session)
    logger.info(f"已繳款的使用者 ID : {valid_user_list} {len(valid_user_list)}")
    
    marthon_user_list = get_marthon_user_list(session)
    logger.info(f"註冊馬拉松的使用者 ID : {marthon_user_list}, {len(marthon_user_list)}")
    
    logger.info("將已繳款的使用者 設定role_id = 3")
    set_player_role_id(session, get_valid_contestants(session))
    
    # 將註冊馬拉松的使用者但繳款的使用者 設定role_id = ??

def set_mentor_role():
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    set_mentor_role_id(session)


def set_mentor_map_player():
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    mentor_dict = get_mentor_map_dict(session)
    insert_participant_into_mentor(session, mentor_dict)
    
    
    