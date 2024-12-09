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
    "process_and_write_old_users",
    default_args=default_args,
    description="Process all users from old_users table and write to users table",
    schedule_interval=None,  # 只運行一次
    start_date=datetime(2023, 12, 9),
    catchup=False,
)


# 定義處理邏輯的函數
def process_and_write_users():
    # 設置資料庫連接
    engine = create_engine(postgres_uri)

    old_query = "SELECT * FROM public.old_users"

    try:
        with engine.connect() as connection:
            # 執行查詢
            result = connection.execute(text(old_query))

            # 遍歷所有使用者數據
            for row in result:
                # 提取需要的欄位
                old_user_id = row["id"]
                email = row["email"]
                name = row["name"]
                google_id = row["googleID"]
                photo_url = row["photoURL"]
                interest_list = row["interestList"]
                is_open_location = row["isOpenLocation"]
                is_open_profile = row["isOpenProfile"]
                role_list = row["roleList"]
                self_introduction = row["selfIntroduction"]
                created_date = row["createdDate"]
                updated_date = row["updatedDate"]

                # 構建插入資料
                insert_query = """
                INSERT INTO public.users (
                    "_id", email, name, googleID, photoURL, interestList, 
                    isOpenLocation, isOpenProfile, roleList, selfIntroduction, 
                    createdDate, updatedDate
                )
                VALUES (
                    :_id, :email, :name, :googleID, :photoURL, :interestList, 
                    :isOpenLocation, :isOpenProfile, :roleList, :selfIntroduction, 
                    :createdDate, :updatedDate
                )
                ON CONFLICT ("_id") DO NOTHING;
                """

                # 執行插入操作
                connection.execute(
                    text(insert_query),
                    {
                        "_id": old_user_id,
                        "email": email,
                        "name": name,
                        "googleID": google_id,
                        "photoURL": photo_url,
                        "interestList": interest_list,
                        "isOpenLocation": is_open_location,
                        "isOpenProfile": is_open_profile,
                        "roleList": role_list,
                        "selfIntroduction": self_introduction,
                        "createdDate": created_date,
                        "updatedDate": updated_date,
                    },
                )

                print(f"Inserted user {old_user_id} into users table")

    except Exception as e:
        print(f"Error occurred: {e}")


# 定義 PythonOperator 執行任務
process_and_write_users_task = PythonOperator(
    task_id="process_and_write_users_to_new_table",
    python_callable=process_and_write_users,
    dag=dag,
)

# 設置 DAG 任務執行順序
process_and_write_users_task
