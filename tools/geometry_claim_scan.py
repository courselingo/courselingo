#!/usr/bin/env python3
"""筛出复核报告里**坐标系必然错**的几何主张 —— 即 px 值超出该图 viewBox 的那些。

★ 为什么写这个（2026-09-29）：
  全仓 452 张图里只有 **165 张「可用」**，而 **195 张「需小修」**。
  而本会话已**实测驳掉至少 6 条几何主张**，其中 4 条的 px 值**超出了那张图 viewBox 的宽度**
  （例：一张 viewBox 只有 707 的图，被报「标题中心在 x≈782」）。
  ⇒ 一个 px 值**落在 viewBox 之外**，就**不可能是图内坐标** —— 那一刻这条主张已经不成立，
    与它说的内容对不对无关。**这是一个可以机械判定的子集。**

用法：
    python geometry_claim_scan.py <课程> [--min 3]
    python geometry_claim_scan.py --all

输出：按图列出「报告里出现的、超出 viewBox 的 px 值」，并给出建议（裁定 / 复核）。

★ 边界的诚实声明：本工具**只**能证明「这个数不可能是图内坐标」，
  **不能**证明「这条主张是假的」 —— 它可能是在**拼版坐标**下成立的（本会话见过）。
  所以它的产物是**待裁定的候选**，不是裁定（同 `附录三十四`：工具给候选集，人下判断）。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
VB = ROOT / "preview" / "visual-review"


def viewbox_of(svg: pathlib.Path) -> tuple[float, float] | None:
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg.read_text(encoding="utf-8", errors="replace"))
    if not m:
        return None
    parts = re.split(r"[\s,]+", m.group(1).strip())
    if len(parts) != 4:
        return None
    try:
        return float(parts[2]), float(parts[3])
    except ValueError:
        return None


# 报告里量坐标的常见写法
NUM_PATTERNS = [
    r"x\s*[≈=]\s*(\d+(?:\.\d+)?)",
    r"y\s*[≈=]\s*(\d+(?:\.\d+)?)",
    r"约\s*(\d+(?:\.\d+)?)\s*(?:px|像素)",
    r"(\d+(?:\.\d+)?)\s*(?:px|像素)",
]


def claims(text: str) -> list[float]:
    out: list[float] = []
    for p in NUM_PATTERNS:
        out += [float(x) for x in re.findall(p, text)]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course", nargs="?")
    ap.add_argument("--min", type=int, default=3, help="至少几个越界值才列出")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    targets = []
    for cd in sorted(COURSES.iterdir()):
        if not (cd / "content").exists():
            continue
        if a.course and not a.all and cd.name != a.course:
            continue
        targets.append(cd)

    print("=== 几何主张的坐标系筛查（px 值超出 viewBox ⇒ 不可能是图内坐标）===\n")
    hits_total = 0
    for cd in targets:
        rows = []
        for f in sorted((cd / "content").rglob("figures/*.svg")):
            rep = cd / "docs" / "audit" / "visual-review" / f"{cd.name}__{f.stem}.md"
            if not rep.exists():
                rep = VB / f"{cd.name}__{f.stem}.md"
            if not rep.exists():
                continue
            vb = viewbox_of(f)
            if not vb:
                continue
            w, h = vb
            txt = rep.read_text(encoding="utf-8", errors="replace")
            # 只在该报告不是「可用」时才有意义
            if not re.search(r"判定[：:]\s*\**\s*(有错误|需小修)", txt):
                continue
            vals = claims(txt)
            over = sorted({v for v in vals if v > max(w, h) + 1})
            if len(over) >= a.min:
                rows.append((f.stem, w, h, over[:6]))
        if rows:
            print(f"--- {cd.name}（{len(rows)} 张）---")
            for stem, w, h, over in rows:
                print(f"  {stem:<34} viewBox {w:.0f}×{h:.0f} ｜ 越界值 {over}")
            hits_total += len(rows)
            print()
    print(f"⇒ 合计 {hits_total} 张图的报告里含**不可能**是图内坐标的 px 值。")
    print("⇒ 它们不必然是假主张（可能用了拼版坐标），但**必须**先裁定或重跑，不能照它改图。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
