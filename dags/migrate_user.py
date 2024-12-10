from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, Column, Text, Boolean, BigInteger, MetaData, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from models import Base, User, Contact, BasicInfo, Location, Area
from config import postgres_uri
import json
from utils.code_enum import want_to_do_list_t
from utils.code import city_mapping


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
    "migrate_old_users_to_new_schema",
    default_args=default_args,
    description="Migrate data from old_users table to the new schema tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)


def process_and_migrate_users():
    """
    遷移舊用戶數據到新 schema（users, contact, basic_info, location, area）。
    包括事務處理，確保所有數據一致性。
    """
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 從舊表格中讀取數據
        old_users = session.execute("SELECT * FROM old_users").fetchall()

        # 輸出結果集，檢查所有欄位名稱
        print("Fetched old_users data:")
        i=0
        for row in old_users:
            print(dict(row))  # 輸出資料結果檢查欄位名稱

        for user_record in old_users:
            try:
                # Debug輸出，查看是否存在欄位問題
                print(f"Processing {i} user_record:", dict(user_record))
                i+=1

                # 將數據插入到 Contact 表
                contact = Contact(
                    google_id=user_record["googleID"],
                    photo_url=user_record["photoURL"],
                    is_subscribe_email=user_record["isSubscribeEmail"],
                    email=user_record["email"],
                    ig=None,
                    discord=None,
                    line=None,
                    fb=None,
                )
                session.add(contact)
                session.flush()  # 先提交，以獲取生成的 ID
                
    
    
                valid_enum_values = set(want_to_do_list_t.enums)  # 從 SQLAlchemy ENUM 類型中提取合法值

                valid_values = [item for item in json.loads(user_record['wantToDoList']) if item in valid_enum_values]
            
                # 將數據插入到 BasicInfo 表
                basic_info = BasicInfo(
                    self_introduction=user_record["selfIntroduction"],
                    share_list=','.join([item.strip() for item in user_record["share"].split('、')]),
                    want_to_do_list=valid_values  
                )
                session.add(basic_info)
                session.flush()

                # 獲取區域和位置數據
                area_name = user_record["location"]
                if area_name:
                    city = city_mapping[area_name.split('@')[1]]
                    area = session.execute(
                        "SELECT * FROM area WHERE City = :city", {"city": city}
                    ).fetchone()
                    if not area:
                        # 如果 Area 不存在，創建新區域
                        area = Area(city=area_name)
                        session.add(area)
                        session.flush()
                    location = Location(
                        area_id=area.id,
                        is_taiwan=True,
                        region=area_name,
                    )
                else:
                    location = Location(is_taiwan=False, region=None)
                session.add(location)
                session.flush()

                # 插入用戶數據到 users 表
                user = User(
                    uuid=str(uuid.uuid4()),
                    gender=user_record["gender"],
                    education_stage=user_record["educationStage"],
                    role_list=user_record["roleList"].split(","),
                    contact_id=contact.id,
                    location_id=location.id,
                    basic_info_id=basic_info.id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                session.add(user)

                # 提交整個事務
                session.commit()
            except KeyError as e:
                # 如果訪問欄位時發生 KeyError，輸出 debug 訊息
                print(f"KeyError: Missing column {e} in user_record:", user_record)
                session.rollback()
            except IntegrityError as e:
                print(f"Integrity error: {e}")
                session.rollback()
                continue
    except Exception as e:
        print(f"Unexpected error: {e}")
        session.rollback()
    finally:
        session.close()


# 定義 PythonOperator 執行遷移過程
migrate_users_task = PythonOperator(
    task_id="migrate_old_users_to_new_schema",
    python_callable=process_and_migrate_users,
    dag=dag,
)

migrate_users_task
