import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 核心配置对齐 ---
# 确保此路径在你的 Mac 上绝对正确
BASE_PATH = "/Users/liuzhenxing/vscode_workplace/menu/JDI"
PYTHON_EXE = "/Users/liuzhenxing/vscode_workplace/menu/.venv/bin/python3"

@app.route("/jdi/git", methods=["POST"])
def jdi_git():
    """
    第一战略：同步到 GitHub
    """
    data = request.json
    message = data.get("message", "JDI: auto-sync")
    print(f"收到同步请求: {message}")
    
    try:
        # 1. 检查目录是否存在
        if not os.path.exists(BASE_PATH):
            return jsonify({"status": "error", "message": f"路径不存在: {BASE_PATH}"})

        # 2. 执行 Git 操作
        # add
        subprocess.run(["git", "add", "-A"], check=True, cwd=BASE_PATH)
        # commit
        subprocess.run(["git", "commit", "-m", message], cwd=BASE_PATH)
        # push
        res_push = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=BASE_PATH)
        
        if res_push.returncode == 0:
            print("Git Push 成功")
            return jsonify({"status": "success", "output": res_push.stdout})
        else:
            print(f"Git Push 失败: {res_push.stderr}")
            return jsonify({"status": "error", "message": res_push.stderr})
            
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route("/jdi/write", methods=["POST"])
def jdi_write():
    """
    代码投喂接口
    """
    data = request.json
    filename = data.get("filename")
    content = data.get("content")
    target_path = os.path.join(BASE_PATH, filename)
    
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return jsonify({"status": "success", "message": f"文件 {filename} 已成功持久化到本地"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/jdi/run", methods=["POST"])
def jdi_run():
    """
    异步脚本拉起
    """
    try:
        script = request.json.get("script")
        log_file_path = os.path.join(BASE_PATH, "monitor.log")
        
        # 实时无缓冲日志模式
        log_file = open(log_file_path, "w", encoding="utf-8")
        
        subprocess.Popen(
            [PYTHON_EXE, "-u", script], 
            cwd=BASE_PATH, 
            stdout=log_file, 
            stderr=log_file,
            start_new_session=True
        )
        return jsonify({"status": "success", "message": f"脚本 {script} 已在后台启动"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # 厂长的私有内核运行在 9000 端口
    # 添加 threaded=True 以增强稳定性
    app.run(port=9000, threaded=True)