# 流水线接口规范 · Pipeline Spec (FROZEN)

> 本文件是**接口契约**。脚本、SKILL、SOP、CI 都按此实现。改动需同步全部消费方。

## 0. 设计约束（为什么是这样）

| 约束 | 来源 | 后果 |
| --- | --- | --- |
| 网络出口不稳定（DNS fake-IP `198.18.0.x`，npm registry 时通时断） | 本机实测 | **零依赖**：只用 Python 3.11+ 标准库（`tomllib` 内置），`git clone` 后直接可跑，不需要 `npm install` / `pip install` |
| 课程授权**尚未核实** | 见 [licensing-research-log.md](./licensing-research-log.md) | 默认产出 `explanation`；`transcript` 模式被**校验脚本硬拦截** |
| 内容是全项目的核心资产 | 架构决策 | 内容用纯 Markdown + TOML，**与渲染器解耦**，将来可整体迁移到 VitePress / MkDocs 而无需改内容 |

## 1. 课程仓库结构（由 `scripts/new_course.py` 生成）

```
course.toml               课程元数据 + 授权闸门
glossary.toml             术语表（核心资产）
content/
  <NN>-<slug>/
    index.md              讲座讲解，+++ TOML front matter
    figures/*.svg         配图
scripts/
  new_lecture.py          新建讲座骨架
  validate.py             校验（CI 强制）
  build.py                构建静态站 → site/
site/                     构建产物（不入库）
```

## 2. `course.toml`

```toml
[course]
id = "mit-6.5840"                 # 必填，唯一
title = "Distributed Systems"     # 必填
title_zh = "分布式系统"            # 必填
institution = "MIT"
course_number = "6.5840 / 6.824"
homepage = "https://pdos.csail.mit.edu/6.824/"
source_language = "en"
target_language = "zh"

[license]
verified = false                  # ★ 授权闸门。false 时禁止 transcript 模式
terms = ""                        # 例如 "CC BY-NC-SA 4.0"
evidence_url = ""
checked_at = ""                   # ISO 日期
allows_commercial = false
allows_derivatives = false
share_alike = false
notes = ""

# 可选但推荐：按材料类型逐项核实。
# 「笔记已授权」不等于「视频也已授权」—— 各类材料的许可经常不同。
# 一旦存在 [license.materials]，授权闸门就只认它，不再看上面的 verified。
[license.materials]
notes = false                     # 讲座笔记 / 幻灯片
video = false                     # 讲座视频（常叠加平台条款）
textbook = false                  # 教材
other = false

[output]
default_mode = "explanation"      # explanation | transcript
```

**授权闸门判定顺序**（`validate.py` 的 `license_allows()`）：

1. 若存在 `[license.materials]` → 只看 `materials[<该讲座的 source_kind>]` 是否为 `true`；
2. 否则退回 `[license].verified`。

为什么需要逐项核实：一门课的笔记可能开放，视频却另有平台条款。用一个布尔表示整门课的授权，
会把「笔记已核实」误当成「视频也已核实」—— 而误解授权正是本项目最大的风险。

注意 `assignments`（作业答案）**不在**可选类型内：作业答案翻译是**永久排除项**，
不是「核实了就能开」的开关。见 [content-policy.md](./content-policy.md)。

## 3. `glossary.toml`

```toml
[[term]]
en = "replication"                # 必填
zh = "副本"                        # 必填
key = "replication"               # 可选；默认由 en 推导
aliases = ["replica"]             # 可选
notes = "此处指数据副本机制"        # 可选
```

**key 推导规则（重要）**：`key` 默认由 `en` 生成 —— 转小写、空格与下划线转连字符、去掉其他非法字符。
正文标记必须用 **key**，不是 `en` 原文：

| en | key（正文中这样写） |
| --- | --- |
| `replication` | `[[term:replication]]` |
| `distributed system` | `[[term:distributed-system]]` |
| `leader election` | `[[term:leader-election]]` |

同一课程内 key 必须唯一（重复即 ERROR）。需要与 `en` 不同的 key 时，显式写 `key = "..."`。

## 4. 讲座 `content/<NN>-<slug>/index.md`

TOML front matter，`+++` 分隔：

```markdown
+++
title = "主从复制"
lecture = 3                       # 必填，整数，全课程唯一
slug = "primary-backup-replication"  # 必填，唯一
status = "draft"                  # draft | reviewed | approved
source_kind = "notes"             # notes | video | textbook | other
source_url = "https://..."        # 必填（署名与可溯源）
source_title = "Primary-Backup Replication"
output_mode = "explanation"       # explanation | transcript
+++

正文…
```

## 5. 术语标记语法（渲染 + 校验的关键）

正文中用 `[[term:replication]]` 引用术语表条目（key 的推导见 §3）：

- **渲染**：输出 `<abbr class="term" title="副本 · replication">…</abbr>`，首现显示「中文（English）」，后续只显示中文。
- **校验**：
  - 引用了 glossary 中不存在的 key → **ERROR**
  - 正文中出现了 glossary 的 `en` 原词却没打标记 → **WARN**（提示可能术语漂移）
- **不算引用的情况**（否则会把「写法示例」误判为真实引用）：
  - 写在行内 code 里的 `` `[[term:key]]` ``
  - 写在 HTML 注释 `<!-- -->` 里的（注释在渲染时会被整段丢弃）

## 6. `scripts/validate.py` 退出码约定

| 退出码 | 含义 |
| --- | --- |
| `0` | 通过（可能有 WARN） |
| `1` | 校验失败（ERROR） |
| `2` | 用法/IO 错误 |

检查项（ERROR）：

1. `course.toml` 可解析且 `[course]` 必填字段齐全。
2. **授权闸门**：存在任一 `output_mode="transcript"` 的讲座，而 `license.verified != true` → ERROR。
3. 讲座 front matter 必填字段齐全；`lecture` 与 `slug` 全课程唯一；`source_url` 非空。
4. `[[term:key]]` 引用的 key 必须存在于 `glossary.toml`。
5. `glossary.toml` 中 `en` / `zh` 非空且 `en` 唯一。
6. **原文转载探测**：正文中出现「几乎全为 ASCII 且长度 > 400 字符」的连续段落 → ERROR（疑似整段照抄原文，违反内容策略）。

检查项（WARN）：

7. glossary 的 `en` 原词在正文出现但未加 `[[term:]]` 标记。
8. `status = "draft"` 的讲座在 `build` 时会标注「草稿」。

## 7. `scripts/build.py` 契约

```
python scripts/build.py [--out site] [--base-url /]
```

- 读取 `course.toml` / `glossary.toml` / `content/**/index.md`
- Markdown 子集渲染（**必须**支持）：ATX 标题、段落、围栏代码块（含语言类名与 HTML 转义）、无序/有序列表、表格、引用块、水平线、链接、图片、行内 `` `code` `` / `**粗体**` / `*斜体*`
- 术语 `[[term:key]]` 解析
- 输出：`site/index.html`（课程首页 + 讲座目录）、`site/<slug>/index.html`、`site/glossary/index.html`、`site/assets/style.css`
- 每页含：侧边栏导航、面包屑、`<meta name="description">`、明暗色适配、页脚署名与「非官方 · 社区项目」声明
- 零第三方依赖；对中文排版友好（`lang="zh-CN"`、合适行高与字距）

## 8. CI 契约（`.github/workflows/`）

| 工作流 | 触发 | 行为 |
| --- | --- | --- |
| `validate.yml` | push / PR | 跑 `validate.py`，有 ERROR 即失败 |
| `deploy.yml` | push to `main` | `validate.py` → `build.py` → 部署 `site/` 到 GitHub Pages |

- 运行环境 `ubuntu-latest` + `actions/setup-python@v5`（3.12），**不需要** npm。
- Pages 通过 `actions/configure-pages` + `actions/upload-pages-artifact` + `actions/deploy-pages` 部署，权限 `pages: write` / `id-token: write`。

## 9. Agent Skills 契约

`skills/<name>/SKILL.md`，YAML front matter 两字段：

```markdown
---
name: course-translate
description: <一句话说明能力 + 何时使用（英文，供模型路由）>
---
```

首批 5 个：`course-init` / `course-translate` / `course-explain` / `course-diagram` / `course-validate-publish`。
