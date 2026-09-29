#!/usr/bin/env python3
"""生成「质量审核记录」的骨架 —— 把能自动取到的部分取到，只留判断给 Lead。

★ 为什么写这个（2026-09-29）：
  本项目提级的硬条件是「有审核记录」（§9，check_reviewed 会读它）。
  而已产出 38 讲里只有 4 讲提级，缺口几乎全是「审核记录 + 透镜 3」——
  这两件只有 Lead 能做（记录要他签、透镜 3 要他设计）。
  ⇒ 而记录里**大部分内容是机械的**：哈希、六道退出码、事实核对结论、视觉复核分布。
  ⇒ 所以把它批量化：机械的自动填，判断的留空。

用法：
    python make_audit_record.py <课程> [<slug> ...]
    python make_audit_record.py --all          # 所有缺记录的讲

设计原则（与项目判据一致）：
  · **只填机器能证的**（哈希、退出码、报告里的判定行），**不替 Lead 下任何判断**
  · 事实核对的 P0/P1/P2 从记录里**原样抄**（不解析成语义，只摘那一行）
  · 视觉复核的**分布**给出来，并**逐张列出非「可用」的**（那是 Lead 必须处置的）
  · 已存在记录**不覆盖**（打印跳过），除非加 --force
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
VB = ROOT / "preview" / "visual-review"
PY = sys.executable


def nhash(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def gates(course_dir: pathlib.Path) -> list[tuple[str, int]]:
    """跑六道闸门，返回 (名字, 退出码)。"""
    out: list[tuple[str, int]] = []
    specs = [
        ("validate", ["--quiet"]),
        ("check_style", []),
        ("audit_content", ["--strict"]),
        ("check_figures", ["--strict"]),
        ("check_reviewed", []),
    ]
    for name, extra in specs:
        s = course_dir / "scripts" / f"{name}.py"
        if not s.exists():
            out.append((name, -1))
            continue
        r = subprocess.run([PY, str(s), "--root", str(course_dir), *extra],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out.append((name, r.returncode))
    s = course_dir / "scripts" / "build_site.py"
    if s.exists():
        r = subprocess.run([PY, str(s), "--root", str(course_dir), "--out", "site-mkdocs"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out.append(("build_site", r.returncode))
    return out


def factcheck_summary(course_dir: pathlib.Path, slug: str) -> tuple[str, str]:
    """返回 (记录文件名, 结论行)。"""
    ad = course_dir / "docs" / "audit"
    short = slug.split("/")[-1]
    for f in sorted(ad.glob("*factcheck*.md")):
        if short.lstrip("0") and short.lstrip("0") in f.stem:
            t = f.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"P0[^\n]{0,110}", t)
            return f.name, (m.group(0).strip() if m else "（未找到 P0 行）")
    return "（无）", "（无事实核对记录）"


def visual_summary(course_dir: pathlib.Path, slug: str) -> tuple[dict[str, int], list[str]]:
    """返回 (判定分布, 需要 Lead 处置的图名列表)。

    ★★ 必须**查新鲜度** —— 否则会把「早已修好」的旧判定报成拦路石。
    实测（2026-09-29，本脚本第一版）：它报 `cs168` 第 2 讲「有错误 2 张」（layers-3 / layers-6），
    而这两张**作者早已修好并报了新哈希** —— 因为报告是**过期**的，而本函数当时不看这一点。
    **⇒ 一份精确的统计若建立在过期报告上，它比没有统计更糟**（它会让人去修已经修好的东西）。
    ⇒ 与 `refresh_one.py` 同一口径：**报告里记的被复核 SVG 哈希 ≠ SVG 的当前 nhash ⇒ 过期**。
    """
    figs = sorted((course_dir / "content" / slug / "figures").glob("*.svg"))
    dist = {"可用": 0, "需小修": 0, "有错误": 0, "?": 0, "缺报告": 0, "过期": 0}
    bad: list[str] = []
    for f in figs:
        rep = course_dir / "docs" / "audit" / "visual-review" / f"{course_dir.name}__{f.stem}.md"
        if not rep.exists():
            rep2 = VB / f"{course_dir.name}__{f.stem}.md"
            rep = rep2 if rep2.exists() else rep
        if not rep.exists():
            dist["缺报告"] += 1
            bad.append(f"{f.stem}（无报告）")
            continue
        txt = rep.read_text(encoding="utf-8", errors="replace")
        # ★ 新鲜度：报告里记的被复核 SVG 哈希 必须等于 SVG 的当前 nhash
        m = re.search(r"SHA256\(前16\)[：:]\s*`?([0-9A-F]{16})", txt)
        cur = nhash(f)[:16]
        if not m or (m.group(1) != cur and not cur.startswith(m.group(1))):
            dist["过期"] += 1
            bad.append(f"{f.stem}（**报告过期**：报告记 {m.group(1) if m else '?'} / 现值 {cur}）"
                       "⇒ 先重跑视觉复核，不要照这份报告的判定改")
            continue
        for k in ("有错误", "需小修", "可用"):
            if re.search(rf"判定[：:]\s*\**\s*{k}", txt):
                dist[k] += 1
                if k != "可用":
                    bad.append(f"{f.stem}（{k}）")
                break
        else:
            dist["?"] += 1
            bad.append(f"{f.stem}（判定无法解析）")
    return dist, bad


def adjudications_note(course_dir: pathlib.Path, slug: str) -> str:
    """指出本讲有哪些图**已被实测裁定覆盖**。

    ★ 为什么需要（2026-09-29，实测）：本脚本第一版只查新鲜度、**不读裁定表**，
    于是它在 `cs168` 第 2 讲上仍报「需小修 1」（`headers-1`），
    而 `headers-1` **已经被裁定为可用**（实测两框都 344、外边距 22/22）。
    ⇒ 与「不查新鲜度」是同一类问题：**工具不读那个权威来源。**
    ⇒ 一份审核记录应当同时写出**原始判定**与**已被裁定的部分**，否则 Lead 会重复处置。
    """
    adj = course_dir / "docs" / "audit" / "visual-adjudications.md"
    if not adj.exists():
        return ""
    figs = {f.stem for f in (course_dir / "content" / slug / "figures").glob("*.svg")}
    rows: list[str] = []
    for ln in adj.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 4 or cells[0] in ("图", "---") or set(cells[0]) <= {"-"}:
            continue
        if cells[0] in figs and "可用" in cells[2]:
            rows.append(f"- `{cells[0]}`：原判「{cells[1]}」→ 裁定「{cells[2]}」｜依据：{cells[3][:100]}…")
    if not rows:
        return ""
    return ("\n**★ 其中以下图已由 `docs/audit/visual-adjudications.md` 的实测裁定覆盖**"
            "（`check_reviewed.py` 会读它）：\n\n" + "\n".join(rows) + "\n")


def make(course_dir: pathlib.Path, slug: str, force: bool) -> str:
    idx = course_dir / "content" / slug / "index.md"
    if not idx.exists():
        return f"跳过（无页面）：{slug}"
    ad = course_dir / "docs" / "audit"
    ad.mkdir(parents=True, exist_ok=True)
    # 编号：用 slug 里的序号
    num = re.match(r"(\d+)", slug)
    n = num.group(1) if num else "??"
    out = ad / f"lecture-{n}-quality-audit.md"
    if out.exists() and not force:
        return f"跳过（已有记录）：{out.name}"

    gs = gates(course_dir)
    bad_gates = [f"{k}={v}" for k, v in gs if v != 0]
    fc_name, fc_line = factcheck_summary(course_dir, slug)
    dist, bad_figs = visual_summary(course_dir, slug)
    adj_note = adjudications_note(course_dir, slug)
    h = nhash(idx)[:16]

    body = f"""# 质量审核记录 · {slug}（第 {int(n)} 讲）

> §9 要求：`status = "reviewed"` 的前置条件是「**P0/P1 清零 + 有审核记录**」。
> 本文件是**自动生成的骨架** —— 机械部分已填，**判断部分留空待 Lead 填**。
> 自动生成时间：{__import__('datetime').datetime.now():%Y-%m-%d %H:%M}

## 1. 被审核版本

| 项 | 值 |
| --- | --- |
| 页面 | `content/{slug}/index.md` |
| 归一化哈希（CRLF→LF 后 SHA256 前 16） | `{h}` |
| 产出形态 | `output_mode = "explanation"`（依 `courselingo/docs/output-mode-decision.md` §3） |
| 源材料 | 见该页 front matter 的 `source_url` / `source_title` |

## 2. 六道机检（自动跑）

| 闸门 | 退出码 |
| --- | --- |
{chr(10).join(f"| `{k}.py` | {v} |" for k, v in gs)}

{"**❌ 有闸门未过：" + "、".join(bad_gates) + "**" if bad_gates else "**✅ 六道全 0。**"}

## 3. 第一道人工闸门 · 非作者事实核对

- 记录：`docs/audit/{fc_name}`
- **结论行（原样摘抄）**：{fc_line}
- **⬜ 待 Lead 填**：逐条 P0/P1 的处置与复核情况

## 4. 第二道人工闸门 · 配图视觉复核（自动统计）

| 判定 | 张数 |
| --- | --- |
| 可用 | {dist['可用']} |
| 需小修 | {dist['需小修']} |
| 有错误 | {dist['有错误']} |
| 判定无法解析 | {dist['?']} |
| 缺报告 | {dist['缺报告']} |

""" + (("**⬜ 待处置（非「可用」的图）**：\n\n" + "\n".join(f"- `{b}`" for b in bad_figs) +
        "\n\n⇒ 每一张要么改，要么写进 `docs/audit/visual-adjudications.md`（实测裁定，须含依据数值）。\n")
       if bad_figs else "**✅ 全部「可用」。**\n") + adj_note + f"""
## 5. 第三道人工闸门 · 透镜 3（陌生读者测试）

**⬜ 待 Lead 执行**（用一个**无项目上下文**的 subagent，只给它这一页 + 8 个机制问题）。

判据：❌ > 20% ⇒ P1；⚠️ > 40% ⇒ P1。

```
透镜 3：✅ ? 题 ｜ ⚠️ ? 题 ｜ ❌ ? 题
```

## 6. 本轮修复引入了什么新错

**⬜ 待 Lead 填。**

## 7. 结论

**⬜ 待 Lead 填**（P0 是否清零 / 三道人工闸门是否都过 / 是否同意提级）。
"""
    out.write_text(body, encoding="utf-8")
    return f"已生成：{out.name}（图 {dist['可用']}/{sum(dist.values())} 可用，闸门未过 {len(bad_gates)} 道）"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("course", nargs="?")
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    targets: list[tuple[pathlib.Path, str]] = []
    for cd in sorted(COURSES.iterdir()):
        if not cd.is_dir() or not (cd / "content").exists():
            continue
        if a.course and not a.all and cd.name != a.course:
            continue
        for idx in sorted((cd / "content").rglob("index.md")):
            slug = str(idx.parent.relative_to(cd / "content")).replace("\\", "/")
            if a.slugs and slug not in a.slugs and slug.split("/")[-1] not in a.slugs:
                continue
            if not a.slugs and not a.all:
                continue
            targets.append((cd, slug))

    if not targets:
        print("没有目标。用法：make_audit_record.py <课程> <slug>…  或  --all")
        return 1
    for cd, slug in targets:
        print(f"  {make(cd, slug, a.force)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
