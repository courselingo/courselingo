"""safe_commit.py —— **只有在全仓门全绿时才允许提交**。

★ 为什么需要它（`附录五十八`）：第 48 轮我在作者还在写的时候提交了他的目录，
  而那个快照**少了 4 条术语定义** ⇒ **HEAD 的干净检出 3 个 ERROR** ⇒
  **任何克隆这个仓的人都跑不过 validate**，而他会以为是自己弄坏了。
  ⇒ 那次是我**没有看** ERROR 就提交。

★ 而这一轮（第 56 轮）我又一次看到同一状态：cs168 第 21 讲的正文用了
  `[[term:fairness]]` / `[[term:pricing]]` 而 glossary 还没有它们 ⇒
  `validate` 报 **5 个错误** —— 那位作者**正在写**。
  ⇒ **同一个诱惑又出现了：看到文件存在就想提交。**

⇒ 所以把纪律变成结构：**提交之前跑全仓门，任一红就不提交**，并打印**是谁的红**。
  ★ 而它与我此前那条（`附录五十九`：工具的报数要「读回核验」）是同一条：
    **不要用一个「看起来对」的信号代表「做成了」** ——
    而「文件存在」不是「这一讲做完了」。

用法：
    python tools/safe_commit.py <课程> "<提交信息>" [--paths a b c]
    python tools/safe_commit.py --all-check        # 只检查，不提交
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

PY = sys.executable
# ★ 本文件住在**平台仓**的 tools/ 里（`附录六十三` 修：我原先把它建在工作区根，而那不是 git 仓）
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent / "courses"
# ★ `--strict` 只加在「页面会渲染坏」的那两道门上（2026-09-29 修，附录七十五）。
#
# 起因：一位作者修好了 `audit_content.py` 里「点名不足」那条分支的 `NameError`
#   （它此前会让**点名不足的页面**整道闸门崩掉，于是那条警告报不出来），
#   并把计数从**子串匹配**改成**词边界** ——
#   ⇒ 而修好之后，**五门课同时变红**：原先池里的 `Go` 命中 `goal`/`go through`、
#     `Raft` 命中 `draft` ⇒ 计数虚高 ⇒ 那些页**不该通过却通过了**。
#
# ⇒ 而那些红是**真的**（它们是内容欠账），而它们不该**阻塞提交**：
#   · `validate --strict`  ⇒ 术语未定义 / 漂移 / 名字写两遍 —— 这些**会让页面渲染坏** ⇒ 必须挡
#   · `audit_content --strict` ⇒ 点名不足 / 密度 / 破折号 —— 这些是**质量欠账**，页面是好的
#
# ★ 而这个区分很重要，因为若 WARN 也挡提交，我为了能提交就会去改内容 ——
#   而那正是「**为工具改内容**」，是本项目明确禁止的。
# ⇒ 所以：**ERROR 挡住提交，WARN 只当清单**。
GATES = [
    ("validate", ["--strict"]),
    ("check_style", []),
    ("audit_content", []),
    ("check_figures", ["--strict"]),
    ("check_reviewed", []),
]


def run_gates(cdir: pathlib.Path) -> tuple[bool, list[tuple[str, int, list[str]]]]:
    """跑全仓门。返回 (全绿?, [(门, exit, 报错的文件)])。"""
    results = []
    allok = True
    for gate, extra in GATES:
        f = cdir / "scripts" / f"{gate}.py"
        if not f.exists():
            continue
        r = subprocess.run([PY, str(f), "--root", str(cdir)] + extra,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        # ★ 只从**含 ❌ 的行**里抓文件名（2026-09-29 修）——
        #   第一版从整段输出里抓，于是「✅ 20 篇全过」这类汇总行也被算进去，
        #   结果「红的文件」列了全部 21 讲（而实际只有 1 讲红）。
        #   ⇒ 而那个字段恰恰是操作者唯一要的答案：「到底哪一讲是红的？」
        if r.returncode != 0:
            bad_lines = [l for l in out.splitlines() if "❌" in l]
            files = sorted({m for l in bad_lines
                            for m in re.findall(r"content[/\\]([\w\-.]+)[/\\]", l)})
        else:
            files = []
        results.append((gate, r.returncode, files))
        if r.returncode != 0:
            allok = False
    return allok, results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course", nargs="?")
    ap.add_argument("message", nargs="?")
    ap.add_argument("--paths", nargs="*", default=None)
    ap.add_argument("--all-check", action="store_true")
    a = ap.parse_args()

    courses = [a.course] if a.course else [d.name for d in sorted(ROOT.iterdir())
                                           if (d / "content").exists()]
    for name in courses:
        # 允许传 "cs168" 或 "courses/cs168"
        cdir = ROOT / pathlib.Path(name).name
        if not cdir.exists():
            print(f"  {name:<14} ✘ 不存在")
            continue
        allok, results = run_gates(cdir)
        stale = sorted({f for _, _, fs in results for f in fs})
        mark = "✅ 全绿" if allok else "**✘ 有红**"
        print(f"  {name:<14} {mark}" + (f" ｜ 红的文件：{', '.join(stale)}" if stale else ""))

        if a.all_check or not a.message:
            continue
        if not allok:
            print(f"  ⇒ **拒绝提交**：全仓门没全绿 ⇒ 很可能有人在写别的讲次。")
            print(f"     ★ 而这不是「等一会儿再试」就行的 —— 先确认那一讲是不是**别人的在制品**。")
            print(f"     ★ 若确实是你这一讲的错，先修它；若是别人的，只提交你自己那几条路径时")
            print(f"       也必须确认**那几条路径自身是干净的**（本条判据是全仓的，不细分路径）。")
            continue
        cmd = ["git", "-C", str(cdir), "add"] + (a.paths if a.paths else ["-A"])
        subprocess.run(cmd, capture_output=True)
        staged = subprocess.run(["git", "-C", str(cdir), "diff", "--cached", "--name-only"],
                                capture_output=True, text=True).stdout.split()
        if not staged:
            print(f"  ⇒ 暂存区为空，不提交")
            continue
        # ★ 提交前再跑一次（防止 add 与检查之间有人改了别的文件）
        allok2, results2 = run_gates(cdir)
        if not allok2:
            subprocess.run(["git", "-C", str(cdir), "reset"], capture_output=True)
            print(f"  ⇒ **暂存后又出现红 ⇒ 已 reset，不提交**")
            continue
        c = subprocess.run(["git", "-C", str(cdir), "commit", "-q", "-m", a.message],
                           capture_output=True, text=True)
        if c.returncode != 0:
            print(f"  ⇒ 提交失败：{c.stderr.strip()[:100]}")
            continue
        head = subprocess.run(["git", "-C", str(cdir), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        print(f"  ⇒ 已提交 {len(staged)} 个文件 ｜ HEAD={head}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
