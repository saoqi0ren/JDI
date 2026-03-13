import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- JDI 协议：Git 代理 ---
@app.route('/jdi/git', methods=['POST'])
def jdi_git():
    data = request.json
    action = data.get('action')
    message = data.get('message', 'JDI: auto-sync')
    
    if action == "push":
        try:
            subprocess.run(["git", "add", "-A"], check=True)
            res = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
            # 允许 "nothing to commit" 状态
            if res.returncode != 0 and "nothing to commit" not in res.stderr:
                return jsonify({"status": "error", "message": res.stderr})
            
            res_push = subprocess.run(["git", "push"], capture_output=True, text=True)
            return jsonify({"status": "success", "message": "已同步至 GitHub", "output": res_push.stdout or res_push.stderr})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
            
    return jsonify({"status": "error", "message": "Unknown action"})

# --- JDI 协议：文件生产 ---
@app.route('/jdi/write', methods=['POST'])
def jdi_write():
    data = request.json
    filename = data.get('filename')
    content = data.get('content')
    
    # 确保路径存在
    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    return jsonify({"status": "success", "message": f"文件 {filename} 已通过 JDI 写入"})

# --- 测试用例 ---
@app.route('/jdi/helloworld', methods=['POST'])
def helloworld():
    return jsonify({"status": "success", "data": "Hello, JDI Protocol!"})

if __name__ == "__main__":
    app.run(port=9000)