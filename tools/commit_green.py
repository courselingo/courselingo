#!/usr/bin/env python
"""commit_green.py —— 只在五道全绿时才提交（把「看到红还提交」变成结构上不可能）。

用法：
    python commit_green.py --repo <仓根> --msg <信息文件> --add <路径> [--add <路径> ...]

行为：
  ① 先跑五道（validate --strict / check_style / audit_content / check_figures --strict / check_reviewed）
  ② **任何一道非零** ⇒ 打印那一道的红行、**拒绝提交**、退出码 2（一笔都不动）
  ③ 五道全绿 ⇒ `git add <路径...>` 然后 `git commit -F <信息文件>`

★ 为什么要有这个工具（来源是一天内两次真实的错）：
  · 第 181 轮：我提交 #36 时**只核了 validate 里那一页的行**，没跑 check_figures ⇒ 提交了 2 个 viewBox error
  · 第 188 轮：我**跑了** check_figures 而输出里写着「4 个 error」，**而我仍然提交了**
  ⇒ 第二次的根因不是粗心，而是**流程**：我把「跑门」与「提交」放进同一个命令块，
    于是「看到红」与「提交」之间**没有插入判断的机会**。
  ⇒ 所以我把它升级成机制（第 166 轮那条三层：要求 → 顺序 → 机制）。
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

PY = pathlib.Path(r"C:\Users\keriko\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe")
PY311 = pathlib.Path(r"C:\Users\keriko\AppData\Local\Programs\Python\Python311\python.exe")

GATES = [
    ("validate", ["--strict"], PY),
    ("check_style", [], PY),
    ("audit_content", [], PY),          # 非 strict
    ("check_figures", ["--strict"], PY),
    ("check_reviewed", [], PY),
    ("build_site", ["--out", "site-mkdocs"], PY311),  # 这一道用带 mkdocs 的解释器
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--msg", required=True, help="提交信息文件路径")
    ap.add_argument("--add", action="append", default=[])
    ap.add_argument("--skip-build", action="store_true")
    a = ap.parse_args()

    repo = pathlib.Path(a.repo).resolve()
    reds: list[tuple[str, str]] = []
    for name, extra, interp in GATES:
        if a.skip_build and name == "build_site":
            continue
        script = repo / "scripts" / f"{name}.py"
        if not script.exists():
            continue
        cmd = [str(interp), str(script), "--root", str(repo), *extra]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode != 0:
            red = [ln.strip() for ln in out.splitlines() if "❌" in ln or "error" in ln.lower()]
            reds.append((name, red[0][:150] if red else out.strip().splitlines()[-1][:150] if out.strip() else "（无输出）"))
        print(f"  {name:<16} exit={r.returncode}  " + ("OK" if r.returncode == 0 else "RED"))

    if reds:
        print("\n" + "=" * 70)
        print("  ✘ 有红 ⇒ **拒绝提交**（一笔都不动）")
        for name, line in reds:
            print(f"    {name}: {line}")
        print("=" * 70)
        return 2

    if a.add:
        subprocess.run(["git", "-C", str(repo), "add", *a.add], check=True)
    r = subprocess.run(["git", "-C", str(repo), "commit", "-q", "-F", a.msg],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(f"\n  ✅ 五道全绿 ⇒ 已提交 ｜ commit exit={r.returncode}")
    if r.returncode != 0:
        print("  " + ((r.stdout or "") + (r.stderr or "")).strip()[:300])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
