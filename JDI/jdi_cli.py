import requests
import sys
import json
import time

# 内核地址
KERNEL_URL = "http://localhost:9000"

def send_command(text):
    try:
        # 1. 封装高频同步指令 (@sync 或 @s)
        if text.startswith("@sync") or text.startswith("@s"):
            # 提取消息内容，如果没有则使用默认时间戳
            parts = text.split(" ", 1)
            msg = parts[1].strip() if len(parts) > 1 else f"JDI Auto-sync: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            print(f"📦 正在准备同步，消息内容: {msg}")
            res = requests.post(f"{KERNEL_URL}/jdi/git", json={"message": msg})
            result = res.json()
            
            if result.get("status") == "success":
                print(f"✅ 同步成功: GitHub 已更新")
            else:
                print(f"❌ 同步失败: {result.get('message')}")
            
        # 2. 运行脚本指令
        elif text.startswith("@run "):
            script = text.replace("@run ", "").strip()
            res = requests.post(f"{KERNEL_URL}/jdi/run", json={"script": script})
            print(f"🚀 内核响应: {res.json().get('message')}")
            
        # 3. 日志读取指令
        elif text == "@logs" or text == "@l":
            res = requests.get(f"{KERNEL_URL}/jdi/logs")
            data = res.json()
            if data.get("status") == "success":
                logs = data.get("logs", [])
                print("\n--- 实时日志预览 (最近20行) ---")
                if not logs:
                    print("暂无日志数据。")
                else:
                    for line in logs:
                        print(line)
            else:
                print(f"❌ 获取日志失败: {data.get('message')}")

        # 4. 状态快照
        elif text == "@status":
            res = requests.get(f"{KERNEL_URL}/jdi/status")
            print(f"🧠 当前内核记忆快照: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")
                
        else:
            print("❓ 未知指令。目前支持: \n  @s / @sync [信息] (默认使用时间戳)\n  @run [脚本名]\n  @l / @logs\n  @status")
            
    except Exception as e:
        print(f"💥 通信异常: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 支持直接命令行传参: python jdi_cli.py "@s"
        send_command(" ".join(sys.argv[1:]))
    else:
        # 进入交互模式
        print("--- JDI 交互终端 (已连接至 Kernel: 9000) ---")
        print("输入 @指令 操控系统，或输入 exit 退出。")
        while True:
            try:
                cmd = input("JDI > ").strip()
                if not cmd: continue
                if cmd.lower() in ['exit', 'quit']: 
                    print("退出终端。")
                    break
                send_command(cmd)
            except KeyboardInterrupt:
                print("\n检测到中断，退出终端。")
                break