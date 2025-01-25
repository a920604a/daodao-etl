from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pymongo
from sqlalchemy import create_engine
import os
import json
from bson import ObjectId




class MongoToPostgresETL:
    def __init__(self, mongo_uri, db_name, postgres_uri):
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.db_name = db_name
        self.postgres_engine = create_engine(postgres_uri)

    def extract_data(self, collection_name, **kwargs):
        print(f"Extracting data from MongoDB collection: {collection_name}")
        db = self.mongo_client[self.db_name]
        collection = db[collection_name]
        data = list(collection.find({}))
        print(f"Extracted {len(data)} records from {collection_name}")

        for record in data:
            # 將 _id 欄位格式化為 BSON 格式
            # record["_id"] = {"$oid": str(record["_id"])}
            record["_id"] = str(record["_id"]).zfill(24)[:24]  # MongoDB 的 ObjectId 通常是 24 位十六進位字符串。確保字符串為 24 位十六進位格式
            
            for key in record.keys():
                if isinstance(record[key], datetime):
                    record[key] = {"$date": record[key].isoformat()}

        df = pd.DataFrame(data)
        # 1. 重命名 _id 字段
        df.rename(columns={"_id": "mongo_id"}, inplace=True)
        print(df.head())
        print(df.columns)
        kwargs["ti"].xcom_push(key="extracted_df", value=df.to_dict(orient="records"))
        
        
    def convert_bson_to_json(self, obj):
        """
        遞歸處理 BSON 對象，將其轉換為可 JSON 序列化的格式。
        """
        if isinstance(obj, dict):
            # 遍歷字典中的每個鍵值對
            return {key: self.convert_bson_to_json(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            # 遍歷列表中的每個元素
            return [self.convert_bson_to_json(item) for item in obj]
        elif isinstance(obj, ObjectId):
            # 將 ObjectId 轉換為字符串
            return str(obj)
        elif isinstance(obj, datetime):
            # 將 datetime 轉換為 ISO 格式
            return {"$date": obj.isoformat()}
        else:
            # 返回其他非 BSON 類型的原始值
            return obj

    def extract_marathon_data(self, collection_name, **kwargs):
        print(f"Extracting data from MongoDB collection: {collection_name}")
        db = self.mongo_client[self.db_name]
        collection = db[collection_name]
        data = list(collection.find({}))
        print(f"Extracted {len(data)} records from {collection_name}")

        # 遞歸處理所有 BSON 數據，轉換為 JSON 可序列化格式
        data = [self.convert_bson_to_json(record) for record in data]

        # 將數據轉換為 DataFrame
        df = pd.DataFrame(data)

        # 重命名 _id 為 mongo_id
        df.rename(columns={"_id": "mongo_id"}, inplace=True)

        # 輸出查看 DataFrame
        print(df.head())
        print(df.columns)

        # 確保 DataFrame 中所有值都可以 JSON 序列化（例如將日期轉換為字符串格式）
        for column in df.select_dtypes(include=["datetime64[ns]"]).columns:
            df[column] = df[column].astype(str)

        # 將 DataFrame 傳遞給 XCom
        kwargs["ti"].xcom_push(key="extract_marathon_df", value=df.to_dict(orient="records"))

    def transform_users(self, **kwargs):
        extracted_data = kwargs["ti"].xcom_pull(key="extracted_df")
        df = pd.DataFrame(extracted_data)
        print(f"Transforming user data {df.columns}")

        if "mongo_id" in df.columns:
            df["mongo_id"] = df["mongo_id"].astype(str)

        json_columns = [
            "interestList",
            "roleList",
            # "tagList",
            "wantToDoList",
            "contactList",
        ]
        for column in json_columns:
            df[column] = df[column].apply(
                lambda x: json.dumps(x) if isinstance(x,( list, dict)) else None
            )

        df["isOpenLocation"] = df["isOpenLocation"].astype(bool)
        df["isOpenProfile"] = df["isOpenProfile"].astype(bool)
        df["isSubscribeEmail"] = df["isSubscribeEmail"].astype(bool)

        print("User transformation complete")
        print(df.iloc[0])
        kwargs["ti"].xcom_push(
            key="transform_users", value=df.to_dict(orient="records")
        )

    def transform_activities(self, **kwargs):
        extracted_data = kwargs["ti"].xcom_pull(key="extracted_df")
        df = pd.DataFrame(extracted_data)
        print(f"Transforming activities data {df.columns}")

        if "mongo_id" in df.columns:
            df["mongo_id"] = df["mongo_id"].astype(str)

        # json_columns = ['category', 'area', 'partnerEducationStep', 'tagList']
        # for column in json_columns:
        #     df[column] = df[column].apply(lambda x: json.dumps(x) if isinstance(x, list) else None)
        
        
        
        def parse_date(date_dict):
            if isinstance(date_dict, dict) and "$date" in date_dict:
                date_str = date_dict["$date"]
                return datetime.fromisoformat(date_str[:-3])
            return pd.NaT
            
        df["deadline"] = df["deadline"].apply(parse_date)
        if "deadline" in df.columns:
            df["deadline"] = pd.to_datetime(
                df["deadline"], errors="coerce"
            ).dt.strftime("%Y-%m-%d %H:%M:%S")
            
        print("Activities transformation complete")
        kwargs["ti"].xcom_push(
            key="transform_activities", value=df.to_dict(orient="records")
        )
    

    def transform_marathons(self, **kwargs):
        """
        转换 MongoDB 中的马拉松数据，使其适合加载到 PostgreSQL
        """
        # 从 XCom 中提取数据
        extracted_data = kwargs["ti"].xcom_pull(key="extract_marathon_df")
        df = pd.DataFrame(extracted_data)

        # 需要转为 JSON 字符串的列
        json_columns = [
            "motivation", "strategies", "resources", "milestones", "outcomes", "pricing"
        ]

        def is_valid_json(data):
            """检查字符串是否是有效的 JSON 格式"""
            try:
                json.loads(data)
                return True
            except (TypeError, json.JSONDecodeError):
                return False

        def json_serial(obj):
            """处理 datetime 的序列化"""
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        def process_nested_structure(value):
            """递归处理嵌套结构，解析日期并转换为 JSON"""
            if isinstance(value, dict):
                for key, val in value.items():
                    if isinstance(val, dict) and "$date" in val:
                        # 处理 MongoDB 的日期格式
                        value[key] = datetime.fromisoformat(val["$date"][:-3])
                    else:
                        value[key] = process_nested_structure(val)
            elif isinstance(value, list):
                return [process_nested_structure(item) for item in value]
            return value

        def process_json_column(value):
            """处理 JSON 字段，包括解析嵌套对象和日期格式"""
            if isinstance(value, dict) or isinstance(value, list):
                # 如果是嵌套结构，直接转换为 JSON 字符串
                return json.dumps(value, ensure_ascii=False, default=json_serial)
            if isinstance(value, str) and is_valid_json(value):
                # 如果是有效的 JSON 字符串，保持原样
                return json.dumps(json.loads(value), ensure_ascii=False, default=json_serial)
            return None

        # 检查并处理需要转换的列
        for column in json_columns:
            if column in df.columns:
                # 先解析 MongoDB 日期格式
                df[column] = df[column].apply(lambda x: process_nested_structure(x) or x)
                # 转换为 JSON 字符串
                df[column] = df[column].apply(process_json_column)

        # 输出第一个记录查看是否转换正确
        print(df.head())
        kwargs["ti"].xcom_push(
            key="transform_marathons", value=df.to_dict(orient="records")
        )

        return df

    
    def load_data(self, table_name,target_table_name,  **kwargs):
        transform_data = kwargs["ti"].xcom_pull(key=f"transform_{table_name}")
        df = pd.DataFrame(transform_data)
        print(df.head())

        def parse_date(date_dict):
            if isinstance(date_dict, dict) and "$date" in date_dict:
                date_str = date_dict["$date"]
                return datetime.fromisoformat(date_str[:-3])
            return pd.NaT

        df["createdDate"] = df["createdDate"].apply(parse_date)
        df["updatedDate"] = df["updatedDate"].apply(parse_date)

        df["createdDate"] = pd.to_datetime(
            df["createdDate"], errors="coerce"
        ).dt.strftime("%Y-%m-%d %H:%M:%S")
        df["updatedDate"] = pd.to_datetime(
            df["updatedDate"], errors="coerce"
        ).dt.strftime("%Y-%m-%d %H:%M:%S")

        df["created_at"] = pd.to_datetime("now")
        df["created_by"] = kwargs["task_instance"].task.owner
        df["updated_at"] = pd.to_datetime("now")
        df["updated_by"] = kwargs["task_instance"].task.owner
        
        
        import json
        for column in df.select_dtypes(include=["object"]).columns:
            if df[column].apply(lambda x: isinstance(x, dict)).any():
                df[column] = df[column].apply(json.dumps)


        try:
            df.to_sql(
                target_table_name,
                con=self.postgres_engine,
                if_exists="append",
                index=False,
                method="multi",
            )
        except Exception as e:
            print(f"Failed to load data into {target_table_name}: {e}")


