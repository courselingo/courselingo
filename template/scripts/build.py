#!/usr/bin/env python3
"""CourseLingo 静态站构建器。

零依赖：仅用 Python 3.11+ 标准库。支持 Markdown 子集（见 docs/pipeline-spec.md §7）：
ATX 标题、段落、围栏代码块、有序/无序列表、表格、引用块、水平线、
链接、图片、行内 code / **粗体** / *斜体*，以及 [[term:key]] 术语标记。

用法：
    python scripts/build.py [--root .] [--out site] [--base-url /]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
import shutil
import sys
import tomllib
from pathlib import Path

TERM_RE = re.compile(r"\[\[term:([A-Za-z0-9_.\-]+)\]\]")
FENCE_OPEN_RE = re.compile(r"^\s*(?:```|~~~)\s*([\w+#.-]*)\s*$")
FENCE_ANY_RE = re.compile(r"^\s*(?:```|~~~)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
UL_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

FONT_STACK = (
    '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", '
    '"Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans SC", '
    '"Noto Sans CJK SC", sans-serif'
)


def slugify(en: str) -> str:
    s = en.strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"[^a-z0-9.\-]", "", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def split_front_matter(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "+++":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "+++":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", text


def license_allows(cfg: dict, source_kind: str) -> bool:
    """与 validate.py 同一套授权闸门判定（见 docs/pipeline-spec.md §2）。"""
    lic = cfg.get("license")
    if not isinstance(lic, dict):
        return False
    materials = lic.get("materials")
    if isinstance(materials, dict) and materials:
        return materials.get(source_kind) is True
    return lic.get("verified") is True


# --------------------------------------------------------------------------
# 行内渲染
# --------------------------------------------------------------------------
def render_inline(text: str, terms: dict[str, tuple[str, str]], used: dict[str, int]) -> str:
    out = html.escape(text, quote=False)

    codes: list[str] = []

    def stash(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    out = re.sub(r"`([^`]+)`", stash, out)

    def term_repl(m: re.Match) -> str:
        key = m.group(1).lower()
        entry = terms.get(key)
        if not entry:
            return m.group(0)
        en, zh = entry
        used[key] = used.get(key, 0) + 1
        label = f"{zh}（{en}）" if used[key] == 1 else zh
        title = html.escape(f"{zh} · {en}", quote=True)
        return f'<abbr class="term" title="{title}">{label}</abbr>'

    out = TERM_RE.sub(term_repl, out)

    out = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">',
        out,
    )
    out = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>',
        out,
    )
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", out)

    out = re.sub(
        r"\x00(\d+)\x00",
        lambda m: f"<code>{codes[int(m.group(1))]}</code>",
        out,
    )
    return out


# --------------------------------------------------------------------------
# 块级渲染
# --------------------------------------------------------------------------
def build_list(items: list[tuple[int, bool, str]], terms, used) -> str:
    parts: list[str] = []
    stack: list[tuple[int, str]] = []
    for indent, ordered, text in items:
        tag = "ol" if ordered else "ul"
        while stack and indent < stack[-1][0]:
            parts.append(f"</{stack[-1][1]}>")
            stack.pop()
        if not stack or indent > stack[-1][0]:
            parts.append(f"<{tag}>")
            stack.append((indent, tag))
        elif stack[-1][1] != tag:
            parts.append(f"</{stack[-1][1]}>")
            stack.pop()
            parts.append(f"<{tag}>")
            stack.append((indent, tag))
        parts.append(f"<li>{render_inline(text, terms, used)}</li>")
    while stack:
        parts.append(f"</{stack[-1][1]}>")
        stack.pop()
    return "".join(parts)


def render_markdown(body: str, terms: dict[str, tuple[str, str]]) -> tuple[str, list[str]]:
    # HTML 注释是作者备忘，不渲染
    body = HTML_COMMENT_RE.sub("", body)
    lines = body.splitlines()
    parts: list[str] = []
    used: dict[str, int] = {}
    para: list[str] = []
    headings: list[str] = []

    def flush_para() -> None:
        if para:
            parts.append("<p>" + render_inline(" ".join(para), terms, used) + "</p>")
            para.clear()

    i = 0
    while i < len(lines):
        line = lines[i]

        m = FENCE_OPEN_RE.match(line)
        if m:
            flush_para()
            lang = m.group(1)
            i += 1
            buf: list[str] = []
            while i < len(lines) and not FENCE_ANY_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            code = html.escape("\n".join(buf))
            parts.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        m = HEADING_RE.match(line)
        if m:
            flush_para()
            level = len(m.group(1))
            text = m.group(2)
            anchor = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text).strip("-").lower()
            headings.append(text)
            parts.append(
                f'<h{level} id="{html.escape(anchor, quote=True)}">'
                f"{render_inline(text, terms, used)}</h{level}>"
            )
            i += 1
            continue

        if HR_RE.match(line):
            flush_para()
            parts.append("<hr>")
            i += 1
            continue

        # 表格
        if line.strip().startswith("|") and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            flush_para()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{render_inline(c, terms, used)}</th>" for c in header)
            trs = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c, terms, used)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            parts.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>")
            continue

        # 引用块
        if line.strip().startswith(">"):
            flush_para()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            inner = " ".join(x for x in buf if x)
            parts.append(f"<blockquote><p>{render_inline(inner, terms, used)}</p></blockquote>")
            continue

        # 列表
        if UL_RE.match(line) or OL_RE.match(line):
            flush_para()
            items: list[tuple[int, bool, str]] = []
            while i < len(lines):
                mu = UL_RE.match(lines[i])
                mo = OL_RE.match(lines[i])
                if mu:
                    items.append((len(mu.group(1)), False, mu.group(2)))
                elif mo:
                    items.append((len(mo.group(1)), True, mo.group(2)))
                else:
                    break
                i += 1
            parts.append(build_list(items, terms, used))
            continue

        if not line.strip():
            flush_para()
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush_para()
    return "\n".join(parts), headings


# --------------------------------------------------------------------------
# 页面外壳
# --------------------------------------------------------------------------
def page(
    *,
    site_title: str,
    page_title: str,
    description: str,
    body_html: str,
    nav_html: str,
    base: str,
    banner: str,
    footer_note: str,
) -> str:
    full_title = f"{page_title} · {site_title}" if page_title else site_title
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="{base}index.html">{html.escape(site_title)}</a>
  <span class="badge">非官方 · 社区项目</span>
</header>
{banner}
<div class="layout">
  <nav class="sidebar">{nav_html}</nav>
  <main class="content">
{body_html}
  </main>
</div>
<footer class="footer">
  <p>{footer_note}</p>
  <p class="muted">由 CourseLingo 流水线生成 · 构建于 {_dt.date.today().isoformat()}</p>
</footer>
</body>
</html>
"""


def nav_for(lectures: list[dict], current: str | None, base: str) -> str:
    items = []
    for lec in sorted(lectures, key=lambda x: x["lecture"]):
        cls = ' class="active"' if current == lec["slug"] else ""
        tag = "span" if lec["status"] == "draft" else "a"
        draft = ' <span class="draft">草稿</span>' if lec["status"] == "draft" else ""
        label = f'{lec["lecture"]}. {html.escape(lec["title"])}'
        if tag == "a":
            items.append(f'<li{cls}><a href="{base}{lec["slug"]}/index.html">{label}</a>{draft}</li>')
        else:
            items.append(f'<li{cls}><span>{label}</span>{draft}</li>')
    items.append(f'<li><a href="{base}glossary/index.html">术语表</a></li>')
    return "<h2>课程目录</h2><ul>" + "".join(items) + "</ul>"


CSS = """
:root {
  --bg: #ffffff; --fg: #1f2937; --muted: #6b7280;
  --primary: #2563eb; --accent: #f59e0b;
  --border: #e5e7eb; --code-bg: #f6f8fa; --sidebar-bg: #fafbfc;
  --max: 46rem;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1115; --fg: #e5e7eb; --muted: #9ca3af;
    --border: #262b35; --code-bg: #171a21; --sidebar-bg: #14171d;
    --primary: #60a5fa; --accent: #fbbf24;
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: %FONT%;
  font-size: 16.5px; line-height: 1.85;
  letter-spacing: .01em;
}
.topbar {
  display: flex; align-items: center; gap: .75rem;
  padding: .9rem 1.25rem; border-bottom: 1px solid var(--border);
  position: sticky; top: 0; background: var(--bg); z-index: 10;
}
.brand { font-weight: 700; color: var(--fg); text-decoration: none; letter-spacing: .01em; }
.badge {
  font-size: .72rem; color: var(--muted); border: 1px solid var(--border);
  border-radius: 999px; padding: .1rem .55rem;
}
.layout { display: flex; gap: 2rem; max-width: 76rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }
.sidebar { flex: 0 0 17rem; font-size: .93rem; }
.sidebar h2 { font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin: 0 0 .6rem; }
.sidebar ul { list-style: none; margin: 0; padding: 0; }
.sidebar li { margin: .18rem 0; }
.sidebar a { color: var(--fg); text-decoration: none; display: block; padding: .3rem .5rem; border-radius: .4rem; }
.sidebar a:hover { background: var(--sidebar-bg); color: var(--primary); }
.sidebar li.active a, .sidebar li.active span { color: var(--primary); font-weight: 600; }
.draft { font-size: .7rem; color: var(--accent); border: 1px solid var(--accent); border-radius: 999px; padding: 0 .35rem; margin-left: .3rem; }
.content { flex: 1 1 auto; min-width: 0; max-width: var(--max); }
.content h1 { font-size: 1.85rem; line-height: 1.35; margin: 0 0 .4rem; }
.content h2 { font-size: 1.32rem; margin: 2.4rem 0 .7rem; padding-bottom: .3rem; border-bottom: 1px solid var(--border); }
.content h3 { font-size: 1.1rem; margin: 1.8rem 0 .5rem; }
.content p { margin: .95rem 0; }
.content a { color: var(--primary); }
.content ul, .content ol { padding-left: 1.4rem; }
.content li { margin: .3rem 0; }
abbr.term {
  text-decoration: none; border-bottom: 1px dashed var(--primary);
  cursor: help; color: var(--primary);
}
code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: .9em; background: var(--code-bg); padding: .12em .35em; border-radius: .25rem;
}
pre {
  background: var(--code-bg); border: 1px solid var(--border); border-radius: .6rem;
  padding: 1rem 1.1rem; overflow-x: auto; line-height: 1.6;
}
pre code { background: none; padding: 0; font-size: .87rem; }
blockquote {
  margin: 1.2rem 0; padding: .7rem 1rem; border-left: 3px solid var(--accent);
  background: var(--sidebar-bg); border-radius: 0 .4rem .4rem 0; color: var(--fg);
}
blockquote p { margin: .2rem 0; }
table { border-collapse: collapse; width: 100%; margin: 1.2rem 0; font-size: .95rem; display: block; overflow-x: auto; }
th, td { border: 1px solid var(--border); padding: .5rem .7rem; text-align: left; }
th { background: var(--sidebar-bg); font-weight: 600; }
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
img { max-width: 100%; height: auto; border-radius: .5rem; }
.notice {
  max-width: 76rem; margin: 1rem auto 0; padding: .7rem 1rem; border-radius: .5rem;
  font-size: .9rem; border: 1px solid var(--accent); background: var(--sidebar-bg);
}
.footer { max-width: 76rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; border-top: 1px solid var(--border); font-size: .87rem; color: var(--muted); }
.footer .muted { color: var(--muted); font-size: .82rem; }
.lecture-list { list-style: none; padding: 0; }
.lecture-list li { padding: .7rem 0; border-bottom: 1px solid var(--border); }
.lecture-list .num { color: var(--muted); font-variant-numeric: tabular-nums; margin-right: .5rem; }
@media (max-width: 52rem) {
  .layout { flex-direction: column; gap: 1.5rem; }
  .sidebar { flex: none; }
}
""".replace("%FONT%", FONT_STACK)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="CourseLingo 静态站构建器")
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="site")
    parser.add_argument("--base-url", default="./")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    out_dir = (root / args.out).resolve()
    base = args.base_url if args.base_url.endswith("/") else args.base_url + "/"

    if not (root / "course.toml").exists():
        print(f"错误：{root} 下没有 course.toml", file=sys.stderr)
        return 2

    with (root / "course.toml").open("rb") as fh:
        cfg = tomllib.load(fh)
    course = cfg.get("course", {})
    license_ = cfg.get("license", {})
    verified = license_.get("verified") is True
    site_title = course.get("title_zh") or course.get("title") or "CourseLingo"

    terms: dict[str, tuple[str, str]] = {}
    gl_path = root / "glossary.toml"
    if gl_path.exists():
        with gl_path.open("rb") as fh:
            gl = tomllib.load(fh)
        for t in gl.get("term", []):
            en, zh = str(t.get("en", "")).strip(), str(t.get("zh", "")).strip()
            if en and zh:
                terms[slugify(str(t.get("key") or en))] = (en, zh)

    lectures: list[dict] = []
    for p in sorted((root / "content").glob("*/index.md")):
        fm_text, body = split_front_matter(p.read_text(encoding="utf-8"))
        fm = tomllib.loads(fm_text) if fm_text else {}
        lectures.append({**fm, "_path": p, "_body": body})
    lectures.sort(key=lambda x: x.get("lecture", 0))

    # 发布前的第二道闸门：即便有人跳过 validate.py，build 也不会渲染未授权的逐字稿。
    blocked = [
        lec for lec in lectures
        if lec.get("output_mode") == "transcript"
        and not license_allows(cfg, str(lec.get("source_kind", "")))
    ]
    if blocked:
        print("⛔ 构建中止：以下讲座是 transcript 模式，但对应材料的授权未核实。", file=sys.stderr)
        for lec in blocked:
            print(
                f"   - {lec.get('slug')}  (source_kind={lec.get('source_kind')})",
                file=sys.stderr,
            )
        print("   翻译完整逐字稿属于衍生作品，必须先核实授权。见 docs/content-policy.md", file=sys.stderr)
        return 1

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "assets").mkdir(parents=True, exist_ok=True)
    (out_dir / "assets" / "style.css").write_text(CSS, encoding="utf-8")

    banner = ""
    if not verified:
        banner = (
            '<div class="notice">⚠️ <strong>本课程授权状态：未核实。</strong>'
            "当前仅发布 CourseLingo 原创讲解，不包含课程原始材料。"
            "见 docs/content-policy.md。</div>"
        )
    footer_note = (
        f"{html.escape(site_title)} · 本文为 CourseLingo 原创讲解，非官方材料，"
        "与原课程方无隶属关系。"
    )

    # 首页
    lis = "".join(
        f'<li><span class="num">{lec.get("lecture")}</span>'
        f'<a href="{base}{lec.get("slug")}/index.html">{html.escape(str(lec.get("title","")))}</a>'
        + (' <span class="draft">草稿</span>' if lec.get("status") == "draft" else "")
        + "</li>"
        for lec in lectures
    )
    src = course.get("homepage") or ""
    home_body = f"""<h1>{html.escape(site_title)}</h1>
<p class="muted">{html.escape(str(course.get('title','')))} · {html.escape(str(course.get('institution','')))} {html.escape(str(course.get('course_number','')))}</p>
<h2>讲座</h2>
<ul class="lecture-list">{lis}</ul>
<h2>关于</h2>
<p>本站是 <strong>CourseLingo（译课 AI）</strong> 的产出示例：用中文重新讲解经典 CS 课程的概念，而不是逐句翻译原文。</p>
<p>原始课程：{'<a href="' + html.escape(str(src), quote=True) + '">' + html.escape(str(src)) + '</a>' if src else '（未填写）'}</p>"""
    (out_dir / "index.html").write_text(
        page(
            site_title=site_title, page_title="", description=str(course.get("title", "")),
            body_html=home_body, nav_html=nav_for(lectures, None, base),
            base=base, banner=banner, footer_note=footer_note,
        ),
        encoding="utf-8",
    )

    # 讲座页
    for lec in lectures:
        slug = str(lec.get("slug", ""))
        body_html, _ = render_markdown(lec["_body"], terms)
        head = f'<h1>{html.escape(str(lec.get("title","")))}</h1>'
        meta = (
            f'<p class="muted">第 {lec.get("lecture")} 讲 · 来源：'
            f'<a href="{html.escape(str(lec.get("source_url","")), quote=True)}">'
            f'{html.escape(str(lec.get("source_title", "")) or "原始出处")}</a> · '
            f'授权：{"已核实" if verified else "未核实"}</p>'
        )
        draft = (
            '<div class="notice">📝 本讲为<strong>草稿</strong>，尚未经过人工复核。</div>'
            if lec.get("status") == "draft" else ""
        )
        target = out_dir / slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(
            page(
                site_title=site_title, page_title=str(lec.get("title", "")),
                description=f'{lec.get("title")} — {site_title}',
                body_html=head + meta + draft + body_html,
                nav_html=nav_for(lectures, slug, base),
                base="../", banner=banner, footer_note=footer_note,
            ),
            encoding="utf-8",
        )
        fig_src = lec["_path"].parent / "figures"
        if fig_src.is_dir():
            shutil.copytree(fig_src, target / "figures", dirs_exist_ok=True)

    # 术语表页
    rows = "".join(
        f"<tr><td><code>{html.escape(en)}</code></td><td>{html.escape(zh)}</td></tr>"
        for en, zh in sorted(terms.values())
    )
    gl_body = (
        f"<h1>术语表</h1><p>全课程统一的译法。同一个概念在任何讲座里都用同一个词。</p>"
        f"<p class='muted'>共 {len(terms)} 条。</p>"
        f"<table><thead><tr><th>English</th><th>中文</th></tr></thead><tbody>{rows}</tbody></table>"
    )
    (out_dir / "glossary").mkdir(parents=True, exist_ok=True)
    (out_dir / "glossary" / "index.html").write_text(
        page(
            site_title=site_title, page_title="术语表", description="课程术语表",
            body_html=gl_body, nav_html=nav_for(lectures, None, base),
            base="../", banner=banner, footer_note=footer_note,
        ),
        encoding="utf-8",
    )

    print(f"构建完成：{out_dir}")
    print(f"  课程：{site_title}  |  讲座 {len(lectures)} 篇  |  术语 {len(terms)} 条")
    print(f"  授权：{'已核实' if verified else '未核实（首页已显示提示条）'}")
    print(f"  入口：{out_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
