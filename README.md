# 数字媒体程序基础第五次作业

## 第05讲 网络场景分层与协议标注 — 源码与实测记录

本仓库保存第 05 讲实验的**可复现材料**：场景标注数据、报告填写脚本、三张自绘图的 HTML 源文件，以及本机真实网络命令的输出记录。

> 说明：本讲实验本身是标注 + 绘图 + 命令验证类，**不要求提交代码链接**。应提交要求，把这些可复现材料整理上传，方便查看与复核。实验报告成品（docx/pdf）与三张 PNG 图为本地提交物，不在本仓库内。

## 文件清单

| 文件 | 作用 |
|---|---|
| `content.py` | 集中管理填入报告的全部内容数据：实验目的、环境、8 行步骤、10 场景标注、问题与解决、结论、提交物自查 |
| `fill_report.py` | 通过 editor_sdk 把 `content.py` 的内容写入 docx 模板，并插入三张截图、替换占位提示 |
| `encap.html` | 图 1「封装与解封装示意」的 HTML 源，用 Chrome 无头截图生成 PNG |
| `verify.html` | 图 2「命令验证输出」的 HTML 源 |
| `pcap.html` | 图 3「协议头逐层解析」的 HTML 源 |
| `results/ipconfig_all.txt` | `ipconfig /all` 原始输出（GBK 编码） |
| `results/ipconfig_all.utf8.txt` | 同上，转 UTF-8 |
| `results/ping_gateway.txt` / `.utf8.txt` | `ping 10.250.0.1` 原始与 UTF-8 输出 |
| `results/ping_external.txt` / `.utf8.txt` | `ping 223.5.5.5` 原始与 UTF-8 输出 |
| `results/nslookup_baidu.txt` | `nslookup www.baidu.com` 输出 |
| `results/netstat_established.txt` | `netstat -ano` 中 ESTABLISHED 连接 |
| `数字媒体程序基础第五次作业.zip` | 上述全部文件的打包 |

## 本机实测环境

- IPv4 `10.250.0.162` / 掩码 `255.255.255.0` / 网关 `10.250.0.1` / DNS `114.114.114.114`
- WLAN MAC `F8-54-F6-60-88-06`，网关 MAC（arp）`3C-15-FB-A9-72-2F`
- `ping` 网关：平均 12 ms，TTL=255，0% 丢包；`ping` 外网 `223.5.5.5`：平均 24 ms，TTL=50，0% 丢包
- `nslookup www.baidu.com`：CNAME `www.a.shifen.com`，A `183.2.172.177`，另有 2 条 AAAA
- `netstat -ano`：ESTABLISHED 连接目的端口均为 443

## 关于抓包

本机未安装 Wireshark/tshark，且原始套接字抓包需管理员权限（WinError 10013）。按实验指南「未安装则提交说明」的要求，改用 `ipconfig` / `arp` / `netstat` 的实测 MAC、IP、端口字段，按 Ethernet II / IPv4 / TCP 首部格式逐层展开，并在图中明确标注哪些字段为实测、哪些为示意值，**未伪造抓包截图**。

## 复现方法

1. 在 cmd / PowerShell 依次执行 `ipconfig /all`、`ping 10.250.0.1`、`ping 223.5.5.5`、`nslookup www.baidu.com`、`netstat -ano`、`arp -a`，结果与 `results/` 中记录对照。
2. 用 Chrome 无头模式把三张 HTML 渲染为 PNG：
   ```
   chrome.exe --headless=new --screenshot=图.png --window-size=1120,900 file:///路径/xxx.html
   ```
3. `content.py` 为纯数据文件，`fill_report.py` 依赖本机 editor_sdk 环境，仅作填写过程留档。
