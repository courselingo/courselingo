"""dup_term.py —— 找「术语名被写了两遍」的标记。

起因（2026-09-29，第 48 轮）：cs168 第 18 讲作者用**渲染后的 HTML** 证明：
    `[[term:router]]（router，路由器）` 渲染成 **`路由器（router）（router，路由器）`**
    —— 因为术语模板本身已经渲染出「中文（English）」，而作者又手打了一遍。
  它有实测证据（`site-mkdocs/lectures/bgp-implementation-and-issues.html`）。

★ 而这是**选择性**的：有的括号是合法的 ——
    `[[term:interior-gateway-protocol]]（IGP）` 里的 IGP 是**另一个缩写**（≠ 术语的 en），
    模板渲染出「内部网关协议（interior gateway protocol）」，作者补的是简称 ⇒ **不能删**。

⇒ 判据（精确）：`[[term:K]]（X，Y）` 且 **X == glossary[K].en** 且 **Y == glossary[K].zh**
   ⇒ 那是「把模板已经渲染的东西又打了一遍」⇒ 报。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"


def load_terms(cdir: pathlib.Path) -> dict[str, dict]:
    """读 glossary 的术语。

    ★ 坑（2026-09-29，我自己踩的）：**键不是 `key` 字段，而是由 `en` 推导的**
      —— glossary 表头逐字写着「规则：key 默认由 en 推导（小写、空格转连字符）」。
      我第一版只找 `key` ⇒ 只读到那一条显式写了 key 的（`as-path`）⇒ 判据报「0 处」。
      ⇒ 那是「检查没响」的成因 ①（它没跑对），而它的表现与「没问题」一模一样。
    """
    g = cdir / "glossary.toml"
    if not g.exists():
        return {}
    try:
        data = tomllib.loads(g.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out: dict[str, dict] = {}
    for t in data.get("term", []) or []:
        k = t.get("key")
        if not k and t.get("en"):
            k = str(t["en"]).lower().replace(" ", "-")
        if k:
            out[str(k)] = t
    return out


# [[term:k]]（X，Y）   允许全角/半角逗号
PAT = re.compile(r"\[\[term:([^\]]+)\]\]\s*[（(]\s*([^，,）)]+?)\s*[，,]\s*([^）)]+?)\s*[）)]")


def scan(cdir: pathlib.Path) -> list[str]:
    terms = load_terms(cdir)
    hits: list[str] = []
    for f in sorted(cdir.glob("content/**/index.md")):
        txt = f.read_text(encoding="utf-8", errors="replace")
        for m in PAT.finditer(txt):
            key, x, y = m.group(1), m.group(2).strip(), m.group(3).strip()
            t = terms.get(key)
            if not t:
                continue
            en = str(t.get("en", "")).strip()
            zh = str(t.get("zh", "")).strip()
            if en and zh and x.lower() == en.lower() and y == zh:
                rel = f.relative_to(cdir).as_posix()
                hits.append(f"{rel}: [[term:{key}]]（{x}，{y}） —— 模板已渲染「{zh}（{en}）」⇒ 重复")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course", nargs="?", default=None)
    a = ap.parse_args()
    courses = [a.course] if a.course else [d.name for d in sorted(COURSES.iterdir()) if (d / "content").exists()]
    total = 0
    for name in courses:
        cdir = COURSES / name
        hits = scan(cdir)
        if hits:
            print(f"\n=== {name}（{len(hits)} 处）===")
            for h in hits[:20]:
                print("  " + h)
            if len(hits) > 20:
                print(f"  … 另有 {len(hits)-20} 处")
        total += len(hits)
    print(f"\n⇒ 共 {total} 处")
    return 0


if __name__ == "__main__":
    sys.exit(main())
