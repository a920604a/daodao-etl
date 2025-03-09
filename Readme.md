
## Launch setting
echo -e "AIRFLOW_UID=$(id -u)" >> .env

`.env` like
```
_AIRFLOW_WWW_USER_USERNAME=
_AIRFLOW_WWW_USER_PASSWORD=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
DAO_POSTGRES_USER=
DAO_POSTGRES_PASSWORD=
DAO_POSTGRES_DB=
MONGO_URI=mongodb://mongo-daodao:27017
MONGO_DB_NAME=
POSTGRES_URI=postgresql+psycopg2://DAO_POSTGRES_USER:DAO_POSTGRES_PASSWORD@postgres-daodao:5432/DAO_POSTGRES_DB
AIRFLOW_UID=
```

rm -rf ./logs ./plugins ./config ./data
mkdir -p ./logs ./plugins ./config ./data ./data/airflow-db-volume

docker compose down --volumes --remove-orphans --rmi all


docker compose run --rm airflow-init 
docker compose up -d
docker exec mongo-daodao mongorestore /backup

## Airflow setting
Airflow Admin -> Variable
- MONGO_URI=.env.MONGO_URI
- POSTGRES_URI =.env.POSTGRES_URI
- MONGO_DB_NAME=.env.MONGO_DB_NAME
- NOTION_API_KEY=.env.NOTION_API_KEY
- NOTION_DATABASE_RESOURCE_ID=.env.NOTION_DATABASE_RESOURCE_ID
- NOTION_DATABASE_STORE_ID=.env.NOTION_DATABASE_STORE_ID

## TODO
- 找揪團、找夥伴 
  - 資料可以導入pgsql 但需要normal
- 找故事
  - https://www.notion.so/daodaoedu/776e54be135a47198c5a50b0f0868e68
  - 目前沒欠缺 內文 (notion-title, notion-property, notioh-page-content) , 是否要存入 SQL DB
- 找資源
  - https://daodaoedu.notion.site/edc9ef670495412c803d4028510c518e?v=db43b8f6d18f48f0b64f61d80b65e894
  - 思考 領域 list 上 快速搜尋
  - 思考 熱門標籤 上 快速搜尋,使用 Cache 




- 參考電傷網站如何在 多個 tag 底下 建立schema 
- review 馬拉松。活動規劃、報名資料、分享區、公告
- 使用者、角色、權限、個人名片


## metadata setting
`.marathon.json` 
```
{
    "paid_names_list": [
        "username_1",
        "username_2",
        "username_3"
    ],
    "mentor_list": [
        "mentor1@gmail.com",
        "mentor2@gmail.com",
        "mentor3@gmail.com",
    ]
     "mentor_mapping": {
        "mentor1@gmail.com": [
            "username_1",
            "username_2"
        ],
        "mentor2@gmail.com": [
            "username_3"
        ]
    }
}
```
`.env.json`
```json
{
  "MONGO_URI": "",
  "MONGO_OLD_DB_NAME": "2025-01-30-prod",
  "MONGO_DB_NAME": "2025-02-17-prod",
  "POSTGRES_URI": "",
  "NOTION_API_KEY": "",
  "NOTION_DATABASE_RESOURCE_ID": "",
  "NOTION_DATABASE_STORE_ID": ""
}

```

migrate_user -> migrate_groups
1. users
2. groups
3. 馬拉松
4. 學習計畫
   1. 便利貼(可與專案有關無關)
   2. 復盤(針對計畫，每兩週必須針對計畫做一次，馬拉松限制兩週做一次，考慮不需兩週)
   3. 學習成果(針對計畫且只會有一個)
   4. 補上 user schema
   5. mentor mapping 學生/馬拉松學生
   6. project api



`docker network create shared-daodao-network`
