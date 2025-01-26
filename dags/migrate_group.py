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
    tags=['migrate', 'groups'],
    default_args=default_args,
    description="Migrate data from old_activities table to groups and user_join_group tables",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)

def transform_and_load_data(**kwargs):
    engine = create_engine(postgres_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        logger.info("Reading data from old_activities table...")
        # 讀取舊表資料
        query = "SELECT * FROM public.old_activities"
        df = pd.read_sql(query, engine)
        
        # 批次處理資料
        batch_size = 1000
        total_records = len(df)
        successful_inserts = 0
        
        for i in range(0, total_records, batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_records = []
            join_group_records = []
            
            for _, row in batch.iterrows():
                # print(f"row {row}")
                try:
                    # 查找對應的 user
                    user = session.query(Users).filter_by(mongo_id=row['userId']).first()
                    if user is None:
                        logger.error(f"User with UUID {row['userId']} not found!")
                        continue
                    
                    # 從舊表中取得 group_type 和 partnerEducationStep 並拆分成多個值
                    # 確認 activityCategory 是否存在並解析為列表
                    # 移除大括號，解析 activityCategory
                    if pd.notna(row.get('activityCategory')):
                        cleaned_activity_category = str(row['activityCategory']).strip('{}')  # 移除大括號
                        group_type_list = [value.strip() for value in cleaned_activity_category.split(',') if value.strip()]
                        
                        
                        # 就地修改
                        for i, item in enumerate(group_type_list):
                            group_type_list[i] = group_type_mapping.get(item, "其他")
                        
                    else:
                        group_type_list = []

                    # 移除大括號，解析 partnerEducationStep
                    if pd.notna(row.get('partnerEducationStep')):
                        cleaned_partner_education_step = str(row['partnerEducationStep']).strip('{}')  # 移除大photo_url括號
                        partner_education_step_list = [value.strip() for value in cleaned_partner_education_step.split(',') if value.strip()]
                        
                        # 就地修改
                        for i, item in enumerate(partner_education_step_list):
                            partner_education_step_list[i] = partnerEducationStep_mapping.get(item, "不設限")
                            
                    else:
                        partner_education_step_list = []
                    
                    print(f"partner_education_step_list {partner_education_step_list}")
                    # 輸出解析結果
                    print(f"row['activityCategory']: {row['activityCategory']}, group_type_list: {group_type_list}")
                    print(f"row['partnerEducationStep']: {row['partnerEducationStep']}, partner_education_step_list: {partner_education_step_list}")

                    print(f"deadline {str(row['deadline']).strip('{}')}")
                    # 查詢 public.area 表的所有 city 與 id
                    area_mapping = {
                        area.city: area.id for area in session.query(Area).all()
                    }

                    # 將 row['area'] 分割為列表
                    area_list = str(row['area']).split(',')

                    # 獲取對應的 area_id 列表
                    area_ids = [area_mapping.get(area.strip()) for area in area_list if area.strip() in area_mapping]
                    print(f"area_ids {area_ids}")

                    # 判斷是否包含 '線上'
                    is_online = '線上' in area_list


                    # 創建新的 group 記錄
                    group = Group(
                        title=str(row['title'])[:255] if pd.notna(row['title']) else None,
                        photo_url=str(row['photoURL'])[:255] if pd.notna(row['photoURL']) else None,
                        photo_alt=str(row['photoAlt'])[:255] if pd.notna(row['photoAlt']) else None,
                        category=str(row['category'])[:255] if pd.notna(row['category']) else None,
                        group_type=group_type_list,  # 使用處理後的 group_type_list
                        partner_education_step=partner_education_step_list,  # 使用處理後的 partner_education_step_list
                        description=str(row['description'])[:255] if pd.notna(row['description']) else None,
                        area_id=area_ids,  # 根據需求調整
                        is_grouping=row['isGrouping'],
                        createdDate=datetime.fromisoformat(row['createdDate']).replace(tzinfo=None),
                        updatedDate=datetime.fromisoformat(row['updatedDate']).replace(tzinfo=None),
                        time=row['time'],  # time 需要對應正確格式
                        partner_style=str(row['partnerStyle'])[:255] if pd.notna(row['partnerStyle']) else None,
                        created_at=datetime.now(),
                        created_by=user.id,  # 使用對應的 user.id
                        updated_at=datetime.now(),
                        updated_by=kwargs["task_instance"].task.owner,
                        motivation=str(row['motivation'])[:255] if pd.notna(row['motivation']) else None,
                        contents=str(row['content'])[:255] if pd.notna(row['content']) else None,
                        expectation_result=str(row['outcome'])[:255] if pd.notna(row['outcome']) else None,
                        notice=str(row['notice'])[:255] if pd.notna(row['notice']) else None,
                        tag_list=str(row['tagList'])[:255] if pd.notna(row['tagList']) else None,
                        group_deadline=pd.to_datetime(row['deadline']) if pd.notna(row['deadline']) else None,
                        hold_time=None,  # 根據需求調整
                        is_online=is_online,  # 根據需求調整
                        TBD=False,  # 根據需求調整
                    )
                    batch_records.append(group)
                    
                    # 創建 user_join_group 記錄，表示發起人
                    user_join_group = UserJoinGroup(
                        user_id=user.id,
                        group_id=None,  # 設置為None，因為 group 尚未插入資料庫
                        group_participation_role_t='Initiator',  # 發起人角色
                        participated_at=pd.to_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                    )
                    join_group_records.append(user_join_group)
                    
                except Exception as e:
                    logger.error(f"Error processing row: {row}")
                    logger.error(f"Error details: {str(e)}")
                    continue

            # 插入 groups 資料並更新 user_join_group
            try:
                # 批次插入 groups
                session.bulk_save_objects(batch_records)
                session.commit()
                
                # 更新 user_join_group 中的 group_id
                for group, join_group in zip(batch_records, join_group_records):
                    join_group.group_id = group.id
                session.bulk_save_objects(join_group_records)
                session.commit()

                successful_inserts += len(batch_records)
                logger.info(f"Processed {successful_inserts}/{total_records} records")
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Integrity error in batch: {str(e)}")
                # 這裡可以添加更詳細的錯誤處理邏輯
            except Exception as e:
                session.rollback()
                logger.error(f"Error in batch: {str(e)}")
                raise
        
        logger.info(f"Migration completed. Successfully inserted {successful_inserts} records")
        
        # 驗證資料
        new_count = session.query(Group).count()
        logger.info(f"Total records in new table: {new_count}")
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise
    finally:
        session.close()

    
# 定義 PythonOperator 執行遷移過程
migrate_activities_task = PythonOperator(
    task_id="migrate_old_activities_to_groups",
    python_callable=transform_and_load_data,
    dag=dag,
)

migrate_activities_task
