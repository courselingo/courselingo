#!/usr/bin/env python3
"""从模板生成一个新的课程仓库。

用法：
    python scripts/new_course.py --id mit-6.5840 --out ../courses/mit-6.5840 \
        --title "Distributed Systems" --title-zh "分布式系统" \
        --institution MIT --course-number "6.5840 / 6.824" \
        --homepage "https://pdos.csail.mit.edu/6.824/"

默认会移除模板自带的演示讲座，得到一个干净的课程仓库。
加 --keep-demo 可保留演示内容（用于验证流水线）。
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

PLATFORM_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = PLATFORM_ROOT / "template"

COURSE_TOML = '''# CourseLingo 课程元数据

[course]
id = "{id}"
title = "{title}"
title_zh = "{title_zh}"
institution = "{institution}"
course_number = "{course_number}"
homepage = "{homepage}"
source_language = "en"
target_language = "zh"

# ★ 授权闸门。
# verified = true 之前，validate.py 会硬拦截任何 output_mode = "transcript" 的讲座。
[license]
verified = false
terms = ""
evidence_url = ""
checked_at = ""
allows_commercial = false
allows_derivatives = false
share_alike = false
notes = "尚未核实。核实后请填写 terms / evidence_url / checked_at，并把 verified 改为 true。"

# 按材料类型逐项核实（推荐）。
# 「笔记已授权」不等于「视频也已授权」—— 各类材料的许可经常不同。
# 一旦这里写了值，授权闸门就只认它，不再看上面的 verified。
[license.materials]
notes = false
slides = false
video = false
textbook = false
other = false

[output]
default_mode = "explanation"
'''

PAPERS_TOML = '''# CourseLingo 论文登记表
#
# 为什么单独一张表：**每篇论文的授权都不一样**（USENIX / ACM / IEEE / 技术报告），
# 不能用课程级的一个布尔表示。翻译全文 = 复制整篇表达，风险与翻译逐字稿同级。
#
# ★「网上能免费下载」≠「可以翻译」。作者把 PDF 挂在自己主页上不构成任何授权。
#
# 规则：
#   output_mode = "guide"        -> 我们自己写的导读，任何时候都可以做
#   output_mode = "translation"  -> 全文翻译，必须 verified = true 且 allows_translation = true
#
# 核实方法见 docs/paper-licensing.md。

# [[paper]]
# key = "mapreduce"
# title = "MapReduce: Simplified Data Processing on Large Clusters"
# authors = ["Jeffrey Dean", "Sanjay Ghemawat"]
# venue = "OSDI 2004"
# year = 2004
# publisher = "USENIX"
# url = "https://www.usenix.org/conference/osdi-04/mapreduce-simplified-data-processing-large-clusters"
#
# [paper.license]
# verified = false
# terms = ""
# evidence_url = ""
# checked_at = ""
# allows_translation = false
# allows_commercial = false
# share_alike = false
# notes = ""
'''

GLOSSARY_TOML = '''# CourseLingo 术语表 —— 本项目的核心资产
#
# 规则：key 默认由 en 推导（小写、空格转连字符）。
#   例如 en = "leader election" -> 正文中写 [[term:leader-election]]
# 每新增一条，都要问：这个译法在全课程都成立吗？

[[term]]
en = "example term"
zh = "示例术语"
notes = "删掉这一条，换成课程里真正需要统一的术语"

# [[term]]
# en = "leader election"
# zh = "领导者选举"
# aliases = []
# notes = "在多个节点中选出一个负责协调的节点"
'''


def force_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


def toml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main(argv: list[str] | None = None) -> int:
    force_utf8()
    parser = argparse.ArgumentParser(description="从模板生成新的课程仓库")
    parser.add_argument("--id", required=True, help="课程 id，例如 mit-6.5840")
    parser.add_argument("--out", required=True, help="目标目录")
    parser.add_argument("--title", required=True, help="英文课程名")
    parser.add_argument("--title-zh", required=True, help="中文课程名")
    parser.add_argument("--institution", required=True, help="学校 / 机构（必填，课程出处）")
    parser.add_argument("--course-number", default="", help="课程编号")
    parser.add_argument("--homepage", default="", help="课程主页")
    parser.add_argument("--keep-demo", action="store_true", help="保留模板的演示讲座")
    parser.add_argument("--force", action="store_true", help="目标已存在时覆盖")
    args = parser.parse_args(argv)

    if not TEMPLATE_DIR.is_dir():
        print(f"错误：找不到模板目录 {TEMPLATE_DIR}", file=sys.stderr)
        return 2

    if not re.fullmatch(r"[a-z0-9][a-z0-9.\-]*", args.id):
        print(f"错误：id={args.id!r} 不合规（小写字母、数字、点、连字符）", file=sys.stderr)
        return 2

    out = Path(args.out).resolve()
    if out.exists():
        if not args.force:
            print(f"错误：{out} 已存在（用 --force 覆盖）", file=sys.stderr)
            return 2
        shutil.rmtree(out)

    # 复制模板，跳过构建产物
    shutil.copytree(
        TEMPLATE_DIR, out,
        ignore=shutil.ignore_patterns("site", "__pycache__", "*.pyc"),
    )

    if not args.keep_demo:
        demo = out / "content" / "01-what-is-a-distributed-system"
        if demo.is_dir():
            shutil.rmtree(demo)
        demo_papers = out / "content" / "papers"
        if demo_papers.is_dir():
            shutil.rmtree(demo_papers)
        (out / "papers.toml").write_text(PAPERS_TOML, encoding="utf-8")

    (out / "course.toml").write_text(
        COURSE_TOML.format(
            id=toml_escape(args.id), title=toml_escape(args.title),
            title_zh=toml_escape(args.title_zh), institution=toml_escape(args.institution),
            course_number=toml_escape(args.course_number), homepage=toml_escape(args.homepage),
        ),
        encoding="utf-8",
    )
    (out / "glossary.toml").write_text(GLOSSARY_TOML, encoding="utf-8")

    print(f"课程仓库已生成：{out}")
    print(f"  课程：{args.title_zh}（{args.title}）")
    print(f"  授权：未核实 —— 只能产出 explanation 模式")
    print()
    print("下一步：")
    print("  1. 核实授权，填写 course.toml 的 [license]（见 docs/content-policy.md）")
    print("  2. 扩充 glossary.toml 的术语")
    print(f"  3. cd {out} && python scripts/new_lecture.py --title \"...\" --slug ... --source-url ...")
    print("  4. python scripts/validate.py && python scripts/build.py")
    if not args.keep_demo:
        print()
        print("注意：演示讲座与演示论文已移除，validate.py 现在会报「没有任何内容」——这是预期的。")
        print("      论文页放在 content/papers/<key>/index.md，key 对应 papers.toml 中登记的条目。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
