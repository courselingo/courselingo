---
name: course-translate
description: Produce one CourseLingo lecture's Chinese explanation end to end — read source material at runtime, respect the license gate, write in the project voice, apply [[term:key]] glossary markers, and fill the frozen TOML front matter. Use when writing, drafting, or revising a single lecture's index.md under content/.
---

# course-translate · 单讲产出（术语约束下的写作）

**一篇讲座 = 一个 `content/<NN>-<slug>/index.md`。**

## ⚠️ 先纠正一个词

这个 skill 名字里有 "translate"，但**产出的是原创中文讲解，不是译文**。

| | 是什么 |
| --- | --- |
| ✅ 我们要的 | 讲同一批**概念**、我们**自己写**的中文讲解、推导、代码注释 |
| ⛔ 不要的 | 逐句对照翻译、完整讲座逐字稿翻译、视频字幕翻译 |
| ⛔ 永久排除 | 官方作业 / Lab 答案的翻译 |

理由：**思想与概念不受著作权保护，表达才受保护。** 翻译完整逐字稿属于衍生作品，复制了原作的全部表达，合法性完全取决于许可条款 —— 而绝大多数课程尚未核实。所以默认产出形态是「讲解」而非「翻译」。

**深度参照**（概念前置 / 推导 / 代码注释 / 配图）见 `course-explain` skill。

---

## 前置阅读

| 文件 | 取什么 |
| --- | --- |
| `glossary.toml` | **冻结**术语的 `en` → `zh` 映射，写正文时逐条遵守 |
| `docs/pipeline-spec.md` §4/§5 | front matter 8 字段、`[[term:key]]` 语法 |
| `docs/content-policy.md` | 署名规范、禁止转载的内容类型 |
| `docs/brand.md` | 语气与用词规范 |
| `.github/CONTRIBUTING.md` §2 | 讲解质量标准四条 |
| `docs/SOP.md` §5/§9.2/§10 | 生产清单、写作提示词、质量基线 |

---

## 步骤 1 · 确认闸门状态（先做，不要跳）

从 `course.toml` 读 `[license].verified`：

| `verified` | 本讲允许的 `output_mode` |
| --- | --- |
| `false` | **只有 `"explanation"`** |
| `true` | `"explanation"` 或 `"transcript"`，且仅限**已核实授权的那种材料**（`source_kind` 要对得上） |

即便 `verified = true`：

- 视频字幕翻译**仍默认关闭**（平台条款叠加）
- 作业答案翻译**永久排除**

> `validate.py` 会在 `transcript` + `verified != true` 时 **exit 1**。这是报警器，不是许可 ——
> **不要为了绕过它去改 `verified`。** 改 `verified` 需要步骤见 `course-init` 的双人闸门。

## 步骤 2 · 确认讲座身份（先分配，再动手）

```bash
python scripts/new_lecture.py     # 生成骨架（不要手搓 front matter）
```

**并行写多讲之前，由一人先分配编号表**，否则 `lecture` / `slug` 必然撞车（spec 要求两者全课程唯一）。

## 步骤 3 · 运行时读源材料（绝不入库）

- 源材料（官方页面 / 笔记 / 大纲）**只在运行时读取**。
- **不要把英文原文、幻灯片、图片、视频、题面写进仓库。** 一个字都不行。
- 不要「先粘进草稿再改」——长英文段落会触发 `validate.py` 的转载探测（ERROR 6），而且它本来就该被拦。

## 步骤 4 · 填 front matter（spec §4，8 字段，不加字段）

```markdown
+++
title = "主从复制"
lecture = 3
slug = "primary-backup-replication"
status = "draft"
source_kind = "notes"
source_url = "https://pdos.csail.mit.edu/6.824/notes/l03.txt"
source_title = "Primary-Backup Replication"
output_mode = "explanation"
+++
```

| 字段 | 规则 |
| --- | --- |
| `title` | 讲座**中文**标题 |
| `lecture` | 整数，**全课程唯一** |
| `slug` | 字符串，**全课程唯一**；与目录名 `<NN>-<slug>` 的 slug 一致 |
| `status` | 新写的**永远是 `"draft"`** |
| `source_kind` | `notes` / `video` / `textbook` / `other`，如实填（当前实现还收 `slides`，spec 未定义，见 `docs/SOP.md` §14-11） |
| `source_url` | **必填非空**，官方地址（署名 + 可溯源） |
| `source_title` | 原标题 |
| `output_mode` | 与步骤 1 的结论一致 |

多源讲座（笔记 + 视频 + 教材）默认只能填一个来源：填**主讲来源**，其余在正文「溯源」小节列出（spec 无多源字段，见 `docs/SOP.md` §14-7）。

## 步骤 5 · 按术语表写正文

### 术语纪律（最关键）

1. 每条术语**首次出现**用 `[[term:<key>]]` 标记：
   ```markdown
   主从复制（primary-backup replication）的核心是 [[term:replication]] …
   ```
   渲染规则（spec §5）：首现显示「中文（English）」，后续只显示中文。
2. **key 怎么算**：key 由 glossary 的 `en` 派生 —— **小写化、空格与下划线转连字符、去掉其他非 `[a-z0-9.-]` 字符**。
   `leader election` → `[[term:leader-election]]`；`primary-backup replication` → `[[term:primary-backup-replication]]`。
   **写成 `[[term:leader election]]`（带空格）会 ERROR：key 不存在。**
   （spec §5 只给了单词示例，此派生规则见 `docs/SOP.md` §14-10。）
3. **不要用中文替代词绕过标记**。写了「副本」却没打 `[[term:replication]]` → `validate.py` WARN 7（术语漂移前兆）。
4. **不要直接写英文原词**代替标记。
5. **同一个概念全篇同一个中文词** —— 以 `glossary.toml` 的 `zh` 为唯一来源。
6. 需要新术语 → **回 `course-init` 走评审加词**，不要就地造译名。
7. **不要在正文中改术语表。**

### 授权纪律

- 不逐句改写原文（换同义词不算「自己写」）。
- 不复制源材料的句子、幻灯片、图片、题面。
- 引用只给 **URL + 位置**（讲座号 / 时间戳 / 页码），**不给文本**。
- 正文不保留整段英文原句。
- 不得出现成段的英文散文（「几乎全为 ASCII 且长度 > 400 字符」的段落 → ERROR 6）。围栏代码块不受这条限制，但也别整段照抄。

### 代码纪律

- 每个代码块**关键行必须有中文注释**，解释「为什么这么写」，而不是整块照抄。
- 代码块**保持短小**（单块 ≤ 400 字符），超长就拆分并用正文文字承接。
  （当前实现的转载探测会跳过围栏代码块，所以这条是**可读性原则**，不是校验要求。详见 `docs/SOP.md` §14-6。）

### 语气纪律（brand.md）

- 像助教，不像营销号：直接讲清楚，不铺垫、不煽情。
- 承认复杂：难概念拆开讲，不说「其实很简单」。
- 不吹牛：进度、局限、授权边界如实写。
- 面向读者写「**你**」，不用「用户」「学员」。
- 用「讲解」不用「解析」；用「课程」不用「网课」。
- **禁用词**：全网最全 / 颠覆 / 封神。

### 正文结构（最少包含）

1. 读者画像与前置知识（1 段）
2. 概念前置：本讲依赖但原文默认已知的背景
3. 主线推导：不跳步，中间过程写出来
4. 代码 / 伪代码走查：逐行中文注释
5. 小结：3–7 条要点 + 常见误解
6. 溯源：对应原文位置（讲座号 / 时间戳 / 页码 / 章节名）

需要画图 → 交给 `course-diagram` skill；图放 `content/<NN>-<slug>/figures/*.svg`，正文 `![中文说明](figures/xxx.svg)` 引用（alt 文本必写）。

## 步骤 6 · 写完自审，再交校验

```bash
python scripts/validate.py     # 0=通过 1=有ERROR 2=用法/IO错误
python scripts/build.py --out site   # 本地看渲染效果（术语首现样式、代码块）
```

自审 prompt 见 `docs/SOP.md` §9.3。**不要跳过自审**，把没自查的稿子丢给复核者是浪费复核者。

### 单讲产出清单

**契约层**
- [ ] front matter 8 字段齐全，`+++` 成对
- [ ] `lecture` / `slug` 唯一，`source_url` 非空
- [ ] `output_mode` 与 `[license].verified` 不冲突
- [ ] 每个 `[[term:key]]` 的 key 都在 `glossary.toml` 中（多词术语用连字符：`leader-election`）
- [ ] 正文出现的每个 glossary `en` 原词都已打标记
- [ ] 无「几乎全为 ASCII 且 > 400 字符」的段落

**质量层**
- [ ] 概念前置已补
- [ ] 推导无跳步
- [ ] 每个代码块关键行有中文注释，代码块保持短小
- [ ] 结尾有原文位置（可溯源）
- [ ] 术语全文一致
- [ ] 语气合规，无禁用词
- [ ] 无逐句改写痕迹、无整段英文、无图片复制

**收尾**
- [ ] `status` 保持 `"draft"`（复核通过后才由复核者推到 `reviewed` / `approved`）
- [ ] `python scripts/validate.py` **exit 0**
- [ ] 提交信息用祈使句 + 范围前缀：`6.824: 讲解 Lecture 3 主从复制`

## 不要做

- ❌ 把整讲逐句翻译成中文（这是 `transcript` 语义，被闸门禁止）
- ❌ 在 `verified = false` 时写 `output_mode = "transcript"`，或给 `course.toml` / front matter 加 spec 未定义的字段
- ❌ 改 `glossary.toml` 的既有条目（→ 开 issue，走双人评审）
- ❌ 把英文原文 / 课件 / 视频 / 作业答案粘进仓库
- ❌ 自己发明 front matter 字段或 `course.toml` 字段
- ❌ 自己发明 `scripts/*.py` 的命令行参数（只有 `validate.py` / `build.py` 的用法是冻结的）
