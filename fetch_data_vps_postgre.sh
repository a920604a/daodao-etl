#!/bin/bash

# 遠端機器資訊
REMOTE_HOST="daodao"  # SSH 目標，需在 ~/.ssh/config 配置過 Host 別名，否則使用 user@ip
REMOTE_BACKUP_SCRIPT="/root/backup_pg.sh"
REMOTE_BACKUP_DIR="/home/backup/"
LOCAL_DEST_DIR="./backup"

# 1. 在遠端機器執行備份腳本
echo "執行遠端備份腳本..."
ssh -tt "$REMOTE_HOST" "bash $REMOTE_BACKUP_SCRIPT"

# 2. 查找最新的 .sql 備份檔案
echo "查找最新的 .sql 備份檔案..."
LATEST_BACKUP=$(ssh "$REMOTE_HOST" "ls -t $REMOTE_BACKUP_DIR*.sql 2>/dev/null | head -n 1")

# 3. 確保找到最新的 .sql 檔案
if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ 未找到最新的 .sql 備份檔案，請檢查遠端機器。"
    exit 1
fi

echo "最新的 .sql 備份檔案為: $LATEST_BACKUP"

# 4. 使用 scp 下載最新的備份到本地
echo "下載最新的 .sql 備份檔案..."
scp "$REMOTE_HOST:$LATEST_BACKUP" "$LOCAL_DEST_DIR"

if [ $? -eq 0 ]; then
    echo "✅ 下載完成！備份儲存於 $LOCAL_DEST_DIR"
else
    echo "❌ 下載失敗，請檢查 SCP 設定。"
    exit 1
fi
