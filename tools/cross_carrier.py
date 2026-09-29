"""cross_carrier.py —— 比对「同一个数 / 同一个序数」在**三个载体**之间是否一致。

★ **本工具**不是闸门**，是一个**线索生成器**。它被实测证明精确率极低，见下。

起因（2026-09-29，第 44 轮）：一位独立复核者在 cs168 第 16 讲查出 4 处六道闸门全都查不出的缺陷，
      其中一处是 **图注与正文说反了**（图说「第一、二步与第三步矛盾」，正文说「第三与第四步矛盾」），
      另一处是 **表格 5 行而正文说「四步」**。

⇒ 那类缺陷的形状是：**两个载体各自自洽、合起来矛盾。**
  我本以为「数值/序数那一半可机械化」（`附录二十六`：让一类错误画不出来）——
  **⇒ 而我把它做出来、并在全部既有语料上量了一遍，结论是**不行**：

```
                        A(数量冲突)  B(序数不同)  C(同页多值)   合计   命中讲次
  mlsys-15442  21 讲        41          22          173       236    21/21
  cs168        17 讲        15          20           91       126    17/17
  eth-ca       20 讲        36          26          131       193    20/20
  mit-6.006     7 讲         5           3           39        47     6/7
  ⇒ C 占全部命中的 73% —— 而它是**语言的正常样子**（一页里正常地会用「个/条」配很多不同的数）
  ⇒ A+B 合计 105 处。而**已知的真缺陷只有 1 处**（cs168 第 16 讲那处）
    ⇒ **精确率约 3%** ⇒ 作为闸门会把所有作者的时间吃掉。
```

⇒ **所以：中文数词/序数的跨载体一致性，不可机械化。**
   根因是中文说一个数有很多种写法，而一页里**正常**地会用很多不同的数值 ——
   判据无法区分「同一个量的两种写法」与「两个不同的量」。

★ 这是我**第二次**造出一条误报的检查（第一次是 2026-09-29 那条「中文标点前的孤立英文词」）。
  而两次的教训是同一条：**「想抓一类缺陷」与「那类缺陷可机械化」是两件事。**
  ⇒ 而第二次我学会了**先量再定**（第一次是先加了才测，让一位作者实测后报回来）。

★★ 用法（**当作人工复核的线索清单，不要当门**）：
    python cross_carrier.py <课程> [--lecture <目录名>] [--all]
      · 默认只报 A 与 B（定位到具体图，噪音相对小）
      · `--all` 才输出 C（同页多值）—— ~~它几乎每页都响~~ 它每页都响
    ★ 每条命中都要人**回去读那两个载体**再判；**不要把它的输出当作缺陷清单。**
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"

CN = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7,
      "八": 8, "九": 9, "十": 10, "十一": 11, "十二": 12}
QUANT = "步|条|个|层|类|种|张|行|列|块|段|件|项|轮|遍|点"

# 「四步」「五条」「三个」这类
RE_CN_NUM = re.compile(rf"([一二两三四五六七八九十]{{1,3}})\s*({QUANT})")
RE_AR_NUM = re.compile(rf"(\d{{1,2}})\s*({QUANT})")


def nums_near(text: str) -> list[tuple[str, str, int]]:
    """返回该文本里所有「数 + 量词」，形如 [("四","步",4), ("5","条",5)]。"""
    out: list[tuple[str, str, int]] = []
    for m in RE_CN_NUM.finditer(text):
        if m.group(1) in CN:
            out.append((m.group(1), m.group(2), CN[m.group(1)]))
    for m in RE_AR_NUM.finditer(text):
        out.append((m.group(1), m.group(2), int(m.group(1))))
    return out


def ordinals(text: str) -> set[int]:
    """返回文本里出现的序数（「第一步」「第三」「第四类」… → {1,3,4}）。"""
    s: set[int] = set()
    for m in re.finditer(rf"第\s*([一二两三四五六七八九十]{{1,3}})\s*(?:{QUANT})?", text):
        if m.group(1) in CN:
            s.add(CN[m.group(1)])
    for m in re.finditer(rf"第\s*(\d{{1,2}})\s*(?:{QUANT})?", text):
        s.add(int(m.group(1)))
    return s


def check_lecture(ldir: pathlib.Path) -> list[str]:
    idx = ldir / "index.md"
    if not idx.exists():
        return []
    lines = idx.read_text(encoding="utf-8", errors="replace").splitlines()
    findings: list[str] = []

    for i, ln in enumerate(lines):
        m = re.match(r"^\s*!\[([^\]]*)\]\(([^)]+)\)", ln)
        if not m:
            continue
        alt, path = m.group(1), m.group(2)
        svg = ldir / path
        svgtext = ""
        if svg.exists():
            svgtext = svg.read_text(encoding="utf-8", errors="replace")
        title = ""
        desc = ""
        mt = re.search(r"<title[^>]*>(.*?)</title>", svgtext, re.S)
        if mt:
            title = mt.group(1)
        md = re.search(r"<desc[^>]*>(.*?)</desc>", svgtext, re.S)
        if md:
            desc = md.group(1)

        # 正文窗口：图片上下各 6 行
        lo, hi = max(0, i - 6), min(len(lines), i + 7)
        prose = "\n".join(x for j, x in enumerate(lines[lo:hi]) if j + lo != i)

        fig_side = f"{alt}\n{title}\n{desc}"

        # ── A. 数量词冲突 ──
        fig_nums = nums_near(fig_side)
        prose_nums = nums_near(prose)
        for q in {q for _, q, _ in fig_nums} & {q for _, q, _ in prose_nums}:
            fv = {v for _, qq, v in fig_nums if qq == q}
            pv = {v for _, qq, v in prose_nums if qq == q}
            if fv and pv and not (fv & pv):
                findings.append(
                    f"[A·数量冲突] {ldir.name}/{svg.name or path}（index.md L{i+1}）"
                    f" 图侧说「{'/'.join(str(x) for x in sorted(fv))}{q}」"
                    f"，而正文说「{'/'.join(str(x) for x in sorted(pv))}{q}」"
                )

        # ── B. 序数集合不同 ──
        fo, po = ordinals(fig_side), ordinals(prose)
        if fo and po and fo != po:
            only_f, only_p = sorted(fo - po), sorted(po - fo)
            if only_f or only_p:
                findings.append(
                    f"[B·序数不同] {ldir.name}/{svg.name or path}（index.md L{i+1}）"
                    f" 图侧提到第 {fo}，正文提到第 {po}"
                    f"（只在图侧 {only_f}，只在正文 {only_p}）"
                )

    # ── C. 同页同量词、不同数 ──
    whole = "\n".join(lines)
    by_q: dict[str, set[int]] = {}
    for _, q, v in nums_near(whole):
        by_q.setdefault(q, set()).add(v)
    for q, vs in by_q.items():
        if len(vs) > 1:
            findings.append(f"[C·同页多值] {ldir.name} 量词「{q}」在本页出现多个值：{sorted(vs)}")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course")
    ap.add_argument("--lecture", default=None)
    ap.add_argument("--all", action="store_true",
                    help="连 C（同页多值）也输出 —— 它几乎每页都响，默认不出")
    a = ap.parse_args()
    cdir = COURSES / a.course
    if not cdir.exists():
        print(f"✗ 没有这门课：{cdir}")
        return 2
    dirs = sorted(cdir.glob(f"content/{a.lecture}")) if a.lecture else sorted((cdir / "content").iterdir())
    total = 0
    for ld in dirs:
        if not ld.is_dir():
            continue
        fs = check_lecture(ld)
        if not a.all:
            fs = [x for x in fs if not x.startswith("[C")]
        if fs:
            total += len(fs)
            print(f"\n=== {ld.name} ===")
            for f in fs:
                print("  " + f)
    print(f"\n⇒ 共 {total} 条（★ 这些是**线索**，不是结论 —— 每一条都要人回去读那两个载体再判）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
