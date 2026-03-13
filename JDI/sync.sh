#!/bin/bash

# 获取提交信息，默认为 auto-sync
MESSAGE=${1:-"JDI: auto-sync"}

echo "🚀 Starting sync to GitHub..."

# Use a clean variable to handle JSON payload and avoid shell escape issues
# The -s flag makes curl silent, and we capture the response
RESPONSE=$(curl -s -X POST http://localhost:9000/jdi/git \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"$MESSAGE\"}")

# Basic check of the response
if [[ $RESPONSE == *"success"* ]]; then
    echo "✅ Sync command issued successfully."
    echo "🚀 JDI Response: $RESPONSE"
else
    echo "❌ Sync failed. Please ensure the kernel is running."
    echo "Debug Info: $RESPONSE"
fi