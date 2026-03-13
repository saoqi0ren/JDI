import requests
import sys
import json
import time
import subprocess
import os

# Configuration
KERNEL_URL = "http://localhost:9000"
BASE_PATH = "/Users/liuzhenxing/vscode_workplace/menu/JDI"
KERNEL_SCRIPT = "kernel.py"

def check_kernel():
    """Check if the JDI Kernel is currently online."""
    try:
        response = requests.get(f"{KERNEL_URL}/jdi/status", timeout=1)
        return response.status_code == 200
    except:
        return False

def start_kernel():
    """Attempt to start the Kernel process in the background."""
    print("🛰  Attempting to launch JDI Kernel...")
    try:
        # Start kernel.py as a background process
        log_file = open(os.path.join(BASE_PATH, "kernel.log"), "a")
        subprocess.Popen(
            [sys.executable, KERNEL_SCRIPT],
            cwd=BASE_PATH,
            stdout=log_file,
            stderr=log_file,
            start_new_session=True
        )
        time.sleep(2)  # Wait for Flask to initialize
        if check_kernel():
            print("✅ Kernel launched successfully on port 9000.")
            return True
        else:
            print("❌ Kernel failed to respond after launch.")
            return False
    except Exception as e:
        print(f"💥 Failed to launch Kernel: {e}")
        return False

def send_command(text):
    """Parse and execute JDI commands."""
    try:
        # 1. Start Command
        if text == "@start":
            if check_kernel():
                print("ℹ️  Kernel is already running.")
            else:
                start_kernel()

        # 2. Sync Command (@sync or @s)
        elif text.startswith("@sync") or text.startswith("@s"):
            parts = text.split(" ", 1)
            msg = parts[1].strip() if len(parts) > 1 else f"JDI Auto-sync: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            print(f"📦 Preparing sync: {msg}")
            res = requests.post(f"{KERNEL_URL}/jdi/git", json={"message": msg})
            result = res.json()
            
            if result.get("status") == "success":
                print(f"✅ Sync successful: GitHub updated.")
            else:
                print(f"❌ Sync failed: {result.get('message')}")
            
        # 3. Run Script Command
        elif text.startswith("@run "):
            script = text.replace("@run ", "").strip()
            res = requests.post(f"{KERNEL_URL}/jdi/run", json={"script": script})
            print(f"🚀 Kernel: {res.json().get('message')}")
            
        # 4. Log Retrieval (@logs or @l)
        elif text == "@logs" or text == "@l":
            res = requests.get(f"{KERNEL_URL}/jdi/logs")
            data = res.json()
            if data.get("status") == "success":
                logs = data.get("logs", [])
                print("\n--- Real-time Log Stream (Last 20 lines) ---")
                if not logs:
                    print("No log data available.")
                else:
                    for line in logs:
                        print(line)
            else:
                print(f"❌ Log fetch failed: {data.get('message')}")

        # 5. Status Snapshots
        elif text == "@status":
            res = requests.get(f"{KERNEL_URL}/jdi/status")
            print(f"🧠 Kernel Memory Snapshot: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")
                
        else:
            print("❓ Unknown command. Supported: \n  @start           (Launch Kernel)\n  @s / @sync [msg] (Git Sync)\n  @run [script]    (Execute script)\n  @l / @logs       (Tailing logs)\n  @status          (System memory)")
            
    except Exception as e:
        print(f"💥 Connection Error: Ensure Kernel is running. Try '@start'. Details: {str(e)}")

if __name__ == "__main__":
    print("--- JDI Command Center ---")
    
    # Auto-check on startup
    if not check_kernel():
        print("⚠️  Kernel is offline.")
        user_input = input("Would you like to start the Kernel now? (y/n): ").lower()
        if user_input == 'y':
            start_kernel()
    else:
        print("✅ Kernel is online and connected.")

    if len(sys.argv) > 1:
        send_command(" ".join(sys.argv[1:]))
    else:
        print("Type @command to control the system, or 'exit' to quit.")
        while True:
            try:
                cmd = input("JDI > ").strip()
                if not cmd: continue
                if cmd.lower() in ['exit', 'quit']: 
                    print("Terminal closed.")
                    break
                send_command(cmd)
            except KeyboardInterrupt:
                print("\nInterrupted, exiting.")
                break