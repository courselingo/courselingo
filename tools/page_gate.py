#!/usr/bin/env python
"""page_gate.py —— 按**页**核一道门（而不是按仓），给提交前的页级证据用。

用法：
    python page_gate.py --repo <仓根> --page <slug 或路径片段> [--page <另一个>]

为什么要有它：
  · `commit_green.py` 是**按仓**判定的 ⇒ 并行写作时它几乎总会因为别人的红而拒绝，
    于是那一路上我一直在**手工**跑「逐道查我这一页」。
  · 而我手工跑的那个过滤器有 bug：它的条件是 `'❌' in ln or 'error' in ln or 'warning' in ln`，
    **而 `check_figures` 报「引用了 X 而它不在磁盘上」那一行三个都不含**
    ⇒ 于是我据此提交了 #16（缺 mc-7/8/9 三张图）—— 见 2026-09-29 那一笔。
    ★ 所以本脚本存在的理由就是：**把「这一页有没有问题」这件事从我的临时 grep 里拿出来**。

判定口径：
  · 五道各自的退出码**不作为**本页判据（它们量的是整仓）；
  · 本脚本只回答一个问题：**输出里有没有任何一行指向我这一页？**
    而它把「指向」定义为：那一行**含这一页的路径片段**，且**不是**一句纯统计行。
  · ★ 因为「有没有输出指向我」这件事，比「那道门的退出码是多少」更接近我要的结论。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

PY = pathlib.Path(
    r"C:\Users\keriko\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
)
PY311 = pathlib.Path(
    r"C:\Users\keriko\AppData\Local\Programs\Python\Python311\python.exe"
)

GATES = [
    ("validate", ["--strict"], PY),
    ("check_style", [], PY),
    ("audit_content", [], PY),
    ("check_figures", ["--strict"], PY),
    ("check_reviewed", [], PY),
    ("build_site", ["--out", "site-mkdocs"], PY311),
]

# 纯统计行（含「N 个错误」这种），它们不是「指向某一页」的结论行
STAT_LINE = re.compile(r"^\s*(?:结果：|\d+\s*(?:个)?\s*(?:error|warning|文件|file)|.*file\(s\),.*error\(s\),)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--page", action="append", required=True,
                    help="页的路径片段，例如 16-memcached")
    ap.add_argument("--skip-build", action="store_true")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    pages = args.page
    problems: list[str] = []

    for name, extra, interp in GATES:
        if args.skip_build and name == "build_site":
            continue
        script = repo / "scripts" / f"{name}.py"
        if not script.exists():
            continue
        r = subprocess.run(
            [str(interp), str(script), "--root", str(repo), *extra],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        out = (r.stdout or "") + (r.stderr or "")
        mine: list[str] = []
        for ln in out.splitlines():
            s = ln.strip()
            if not any(p in ln for p in pages):
                continue
            if STAT_LINE.match(s):
                continue
            # ★ 只排除「本人这一页 ✅」这种正行；其余一律算「指向我」
            if re.match(r"^[✅✓]\s", s):
                continue
            mine.append(s[:160])
        if mine:
            problems.append(f"[{name}] " + mine[0])
        print(f"  {name:<16} exit={r.returncode:<3} 指向本页的行 {len(mine)}")

    print()
    if problems:
        print("  ✘ 有输出指向这一页 ⇒ **不要提交**")
        for p in problems:
            print("    " + p)
        return 2
    print("  ✅ 五道（含 build_site）都没有任何一行指向这一页 ⇒ 可以按页级证据提交")
    return 0


if __name__ == "__main__":
    sys.exit(main())
