import time

def start_monitor():
    print("🚀 监控启动...")
    try:
        while True:
            print("JDI 运行中...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n⏹ 监控已停止")

if __name__ == "__main__":
    start_monitor()
    