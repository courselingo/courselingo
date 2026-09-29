#!/usr/bin/env python3
"""配图「需小修」的分诊 —— 把复核主张按「机检是否覆盖」分类。

★ 为什么（2026-09-29）：
  全仓 452 张图只有 165 张「可用」，**195 张「需小修」**。
  而按成因分类，**几何类占 98%**（`mlsys` 181 张里 177 张）。
  而我实测过多次：**那类几何主张有相当一部分是假的**（px 值超出 viewBox、按基线当中心量…）。

  ⇒ 于是关键问题是：**哪些可以机械地降级，哪些必须逐条实测？**
  ⇒ 答案取决于 `svg-lint`（`check_figures.py` 调它）**查不查那一类**。

`svg-lint` 的 12 项检查（读 `lib/checks/` 得到）：
  arrow-marker · baseline-offset · block-spacing · box-height · connector-geometry ·
  font-stack · light-bg-fallback · overlap · palette-conformance · text-overflow ·
  viewbox-clipping · xml-escaping

⇒ **它覆盖**：重叠 / 文字溢出 / 相邻块间距（最小值）/ 框高 / 框内文字垂直居中 /
  连接线几何 / 箭头尺寸 / 裁切 / 调色板 / 字体 / 转义。
⇒ **它不覆盖**：「对称 / 居中」、**「两个框宽度相等」**、「垂直间距均不均」。

用法：
    python figure_triage.py <课程>           # 分诊一个课程
    python figure_triage.py --all

输出：两类清单
  A. **机检覆盖**（`svg-lint --strict` 0/0）⇒ 该主张针对的性质**已被机检过且通过** ⇒ 低风险，可据实裁定
  B. **机检不覆盖**（居中 / 等宽 / 间距均匀）⇒ **必须逐条实测**，不能照它改图

★ 边界（必须说清）：A 类**不等于**「主张是假的」——
  机检过的是**那一类性质**，不是**那一条具体断言**。
  例：复核者说「两框间距 25 而别处 30」（不「均」），而 `block-spacing` 只查「≥25」⇒ 通过**不**能反驳它。
  ⇒ 所以 A 类的正确用法是**降低优先级**（residual risk 低），不是免检。
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

import json

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
VB = ROOT / "preview" / "visual-review"
LINTER = ROOT / "courselingo" / "tools" / "svg-lint" / "bin" / "svg-lint.mjs"

# 机检覆盖的主张类
COVERED = {
    "重叠/相碰": r"相碰|重叠|压住|覆盖",
    "文字溢出": r"溢出|超出方框|溢出方框|撑破",
    "间距不足": r"拥挤|间距过小|间距不足|贴住|贴得",
    "框高/基线": r"框高|过矮|压边|基线|垂直居中",
    "裁切": r"裁切|超出画布|超出 viewBox|被切",
    "箭头几何": r"箭头.*(落点|偏移|偏离|不接|悬空|没接)|落点.*箭头",
}
# 机检**不**覆盖的
UNCOVERED = {
    "居中/对称": r"不居中|未居中|不对称|偏左|偏右|偏上|偏下|居中",
    "等宽": r"不等宽|宽度不一|宽窄|宽度不一致",
    "间距均匀": r"间距.*(不一|不均|不匀)|节奏不均|疏密",
    "信息缺失": r"缺失|未标注|没有标注|找不到|丢掉|省掉|为排版|无法体现|名实不符",
    "语义/指代": r"不明|指代|先行词|无依据|歧义|看不出|读不出",
    "文字矛盾": r"矛盾|冲突|不一致|相反|说反|对不上",
}


def lint_one(svg: pathlib.Path) -> tuple[int, int]:
    node = "D:/Software/nodejs/node.exe"
    if not pathlib.Path(node).exists():
        node = "node"
    r = subprocess.run([node, str(LINTER), "--strict", str(svg)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    e = len(re.findall(r"\b error\b", out))
    w = len(re.findall(r"\b warning\b", out))
    m = re.search(r"(\d+) error\(s\), (\d+) warning\(s\)", out)
    if m:
        return int(m.group(1)), int(m.group(2))
    return e, w


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    targets = [cd for cd in sorted(COURSES.iterdir())
               if (cd / "content").exists() and (not a.course or a.all or cd.name == a.course)]

    for cd in targets:
        pending = []
        for f in sorted((cd / "content").rglob("figures/*.svg")):
            rep = cd / "docs" / "audit" / "visual-review" / f"{cd.name}__{f.stem}.md"
            if not rep.exists():
                rep = VB / f"{cd.name}__{f.stem}.md"
            if not rep.exists():
                continue
            txt = rep.read_text(encoding="utf-8", errors="replace")
            if not re.search(r"判定[：:]\s*\**\s*(有错误|需小修)", txt):
                continue
            blk = txt.split("## 缺陷", 1)[-1].split("## 判定", 1)[0]
            cov = [k for k, p in COVERED.items() if re.search(p, blk)]
            unc = [k for k, p in UNCOVERED.items() if re.search(p, blk)]
            pending.append((f, cov, unc))
        if a.limit:
            pending = pending[:a.limit]
        if not pending:
            continue
        print(f"=== {cd.name}（{len(pending)} 张需处置）===\n")
        n_cov = n_unc = 0
        for f, cov, unc in pending:
            e, w = lint_one(f)
            lint_ok = (e == 0 and w == 0)
            tag = []
            if cov:
                tag.append("覆盖:" + "/".join(cov))
            if unc:
                tag.append("不覆盖:" + "/".join(unc))
            if lint_ok and cov and not unc:
                n_cov += 1
                verdict = "A 低风险（该主张的类已被机检过且 0/0）"
            elif unc:
                n_unc += 1
                verdict = "B 必须实测（机检不覆盖这一类）"
            else:
                verdict = "C 需看原文"
            print(f"  {f.stem:<34} lint {e}E/{w}W ｜ {verdict}")
            if tag:
                print(f"      {'; '.join(tag)}")
        print(f"\n  ⇒ A（机检覆盖）{n_cov} 张 ｜ B（须实测）{n_unc} 张 ｜ 其余 {len(pending)-n_cov-n_unc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
