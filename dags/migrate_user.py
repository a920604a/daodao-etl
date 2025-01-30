from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User, Contact, BasicInfo, Location, Area, Position, UserProfile
from config import postgres_uri
import json
import logging
from utils.code_enum import want_to_do_list_t, identity_list_t
from utils.code import city_mapping
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import array, ARRAY

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    "migrate_old_users_to_new_user",
    tags=['migrate', 'user'],
    default_args=default_args,
    description="Migrate data from old_user table to the new schema tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)

# 初始化統計變數
statistics = {
    "total_processed": 0,
    "total_successful": 0,
    "total_failed": 0,
    "failed_records": [],
    "contact_inserted": 0,
    "basic_info_inserted": 0,
    "location_inserted": 0,
    "user_inserted": 0,
    "area_inserted": 0,
    "user_profile_inserted": 0,
}

def process_contact(user_record):
    contact_list = {"instagram":"", "discord" : "", "line":"", "facebook":""}
    if user_record["contactList"]:
        try:
            parsed_contact_list = json.loads(user_record["contactList"])
            contact_list.update(parsed_contact_list)
        except json.JSONDecodeError:
            logger.info(f"Invalid JSON format in contactList for user {user_record['mongo_id']}.")

    logger.info(f'contact_list {contact_list}')
    
    contact = Contact(
        google_id=user_record["googleID"],
        photo_url=user_record["photoURL"],
        is_subscribe_email=user_record["isSubscribeEmail"],
        email=user_record["email"],
        ig=contact_list.get("instagram"),
        discord=contact_list.get("discord"),
        line=contact_list.get("line"),
        fb=contact_list.get("facebook"),
    )
    return contact

def process_basic_info(user_record):
    valid_enum_values = set(want_to_do_list_t.enums)
    valid_values = [
        item for item in json.loads(user_record['wantToDoList'])
        if item in valid_enum_values
    ]
    logger.info(valid_values)

    basic_info = BasicInfo(
        self_introduction=user_record["selfIntroduction"],
        share_list=(
            ','.join([item.strip() for item in user_record["share"].split('、')]) 
            if user_record["share"] else ""
        ),
        want_to_do_list=cast(array(valid_values, type_=want_to_do_list_t), ARRAY(want_to_do_list_t))
    )
    return basic_info

def process_location(user_record, session, statistics):
    area_name = user_record["location"]
    if area_name:
        if "@" in area_name:
            city, region = city_mapping.get(area_name.split('@')[1], "Other"), area_name.split('@')[-1]
        else:
            city, region = "Other", "Unknown"

        area = session.execute(
            'SELECT * FROM area WHERE "city" = :city', {"city": city}
        ).fetchone()
        if not area:
            area = Area(city=city)
            session.add(area)
            session.flush()
            statistics["area_inserted"] += 1
        location = Location(
            area_id=area.id,
            isTaiwan=True,
            region=region,
        )
    else:
        location = Location(isTaiwan=False, region=None)
    return location, statistics

def process_identity(user_record, session):
    valid_enum_values = set(identity_list_t.enums)
    valid_values = [
        item for item in json.loads(user_record['roleList'])
        if item in valid_enum_values
    ]
    logger.info(valid_values)

    identities = []
    for id in valid_values:
        _identity = session.query(Position).filter(Position.name == id).first()
        if _identity:
            identities.append(_identity)
        else:
            logger.info(f"Position not found for: {id}")
    return identities

def process_birth_day(user_record):
    birth_day_str = user_record['birthDay']
    if birth_day_str:
        try:
            if 'T' in birth_day_str:
                birth_day = datetime.strptime(birth_day_str.split('T')[0], "%Y-%m-%d").date()
            elif '/' in birth_day_str:
                birth_day = datetime.strptime(birth_day_str, "%Y/%m/%d").date()
            else:
                birth_day = None
        except ValueError as e:
            logger.info(f"Invalid date format for birthDay: {birth_day_str}. Error: {e}")
            birth_day = None
    else:
        birth_day = None
    return birth_day

def process_user_profile(user_record, session, user):
    user_profile = UserProfile(
        user_id=user.id,
        nickname=getattr(user_record, "nickname", None),
        bio=getattr(user_record, "selfIntroduction", None),
        skills=getattr(user_record, "skills", []),
        interests=getattr(user_record, "interests", []),
        learning_needs=getattr(user_record, "learningNeeds", []),
        contact_info=getattr(user_record, "contactInfo", {}),
        is_public=getattr(user_record, "isPublic", True),
    )
    session.add(user_profile)
    session.flush()
    return user_profile

def process_and_migrate_users(**kwargs):
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    statistics = kwargs["statistics"]

    try:
        # 從舊表格中讀取數據
        old_user = session.execute("SELECT * FROM old_user").fetchall()

        for i, user_record in enumerate(old_user):
            statistics["total_processed"] += 1
            try:
                contact = process_contact(user_record)
                session.add(contact)
                session.flush()
                statistics["contact_inserted"] += 1

                basic_info = process_basic_info(user_record)
                session.add(basic_info)
                session.flush()
                statistics["basic_info_inserted"] += 1

                location, statistics = process_location(user_record, session, statistics)
                session.add(location)
                session.flush()
                statistics["location_inserted"] += 1

                identities = process_identity(user_record, session)

                birth_day = process_birth_day(user_record)

                user = User(
                    mongo_id=user_record["mongo_id"],
                    gender=user_record["gender"] if user_record["gender"] else 'other',
                    language=None,
                    education_stage=user_record["educationStage"] if user_record["educationStage"] else None,
                    tag_list=user_record['tagList'],
                    is_open_location=user_record['isOpenLocation'],
                    nickname=user_record['name'] if user_record['name'] else None,
                    is_open_profile=user_record['isOpenProfile'],
                    birth_date=birth_day,
                    contact_id=contact.id,
                    location_id=location.id,
                    basic_info_id=basic_info.id,
                    createdDate=datetime.fromisoformat(user_record['createdDate']).replace(tzinfo=None),
                    updatedDate=datetime.fromisoformat(user_record['updatedDate']).replace(tzinfo=None),
                    created_at=datetime.now(),
                    created_by=kwargs["task_instance"].task.owner,
                    updated_at=datetime.now(),
                    updated_by=kwargs["task_instance"].task.owner,
                    identities=identities
                )

                session.add(user)
                session.flush()
                statistics["user_inserted"] += 1
                
                
                # 在這裡插入 UserProfile 紀錄
                
                logger.info(f" user_record {user_record}")

                user_profile = process_user_profile(user_record, session, user)
                statistics["user_profile_inserted"] += 1

                session.commit()
                statistics["total_successful"] += 1
            except Exception as e:
                logger.info(f"Error processing user {user_record['mongo_id']}: {e}")
                session.rollback()
                statistics["total_failed"] += 1
                statistics["failed_records"].append(str(user_record))

        # 統計報告
        logger.info(f"======Migration Summary Report:======")
        logger.info(f"Total processed user: {statistics['total_processed']}")
        logger.info(f"Total successful migrations: {statistics['total_successful']}")
        logger.info(f"Total failed migrations: {statistics['total_failed']}")
        logger.info(f"Contact table insertions: {statistics['contact_inserted']}")
        logger.info(f"BasicInfo table insertions: {statistics['basic_info_inserted']}")
        logger.info(f"Location table insertions: {statistics['location_inserted']}")
        logger.info(f"Area table insertions: {statistics['area_inserted']}")
        logger.info(f"User table insertions: {statistics['user_inserted']}")
        logger.info(f"User Profile table insertions: {statistics['user_profile_inserted']}")
        if statistics['total_failed'] > 0:
            logger.info(f"Failed records:")
            for failed_record in statistics['failed_records']:
                logger.info(failed_record)

    finally:
        session.close()

# 定義 PythonOperator 執行遷移過程
migrate_users_task = PythonOperator(
    task_id="migrate_old_users_to_new_schema",
    python_callable=process_and_migrate_users,
    op_kwargs={"statistics": statistics},
    dag=dag,
)

migrate_users_task
