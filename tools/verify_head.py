"""verify_head.py —— 把「验证一个已提交状态，要在干净检出上跑门」做成一条可执行的检查。

★ 为什么需要它（2026-09-29，第 79 轮）：
```
我提交 mit-6.006 第 11 讲时用了 `git add content/11-…/index.md`，
而那时 `figures/` 还是**未跟踪目录** ⇒ 11 张图被漏掉 ⇒ **工作区是好的而 HEAD 是坏的**。
★ 而 `check_figures` 在**工作区**是绿的（图在盘上）⇒ 我看到的是绿。
⇒ 这一整类（工作区好 / HEAD 坏）只有「**把 HEAD 导出到干净目录再跑门**」才能发现。
```
★ 而它此前只是**一条纪律**（`附录五十八`），而纪律依赖我记得 ⇒ 等于没立（`附录四十六`）。
⇒ 所以这个脚本把三件事合起来：
```
① 用 `git archive HEAD` 导出到临时目录
② ★ 临时目录**必须以仓名命名**（`附录六十一`）：
   因为 `check_reviewed.py` 的报告名是 `f"{root.name}__{f.stem}.md"`，
   而随机名的目录会让五仓**一致地假红**（我在第 51 轮就因此误判过一次）
③ 在那里跑六道，**并单独报「引用了而磁盘上不存在的图」**（那正是这次的形态）
```

用法：
    python verify_head.py            # 五仓全查
    python verify_head.py mit-6.006  # 只查一门
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

PY = sys.executable
WORKSPACE = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = WORKSPACE / "courses"
ALL = ["cs168", "mit-6.006", "eth-ca", "mlsys-15442", "mit-6.5840"]
GATES = [("validate", ["--strict"]), ("check_style", []), ("audit_content", []),
         ("check_figures", ["--strict"]), ("check_reviewed", [])]


def check(name: str) -> bool:
    repo = COURSES / name
    if not (repo / "content").exists():
        print(f"  {name:<14} ✘ 仓不存在")
        return True

    # ★ 关键：临时目录用**仓名**（附录六十一）
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="vhead-")) / name
    tmp.mkdir(parents=True)
    try:
        # ① 导出 HEAD
        tar = subprocess.run(["git", "-C", str(repo), "archive", "HEAD"],
                             capture_output=True)
        if tar.returncode != 0:
            print(f"  {name:<14} ✘ git archive 失败")
            return False
        ex = subprocess.run(["tar", "-x", "-C", str(tmp)], input=tar.stdout,
                            capture_output=True)
        if ex.returncode != 0:
            print(f"  {name:<14} ✘ 解包失败：{ex.stderr.decode('utf-8', 'replace')[:80]}")
            return False

        # ② ★ 先核「引用了而磁盘上没有的图」——那是这一类最常见的形态
        missing: list[str] = []
        for md in sorted(tmp.glob("content/**/index.md")):
            t = md.read_text(encoding="utf-8", errors="replace")
            refs = re.findall(r"\]\((?:\.\./)*figures/([^)\s]+)\)", t)
            if not refs:
                continue
            fdir = md.parent / "figures"
            present = {p.name for p in fdir.glob("*")} if fdir.is_dir() else set()
            for r in dict.fromkeys(refs):
                if r not in present:
                    missing.append(f"{md.relative_to(tmp).as_posix()}: figures/{r}")

        # ③ 跑六道（在干净检出里）
        bad: list[str] = []
        for gate, extra in GATES:
            g = tmp / "scripts" / f"{gate}.py"
            if not g.exists():
                continue
            r = subprocess.run([PY, str(g), "--root", str(tmp)] + extra,
                               capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if r.returncode != 0:
                out = (r.stdout or "") + (r.stderr or "")
                errs = [l.strip() for l in out.split("\n") if "❌" in l][:2]
                bad.append(f"{gate}: " + (" / ".join(e[:70] for e in errs) if errs else f"exit={r.returncode}"))

        ok = not bad and not missing
        flag = "✅" if ok else "**✘**"
        print(f"  {name:<14} {flag} ｜ HEAD 缺图 {len(missing)} 处 ｜ 门红 {len(bad)} 道")
        for m in missing[:4]:
            print(f"        ★ 缺图: {m}")
        for b in bad:
            print(f"        ★ {b}")
        return ok
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)


def main() -> int:
    names = [sys.argv[1]] if len(sys.argv) > 1 else ALL
    print("  === 在**干净检出**上跑门（HEAD 的真实状态，而不是工作区）===")
    allok = all(check(n) for n in names)
    print(f"\n  ⇒ {'全部干净 ✅' if allok else '**有仓的 HEAD 不干净**'}")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
