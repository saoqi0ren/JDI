import sys
import requests
import json

# 配置你的 Kernel 地址
BASE_URL = "http://localhost:9000/jdi"

def jdi_exec(agent, action, message=""):
    url = f"{BASE_URL}/{agent}"
    payload = {"action": action, "message": message}
    try:
        response = requests.post(url, json=payload)
        print(f"🚀 JDI Response: {response.json()}")
    except Exception as e:
        print(f"❌ JDI Error: {e}")

if __name__ == "__main__":
    # 使用方式: python jdi.py git push "提交信息1"
    if len(sys.argv) < 3:
        print("Usage: python jdi.py <agent> <action> [message]")
    else:
        jdi_exec(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")