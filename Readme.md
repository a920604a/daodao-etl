
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
- mongo_uri=.env.MONGO_URI
- postgres_uri =.env.POSTGRES_URI
- table_name=.env.MONGO_DB_NAME
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

1. users
2. groups
3. 馬拉松
4. 學習計畫
