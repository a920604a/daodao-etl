# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError
# from models import  Resource
# from config import postgres_uri
# import json
# import uuid
# import pandas as pd
# from utils.code_enum import want_to_do_list_t, role_list_t
# from utils.code import city_mapping
# from sqlalchemy.sql.expression import cast
# from sqlalchemy.dialects.postgresql import array, ARRAY
# import logging

# #設定日誌
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# #設定DAG name和定義參數
# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "email_on_failure": False,
#     "email_on_retry": False,
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5),
# }

# dag = DAG(
#     "migrate_old_resource_to_new_resource",
#     tags=['migrate', 'resource'],
#     default_args=default_args,
#     description="Migrate data from old_resource table to the new schema tables",
#     schedule_interval=None,
#     start_date=datetime(2023, 12, 9),
#     catchup=False,
# )

# def transform_old_resource_to_new_resource(**kwargs):
#     engine = create_engine(postgres_uri)
#     Session = sessionmaker(bind=engine)
#     session = Session()
    
#     try:
#         logger.info("Reading data from old_resource table...")
#         # 讀取舊表資料
#         query = "SELECT * FROM public.old_resource"
#         df = pd.read_sql(query, engine)
        
        
#         # 批次處理資料
#         batch_size = 1000
#         total_records = len(df)
#         successful_inserts = 0
        
#         for i in range(0, total_records, batch_size):
#             batch = df.iloc[i:i+batch_size]
#             batch_records = []
#             for _, row in batch.iterrows():
#                 try:
#                     resource = Resource(
#                         # uuid=uuid.uuid4(),
#                         # image_url=str(row['Social Image'])[:255] if pd.notna(row['Social Image']) else None,
#                         # author_list=str(row['作者']) if pd.notna(row['作者']) else None,
#                         # tags=str(row['Tags'])[:255] if pd.notna(row['Tags']) else None,
#                         # name=str(row['Name'])[:255] if pd.notna(row['Name']) else None,
#                         # ai_summary=str(row['AI 摘要']) if pd.notna(row['AI 摘要']) else None,
#                         # description=str(row['Description']) if pd.notna(row['Description']) else None,
#                         # content=None,
#                         # created_at=pd.to_datetime(row['Created']) if pd.notna(row['Created']) else None
                        
#                         created_by_user_id=,
#                         image_url=,
#                         resource_name=,
#                         cost=,
#                         tag_list=,
#                         username = ,
#                         age = ,
#                         type_list = Column(Text)
#                         url_link = Column(Text)
#                         filed_name_list = Column(Text)
#                         video_url = Column(Text)
#                         introduction = Column(Text)
#                         area = Column(Text)
#                         supplement = Column(Text)

                        
                        
#                     )
#                     batch_records.append(resource)
#                 except Exception as e:
#                     logger.error(f"Error processing row: {row}")
#                     logger.error(f"Error details: {str(e)}")
#                     continue
            
#             try:
#                 session.bulk_save_objects(batch_records)
#                 session.commit()
#                 successful_inserts += len(batch_records)
#                 logger.info(f"Processed {successful_inserts}/{total_records} records")
#             except IntegrityError as e:
#                 session.rollback()
#                 logger.error(f"Integrity error in batch: {str(e)}")
#                 # 這裡可以添加更詳細的錯誤處理邏輯
#             except Exception as e:
#                 session.rollback()
#                 logger.error(f"Error in batch: {str(e)}")
#                 raise
        
#         logger.info(f"Migration completed. Successfully inserted {successful_inserts} records")
        
#         # 驗證資料
#         new_count = session.query(Resource).count()
#         logger.info(f"Total records in new table: {new_count}")
        
#     except Exception as e:
#         logger.error(f"Migration failed: {str(e)}")
#         raise
#     finally:
#         session.close()
    
    
    
# # 定義 PythonOperator 執行遷移過程
# migrate_resource_task = PythonOperator(
#     task_id="migrate_old_data_to_new_resource",
#     python_callable=transform_old_resource_to_new_resource,
#     dag=dag,
# )

# migrate_resource_task


