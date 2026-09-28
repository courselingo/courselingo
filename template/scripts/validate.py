#!/usr/bin/env python3
"""CourseLingo 课程内容校验器。

零依赖：仅用 Python 3.11+ 标准库（tomllib）。退出码约定见 docs/pipeline-spec.md：
    0 = 通过（可能含 WARN）
    1 = 校验失败（存在 ERROR）
    2 = 用法 / IO 错误
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

TERM_RE = re.compile(r"\[\[term:([A-Za-z0-9_.\-]+)\]\]")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
TABLE_RE = re.compile(r"^\s*\|")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]*)\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

REQUIRED_COURSE = ["id", "title", "title_zh", "institution", "source_language", "target_language"]
REQUIRED_LICENSE = [
    "verified", "terms", "evidence_url", "checked_at",
    "allows_commercial", "allows_derivatives", "share_alike",
]
REQUIRED_LECTURE = [
    "title", "lecture", "slug", "status", "source_kind", "source_url", "output_mode",
]
VALID_STATUS = {"draft", "reviewed", "approved"}
VALID_MODES = {"explanation", "transcript"}
VALID_SOURCE_KINDS = {"notes", "video", "textbook", "slides", "other"}

# 疑似整段转载原文的判定阈值
VERBATIM_MIN_CHARS = 400
VERBATIM_ASCII_RATIO = 0.90
VERBATIM_MIN_SPACES = 40


def slugify(en: str) -> str:
    """把英文术语转成标记 key：'distributed system' -> 'distributed-system'。"""
    s = en.strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"[^a-z0-9.\-]", "", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def force_utf8() -> None:
    """Windows 控制台默认 GBK，输出中文与 ✅ 会崩。统一改成 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str]] = []

    def error(self, where: object, msg: str) -> None:
        self.items.append(("ERROR", str(where), msg))

    def warn(self, where: object, msg: str) -> None:
        self.items.append(("WARN", str(where), msg))

    @property
    def errors(self) -> list[tuple[str, str, str]]:
        return [i for i in self.items if i[0] == "ERROR"]

    @property
    def warns(self) -> list[tuple[str, str, str]]:
        return [i for i in self.items if i[0] == "WARN"]


def load_toml(path: Path, rep: Report) -> dict | None:
    if not path.exists():
        rep.error(path.name, "文件不存在")
        return None
    try:
        with path.open("rb") as fh:
            return tomllib.load(fh)
    except tomllib.TOMLDecodeError as exc:
        rep.error(path.name, f"TOML 解析失败：{exc}")
        return None
    except OSError as exc:
        rep.error(path.name, f"读取失败：{exc}")
        return None


def split_front_matter(text: str) -> tuple[str | None, str]:
    """按 +++ 分隔 TOML front matter 与正文。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "+++":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "+++":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text


def iter_paragraphs(body: str):
    """产出正文中的段落文本，跳过代码块 / 标题 / 表格行。"""
    in_fence = False
    buf: list[str] = []
    for raw in body.splitlines():
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            if buf:
                yield "\n".join(buf)
                buf = []
            continue
        if in_fence:
            continue
        if not raw.strip() or HEADING_RE.match(raw) or TABLE_RE.match(raw):
            if buf:
                yield "\n".join(buf)
                buf = []
            continue
        buf.append(raw)
    if buf:
        yield "\n".join(buf)


def strip_html_comments(text: str) -> str:
    """去掉 <!-- --> 注释：那是作者备忘，不是正文，也不该触发术语校验。"""
    return HTML_COMMENT_RE.sub("", text)


def license_allows(cfg: dict, source_kind: str) -> bool:
    """授权闸门判定。

    优先看 [license.materials] 是否按材料类型逐项核实 —— 因为「笔记已授权」不等于
    「视频也已授权」。没有该段时退回 [license].verified 这个总开关。
    """
    lic = cfg.get("license")
    if not isinstance(lic, dict):
        return False
    materials = lic.get("materials")
    if isinstance(materials, dict) and materials:
        return materials.get(source_kind) is True
    return lic.get("verified") is True


def ascii_ratio(s: str) -> float:
    if not s:
        return 0.0
    return sum(1 for c in s if ord(c) < 128) / len(s)


def verbatim_suspect(paragraph: str) -> str | None:
    """返回可疑文本；不像整段英文原文则返回 None。"""
    text = TERM_RE.sub("", paragraph)
    text = INLINE_CODE_RE.sub("", text)
    text = LINK_RE.sub(r"\1", text)
    text = re.sub(r"[*_>#]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= VERBATIM_MIN_CHARS:
        return None
    if ascii_ratio(text) < VERBATIM_ASCII_RATIO:
        return None
    # 单个超长 URL / 无空格串不算「散文」
    if text.count(" ") < VERBATIM_MIN_SPACES:
        return None
    return text


def check_course(cfg: dict, rep: Report) -> None:
    course = cfg.get("course")
    if not isinstance(course, dict):
        rep.error("course.toml", "缺少 [course] 段")
        return
    for key in REQUIRED_COURSE:
        if not str(course.get(key, "")).strip():
            rep.error("course.toml", f"[course].{key} 为必填且不能为空")

    license_ = cfg.get("license")
    if not isinstance(license_, dict):
        rep.error(
            "course.toml",
            "缺少 [license] 段（授权闸门）—— 授权未核实前，本课程只能产出 explanation 模式",
        )
        return
    for key in REQUIRED_LICENSE:
        if key not in license_:
            rep.error("course.toml", f"[license].{key} 为必填")
    if license_.get("verified") is True:
        if not str(license_.get("terms", "")).strip():
            rep.error("course.toml", "license.verified = true 但 terms 为空（必须写明许可条款）")
        if not str(license_.get("evidence_url", "")).strip():
            rep.error("course.toml", "license.verified = true 但 evidence_url 为空（必须可溯源）")
        if not str(license_.get("checked_at", "")).strip():
            rep.error("course.toml", "license.verified = true 但 checked_at 为空（须记录核实日期）")

    output = cfg.get("output")
    if not isinstance(output, dict) or output.get("default_mode") not in VALID_MODES:
        rep.error("course.toml", f"[output].default_mode 必须是 {sorted(VALID_MODES)} 之一")

    materials = license_.get("materials")
    if materials is not None:
        if not isinstance(materials, dict):
            rep.error("course.toml", "[license.materials] 必须是表（键为材料类型）")
        else:
            for k, v in materials.items():
                if k not in VALID_SOURCE_KINDS:
                    rep.error(
                        "course.toml",
                        f"[license.materials].{k} 不是合法材料类型（可选：{sorted(VALID_SOURCE_KINDS)}）",
                    )
                if not isinstance(v, bool):
                    rep.error("course.toml", f"[license.materials].{k} 必须是布尔值")


def check_glossary(gl: dict, rep: Report) -> dict[str, tuple[str, str]]:
    """校验术语表，返回 {key: (en, zh)}。"""
    terms = gl.get("term")
    if not isinstance(terms, list) or not terms:
        rep.error("glossary.toml", "至少需要一个 [[term]] 条目")
        return {}
    index: dict[str, tuple[str, str]] = {}
    for i, term in enumerate(terms, 1):
        if not isinstance(term, dict):
            rep.error("glossary.toml", f"第 {i} 个 [[term]] 不是表")
            continue
        en = str(term.get("en", "")).strip()
        zh = str(term.get("zh", "")).strip()
        if not en:
            rep.error("glossary.toml", f"第 {i} 个 [[term]] 缺少 en")
        if not zh:
            rep.error("glossary.toml", f"第 {i} 个 [[term]]（en={en!r}）缺少 zh")
        if not en or not zh:
            continue
        key = slugify(str(term.get("key") or en))
        if not key:
            rep.error("glossary.toml", f"术语 en={en!r} 无法生成合法 key")
            continue
        if key in index:
            rep.error(
                "glossary.toml",
                f"重复术语 key={key!r}（en={en!r} 与已有 {index[key][0]!r} 冲突）",
            )
            continue
        index[key] = (en, zh)
    return index


def check_lecture(
    path: Path,
    rel: str,
    rep: Report,
    glossary_index: dict[str, tuple[str, str]],
    cfg: dict,
    seen_lectures: dict[int, str],
    seen_slugs: dict[str, str],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        rep.error(rel, f"读取失败：{exc}")
        return

    fm_text, body = split_front_matter(text)
    if fm_text is None:
        rep.error(rel, "缺少 +++ TOML front matter")
        return
    body = strip_html_comments(body)
    try:
        fm = tomllib.loads(fm_text)
    except tomllib.TOMLDecodeError as exc:
        rep.error(rel, f"front matter TOML 解析失败：{exc}")
        return

    for key in REQUIRED_LECTURE:
        if key not in fm:
            rep.error(rel, f"front matter 缺少必填字段 {key}")

    lecture_no = fm.get("lecture")
    if not isinstance(lecture_no, int):
        rep.error(rel, "lecture 必须是整数")
    elif lecture_no in seen_lectures:
        rep.error(rel, f"lecture={lecture_no} 与 {seen_lectures[lecture_no]} 重复")
    else:
        seen_lectures[lecture_no] = rel

    slug = str(fm.get("slug", "")).strip()
    if slug:
        if slug in seen_slugs:
            rep.error(rel, f"slug={slug!r} 与 {seen_slugs[slug]} 重复")
        else:
            seen_slugs[slug] = rel
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            rep.error(rel, f"slug={slug!r} 不合规（只允许小写字母、数字与连字符）")

    status = fm.get("status")
    if status not in VALID_STATUS:
        rep.error(rel, f"status={status!r} 必须是 {sorted(VALID_STATUS)} 之一")

    kind = fm.get("source_kind")
    if kind not in VALID_SOURCE_KINDS:
        rep.error(rel, f"source_kind={kind!r} 必须是 {sorted(VALID_SOURCE_KINDS)} 之一")

    if not str(fm.get("source_url", "")).strip():
        rep.error(rel, "source_url 不能为空（署名与可溯源要求）")

    mode = fm.get("output_mode")
    if mode not in VALID_MODES:
        rep.error(rel, f"output_mode={mode!r} 必须是 {sorted(VALID_MODES)} 之一")
    elif mode == "transcript" and not license_allows(cfg, str(kind)):
        rep.error(
            rel,
            f'⛔ 授权闸门：output_mode="transcript"，但 course.toml 未核实 {kind!r} 这类材料的授权'
            "（[license.materials] 逐项核实，或 [license].verified 总开关）。"
            "翻译完整逐字稿属于衍生作品，必须先核实该类材料的授权。见 docs/content-policy.md",
        )

    # 术语标记引用（行内 code 里的 [[term:key]] 是写法示例，不算引用）
    used: set[str] = set()
    for m in TERM_RE.finditer(INLINE_CODE_RE.sub("", body)):
        key = m.group(1).lower()
        if key not in glossary_index:
            rep.error(rel, f"[[term:{key}]] 未在 glossary.toml 中定义")
        used.add(key)

    # 原文转载探测 + 术语漂移
    for para in iter_paragraphs(body):
        suspect = verbatim_suspect(para)
        if suspect:
            rep.error(
                rel,
                "疑似整段转载英文原文（违反内容策略）："
                f"{suspect[:60]}…（{len(suspect)} 字符，几乎全为 ASCII）",
            )
        low = para.lower()
        for key, (en, _zh) in glossary_index.items():
            if key in used:
                continue
            if re.search(rf"(?<![A-Za-z0-9]){re.escape(en.lower())}(?![A-Za-z0-9])", low):
                rep.warn(
                    rel,
                    f"术语 {en!r} 在正文出现但未加 [[term:{key}]] 标记（可能术语漂移）",
                )


def main(argv: list[str] | None = None) -> int:
    force_utf8()
    parser = argparse.ArgumentParser(description="CourseLingo 课程内容校验器")
    parser.add_argument("--root", default=".", help="课程仓库根目录（默认当前目录）")
    parser.add_argument("--quiet", action="store_true", help="只输出问题与结论")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"错误：根目录不存在 {root}", file=sys.stderr)
        return 2

    rep = Report()
    cfg = load_toml(root / "course.toml", rep)
    gl = load_toml(root / "glossary.toml", rep)

    license_verified = False
    if cfg:
        check_course(cfg, rep)
        license_ = cfg.get("license") or {}
        license_verified = license_.get("verified") is True

    glossary_index: dict[str, tuple[str, str]] = {}
    if gl:
        glossary_index = check_glossary(gl, rep)

    content_dir = root / "content"
    lectures: list[Path] = []
    if not content_dir.is_dir():
        rep.error("content/", "目录不存在")
    else:
        lectures = sorted(content_dir.glob("*/index.md"))
        if not lectures:
            rep.error("content/", "没有任何讲座（content/<slug>/index.md）")
        seen_lectures: dict[int, str] = {}
        seen_slugs: dict[str, str] = {}
        for p in lectures:
            check_lecture(
                p, str(p.relative_to(root)).replace("\\", "/"),
                rep, glossary_index, cfg, seen_lectures, seen_slugs,
            )

    if not args.quiet:
        print(f"课程仓库：{root}")
        print(f"讲座数量：{len(lectures)}   术语条目：{len(glossary_index)}")
        print(f"授权状态：{'已核实' if license_verified else '未核实（仅允许 explanation 模式）'}")
        print("-" * 68)

    for level, where, msg in rep.items:
        icon = "❌" if level == "ERROR" else "⚠️ "
        print(f"{icon} [{where}] {msg}")

    print("-" * 68)
    print(f"结果：{len(rep.errors)} 个错误，{len(rep.warns)} 个警告")

    if rep.errors:
        print("校验失败。授权与术语问题请勿绕过 —— 见 docs/content-policy.md")
        return 1
    print("校验通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
