# JDI (Just Do It) Protocol OS Kernel

这是一个受 API 驱动的本地自动化内核。通过 JDI 协议，你可以通过网络请求直接遥控本地文件系统与 Git 仓库。

## 协议接口
- `POST /jdi/git`: 触发 Git 同步 (add/commit/push)
- `POST /jdi/write`: 远程创建或覆写本地文件
- `POST /jdi/helloworld`: 系统存活检测

## 快速开始
1. 启动内核：`python JDI/examples/jdi_kernel.py`
2. 自动化同步：`./sync.sh "feat: 你的提交信息"`
3. 远程投喂代码：通过 curl 调用 `/jdi/write` 接口

## 核心组件
- `kernel.py`: 协议后端引擎
- `jdi.py`: 协议命令行客户端
- `sync.sh`: Git 自动化流水线