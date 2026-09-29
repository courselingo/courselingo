"""只刷新指定课程的过期视觉复核 —— 先重栅格化该课程，再只复核过期的。

为什么要按课程限定：另两门课的作者仍在改图，
全课程刷新会再把「正在被编辑」的图扫进来，产出「报告新鲜、画面过期」的结果。

用法：python refresh_one.py mit-6.006
"""
from __future__ import annotations

import concurrent.futures
import datetime
import hashlib
import os
import pathlib
import re
import sys
import threading
import time
from collections import Counter

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
OUT = ROOT / "preview" / "visual-review"
PNG = ROOT / "preview" / "png"
sys.path.insert(0, str(ROOT))
import rasterize as R  # noqa: E402
import vision  # noqa: E402
import visual_review as VR  # noqa: E402

# 并发度：保守取 3（模型延迟为主，不是本地算力）
WORKERS = int(os.environ.get("REFRESH_WORKERS", "3"))

course = sys.argv[1] if len(sys.argv) > 1 else "mit-6.006"
cdir = COURSES / course

print(f"=== 1) 重栅格化 {course} ===")
figs = sorted(cdir.glob("content/**/figures/*.svg"))
made = 0
for f in figs:
    try:
        if R.raster(f):
            made += 1
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ {f.name}: {e}")
print(f"  {made}/{len(figs)} 张")

print(f"\n=== 2) 找出 {course} 的过期报告（PNG 或报告比 SVG 旧）===")
# ★ --force <stem>：对**没有改动**的图强制重跑一次。
#
# 为什么要这个能力（2026-09-28，mit6006-author 提出的可检验预测）：
#   实测发现复核者报的几何数字与真值差约 2.3–2.4 倍（215 vs 92、675 vs 275、210 vs 91），
#   而 92 × 2.34 = 215 **正好**。假设是：**它在某个缩放栅格上读像素，却按 viewBox 坐标系报数。**
#   这个假设**可检验** —— 对同一张**未改动**的图再跑一次：
#     · 若它又报同样的 215/675/210 ⇒ 支持「读的是被放大过的像素」（有系统性偏置）
#     · 若它这次报对了 ⇒ 是随机误差，不是尺度问题
#   **没有这个开关，就测不了这个假设**，只能停在「它就是不准」。
FORCE = []
for i, a in enumerate(sys.argv):
    if a == "--force" and i + 1 < len(sys.argv):
        FORCE = [s.strip() for s in sys.argv[i + 1].split(",") if s.strip()]

stale = []
for f in figs:
    if FORCE and f.stem in FORCE:
        stale.append((f, "强制"))
        continue
    rep = OUT / f"{course}__{f.stem}.md"
    png = PNG / f"{course}__{f.stem}.png"
    why = None
    # ★★ 主判据：**内容哈希**，不是 mtime。
    #
    # 实测（2026-09-29，mit-6.5840）：跑完一轮全量刷新后，`freshness.py` 报 88/88 新鲜，
    # 而 `check_reviewed.py` 仍说 `zookeeper-18:可用（但报告核的是旧版：报告 F7602F33… / 现值 E47FCEFD…）`。
    #
    # 根因：**报告可能比 SVG「更新」，但它记的是更旧的哈希。**
    #   我的刷新流程是「先重栅格化，再找过期」——
    #   重栅格化让 PNG 变新，而报告的 mtime 也可能已比 SVG 新，
    #   **于是「报告旧」这个判据为假，那张图被当成新鲜跳过** —— 而它核的是旧版。
    #
    # ⇒ 与 `附录十三` 同一条：**mtime 不是内容。**
    #   过期判定的正确判据是「**报告记的哈希 ≠ 当前文件的归一化哈希**」。
    cur = hashlib.sha256(f.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()[:16]
    rec = None
    if rep.exists():
        m = re.search(r"(?is)SHA256(?:.{0,24}?)([0-9A-F]{16,64})",
                      rep.read_text(encoding="utf-8", errors="replace"))
        rec = m.group(1).upper()[:16] if m else None
    if rec is None:
        why = "无版本戳" if rep.exists() else "无报告"
    elif rec != cur:
        why = f"报告核的是旧版({rec}≠{cur})"
    elif not png.exists() or png.stat().st_mtime < f.stat().st_mtime:
        why = "PNG 旧"
    if why:
        stale.append((f, why))
print(f"  {len(stale)} 张：" + ", ".join(f"{f.stem}({w})" for f, w in stale))

if not stale:
    print("\n无待办")
    raise SystemExit(0)

key, base = vision.read_key(), vision.read_base_url()
if not key:
    print("✗ 无密钥")
    raise SystemExit(2)

print(f"\n=== 3) 复核（并发 {WORKERS}）===")
res = Counter()
_lock = threading.Lock()


def do_one(item: tuple[pathlib.Path, str]) -> str:
    """跑一张图的复核并写报告。返回判定（线程安全地累计）。"""
    f, why = item
    png = PNG / f"{course}__{f.stem}.png"
    # ★★ 把 viewBox 交给复核模型，并要求它的坐标落在范围内。
    #
    # 实测（2026-09-29）：一次复核给出 **4 条几何主张，作者逐条量测后全部不成立** ——
    #   「中部两框不等宽 707 vs 622」→ 实测两框**都是 344**
    #   「标题偏右 40–50px」          → 渲染后量墨迹：中心 379.5 对画布 380.0
    #   「右端标签右缘距画布仅 2–3px」→ `text-anchor="end" x="738"`，右边距 **22px**
    #   「第四框明显窄 / 整排偏左」   → 四框**都是 160**，间隙 25/25/25
    # **根因是坐标系**：它报的数常常**超出那张图 viewBox 的宽度本身**
    # （有一张 viewBox 只有 707，而它报 782 / 716）。
    # ⇒ 所以把 viewBox 写进提示，**给它一个能自查的边界**。
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', f.read_text(encoding="utf-8", errors="replace"))
    vb = m.group(1).strip() if m else None
    ok, out = vision.call(base, key, VR.MODEL, VR.prompt_for(vb), [png], timeout=300)
    # ★★ 必须**行尾归一化**，与 `visual_review.py` 的写法一致。
    #
    # 实测（2026-09-29）：本行原来写的是 `hashlib.sha256(f.read_bytes())`（**字节哈希**），
    # 而本文件第 82 行的过期判定与 `check_reviewed.py` 比的是**归一化哈希** ⇒
    # **报告永远与它自己描述的图对不上**，刷新跑多少遍都判「报告核的是旧版」。
    #
    # 根因不是算错，是**同一段逻辑在两个文件里各写了一遍**：
    # 我早先把归一化补进了 `visual_review.py`，**而管线跑的是这一份**。
    # ⇒ `附录十四` 的教科书形态：**我修的是我正在看的那份源，不是它在跑的那份。**
    #
    # ⇒ 规矩：**同一段逻辑只留一处实现**；做不到时，**改一处必须 grep 另一处**。
    h = hashlib.sha256(f.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()[:16]
    body = (
        f"# {course}/figures/{f.stem}.svg\n\n模型 {VR.MODEL}\n"
        f"复核对象 SHA256(前16)：`{h}`\n"
        f"SVG mtime：{datetime.datetime.fromtimestamp(f.stat().st_mtime):%Y-%m-%d %H:%M:%S}\n\n{out}\n")
    (OUT / f"{course}__{f.stem}.md").write_text(body, encoding="utf-8")
    # ★★ 同时写一份到**仓库内** `docs/audit/visual-review/`。
    #
    # 为什么必须写两份（2026-09-29 实测）：
    #   `check_reviewed.py` **先**读仓库内那份、找不到才读工作区。
    #   而我早先只写工作区 ⇒ 我刷新完、刷新报告是新的，
    #   而闸门读的仍是**上一次同步进仓的旧报告** ⇒
    #   报出「gfs-29:有错误」这种**用旧证据下的结论**。
    #   （我因此一度以为「刷新没生效」，其实是「闸门没看到新报告」。）
    #
    # ⇒ 证据住在两处时，**写入必须同时覆盖两处**；否则「我刷过了」与「闸门看到了」是两件事。
    try:
        repo_vr = ROOT / "docs" / "audit" / "visual-review"
        repo_vr.mkdir(parents=True, exist_ok=True)
        (repo_vr / f"{course}__{f.stem}.md").write_text(body, encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        print(f"    ⚠ 不能写入仓库内副本: {e}")
    flat = re.sub(r"[*_`\s]", "", out or "") if ok else ""
    v = next((c for c in ("有错误", "需小修", "可用") if f"判定：{c}" in flat), "?")
    with _lock:
        res[v] += 1
        print(f"  {f.stem:<24} {'✓ ' + v if ok else '✗ ' + out[:60]}", flush=True)
    return v


# ★ 并发。理由：每次调用是**模型延迟**（数分钟），不是本地算力 ——
#   串行跑 12 张 ≈ 60 分钟，而这段时间里作者的任何一次改图都会让前面的白跑。
#   **缩短窗口本身就是减少「刷新与编辑赛跑」的概率。**
#   并发度保守取 3：既能压掉大部分等待，又不至于把接口打限流。
with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
    list(pool.map(do_one, stale))

print(f"\n=== {course} 本轮结果 ===")
for k in ("可用", "需小修", "有错误", "?"):
    if res[k]:
        print(f"  {k:<8} {res[k]:>3}")
