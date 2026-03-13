import subprocess
import os
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 核心配置 ---
BASE_PATH = "/Users/liuzhenxing/vscode_workplace/menu/JDI"
PYTHON_EXE = "/Users/liuzhenxing/vscode_workplace/menu/.venv/bin/python3"
STATUS_FILE = os.path.join(BASE_PATH, ".jdi_status.json")

def update_status(action, details):
    """
    将当前操作状态持久化到本地 JSON，用于防止 AI 失忆
    """
    status = {
        "last_action": action,
        "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_path": BASE_PATH,
        "python_exe": PYTHON_EXE,
        "details": details
    }
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"状态写入失败: {e}")

@app.route("/jdi/git", methods=["POST"])
def jdi_git():
    """
    第一战略：同步到 GitHub 并保存会话快照
    """
    data = request.json
    message = data.get("message", "JDI: auto-sync")
    print(f"收到同步请求: {message}")
    
    try:
        if not os.path.exists(BASE_PATH):
            return jsonify({"status": "error", "message": f"路径不存在: {BASE_PATH}"})

        # 在同步前，生成一个 session 快照文件，防止 AI 失忆
        session_info = f"# JDI Session Snapshot\nLast Sync: {time.strftime('%Y-%m-%d %H:%M:%S')}\nMessage: {message}\n"
        with open(os.path.join(BASE_PATH, "SESSION.md"), "w", encoding="utf-8") as f:
            f.write(session_info)

        # 执行 Git 操作
        subprocess.run(["git", "add", "-A"], check=True, cwd=BASE_PATH)
        subprocess.run(["git", "commit", "-m", message], cwd=BASE_PATH)
        res_push = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=BASE_PATH)
        
        if res_push.returncode == 0:
            update_status("git_push", {"message": message, "result": "success"})
            return jsonify({"status": "success", "output": res_push.stdout})
        else:
            return jsonify({"status": "error", "message": res_push.stderr})
            
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route("/jdi/write", methods=["POST"])
def jdi_write():
    """
    代码投喂接口：写入并更新状态
    """
    data = request.json
    filename = data.get("filename")
    content = data.get("content")
    target_path = os.path.join(BASE_PATH, filename)
    
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        update_status("file_write", {"filename": filename})
        return jsonify({"status": "success", "message": f"文件 {filename} 已成功持久化"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/jdi/run", methods=["POST"])
def jdi_run():
    """
    异步脚本拉起：记录运行中的任务
    """
    try:
        script = request.json.get("script")
        log_file_path = os.path.join(BASE_PATH, "monitor.log")
        log_file = open(log_file_path, "w", encoding="utf-8")
        
        subprocess.Popen(
            [PYTHON_EXE, "-u", script], 
            cwd=BASE_PATH, 
            stdout=log_file, 
            stderr=log_file,
            start_new_session=True
        )
        update_status("script_run", {"script": script})
        return jsonify({"status": "success", "message": f"脚本 {script} 已启动"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/jdi/status", methods=["GET"])
def get_jdi_status():
    """
    新增接口：供 AI 或厂长随时读取当前系统的“记忆快照”
    """
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"status": "none", "message": "尚无持久化记忆"})

if __name__ == "__main__":
    app.run(port=9000, threaded=True)