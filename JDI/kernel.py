import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
# 路径对齐到 JDI 文件夹
BASE_PATH = "/Users/liuzhenxing/vscode_workplace/menu/JDI"
PYTHON_EXE = "/Users/liuzhenxing/vscode_workplace/menu/.venv/bin/python3"

@app.route("/jdi/git", methods=["POST"])
def jdi_git():
    data = request.json
    try:
        # 强制在 JDI 目录下执行 Git 操作
        subprocess.run(["git", "add", "-A"], check=True, cwd=BASE_PATH)
        subprocess.run(["git", "commit", "-m", data.get("message", "JDI: auto-sync")], cwd=BASE_PATH)
        res_push = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=BASE_PATH)
        return jsonify({"status": "success", "output": res_push.stdout or res_push.stderr})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/jdi/write", methods=["POST"])
def jdi_write():
    data = request.json
    target_path = os.path.join(BASE_PATH, data.get("filename"))
    with open(target_path, "w") as f: f.write(data.get("content"))
    return jsonify({"status": "success", "message": f"文件 {target_path} 已写入"})

@app.route("/jdi/run", methods=["POST"])
def jdi_run():
    try:
        script = request.json.get("script")
        log_file_path = os.path.join(BASE_PATH, "monitor.log")
        log_file = open(log_file_path, "w")
        subprocess.Popen([PYTHON_EXE, "-u", script], cwd=BASE_PATH, stdout=log_file, stderr=log_file, start_new_session=True)
        return jsonify({"status": "success", "message": "已在 JDI 目录下拉起进程"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=9000)