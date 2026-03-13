import os
import time
import shutil

LOG_FILE = "monitor.log"
ARCHIVE_DIR = "archive"
MAX_SIZE_KB = 100 # 设置阈值为100KB，方便演示

def archive():
    if not os.path.exists(LOG_FILE):
        return
        
    size = os.path.getsize(LOG_FILE) / 1024
    if size > MAX_SIZE_KB:
        if not os.path.exists(ARCHIVE_DIR):
            os.makedirs(ARCHIVE_DIR)
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        archive_name = f"monitor_{timestamp}.log.bak"
        shutil.move(LOG_FILE, os.path.join(ARCHIVE_DIR, archive_name))
        
        # 创建新的空日志
        with open(LOG_FILE, "w") as f:
            f.write(f"--- Log Archived and Restarted at {timestamp} ---\n")
        
        print(f"✅ 日志归档成功: {archive_name}", flush=True)
    else:
        print(f"ℹ️ 当前日志大小为 {size:.2f}KB，未达到归档阈值。", flush=True)

if __name__ == "__main__":
    archive()