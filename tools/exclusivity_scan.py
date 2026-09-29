#!/usr/bin/env python3
"""独占性措辞扫描 —— 找出「唯一 / 第一次 / 只有 / 最后一讲 / 收束」这类**跨讲才矛盾**的说法。

★ 为什么写这个（2026-09-29）：
  `mlsys` 第 21 讲的核对者发现第 19 讲**两次自称「最后一讲／全课收束」**，而本课有 21 讲。
  它的判词（我原文采纳）：
    「★ 编排类错误单讲内部读不出来，只能靠跨讲比对 —— 我第 19 讲的 P0-4（自称最后一讲）
      是在核完第 21 讲、把三讲的『收束』措辞并排时才发现的。
      建议后续轮次**固定加一步**：把同一批讲次的『收束/第一次/只有/唯一』这类
      **独占性措辞**横向比一遍。」

⇒ 这类措辞的特征是：**它在单讲内永远自洽**（那一讲讲「第一次」时看不出别人也讲了），
  而**并排看就矛盾**（两讲讲同一件事是「第一次」）。

用法：
    python exclusivity_scan.py <课程>            # 扫全部讲次
    python exclusivity_scan.py <课程> --word 首次  # 只扫某个词

输出：按「措辞」分组，列出**命中的讲次与原文行**，便于并排判读。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"

# ★ 这些词都是「独占性断言」：说了就等于排除了别人
WORDS = [
    "最后一讲", "全课的收束", "收束", "最后讲", "到此结束", "全课结束",
    "第一次", "首次", "第一次出现", "唯一", "仅有", "只有这一", "唯一个",
    "第一次成为主角", "本课唯一", "全课唯一", "此前没", "前面没有", "从未",
]


def scan(course_dir: pathlib.Path, words: list[str]) -> dict[str, list[tuple[str, int, str]]]:
    hits: dict[str, list[tuple[str, int, str]]] = {w: [] for w in words}
    for idx in sorted((course_dir / "content").rglob("index.md")):
        slug = str(idx.parent.relative_to(course_dir / "content")).replace("\\", "/")
        lines = idx.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(lines, 1):
            for w in words:
                if w in ln:
                    hits[w].append((slug, i, ln.strip()))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course")
    ap.add_argument("--word", action="append")
    a = ap.parse_args()
    cd = COURSES / a.course
    if not (cd / "content").exists():
        print(f"没有这个课程：{a.course}")
        return 1
    words = a.word or WORDS
    hits = scan(cd, words)
    print(f"=== {a.course} · 独占性措辞扫描 ===")
    print("（同一措辞命中**两个以上讲次**时风险最高：它们不可能都「第一次」/都「唯一」）\n")
    for w in words:
        h = hits[w]
        if not h:
            continue
        slugs = sorted({s for s, _, _ in h})
        flag = "  ★★ 跨讲（需并排判读）" if len(slugs) > 1 else ""
        print(f"「{w}」 命中 {len(h)} 处 / {len(slugs)} 讲{flag}")
        for s, i, ln in h:
            print(f"    {s:<42} L{i:<4} {ln[:110]}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
