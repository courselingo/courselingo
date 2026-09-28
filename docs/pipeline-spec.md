# 流水线接口规范 · Pipeline Spec (FROZEN)

> 本文件是**接口契约**。脚本、SKILL、SOP、CI 都按此实现。改动需同步全部消费方。

## 0. 设计约束（为什么是这样）

| 约束 | 来源 | 后果 |
| --- | --- | --- |
| 网络出口不稳定（DNS fake-IP `198.18.0.x`，npm registry 时通时断） | 本机实测 | **零依赖**：只用 Python 3.11+ 标准库（`tomllib` 内置），`git clone` 后直接可跑，不需要 `npm install` / `pip install` |
| 课程授权**尚未核实** | 见 [licensing-research-log.md](./licensing-research-log.md) | 默认产出 `explanation`；`transcript` 模式被**校验脚本硬拦截** |
| 内容是全项目的核心资产 | 架构决策 | 内容用纯 Markdown + TOML，**与渲染器解耦**，将来可整体迁移到 VitePress / MkDocs 而无需改内容 |

## 1. 仓库布局

### 平台主仓库（`courselingo/courselingo`）

```
template/                  ★ 课程仓库模板（见下）
scripts/new_course.py      ★ 由 template/ 生成新课程仓库（在平台根，不在课程仓库内）
skills/                    Agent Skills
docs/                      规范与手册
```

### 课程仓库（由 `scripts/new_course.py` 生成）

```
course.toml               课程元数据 + 授权闸门
glossary.toml             术语表（核心资产）
papers.toml               论文登记表：每篇论文的元数据 + **各自的**授权（见 §10）
content/
  <NN>-<slug>/
    index.md              讲座讲解，+++ TOML front matter
    figures/*.svg         配图
  papers/<key>/           论文页（导读或全文翻译），key 对应 papers.toml
    index.md
    figures/*.svg
scripts/
  new_lecture.py          新建讲座骨架
  validate.py             校验（CI 强制）
  build.py                构建静态站 → site/
.github/workflows/        校验 + 部署（随模板一起复制）
site/                     构建产物（不入库）
```

## 2. `course.toml`

```toml
[course]
id = "mit-6.5840"                 # 必填，唯一
title = "Distributed Systems"     # 必填
title_zh = "分布式系统"            # 必填
institution = "MIT"               # 必填（校验要求）
course_number = "6.5840 / 6.824"  # 可选
homepage = "https://pdos.csail.mit.edu/6.824/"   # 可选
source_language = "en"            # 必填（校验要求）
target_language = "zh"            # 必填（校验要求）

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
source_kind = "notes"             # notes | video | textbook | slides | other
source_url = "https://..."        # 必填（署名与可溯源）
source_title = "Primary-Backup Replication"   # 可选，但强烈建议填
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

1. `course.toml` 可解析且 `[course]` 必填字段齐全；`[license.materials]` 的键必须是合法材料类型、值必须是布尔。
2. **授权闸门**：`output_mode="transcript"` 的讲座必须通过 `license_allows(cfg, source_kind)`
   —— 即 `[license.materials][<该讲座的 source_kind>] == true`；没有 `[license.materials]` 时退回
   `[license].verified == true`。判定顺序见 §2。
3. 讲座 front matter 必填字段齐全；`lecture` 与 `slug` 全课程唯一；`source_url` 非空。
4. `[[term:key]]` 引用的 key 必须存在于 `glossary.toml`。
5. `glossary.toml` 中 `en` / `zh` 非空且 `key` 唯一。
6. `content/` 下既没有讲座也没有论文页 → ERROR。
   新建的课程仓库在第一篇内容写出之前会**故意**停在这里。
7. **原文转载探测**：正文中出现疑似整段照抄英文原文的段落 → ERROR。
   阈值：剥掉 Markdown 语法后 **> 400 字符** 且 **ASCII 占比 ≥ 90%** 且 **空格数 ≥ 40**
   （最后一条是为了不把单个超长 URL 误判成散文）。
   跳过：围栏代码块内部、标题行、表格行；行内 code 与链接会被剥除后再判定。
8. **论文登记表**：`papers.toml` 的每个 `[[paper]]` 必须有 `key` / `title` / `authors`（非空数组）
   / `venue` / `url` 与 `[paper.license]` 段；`key` 唯一且合规；
   `license.verified = true` 时 `terms` / `evidence_url` / `checked_at` 不得为空。
9. **论文页**：必须有 `kind = "paper"` 与 `title` / `paper` / `status` / `output_mode`；
   `paper` 必须在 `papers.toml` 中登记且全课程不重复；`output_mode` 只能是 `guide` 或 `translation`。
10. **论文翻译闸门**：`output_mode = "translation"` 时，必须同时满足
    `papers.toml[key].license.verified == true` **且** `allows_translation == true`，缺一即 ERROR。
11. 讲座 front matter 的 `papers = [...]` 中每个 key 都必须在 `papers.toml` 中登记。

检查项（WARN）：

12. glossary 的 `en` 原词在正文出现但未加 `[[term:]]` 标记。
13. `status = "draft"` 的内容在 `build` 时会标注「草稿」。

## 7. `scripts/build.py` 契约

```
python scripts/build.py  [--root .] [--out site] [--base-url ./]
python scripts/validate.py [--root .] [--quiet]
```

- `--base-url` 默认 `"./"`（本地直接打开 `site/index.html` 就能用）；
  部署到 `https://<org>.github.io/<repo>/` 时传 `/<repo>/`。

- 读取 `course.toml` / `glossary.toml` / `content/**/index.md`
- Markdown 子集渲染（**必须**支持）：ATX 标题、段落、围栏代码块（含语言类名与 HTML 转义）、无序/有序列表、表格、引用块、水平线、链接、图片、行内 `` `code` `` / `**粗体**` / `*斜体*`
- 术语 `[[term:key]]` 解析
- 输出：`site/index.html`（课程首页 + 讲座目录 + 论文列表）、`site/<slug>/index.html`、
  `site/papers/<key>/index.html`、`site/glossary/index.html`、`site/assets/style.css`
- 第二/第三道闸门：遇到未授权的 `transcript` 讲座或 `translation` 论文页时**直接退出 1**，不产出任何站点
- 每页含：侧边栏导航、面包屑、`<meta name="description">`、明暗色适配、页脚署名与「非官方 · 社区项目」声明
- 零第三方依赖；对中文排版友好（`lang="zh-CN"`、合适行高与字距）

## 8. CI 契约（`.github/workflows/`）

| 工作流 | 触发 | 行为 |
| --- | --- | --- |
| `validate.yml` | push / PR | 跑 `validate.py`，有 ERROR 即失败 |
| `deploy.yml` | push to `main` | `validate.py` → `build.py` → 部署 `site/` 到 GitHub Pages |

- 运行环境 `ubuntu-latest` + `actions/setup-python@v7`（3.12），**不需要** npm / pip。
- Pages 通过 `actions/configure-pages@v6` + `actions/upload-pages-artifact@v5` +
  `actions/deploy-pages@v5` 部署，权限 `pages: write` / `id-token: write`。
- `checkout@v7`。版本于 2026-09-28 经 GitHub Releases API / tags 核实为当前最新主版本。
- `deploy.yml` 用三个串联 job（`validate` → `build` → `deploy`）落地闸门：
  `build` 依赖 `validate`、`deploy` 依赖 `build`，于是**校验不通过时部署根本不会发生**。

## 9. Agent Skills 契约

`skills/<name>/SKILL.md`，YAML front matter 两字段：

```markdown
---
name: course-translate
description: <一句话说明能力 + 何时使用（英文，供模型路由）>
---
```

首批 5 个：`course-init` / `course-translate` / `course-explain` / `course-diagram` / `course-validate-publish`。

---

## 10. 论文（Papers）

经典课程往往围绕经典论文展开（MIT 6.824 的 MapReduce、GFS、Raft……）。
论文**必须作为一等公民**处理，因为它们的授权与课程**完全无关**，而且通常更严：
多数论文的版权在出版社（ACM / IEEE / USENIX），**翻译整篇论文 = 复制全部表达的衍生作品**，
风险与翻译逐字稿同级。

### 10.1 `papers.toml` —— 逐篇核实，不用课程级布尔

```toml
[[paper]]
key = "mapreduce"                 # 必填，唯一，小写连字符
title = "MapReduce: Simplified Data Processing on Large Clusters"   # 必填
authors = ["Jeffrey Dean", "Sanjay Ghemawat"]                       # 必填，非空数组
venue = "OSDI 2004"               # 必填
year = 2004                       # 可选
publisher = "USENIX"              # 可选但强烈建议
url = "https://..."               # 必填（原文入口）
pdf_url = ""                      # 可选

[paper.license]
verified = false                  # 是否已核实
terms = ""                        # 例如 "CC BY 4.0"
evidence_url = ""                 # 核实依据（必填于 verified=true 时）
checked_at = ""                   # ISO 日期
allows_translation = false        # ★ 是否允许翻译
allows_commercial = false
share_alike = false
notes = ""
```

**为什么不用课程级的 `verified`**：同一门课里的论文来自不同出版社，授权各不相同。
一门课的「笔记授权」推不出「论文授权」。

### 10.2 论文页 `content/papers/<key>/index.md`

```markdown
+++
kind = "paper"                    # 必填，固定为 paper
paper = "mapreduce"               # 必填，对应 papers.toml 的 key
title = "MapReduce 导读"           # 必填
status = "draft"                  # draft | reviewed | approved
output_mode = "guide"             # guide | translation
+++

正文…
```

注意论文页**没有** `lecture` / `slug` / `source_kind` / `source_url`：
序号与出处由 `papers.toml` 提供，避免同一事实写两处。

### 10.3 两档产出与各自的闸门

| `output_mode` | 含义 | 闸门 |
| --- | --- | --- |
| `guide` | **我们自己写的导读** —— 讲清论文要解决什么问题、怎么解、代价是什么 | **不设闸门**（思想与概念不受著作权保护） |
| `translation` | **全文翻译** —— 复制整篇表达 | 必须 `verified = true` **且** `allows_translation = true` |

**两个条件缺一不可。** 只「核实了」不够 —— 核实的结果可能是「不允许翻译」
（例如出版社持有版权、需走授权流程）。这正是 `allows_translation` 独立存在的原因。

### 10.4 讲座与论文互相引用

讲座 front matter 可选加 `papers = ["mapreduce"]`（数组，必须是 `papers.toml` 中已登记的 key）
→ 校验通过后在页面上做交叉链接。这让「第 1 讲读 MapReduce」这种关系成为结构化数据，
而不是散落在正文里的一句话。

### 10.5 build 输出

论文页输出到 `site/papers/<key>/index.html`（相对根目录两层，故 `base="../../"`），
侧栏出现「论文」分组。首页在讲座列表下方增加「经典论文」列表。

### 10.6 授权核实的方法论要求（血泪教训）

核实论文授权时**必须**：

1. **抓原始 HTML**，不要过滤标签后再搜文本 —— 许可常是 `rel="license"` 属性或图片徽章。
2. **「能免费下载」≠「允许翻译」** —— 作者把 PDF 挂在自己主页上不构成任何授权。
3. **查出版社政策**，不只是论文页 —— ACM 有专门的翻译授权流程。
4. **逐篇记录** `evidence_url` 与 `checked_at`，无法核实的标 `⚠️ 未确认`，**不要推测**。

结论汇总见 [paper-licensing.md](./paper-licensing.md)。
