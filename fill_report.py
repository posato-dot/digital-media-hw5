import subprocess, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C

E = "C:/Users/hp/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/workbuddy-local-office-edit/edsdk.py"
FID = "C:/Users/hp/Downloads/第05讲-网络场景分层与协议标注-实验报告.docx"
SHOTS = "C:/Users/hp/WorkBuddy/我的文件/02_临时下载_可随时清理/2026-11-18_第05讲_临时工作区/shots"

T = {"purpose":"jr8r7y04","env":"fozzeush","steps":"l0j9wgic","scen":"xa031xuq",
     "shot":"b4is4hg2","prob":"ne3q7wgx","concl":"wvkg7lfx"}

def call(tool, **p):
    p["file_id"] = FID
    r = subprocess.run([sys.executable, E, "call", tool, "--json", json.dumps(p, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    try:
        out = r.stdout.strip()
        return json.loads(out) if out else {"ok": True}
    except Exception:
        return {"raw": r.stdout[:300], "err": r.stderr[:300]}

def set_cells(tid, cells, label):
    r = call("doc_set_table_cells", table_id=tid, cells=cells)
    ok = "error" not in str(r).lower()
    print("  [%s] %s -> %s" % (label, tid, "OK" if ok else str(r)[:200]))

print("=== 1. 实验目的（表2）===")
set_cells(T["purpose"], [{"row": i+1, "col": 1, "text": v} for i, v in enumerate(C.purpose)], "purpose")
print("=== 2. 实验环境（表3 col=2）===")
set_cells(T["env"], [{"row": r, "col": 2, "text": v} for r, v in C.env.items()], "env")
print("=== 3. 步骤表（表4，8 行 × 4 列）===")
cells = [{"row": ri, "col": ci, "text": val}
         for ri, row in enumerate(C.steps, start=2) for ci, val in enumerate(row, start=1)]
set_cells(T["steps"], cells, "steps(%d)" % len(cells))
print("=== 4. 十场景表（表5）===")
cells = [{"row": ri, "col": ci, "text": val}
         for ri, row in enumerate(C.scenarios, start=2) for ci, val in enumerate(row, start=1)]
set_cells(T["scen"], cells, "scenarios(%d)" % len(cells))
print("=== 5. 问题与解决（表7）===")
cells = [{"row": ri, "col": ci, "text": val}
         for ri, row in enumerate(C.problems, start=2) for ci, val in enumerate(row, start=1)]
set_cells(T["prob"], cells, "problems(%d)" % len(cells))
print("=== 6. 结论与拓展（表8）===")
set_cells(T["concl"], [{"row": i+1, "col": 1, "text": v} for i, v in enumerate(C.conclusion)], "conclusion")

print("=== 7. 文本替换：勾选与提示语 ===")
for old, new in C.checkbox_repls + C.hint_repls:
    r = call("doc_find_and_replace", old_text=old, new_text=new)
    print("  %s -> %s" % (old[:20], "OK" if "error" not in str(r).lower() else str(r)[:120]))

print("=== 8. 路径占位串 ===")
for old, new in [
    ("作品或数据文件路径：" + "_"*40, "作品或数据文件路径：shots/encap.png、shots/verify.png、shots/pcap.png；原始命令输出见 results/"),
    ("其他附件：" + "_"*40, "其他附件：ipconfig_all.txt / ping_gateway.txt / ping_external.txt / nslookup_baidu.txt / netstat_established.txt（本机真实命令输出）"),
    ("评阅教师：" + "_"*10 + "　　　日期：" + "_"*10, "评阅教师：____________　　　日期：____________"),
]:
    r = call("doc_find_and_replace", old_text=old, new_text=new)
    print("  ->", "OK" if "error" not in str(r).lower() else str(r)[:120])

print("=== 9. 插入图片（重新取结构定位）===")
d = call("doc_resolve_document_structure", mode="compact", limit=0, text_preview_length=60)
nodes = d.get("nodes", [])
print("  nodes:", len(nodes))

# 找 4.2 标题段之后的位置
anchor = None
for i, n in enumerate(nodes):
    if (n.get("text_preview") or "").startswith("4.2"):
        anchor = n
        break
print("  4.2 anchor:", (anchor or {}).get("text_preview", "NOT FOUND")[:40])
if anchor:
    idx = anchor["end_index"] + 1
    r1 = call("doc_insert_paragraph_with_text", idx=idx,
              text="图 1 「发消息」封装与解封装示意（发送端加头 / 接收端剥头，含两侧主机与中间路由器）",
              paragraph_property={"jc": "center", "spacing_after": 4})
    print("  caption1:", "OK" if "error" not in str(r1).lower() else str(r1)[:120])
    nxt = r1.get("next_index", idx + 1)
    r2 = call("doc_insert_image", idx=nxt, image_path=SHOTS + "\\encap.png", w=620, h=249)
    print("  image1:", "OK" if "error" not in str(r2).lower() else str(r2)[:120])

# 4.3 截图：定位「作品或数据文件路径」段（表6 之后）
d2 = call("doc_resolve_document_structure", mode="compact", limit=0, text_preview_length=60)
nodes2 = d2.get("nodes", [])
anchor2 = None
for n in nodes2:
    if (n.get("text_preview") or "").startswith("作品或数据文件路径"):
        anchor2 = n
        break
print("  4.3 anchor:", (anchor2 or {}).get("text_preview", "NOT FOUND")[:40])
if anchor2:
    idx = anchor2["end_index"] + 1
    imgs = [
        ("图 2 本机配置验证与连通性测试（ipconfig / ping / nslookup / netstat 真实输出）", "verify.png", 620, 357, 3.63),
        ("图 3 抓包字段逐层解析（Frame / Ethernet II / IPv4 / TCP：真实 MAC / IP / 端口）", "pcap.png", 620, 383, 3.63),
    ]
    for cap, fn, w, h, _ in imgs:
        rc = call("doc_insert_paragraph_with_text", idx=idx, text=cap,
                  paragraph_property={"jc": "center", "spacing_after": 4})
        idx = rc.get("next_index", idx + 1)
        ri = call("doc_insert_image", idx=idx, image_path=SHOTS + "\\" + fn, w=w, h=h)
        idx = ri.get("next_index", idx + 1)
        print("  %s -> %s" % (fn, "OK" if "error" not in str(ri).lower() else str(ri)[:120]))

print("=== 10. 保存 ===")
print(call("save_file"))
