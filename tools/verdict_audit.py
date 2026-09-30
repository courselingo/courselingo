#!/usr/bin/env python
"""verdict_audit.py —— 找出「逐图复核判了要改、而图从那以后没变过」的记录。

## 为什么要有它

2026-09-30 我在清点 `courses/mit-6.5840/docs/audit/visual-review/` 时发现：
**17 份记录里写着「需小修」或「有错误」，而其中 6 份的图从记录写下的那一刻起就没被改过。**

★ 而**没有任何一道闸门报过它** —— 因为 `check_reviewed.py` 校的是
「**声称 `reviewed` 的页**」，而那时有 7 讲是 `draft` ⇒ 它一行都没输出过。

⇒ 所以那 6 处「判定」在记录里放了将近一天，而所有检查都是绿的。
**而根因不是疏忽，是结构**：一道门验的是**状态**（这一页声称什么、证据齐不齐），
而「判定」是**行动**（这张图要改）—— **两者之间没有东西把判定变成待办。**

## 判据

一条记录算「未处理」当且仅当三条同时成立：
  ① 它的「## 判定」一节里写着 `需小修` 或 `有错误`；
  ② 它对应的 `<图名>.svg` **存在**；
  ③ 那个图的 **mtime 不比记录新**（图在记录写下之后没被改过）。

★ 而这条判据有一个已知的漏洞（写在下面，别忘）：
   改了图但**没同步更新记录** ⇒ 会被误报为「未处理」（图的 mtime 比记录新 ⇒ 其实不会被报，见③）
   —— 反向的情况才是漏报：**图被改回了原样**（mtime 新而内容同）⇒ 报不出来。

## 用法

    python verdict_audit.py --root courses/mit-6.5840
    python verdict_audit.py --root courses/mit-6.5840 --all     # 连已处理的也列出来
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# ★ 只取「## 判定」那一节**到下一个 ## 之前**的文字（第一版取固定 400 字符，
#   于是它会读到下一节里去 —— 而 `bft-12` 那处误报正是这么来的：
#   它的判定写的是「可用」，而下一节的缺陷说明里出现了「需小修」三个字）。
# ★★★ 取「## 判定」之后**紧跟着的那个判定词**，而不是在整节里找关键词。
#   第三次收紧的起因（而它是最值钱的一次）：
#   `bft-12` 那一节写的是「**可用**（作者自查；如实记录：**未发现需小修或错误之处**）」——
#   而我的写法在整节里搜「需小修」，于是**命中了那个词出现在否定句里的那一次**。
#   ⇒ ★ 所以判据是：**判定是那一节的第一个词，不是那一节里出现过的任何一个词。**
#     （这一路同类：匹配「未发现 X」里的 X，等于把「没有 X」读成「有 X」。）
VERDICT_FIRST = re.compile(r"##\s*判定[^\n]*\n+\s*\**\s*(可用|需小修|有错误)")
BAD = ("需小修", "有错误")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--all", action="store_true", help="连已处理的也列出来")
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    vrdir = root / "docs" / "audit" / "visual-review"
    if not vrdir.is_dir():
        print(f"  {vrdir} 不存在 —— 跳过")
        return 0

    # ★★ 本仓有两条**合法的消解途径**，而它们都不改图、也不改复核者的原文：
    #   ① 一份更新的复核报告/裁定**覆盖**旧判定（落在 `visual-adjudications.md` 里）
    #   ② 作者在记录**末尾追加一节**「## 修订记录（作者，…）· 本节的判定替代上面的「## 判定」」
    # ⇒ 第一版工具不认这两条，于是它第一次跑出来的 13 处里**至少 11 处是误报** ——
    #   而那正是这一路那条：「一条新判据第一次跑出来的数，要先验证它为什么是这个数，而不是先相信它。」
    adj = root / "docs" / "audit" / "visual-adjudications.md"
    adj_text = adj.read_text(encoding="utf-8", errors="replace") if adj.exists() else ""
    SUPERSEDE_TITLE = re.compile(r"##[^\n]*(修订记录|替代|重裁|已被覆盖)")
    SUPERSEDE_NOTE = ("已修", "替代上面的", "重裁", "判定：可用（缺陷")

    pending: list[str] = []
    handled: list[str] = []
    for rec in sorted(vrdir.glob("*.md")):
        text = rec.read_text(encoding="utf-8", errors="replace")
        m = VERDICT_FIRST.search(text)
        # 而「可用」是绿灯：它可能带着一句「未发现需小修」的自证，而那不算要改。
        if not m or m.group(1) not in BAD:
            continue
        # 消解途径②：末尾追加的修订节 / 明确的「已修」标记
        if SUPERSEDE_TITLE.search(text) or any(n in text for n in SUPERSEDE_NOTE):
            handled.append(f"{rec.name}: 记录里已说明被修订（不动图属合法）")
            continue
        # 消解途径①：被裁定文件覆盖
        #   ★★ 注意口径：裁定表里用的是**图名**（`intro-8`、`zookeeper-3`），**不是**记录文件名
        #   （`mit-6.5840__intro-8`）⇒ 我第一版按记录名搜，于是**一个都没命中**。
        #   而更微妙的是：那份文件里除了表格，还有**散文式的认定** ——
        #   例如 `intro-8` 有两条写着「**成立，不在本表覆盖范围**」，
        #   那是一条**明确记录下来的决定**（决定不改），而它不是「漏了」。
        #   ⇒ 所以这里**按图名在整份裁定文件里搜**（不限于表格）。
        bare = rec.stem.split("__", 1)[-1]
        if bare in adj_text or rec.name in adj_text:
            handled.append(f"{rec.name}: 裁定文件里已对它作出认定（含「成立但不在覆盖范围」这类）")
            continue
        # 记录名形如 mit-6.5840__<前缀>-<n>.md ⇒ 图名 <前缀>-<n>.svg
        stem = rec.stem.split("__", 1)[-1]
        hits = list((root / "content").rglob(f"{stem}.svg"))
        if not hits:
            pending.append(f"{rec.name}: 判定要改，而**找不到对应的图**（{stem}.svg）")
            continue
        svg = hits[0]
        if svg.stat().st_mtime > rec.stat().st_mtime:
            handled.append(f"{rec.name}: 图比记录新（疑似已改而记录未同步）")
        else:
            pending.append(f"{rec.name}: 判定要改，而 {svg.name} 从记录写下之后**没被改过**")

    if args.all and handled:
        print("  —— 已处理/已同步的 ——")
        for h in handled:
            print("    " + h)

    print()
    if pending:
        print(f"  ✘ **{len(pending)} 份记录的判定还没落到图上**：")
        for p in pending:
            print("    " + p)
        print("    ★ 而这一类**任何闸门都看不见**（`check_reviewed` 只校声称 reviewed 的页）——")
        print("      所以它只能靠这一次扫描报出来。**要么去改图，要么在记录里写明为什么决定不改。**")
        return 2
    print("  ✅ 没有「判了要改而图没改」的记录")
    return 0


if __name__ == "__main__":
    sys.exit(main())
