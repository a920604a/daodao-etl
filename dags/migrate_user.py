from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Users, Contact, BasicInfo, Location, Area, Position
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

def process_and_migrate_users(**kwargs):
    """
    遷移舊用戶數據到新 schema（user, contact, basic_info, location, area）。
    包括事務處理，並生成統計報告。
    """
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 初始化統計變數
    total_processed = 0
    total_successful = 0
    total_failed = 0
    failed_records = []

    # 初始化各表插入計數器
    contact_inserted = 0
    basic_info_inserted = 0
    location_inserted = 0
    area_inserted = 0
    user_inserted = 0

    try:
        # 從舊表格中讀取數據
        old_user = session.execute("SELECT * FROM old_user").fetchall()

        # 輸出結果集，檢查所有欄位名稱
        logger.info("Fetched old_user data:")
        for row in old_user:
            logger.info(dict(row))  # 輸出資料結果檢查欄位名稱

        for i, user_record in enumerate(old_user):
            total_processed += 1
            try:
                # Debug輸出，查看是否存在欄位問題
                logger.info(type(user_record))
                logger.info(f"Processing {i} user_record:", dict(user_record))
                i += 1
                
                
                contact_list = {"instagram":"", "discord" : "", "line":"", "facebook":""}
                if user_record["contactList"]:
                    # 只有當 contactList 存在且有值時才解析 JSON 字串
                    try:
                        parsed_contact_list = json.loads(user_record["contactList"])
                        # 合併解析後的 contact_list 和預設的 contact_list
                        contact_list.update(parsed_contact_list)
                    except json.JSONDecodeError:
                        logger.info(f"Invalid JSON format in contactList for user {user_record['mongo_id']}.")
                        # 解析失敗時可以選擇保留 contact_list 為空字典，或者根據需求處理
                        
                logger.info(f'contact_list {contact_list}')


                # 將數據插入到 Contact 表
                contact = Contact(
                    google_id=user_record["googleID"],
                    photo_url=user_record["photoURL"],
                    is_subscribe_email=user_record["isSubscribeEmail"],
                    email=user_record["email"],
                    ig=contact_list.get("instagram"),  # 直接使用 get()，如果沒有 instagram，會返回 None
                    discord=contact_list.get("discord"),  # 同上
                    line=contact_list.get("line"),  # 同上
                    fb=contact_list.get("facebook"),  # 同上
                )
                session.add(contact)
                session.flush()  # 先提交，以獲取生成的 ID
                contact_inserted += 1  # 更新 contact 表插入數量

                # 處理 wish list，過濾不正確的 enum 值
                valid_enum_values = set(want_to_do_list_t.enums)
                valid_values = [
                    item for item in json.loads(user_record['wantToDoList'])
                    if item in valid_enum_values
                ]
                logger.info(valid_values)

                # 將數據插入到 BasicInfo 表
                basic_info = BasicInfo(
                    self_introduction=user_record["selfIntroduction"],
                    share_list = (
                        ','.join([item.strip() for item in user_record["share"].split('、')]) 
                        if user_record["share"] else ""
                    ),
                    want_to_do_list=cast(array(valid_values, type_=want_to_do_list_t), ARRAY(want_to_do_list_t))
                )
                session.add(basic_info)
                session.flush()
                basic_info_inserted += 1  # 更新 basic_info 表插入數量

                # 獲取區域和位置數據
                area_name = user_record["location"]
                logger.info(area_name)
                if area_name:
                    if "@" in area_name:
                        city, region = city_mapping.get(area_name.split('@')[1], "Other"), area_name.split('@')[-1]
                    else:
                        city, region = "Other", "Unknown"

                    area = session.execute(
                        'SELECT * FROM area WHERE "city" = :city', {"city": city}
                    ).fetchone()
                    if not area:
                        # 如果 Area 不存在，創建新區域
                        area = Area(city=city)
                        session.add(area)
                        session.flush()
                        area_inserted += 1  # 更新 area 表插入數量
                    location = Location(
                        area_id=area.id,
                        isTaiwan=True,
                        region=region,
                    )
                else:
                    location = Location(isTaiwan=False, region=None)
                session.add(location)
                session.flush()
                location_inserted += 1  # 更新 location 表插入數量

                logger.info(user_record["roleList"])
                valid_enum_values = set(identity_list_t.enums)
                valid_values = [
                    item for item in json.loads(user_record['roleList'])
                    if item in valid_enum_values
                ]
                logger.info(valid_values)

                # 處理 birthDay
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
                # 插入用戶數據到 user 表
                user = Users(
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
                    createdDate=datetime.fromisoformat(user_record['createdDate']).replace(tzinfo=None),  # 無時區
                    updatedDate=datetime.fromisoformat(user_record['updatedDate']).replace(tzinfo=None),  # 無時區
                    created_at=datetime.now(),  # for developer
                    created_by=kwargs["task_instance"].task.owner,
                    updated_at=datetime.now(),  # for developer
                    updated_by=kwargs["task_instance"].task.owner
                )
                
                l = list()
                for id in valid_values:
                    _identity = session.query(Position).filter(Position.name == id).first()
                    if _identity:
                        l.append(_identity)
                    else:
                        logger.info(f"Position not found for: {id}")

                logger.info(f"_identity {l}")
                user.identities = l
                                
                
                session.add(user)
                user_inserted += 1  # 更新 user 表插入數量

                # 提交整個事務
                session.commit()
                total_successful += 1
            except KeyError as e:
                logger.info(f"KeyError: Missing column {e} in user_record:", user_record)
                session.rollback()
                total_failed += 1
                failed_records.append(str(user_record))
            except IntegrityError as e:
                logger.info(f"Integrity error: {e}")
                session.rollback()
                total_failed += 1
                failed_records.append(str(user_record))
            except Exception as e:
                logger.info(f"Unexpected error: {e}")
                session.rollback()
                total_failed += 1
                failed_records.append(str(user_record))

        # 統計報告
        logger.info(f"Migration Summary Report:")
        logger.info(f"Total processed user: {total_processed}")
        logger.info(f"Total successful migrations: {total_successful}")
        logger.info(f"Total failed migrations: {total_failed}")
        logger.info(f"Contact table insertions: {contact_inserted}")
        logger.info(f"BasicInfo table insertions: {basic_info_inserted}")
        logger.info(f"Location table insertions: {location_inserted}")
        logger.info(f"Area table insertions: {area_inserted}")
        logger.info(f"User table insertions: {user_inserted}")
        if total_failed > 0:
            logger.info(f"Failed records:")
            for failed_record in failed_records:
                logger.info(failed_record)

    finally:
        session.close()

# 定義 PythonOperator 執行遷移過程
migrate_users_task = PythonOperator(
    task_id="migrate_old_users_to_new_schema",
    python_callable=process_and_migrate_users,
    dag=dag,
)

migrate_users_task
