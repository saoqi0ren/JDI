# JDI Deep Session Snapshot
**Timestamp**: 2026-03-13 19:16:08
**Commit Message**: JDI: sync 19:16:08

## 1. System Environment
- BASE_PATH: `/Users/liuzhenxing/vscode_workplace/menu/JDI`
- PYTHON_EXE: `/Users/liuzhenxing/vscode_workplace/menu/.venv/bin/python3`

## 2. Kernel Logic (Self-Reflected)
Current registered routes in `kernel.py`:
- `routes = [line.strip() for line in lines if "@app.route" in line]`
- `@app.route("/jdi/git", methods=["POST"])`
- `@app.route("/jdi/restore", methods=["POST"])`
- `@app.route("/jdi/write", methods=["POST"])`
- `@app.route("/jdi/run", methods=["POST"])`
- `@app.route("/jdi/logs", methods=["GET"])`
- `@app.route("/jdi/status", methods=["GET"])`

## 3. Project Inventory
Files currently in the workspace:
- task.py
- .jdi_state.json
- monitor.py
- kernel.py
- jdi_cli.py
- README.md
- jdi_writer.py
- sync.sh
- JDI_MANIFEST.md
- .jdi_status.json
- @run jdi_writer.py
- sys_monitor.py
- SESSION.md
- jdi.py
- archive_logs.py