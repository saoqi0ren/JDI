import requests
import sys

URL = "http://localhost:9000"

def interactive_write():
    filename = input("📝 请输入要创建的文件名: ").strip()
    if not filename: return
    
    print(f"📥 开始录入 {filename} 的内容 (输入 '@end' 独立行结束):")
    lines = []
    while True:
        try:
            line = sys.stdin.readline()
            if not line: break
            if line.strip() == "@end": break
            lines.append(line)
        except EOFError:
            break
            
    content = "".join(lines)
    try:
        res = requests.post(f"{URL}/jdi/write", json={
            "filename": filename,
            "content": content
        })
        if res.json().get("status") == "success":
            print(f"✅ 物理落盘成功: {filename}")
        else:
            print(f"❌ 写入失败: {res.json().get('message')}")
    except Exception as e:
        print(f"💥 通信异常: {e}")

if __name__ == "__main__":
    interactive_write()