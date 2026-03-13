import psutil
import time
import os

# JDI 哨兵配置
THRESHOLD_CPU = 80.0  # CPU 阈值
THRESHOLD_MEM = 85.0  # 内存阈值

def monitor():
    print(f"--- JDI 哨兵已上线 (PID: {os.getpid()}) ---")
    while True:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        
        status = "NORMAL"
        if cpu > THRESHOLD_CPU or mem > THRESHOLD_MEM:
            status = "⚠️ WARNING"
            
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{status}] CPU: {cpu}% | MEM: {mem}%"
        
        print(log_entry, flush=True)
        
        # 每 10 秒监控一次
        time.sleep(10)

if __name__ == "__main__":
    monitor()