import sys
import requests
import json

# 配置你的本地 kernel 地址
BASE_URL = "http://localhost:9000/jdi"

def jdi_task(command, args):
    if command == "write":
        # 语法: python task.py write <filename> <content>
        payload = {"filename": args[0], "content": args[1]}
        resp = requests.post(f"{BASE_URL}/write", json=payload)
    elif command == "git":
        # 语法: python task.py git push <message>
        payload = {"action": args[0], "message": args[1]}
        resp = requests.post(f"{BASE_URL}/git", json=payload)
    print(resp.json())

if __name__ == "__main__":
    # 使用方式: python task.py <命令> <参数1> <参数2>
    jdi_task(sys.argv[1], sys.argv[2:])