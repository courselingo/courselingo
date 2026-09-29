#!/usr/bin/env python3
"""⛔ 已弃用 —— 不要把测量工具升级成判断工具（本文件是那次失败的留档）。

★ 为什么留在这里而不是删掉（2026-09-29）：
  它想做的事是「把复核者主张与客观实测比对，自动产出裁定草稿」。
  而它**两次都失败**，且失败方向相反：
    ① 第一版把 `cs168/layers-3` 判成「**可用**」—— 而那张是**真有问题**的
       （标题讲「要拉的线」，图里 0 条线）。根因：它把「必要信息缺失」也接到了
       `svg-lint` 那一支，而 `svg-lint` **不检查「图上有没有那句话承诺的结构」**。
    ② 加了一道「缺失类一律交人判」之后，它把 **9/11 张**都判成「需人判」——
       因为复核者在**每份**报告里都写一句「其余各项（…**必要信息缺失**）：**未发现**」，
       而那是它在声明**没发现**缺失，被正则当成了**主张**缺失。
  ⇒ 于是它在「危险」（把真问题判成可用）与「无用」（把假主张判成需人判）之间来回。

★ 结论（本项目的判据）：
  **`tools/figure_measure.py` 只展示客观事实 ⇒ 安全、有用。**
  **本文件下结论 ⇒ 走不通。**
  ⇒ 几何主张的裁定**必须由人做**，工具只能把事实摆到他面前（`附录十一`：几何问属性，判断问人）。

⇒ 保留源码是为了让下一个人**不必再试一次**。要看事实请用 `figure_measure.py`。
"""
from __future__ import annotations

import sys

if __name__ == "__main__":
    print("⛔ 本工具已弃用（见文件头）。几何主张的裁定必须由人做。")
    print("   要看客观事实请用：python tools/figure_measure.py <课程>")
    sys.exit(2)

# ───────── 以下是弃用前的实现（留档，不再执行）─────────
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import hashlib

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
VB = ROOT / "preview" / "visual-review"
LINTER = ROOT / "courselingo" / "tools" / "svg-lint" / "bin" / "svg-lint.mjs"


def num(a: str, k: str) -> float | None:
    m = re.search(rf'\b{k}="(-?[\d.]+)"', a)
    return float(m.group(1)) if m else None


def geom(svg: pathlib.Path) -> dict:
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
        if vw and vh and w >= vw - 1 and h >= vh - 1:
            continue
        rects.append((x, y, w, h))
    texts = []
    for m in re.finditer(r"<text([^>]*)>([^<]*)</text>", raw):
        a, body = m.group(1), m.group(2).strip()
        x = num(a, "x")
        if x is None:
            continue
        fs = num(a, "font-size") or 12
        texts.append({"x": x, "body": body, "fs": fs})
    return {"raw": raw, "vw": vw, "vh": vh, "rects": rects, "texts": texts}


def gaps_of(rects, axis: str) -> list[float]:
    groups: dict[float, list] = {}
    for x, y, w, h in rects:
        key = round(y if axis == "h" else x, 1)
        groups.setdefault(key, []).append((x, x + w) if axis == "h" else (y, y + h))
    out = []
    for _, iv in sorted(groups.items()):
        iv.sort()
        for (a1, b1), (a2, b2) in zip(iv, iv[1:]):
            g = a2 - b1
            if -1 < g < 400:
                out.append(round(g, 1))
    return out


def lint(svg: pathlib.Path) -> str:
    node = "D:/Software/nodejs/node.exe"
    if not pathlib.Path(node).exists():
        node = "node"
    r = subprocess.run([node, str(LINTER), "--strict", str(svg)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+) error\(s\), (\d+) warning\(s\)", out)
    return f"{m.group(1)}E/{m.group(2)}W" if m else "?"


def judge(claim: str, g: dict, lintres: str, stem: str) -> tuple[str, str]:
    """返回 (草稿裁定, 依据)。草稿只有「可用」或「⚠ 需人判」。

    ★★★ 而它**第一版出过一次危险的假裁定**（2026-09-29，实测）：
      它给 `cs168/layers-3` 产出了「**可用**」，理由是 `svg-lint --strict` 0E/0W ——
      **而那一张正是真有问题的那张**（标题讲「要拉的线」，图里 **0 条线**）。
      根因：它把「**必要信息缺失**（连线/箭头）」也接到了 `svg-lint` 那一支，
      而 `svg-lint` **不检查「图上有没有那句话承诺的结构」**。
    ⇒ 这正是我在本文件抬头写的边界（「机检过了只覆盖它查的那一类」）—— **而工具违反了它自己的声明。**

    ★ 修法两条：
      ① **「缺失类」主张一律不自动裁定**（`svg-lint` 与几何属性都答不了「该有的东西在不在」）
      ② `svg-lint` 那一支**只**在主张是关于**重叠/溢出/裁切**（它真查的东西）时才启用
    """
    facts, cites = [], []
    refuted = False

    # ★ 先拦「缺失类」—— 这类**永远**交人判
    MISSING = r"缺失|未标注|没有标注|找不到|丢掉|省掉|为排版|无法体现|名实不符|没画|未画|缺|无任何|一条线都没"
    if re.search(MISSING, claim):
        return ("⚠ 需人判",
                "★ 这是**「图上缺了文字承诺的结构」**类主张 —— "
                "`svg-lint` 与几何属性都**答不了**「该有的东西在不在」。"
                "须人读标题与图，逐句问「这句话承诺的东西图上有吗」（`附录十` 补记第三轮）")

    # ① 不等宽
    if re.search(r"不等宽|宽度不一|宽窄|宽度不一致|明显窄|明显宽", claim) and g["rects"]:
        ws = sorted({round(r[2], 1) for r in g["rects"]})
        facts.append(f"框宽集合 {ws}")
        if len(ws) == 1 and len(g["rects"]) >= 2:
            refuted = True
            cites.append(f"**所有 {len(g['rects'])} 个框 `width` 全等 = {ws[0]:.0f}**")

    # ② 居中 / 偏左偏右
    if re.search(r"不居中|未居中|偏左|偏右|不对称", claim) and g["rects"] and g["vw"]:
        lefts = [r[0] for r in g["rects"]]
        rights = [r[0] + r[2] for r in g["rects"]]
        cl, cr = min(lefts), max(rights)
        cc = (cl + cr) / 2
        lm, rm = cl, g["vw"] - cr
        title = max(g["texts"], key=lambda t: t["fs"]) if g["texts"] else None
        facts.append(f"内容中心 {cc:.1f} / 画布中心 {g['vw']/2:.1f}；边距 {lm:.1f}/{rm:.1f}")
        if abs(lm - rm) <= 2:
            refuted = True
            cites.append(f"左外边距 **{lm:.0f}** / 右外边距 **{rm:.0f}**（差 {abs(lm-rm):.1f}）")
        if title and abs(title["x"] - cc) <= 2 and re.search(r"标题|题", claim):
            refuted = True
            cites.append(f"标题 `x={title['x']:.1f}` vs 内容中心 {cc:.1f} ⇒ **差 {abs(title['x']-cc):.1f}px**")

    # ③ 间距不均
    if re.search(r"间距|间隔|节奏|疏密|空白", claim):
        hg, vg = gaps_of(g["rects"], "h"), gaps_of(g["rects"], "v")
        for name, arr in (("水平", hg), ("垂直", vg)):
            if len(arr) >= 2:
                spread = max(arr) - min(arr)
                facts.append(f"{name}间隙 {arr}")
                if spread <= 1:
                    refuted = True
                    cites.append(f"{name}间隙 `{arr}` ⇒ **最大−最小 = {spread:.1f}**")

    # ④ 重叠/溢出/拥挤/裁切 ⇒ 由 svg-lint 覆盖
    #    ★ 只有当主张**确实**是这几类时才启用（第一版没加这个限定，于是误判了 layers-3）
    if re.search(r"相碰|溢出|拥挤|重叠|裁切|超出画布", claim):
        facts.append(f"svg-lint {lintres}")
        if lintres.startswith("0E/0W"):
            refuted = True
            cites.append(f"`svg-lint --strict` **{lintres}**（它检查重叠/文字溢出/间距/裁切）")

    if not facts:
        return "⚠ 需人判", "（本工具认不出这类主张；请手工量）"
    if refuted:
        return "可用", "；".join(cites) + f"。客观事实：{' ｜ '.join(facts)}｜Lead（`tools/adjudicate_draft.py`）"
    return "⚠ 需人判", f"实测未否证该主张。客观事实：{' ｜ '.join(facts)}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    cd = COURSES / a.course
    vdir = cd / "docs" / "audit" / "visual-review"
    if not (cd / "content").exists():
        print("没有这个课程")
        return 1

    drafts, need = [], []
    for rep in sorted(vdir.glob(f"{cd.name}__*.md")):
        stem = rep.stem.replace(f"{cd.name}__", "")
        if a.only and stem != a.only:
            continue
        txt = rep.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"判定[：:]\s*\**\s*(有错误|需小修)", txt):
            continue
        claim = txt.split("## 缺陷", 1)[-1].split("## 判定", 1)[0].strip().replace("\n", " ")
        svg = next((cd / "content").rglob(f"figures/{stem}.svg"), None)
        if not svg:
            continue
        g = geom(svg)
        lr = lint(svg)
        verdict, basis = judge(claim, g, lr, stem)
        rh = hashlib.sha256(rep.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()[:16]
        row = f"| {stem} | 需小修 | {verdict} | {basis} | `{rh}` |"
        if verdict == "可用":
            drafts.append((stem, row))
        else:
            need.append((stem, basis[:110]))
        if a.limit and len(drafts) + len(need) >= a.limit:
            break

    print(f"=== {cd.name}：可自动裁定 {len(drafts)} 张 ｜ 需人判 {len(need)} 张 ===\n")
    if drafts:
        print("★ 以下为**裁定草稿**（请审阅后再粘进 `visual-adjudications.md`）：\n")
        for stem, row in drafts:
            print(f"  {stem}")
            print(f"    {row}\n")
    if need:
        print("★ 需人判：")
        for stem, why in need:
            print(f"  {stem:<34} {why}")

    if a.write and drafts:
        adj = cd / "docs" / "audit" / "visual-adjudications.md"
        with adj.open("a", encoding="utf-8") as f:
            f.write(f"\n<!-- 由 tools/adjudicate_draft.py 生成的草稿 · 待 Lead 审阅 -->\n")
            for _, row in drafts:
                f.write(row + "\n")
        print(f"\n⇒ 已追加 {len(drafts)} 行到 {adj.name}（**请审阅**）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
