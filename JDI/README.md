# JDI (Just Do It) Protocol
这是一个由 AI 驱动的本地自动化内核协议。
## 🛠 环境准备
1. python3 -m venv .venv
2. pip install flask
3. python kernel.py
## 📡 接口
- /jdi/git
- /jdi/write
- /jdi/run
3.  **赋予脚本权限**：
```bash
chmod +x sync.sh
4.  **执行同步**：
```bash
./sync.sh "fix: restore README and update sync script"