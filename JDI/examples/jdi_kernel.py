import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# JDI 协议：Git 代理
@app.route('/jdi/git', methods=['POST'])
def jdi_git():
    data = request.json
    action = data.get('action')
    message = data.get('message', 'JDI: auto-sync')
    
    if action == "push":
        try:
            # 顺序执行，即使出错也能捕获详细信息
            subprocess.run(["git", "add", "."], check=True)
            # 使用 capture_output 获取具体的 git 错误提示
            res = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
            if res.returncode != 0 and "nothing to commit" not in res.stderr:
                return jsonify({"status": "error", "message": res.stderr})
            
            res_push = subprocess.run(["git", "push"], capture_output=True, text=True)
            return jsonify({"status": "success", "message": "已尝试同步", "git_output": res_push.stderr or res_push.stdout})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
            
    return jsonify({"status": "error", "message": "Unknown action"})

@app.route('/jdi/write', methods=['POST'])
def jdi_write():
    data = request.json
    filename = data.get('filename')
    content = data.get('content')
    # 写入文件
    with open(filename, 'w') as f:
        f.write(content)
    return jsonify({"status": "success", "message": f"文件 {filename} 已生成"})

if __name__ == "__main__":
    app.run(port=9000)