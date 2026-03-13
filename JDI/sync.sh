#!/bin/bash

# 获取提交信息，默认为 auto-sync
MESSAGE=${1:-"JDI: auto-sync"}

echo "🚀 Starting sync to GitHub (JDI Root)..."

# 调用本地 JDI Kernel 的 Git 接口
# 注意：现在的 kernel 会在 BASE_PATH (JDI) 下直接操作 git
RESPONSE=$(curl -s -X POST http://localhost:9000/jdi/git \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"$MESSAGE\"}")

# 检查返回结果
if [[ $RESPONSE == *"success"* ]]; then
    echo "✅ Sync successful."
    echo "🚀 JDI Response: $RESPONSE"
else
    echo "❌ Sync failed. Make sure kernel.py is running and BASE_PATH is correct."
    echo "Debug Info: $RESPONSE"
fi