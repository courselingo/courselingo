#!/usr/bin/env python3
"""把复核者的**具体几何主张**与**客观几何事实**摆在一起，供 Lead 一行裁定。

★ 为什么（2026-09-29）：
  全仓 195 张「需小修」，而几何类占 98%（`mlsys` 181 张里 177 张）。
  实测统计显示**这类主张大多是假的**，但「判它是真是假」本身要量一次。
  ⇒ 于是把「量」机械化：对每张被报的图，直接算出**那几类最常被主张的客观事实**，
    与报告里的原句并排打印 ⇒ Lead **一行对读**即可裁定。

支持的主张类（覆盖实测中最常见的）：
  ① 居中/对称     → 算：标题 x vs 内容中心；左右外边距
  ② 等宽/宽窄     → 算：各 `<rect>` 的 width 列表
  ③ 间距          → 算：相邻 `<rect>` 的水平间隙列表（同行）
  ④ 垂直间距      → 算：同一 x 列上相邻 `<rect>` 的垂直间隙
  ⑤ `↑`/符号缺失  → 算：该字符在文件里出现次数

用法：
    python figure_measure.py <课程> [--only <图名>] [--limit N]

★ 边界：它算的是**客观属性**，不是裁定。裁定仍由 Lead 下（`附录十一`）。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
VB = ROOT / "preview" / "visual-review"


def num(attrs: str, key: str) -> float | None:
    m = re.search(rf'\b{key}="(-?[\d.]+)"', attrs)
    return float(m.group(1)) if m else None


def facts(svg: pathlib.Path) -> dict:
    raw = svg.read_text(encoding="utf-8", errors="replace")
    vb = re.search(r'viewBox="([^"]+)"', raw)
    vw = vh = None
    if vb:
        p = re.split(r"[\s,]+", vb.group(1).strip())
        if len(p) == 4:
            vw, vh = float(p[2]), float(p[3])

    rects = []
    for m in re.finditer(r"<rect([^>]*)>", raw):
        a = m.group(1)
        x, y, w, h = num(a, "x"), num(a, "y"), num(a, "width"), num(a, "height")
        if None in (x, y, w, h):
            continue
        # 排除画布本身
        if vw and vh and w >= vw - 1 and h >= vh - 1:
            continue
        rects.append((x, y, w, h))

    texts = []
    for m in re.finditer(r"<text([^>]*)>([^<]*)</text>", raw):
        a, body = m.group(1), m.group(2).strip()
        x = num(a, "x")
        if x is None:
            continue
        anchor = "middle" if 'text-anchor="middle"' in a else ("end" if 'text-anchor="end"' in a else "start")
        texts.append({"x": x, "body": body, "anchor": anchor, "font": num(a, "font-size") or 12})

    return {"raw": raw, "vw": vw, "vh": vh, "rects": rects, "texts": texts}


def report(course_dir: pathlib.Path, svg: pathlib.Path) -> None:
    f = facts(svg)
    vw = f["vw"]
    print(f"  ── {svg.stem}  viewBox {vw}×{f['vh']}")
    # ① 居中：标题（font-size 最大的那条 text）
    if f["texts"] and vw:
        title = max(f["texts"], key=lambda t: t["font"])
        lefts = [r[0] for r in f["rects"]]
        rights = [r[0] + r[2] for r in f["rects"]]
        if lefts and rights:
            cl, cr = min(lefts), max(rights)
            cc = (cl + cr) / 2
            print(f"       内容边界 {cl:.1f}..{cr:.1f} ⇒ 内容中心 {cc:.1f} ｜ 画布中心 {vw/2:.1f}")
            print(f"       标题 x={title['x']:.1f} anchor={title['anchor']} 「{title['body'][:38]}」")
            print(f"       ⇒ 标题 vs 内容中心 差 {abs(title['x']-cc):.1f}px ｜ 左外边距 {cl:.1f} / 右外边距 {vw-cr:.1f}")
    # ② 宽度
    if f["rects"]:
        ws = Counter(r[2] for r in f["rects"])
        print(f"       框宽分布: " + " ｜ ".join(f"{w:.0f}×{n}" for w, n in ws.most_common(6)))
    # ③ 同行水平间隙
    rows: dict[float, list] = {}
    for x, y, w, h in f["rects"]:
        rows.setdefault(round(y, 1), []).append((x, x + w))
    gaps = []
    for y, iv in sorted(rows.items()):
        iv.sort()
        for (a1, b1), (a2, b2) in zip(iv, iv[1:]):
            g = a2 - b1
            if -1 < g < 400:
                gaps.append(round(g, 1))
    if gaps:
        print(f"       同行水平间隙: {gaps[:10]}  最大-最小 = {max(gaps)-min(gaps):.1f}")
    # ④ 垂直间隙：同一 x 列上相邻 rect 的 y 间隙
    cols: dict[float, list] = {}
    for x, y, w, h in f["rects"]:
        cols.setdefault(round(x, 1), []).append((y, y + h))
    vgaps = []
    for x, iv in sorted(cols.items()):
        iv.sort()
        for (a1, b1), (a2, b2) in zip(iv, iv[1:]):
            g = a2 - b1
            if -1 < g < 300:
                vgaps.append(round(g, 1))
    if vgaps:
        print(f"       同列垂直间隙: {vgaps[:10]}  最大-最小 = {max(vgaps)-min(vgaps):.1f}")
    # ④b 标题底 → 最上一个 rect 顶；最下一个 rect 底 → 最下一条 text 顶（复核者常报的两处）
    if f["texts"] and f["rects"]:
        title = max(f["texts"], key=lambda t: t["font"])
        top_rect = min(r[1] for r in f["rects"])
        bot_rect = max(r[1] + r[3] for r in f["rects"])
        base = title["font"] * 0.75
        title_bottom = 25 + base  # 近似：标题基线在 margin+ascent
        others = [t for t in f["texts"] if t["x"] != title["x"] or t["font"] != title["font"]]
        if others:
            lowest = max(others, key=lambda t: t["y"] if "y" in t else 0) if all("y" in t for t in others) else None
        print(f"       标题基线≈{title_bottom:.0f} ｜ 最上框顶 {top_rect:.0f} ⇒ 标题→框群 {top_rect-title_bottom:.0f}")
        print(f"       最下框底 {bot_rect:.0f} ｜ 画布高 {f['vh']:.0f} ⇒ 框群→画布底 {f['vh']-bot_rect:.0f}")
    # ⑤ 符号
    for ch in ("↑", "↓"):
        n = f["raw"].count(ch)
        if n or ch == "↑":
            print(f"       「{ch}」出现 {n} 次")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course")
    ap.add_argument("--only")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    cd = COURSES / a.course
    if not (cd / "content").exists():
        print("没有这个课程")
        return 1
    shown = 0
    for rep in sorted((cd / "docs" / "audit" / "visual-review").glob(f"{cd.name}__*.md")):
        stem = rep.stem.replace(f"{cd.name}__", "")
        if a.only and stem != a.only:
            continue
        txt = rep.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"判定[：:]\s*\**\s*(有错误|需小修)", txt):
            continue
        svg = next((cd / "content").rglob(f"figures/{stem}.svg"), None)
        if not svg:
            continue
        claim = txt.split("## 缺陷", 1)[-1].split("## 判定", 1)[0].strip().replace("\n", " ")
        print(f"【{stem}】复核者原话：{claim[:260]}")
        report(cd, svg)
        print()
        shown += 1
        if a.limit and shown >= a.limit:
            break
    print(f"⇒ 共 {shown} 张")
    return 0


if __name__ == "__main__":
    sys.exit(main())
