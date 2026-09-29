#!/usr/bin/env python3
"""批量视觉复核：把每个课程的图喂给 qwen3.8-max，收集描述与找问题。

这是本项目**唯一一道能覆盖「图画得对不对、读者一眼能不能看懂」的检查** ——
房规 linter 只能证明几何、间距、溢出、转义没毛病。
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import vision  # noqa: E402

ROOT = pathlib.Path(r"D:\Vibe_Workspace\courselingo")
COURSES = ROOT / "courses"
OUT = ROOT / "preview" / "visual-review"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "qwen3.8-max"

# 比默认更聚焦「找错」，并要求它给出明确的判定行，便于批量汇总
PROMPT = """你是严格的图表审校员，正在审一门中文计算机课程的手绘 SVG 配图。

请输出**恰好四节**，不要寒暄：

## 版面
结构：几行几列、有哪些箭头与走向。

## 全部文字
把图里每一处文字**照抄**出来（中文原样，不要翻译、不要概括、不要漏）。

## 缺陷
逐条列出你实际看到的问题，每条注明**具体是哪个标签/哪个位置**：
- 文字与线条或方框相碰、文字溢出方框、元素拥挤、对齐错位
- 图里的**数字、顺序、箭头方向、结论**有没有自相矛盾或算错的地方
- 有没有为了排版而丢掉的必要信息
没有就说「未发现」，**不要为了凑数编造**。

### ★ 谈「对齐 / 居中 / 宽度 / 间距」时的硬性要求（务必遵守）

图内坐标系是 SVG 用户坐标，**这张图的 viewBox 是 {viewbox}**。
**每一个坐标数字都必须落在 `0…宽` 与 `0…高` 之间** —— 超出这个范围的数**不可能是图内坐标**。

所以：
- **报任何 px/坐标之前，先说明它是「图内坐标」还是「按我看到的图片像素估的」**；
- **要主张两个元素不对称 / 不居中 / 宽度不等，必须同时给出两者的边界坐标，
  并自己检查一遍这些数是否都在 viewBox 内、以及算出来的差是否真的等于你声称的量**；
- **给不出两个边界坐标时，就不要写具体数字** —— 改写成定性描述
  （例如「标题看起来比图身偏右」），并明确标为**估计**；
- **宁可少报一条，也不要给一个自己算不出来的数。**

## 判定
最后一行只写这三个之一，并给一句理由。**按纯文本写，不要加反引号、星号或任何 Markdown 标记**：
判定：可用
判定：需小修
判定：有错误

### ★★ 判「需小修」的门槛（这是硬要求，务必遵守）

**判「需小修」时，必须在这一行**之前**写出它**违反了下面哪一条**具体规则**，
并给出该规则要求的量与你在图上量到的量。**

**这份图集采用的规则（只有这些是「规则」，其余都是口味）：**
```
R1  块间距（相邻元素之间的空白）≥ 25px
R2  框高 = 字号 × 3（即 font-size × 3 = 上内边距 + 字高 + 下内边距）
R3  框内文字垂直居中：文字基线 y = 框的垂直中心 + 字号 × 0.35
R4  画布边距 20–25px（内容最外缘到画布边的距离）
R5  元素不重叠；文字右缘 + 10px < 右侧邻居的左缘
R6  不允许斜的直线段（连接线必须正交或走曲线）
R7  调色板与字体栈按图集规定
```

**⇒ 所以：**
- **能指出「违反了 R几，规则要求 ≥25px，而这里是 18px」⇒ 可以判「需小修」。**
- **只能说「看起来不均 / 有点挤 / 不够对称 / 节奏不好」而指不出上面任何一条 ⇒
  **不要判「需小修」**，把它写进「缺陷」里作为**观察**即可，判定仍给「可用」。**
- **「不对称」「不居中」「两框不等宽」**：这些**本身不是规则** ——
  只有当它伴随 R4（边距超出 20–25px 区间）或 R2（框高不符）时才算违规。
  **⇒ 若确实没有任何一条规则被违反，就给「可用」。**

**★ 原因（写给复核者看，免得觉得被刁难）**：
本图集里 195 张被判「需小修」的图，经逐条实测，**约三分之二的判词在实测下不成立**
（例：「两框不等宽 707 vs 622」→ 实测两框**都是 344**；
 「标题偏右 40–50px」→ 墨迹中心 379.5 对画布 380.0，差 0.5px）。
**⇒ 所以门槛设在「能指认规则」上：这样每一条判词都可以被独立复算。**
"""


def prompt_for(viewbox: str | None = None) -> str:
    """把 `{viewbox}` 填上再交给模型。

    ★ 为什么必须填（2026-09-29）：
    一次复核里，复核者对同一批图给出了 **4 条几何主张，作者逐条量测后全部不成立**
    （例：「中部两框不等宽 707 vs 622」→ 实测两框**都是 344**；
      「标题偏右 40–50px」→ 渲染后量墨迹中心 379.5 对画布 380.0；
      「右端标签右缘距画布仅 2–3px」→ 该文字 `text-anchor="end" x="738"`，右边距 22px）。
    **⇒ 根因是坐标系**：它报的数常常超出那张图 viewBox 的宽度本身
    （有一张 viewBox 只有 707，而它报 782 / 716）。
    **⇒ 所以：把 viewBox 直接写进提示，并要求「每个数必须落在 0…宽 / 0…高 之间」。**
    这一条同时给了它一个**可自查的边界**，而不是让它自由估数。
    """
    return PROMPT.replace("{viewbox}", viewbox or "（未提供；此时不要报任何具体坐标数字）")


def read_verdict(text: str) -> str:
    """从复核报告里读出判定。

    ★ 必须**先剥 Markdown 标记**再匹配。
    起因（2026-09-28）：prompt 里把判定写成反引号包裹的 `` `判定：可用` ``，
    于是模型常常回成加粗体 `**判定**：可用`。
    而解析是字面子串匹配 `f"判定：{v}" in out` ——
    加粗体的字符序列是 `* * 判 定 * * ： 可 用`，`判定：` 并不连续出现 ⇒ **匹配不上** ⇒ 取到 `"?"`。

    两种后果都坏：
      · `visual_review.py` 自己的汇总会把「可用」记成 `"?"`（**统计被低报**）；
      · `check_reviewed.py` 的 `if v in ("有错误","需小修")` 对 `"?"` 为假 ⇒ **静默放行**。

    所以规范化放在一个函数里，三处共用：**剥掉 `*` `_` `` ` `` 与空白**。
    """
    flat = re.sub(r"[*_`\s]", "", text or "")
    for v in ("有错误", "需小修", "可用"):
        if f"判定：{v}" in flat:
            return v
    return "?"


def main() -> int:
    key = vision.read_key()
    base = vision.read_base_url()
    if not key:
        print("✗ 无密钥")
        return 2

    figs = sorted(COURSES.glob("*/content/**/figures/*.svg"))
    print(f"共 {len(figs)} 张图，模型 {MODEL}\n")

    results = []
    for i, f in enumerate(figs, 1):
        course = f.relative_to(COURSES).parts[0]
        png = ROOT / "preview" / "png" / f"{course}__{f.stem}.png"
        if not png.exists():
            print(f"  [{i}/{len(figs)}] 跳过（未栅格化）{f.name}")
            continue
        ok, out = vision.call(base, key, MODEL, PROMPT, [png], timeout=300)
        rec = {"figure": f"{course}/{f.name}", "ok": ok, "report": out}
        # ★ 版本戳 —— 这条是必需的，不是装饰。
        #   一次复核的结论**只对它所看的那一个版本有效**。
        #   实测：102 份报告里有 47 份**比它描述的 SVG 旧**，
        #   于是「有错误 / 需小修」的汇总被过期结论污染
        #   （旧汇总报「12 有错误」，剔掉过期后只剩 2）。
        #   同一个坑本项目在正文上已经踩过：改完要冻结 SHA256 再送检。
        #   **图也必须一样 —— 没有版本戳的复核结论，会被当成对当前版本成立。**
        import hashlib

        # ★ 行尾归一化后再算 —— 否则同内容在 CRLF 工作区与 LF 检出里得到不同哈希。
        #   实测：mit-6.006 提级时 CI 报「报告核的是旧版」，而报告与文件都没错，
        #   错的是哈希把「表示的差异」当成了「内容的差异」。
        h = hashlib.sha256(
            f.read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest().upper()[:16]
        (OUT / f"{course}__{f.stem}.md").write_text(
            f"# {course}/{f.name}\n\n模型 {MODEL}\n"
            f"复核对象 SHA256(前16)：`{h}`\n"
            f"SVG mtime：{__import__('datetime').datetime.fromtimestamp(f.stat().st_mtime):%Y-%m-%d %H:%M:%S}\n\n{out}\n",
            encoding="utf-8")
        verdict = read_verdict(out) if ok else "?"
        rec["verdict"] = verdict
        results.append(rec)
        print(f"  [{i}/{len(figs)}] {f.stem:<36} {'✓ ' + verdict if ok else '✗ ' + out[:60]}")
        time.sleep(1)

    (OUT / "_summary.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    from collections import Counter
    c = Counter(r["verdict"] for r in results)
    print("\n=== 汇总 ===")
    for k in ("可用", "需小修", "有错误", "?"):
        if c[k]:
            print(f"  {k:<8} {c[k]:>3} 张")
    bad = [r["figure"] for r in results if r["verdict"] in ("有错误", "需小修")]
    if bad:
        print("\n  需要看的：")
        for b in bad:
            print(f"    {b}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
