
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
AIRFLOW_UID=
```

docker compose run --rm airflow-init & docker compose up -d
docker compose down --volumes --remove-orphans

docker exec mongo-daodao mongorestore /backup
