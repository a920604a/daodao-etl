#!/bin/bash

# 遠端機器資訊
REMOTE_HOST="daodao"  # SSH 目標，需在 ~/.ssh/config 配置過 Host 別名，否則使用 user@ip
REMOTE_BACKUP_SCRIPT="/root/backup.sh"
REMOTE_BACKUP_DIR="/home/backup/"
LOCAL_DEST_DIR="./backup"

# 1. 在遠端機器執行備份腳本
echo "執行遠端備份腳本..."
ssh -tt "$REMOTE_HOST" "bash $REMOTE_BACKUP_SCRIPT"

# 2. 找到最新的備份資料夾
echo "查找最新的備份資料夾..."
LATEST_BACKUP=$(ssh "$REMOTE_HOST" "ls -td $REMOTE_BACKUP_DIR*/ | head -n 1 | sed 's:/*$::'")

# 3. 確保找到最新的備份資料夾
if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ 未找到最新的備份資料夾，請檢查遠端機器。"
    exit 1
fi

echo "最新的備份資料夾為: $LATEST_BACKUP"

# 4. 使用 scp 下載最新的備份到本地
echo "下載最新的備份..."
scp -r "$REMOTE_HOST:$LATEST_BACKUP" "$LOCAL_DEST_DIR"

if [ $? -eq 0 ]; then
    echo "✅ 下載完成！備份儲存於當前目錄。"
else
    echo "❌ 下載失敗，請檢查 SCP 設定。"
    exit 1
fi
