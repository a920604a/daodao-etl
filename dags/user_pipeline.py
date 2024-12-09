from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from config import postgres_uri


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
    "migrate_old_users_to_new_users",
    default_args=default_args,
    description="Migrate data from old_users to new public.users schema",
    schedule_interval=None,
    start_date=datetime(2023, 12, 9),
    catchup=False,
)


def migrate_old_to_new_users():
    """
    從 `old_users` 數據表遷移數據到新的 `public.users` 結構中。
    """
    # 設置資料庫連接
    engine = create_engine(postgres_uri)

    # 從舊表中查詢所有數據
    old_query = "SELECT * FROM public.old_users"

    # 遍歷每行數據並插入到新結構中
    try:
        with engine.connect() as connection:
            # 執行查詢
            result = connection.execute(text(old_query))

            # 遍歷每個老數據記錄並轉換插入到新用戶表中
            for row in result:
                # 提取舊數據並轉換
                old_id = str(row["_id"])  # 將 MongoDB ID 轉為字符串格式
                email = row["email"]
                name = row["name"]
                google_id = row["googleID"]
                photo_url = row["photoURL"]
                interest_list = row["interestList"]
                is_open_location = row["isOpenLocation"]
                is_open_profile = row["isOpenProfile"]
                created_date = row["createdDate"]
                updated_date = row["updatedDate"]

                # 構建插入數據的 SQL 語句
                insert_query = """
                INSERT INTO public.users (
                    uuid,
                    "_id",
                    gender,
                    language,
                    contact_id,
                    is_open_location,
                    location_id,
                    nickname,
                    role_list,
                    is_open_profile,
                    "birthDay",
                    basic_info_id,
                    created_by,
                    created_at,
                    updated_by,
                    updated_at
                )
                VALUES (
                    gen_random_uuid(),
                    :_id,
                    NULL,
                    NULL,
                    NULL,
                    :is_open_location,
                    NULL,
                    :name,
                    '{}',
                    :is_open_profile,
                    NULL,
                    NULL,
                    :email,
                    NOW(),
                    :email,
                    NOW()
                )
                ON CONFLICT ("_id") DO NOTHING;
                """.format("[]")  # 空字串處理 role_list 為空值

                # 執行插入
                connection.execute(
                    text(insert_query),
                    {
                        "_id": old_id,
                        "is_open_location": is_open_location,
                        "is_open_profile": is_open_profile,
                        "name": name,
                        "email": email,
                    },
                )

                print(f"Migrated user with old _id {old_id} to new users table.")

    except Exception as e:
        print(f"Error occurred during migration: {e}")


# 定義 PythonOperator 執行任務
migrate_users_task = PythonOperator(
    task_id="migrate_users_task",
    python_callable=migrate_old_to_new_users,
    dag=dag,
)
