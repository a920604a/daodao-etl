
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
docker compose down --volumes --remove-orphans

docker compose run --rm airflow-init 
docker compose up -d
docker exec mongo-daodao mongorestore /backup

## Airflow setting
Airflow Admin -> Variable
- mongo_uri=.env.MONGO_URI
- postgres_uri =.env.POSTGRES_URI
- table_name=.env.MONGO_DB_NAME

## TODO
- 找揪團、找夥伴 
  - 資料可以導入pgsql 但需要normal
- 找故事
  - https://www.notion.so/daodaoedu/776e54be135a47198c5a50b0f0868e68
- 找資源
  - https://daodaoedu.notion.site/edc9ef670495412c803d4028510c518e?v=db43b8f6d18f48f0b64f61d80b65e894