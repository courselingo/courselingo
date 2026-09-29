#!/usr/bin/env python3
"""把课程仓库里的 SVG 栅格化成 PNG，供视觉复核。

`read_image` 与 vision API 都只吃位图，SVG 必须先渲染。
用 Chrome headless，2 倍缩放让中文标签看得清（房规要求 12px 正文，
2× 后在屏幕上约 24px，足够判读）。

用法：python rasterize.py [课程根目录...]     默认栅格化 courses/ 下全部
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "preview" / "png"
SCALE = 2


def raster(svg: pathlib.Path) -> pathlib.Path | None:
    t = svg.read_text(encoding="utf-8")
    m = re.search(r'viewBox="([\d.\s-]+)"', t)
    if not m:
        return None
    p = m.group(1).split()
    w, h = float(p[2]), float(p[3])
    # ★ 输出名必须带课程前缀：cs168 与 mit-6.5840 都有 intro-1..intro-9，
    #   只用 stem 会互相覆盖，视觉复核会把**别的课程的图**当成这一张来判。
    #
    # ★★ 课程名必须按「courses/ 之后的那一段」取，不能数 parent 层级 ★★
    #   第一版写了 svg.parent.parent.parent.parent.name，对
    #   courses/<c>/content/03-gfs/figures/x.svg 正好得到 <c>；
    #   但对 courses/<c>/content/papers/raft/figures/x.svg 深一层，
    #   得到的是 "content" —— 22 张论文配图被命名成 content__*.png，
    #   复核脚本按 <c>__*.png 去找，于是**静默跳过**它们。
    #   数量对不上（102 张图只有 80 张被复核）时才发现。
    parts = svg.resolve().parts
    try:
        course = parts[parts.index("courses") + 1]
    except (ValueError, IndexError):
        course = svg.parent.parent.parent.parent.name
    dst = OUT / f"{course}__{svg.stem}.png"
    html = OUT / f"_{course}__{svg.stem}.html"
    html.write_text(
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;background:#fff}"
        f"svg{{width:{w*SCALE}px;height:{h*SCALE}px;display:block}}</style>" + t,
        encoding="utf-8",
    )
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--screenshot={dst}", f"--window-size={int(w*SCALE)},{int(h*SCALE)}",
         html.as_uri()],
        capture_output=True, timeout=120,
    )
    html.unlink(missing_ok=True)
    return dst if dst.exists() and dst.stat().st_size > 500 else None


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    roots = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((ROOT / "courses").iterdir())
    figs: list[pathlib.Path] = []
    for r in roots:
        if r.is_dir():
            figs += sorted(r.glob("content/**/figures/*.svg"))
    print(f"待栅格化 {len(figs)} 张 -> {OUT}\n")
    ok = 0
    for s in figs:
        try:
            if raster(s):
                ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"  ❌ {s.name}: {type(e).__name__}: {e}")
    print(f"成功 {ok}/{len(figs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
