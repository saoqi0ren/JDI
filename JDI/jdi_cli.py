import requests, sys, json, time, subprocess, os, re

# --- 核心配置 ---
URL = "http://localhost:9000"
PATH = "/Users/liuzhenxing/vscode_workplace/menu/JDI"
STATE = os.path.join(PATH, ".jdi_state.json")

def get_state():
    if os.path.exists(STATE):
        try:
            with open(STATE, 'r', encoding='utf-8') as f: return json.load(f)
        except: return {}
    return {}

def save_state(s):
    try:
        with open(STATE, 'w', encoding='utf-8') as f: json.dump(s, f, indent=4)
    except: pass

TASKS = get_state()

def check():
    try: return requests.get(f"{URL}/jdi/status", timeout=1).status_code == 200
    except: return False

def start():
    print("🛰  正在拉起 JDI 核心引擎...")
    log_path = os.path.join(PATH, "kernel.log")
    log = open(log_path, "a", encoding='utf-8')
    subprocess.Popen([sys.executable, "kernel.py"], cwd=PATH, stdout=log, stderr=log, start_new_session=True)
    time.sleep(2)
    return check()

def write_to_local(filename, content):
    """调用内核执行物理落盘"""
    try:
        res = requests.post(f"{URL}/jdi/write", json={"filename": filename, "content": content})
        return res.json().get("status") == "success"
    except Exception as e:
        print(f"💥 写入异常: {e}")
        return False

def send(cmd):
    global TASKS
    try:
        # 1. 交互式录入模式 (@paste)
        if cmd == "@paste":
            filename = input("📝 请输入目标文件名: ").strip()
            if not filename: 
                print("❌ 文件名不能为空")
                return
            
            print(f"📥 进入录入模式。请直接粘贴代码，完成后在独立行输入 '@done'：")
            lines = []
            while True:
                line = sys.stdin.readline()
                if not line: break
                if line.strip() == "@done": break
                lines.append(line)
            
            content = "".join(lines)
            if write_to_local(filename, content):
                print(f"✅ 物理落盘成功: {filename}")
            else:
                print(f"❌ 落盘失败，请检查 Kernel 是否在线")
            return

        # 2. 运行后台脚本 (@run)
        if cmd.startswith("@run "):
            name = cmd.split(" ")[1]
            res = requests.post(f"{URL}/jdi/run", json={"script": name})
            if res.json().get("status") == "success":
                TASKS[name] = time.strftime('%H:%M:%S')
                save_state(TASKS); print(f"🚀 脚本 {name} 已在后台启动")
            else:
                print(f"❌ 启动失败: {res.json().get('message')}")
        
        # 3. 查看状态与日志
        elif cmd == "@ps":
            print("\n🔍 活跃任务:")
            if not TASKS: print("  (暂无活跃任务)")
            for k, v in TASKS.items(): print(f"  🔹 {k:<20} | {v}")
            
        elif cmd == "@l":
            res = requests.get(f"{URL}/jdi/logs")
            logs = res.json().get("logs", [])
            print("\n--- 实时日志预览 ---")
            if not logs: print("  (日志为空)")
            for l in logs[-15:]: print(l)

        # 4. 实时监控模式 (@watch)
        elif cmd == "@watch":
            print("👁️ 进入实时监控模式 (Ctrl+C 退出)...")
            try:
                last_log = ""
                while True:
                    res = requests.get(f"{URL}/jdi/logs")
                    logs = res.json().get("logs", [])
                    if logs and logs[-1] != last_log:
                        # 清理可能存在的双百分号显示问题
                        display_log = logs[-1].replace("%%", "%")
                        print(f"\r{display_log}", end="", flush=True)
                        last_log = logs[-1]
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n停止监控。")

        # 5. 清理屏幕 (@cls)
        elif cmd == "@cls":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("✨ 界面已清理。")
            
        # 6. Git 同步 (@s)
        elif cmd.startswith("@s"):
            msg = cmd[3:].strip() or f"JDI: sync {time.strftime('%H:%M:%S')}"
            res = requests.post(f"{URL}/jdi/git", json={"message": msg})
            print(f"📦 Git 同步: {res.json().get('status')}")
            
        else:
            print(f"❓ 未知指令: {cmd}。常用: @paste, @run, @ps, @l, @watch, @cls, @s")

    except Exception as e: 
        print(f"💥 通信故障: {e}")

if __name__ == "__main__":
    print("\n" + "="*45)
    print("   JDI Command Center v2.7 (Dashboard)")
    print("="*45)
    
    if not check(): 
        if input("⚠️ 内核离线，是否拉起？(y/n): ").lower() == 'y':
            start()
    else: 
        print("✅ 内核在线。输入 @watch 观察系统波动。")
    
    while True:
        try:
            c = input("\nJDI > ").strip()
            if not c: continue
            if c.lower() in ["exit", "quit"]: break
            send(c)
        except KeyboardInterrupt:
            print("\n👋 停止并退出。")
            break
        except EOFError:
            break