#!/bin/bash

# 定義日誌函數
log() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[${timestamp}] $1"
}

# 停止並刪除所有 Docker 容器、卷和鏡像
log "開始停止並刪除 Docker 容器、卷和鏡像..."
docker compose down --volumes --remove-orphans
log "Docker 容器、卷和鏡像刪除完成。"


# 刪除舊的目錄
log "開始刪除舊的目錄..."
rm -rf ./logs ./plugins ./config ./data
log "舊的目錄刪除完成。"

# 創建必要的目錄
log "開始創建必要的目錄..."
mkdir -p ./logs ./plugins ./config ./data ./data/airflow-db-volume
log "目錄創建完成。"



# 初始化 Airflow
log "開始初始化 Airflow..."
docker compose run --rm airflow-init
log "Airflow 初始化完成。"

# 啟動 Docker 容器
log "開始啟動 Docker 容器..."
docker compose up -d
log "Docker 容器啟動完成。"

# 等待 MongoDB 容器啟動
log "等待 MongoDB 容器啟動..."
sleep 10
log "MongoDB 容器啟動完成。"

# 恢復 MongoDB 數據
log "開始恢復 MongoDB 數據..."
docker exec mongo-daodao mongorestore /backup
log "MongoDB 數據恢復完成。"

log "腳本執行完畢！"