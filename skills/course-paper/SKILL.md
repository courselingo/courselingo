---
name: course-paper
description: Handle one classic CS paper in a CourseLingo course repository end to end — decide guide vs. full translation, register the paper in papers.toml with its own [paper.license] block, verify the publisher's licensing from raw HTML evidence, write a guide that genuinely teaches the paper, and keep a permitted translation inside its gate. Use when adding or revising a paper page under content/papers/<key>/, when registering or license-checking a paper, or when deciding whether a paper's translation is allowed.
---

# course-paper · 单篇论文（导读 / 全文翻译）

**一篇论文 = `papers.toml` 里一条 `[[paper]]` + 一个 `content/papers/<key>/index.md`。**

本 skill 只处理**一篇**论文。课程立项与课程授权见 `course-init`；讲解深度与写作质量的标准见 `course-explain`；跑校验、构建与发布见 `course-validate-publish`；画图见 `course-diagram`。

## ⚠️ 先认清一件事：论文的授权与课程**无关**

一门课是 CC BY 3.0 US，**推不出**它课表上的 MapReduce（USENIX）或 GFS（ACM）可以翻译。
所以 **每篇论文各自一个 `[paper.license]`** —— 不是课程级布尔，两篇之间也不能互相顶替。

两档产出、两个闸门（spec §10.3）：

| `output_mode` | 是什么 | 闸门 |
| --- | --- | --- |
| `guide` | **我们自己写的导读**：它要解决什么问题、怎么解、代价是什么 | **不设闸门** —— 思想与概念不受著作权保护 |
| `translation` | **全文翻译**：复制整篇表达（与逐字稿翻译同级风险） | 必须 `verified = true` **且** `allows_translation = true` |

**默认答案永远是 `guide`。** 「不确定能不能翻译」不是停工理由 —— **写导读，然后开工**。
`guide` 不是次等品：读得懂的导读比没人校对的全译更有用。

## 前置阅读（先读，再动手）

| 文件 | 你从中取什么 |
| --- | --- |
| `papers.toml` | 本篇的元数据与 `[paper.license]` —— **唯一来源**，正文里不要再写一套 |
| `docs/pipeline-spec.md` §10 | 冻结契约：登记表字段、论文页 front matter、两档闸门、核实方法论（§10.6） |
| `docs/paper-licensing.md` | **逐篇授权的权威来源**：本篇是否已核实、结论是什么、证据在哪 |
| `docs/content-policy.md` | 授权原则、署名规范、下线机制 |
| `docs/SOP.md` §3（②P/②Q）、§5（论文产出）、§6、§7（⑥P） | 论文轨道的阶段、清单与闸门 |
| `docs/SOP.md` §9.4 / §9.5 | 导读 / 翻译的可粘贴提示词 |
| `template/content/papers/mapreduce/index.md` | 导读的范式：该写哪七块 |
| `glossary.toml` | 冻结术语，正文逐条遵守 |

---

## 步骤 0 · 先定档位（最省事、也最关键的一步）

**在写任何内容之前先回答**：这篇允许翻译吗？

```
papers.toml[key].license.verified          == true  ?
papers.toml[key].license.allows_translation == true  ?
```

| 结果 | 档位 | 动作 |
| --- | --- | --- |
| 任一为 `false`（**包括「还没核实」**） | `guide` | 直接进步骤 3 写导读。**不需要任何授权** |
| 两条都为 `true` **且**证据三件套非空 | 可 `guide`，也可 `translation` | 先确认你想要哪种；想翻译才继续 |
| 不确定 / `docs/paper-licensing.md` 里没结论 | `guide` | 写导读；核实交给 步骤 2，**不要边写翻译边等结论** |

**「已核实」≠「可以翻译」。** 核实的结果完全可能是「查明有版权、须走授权流程」—— 那是 `verified = true` + `allows_translation = false`，翻译仍然被闸门拦死。

> 想开 `translation` 却拿不出证据 → **不要改 `papers.toml` 的字段**。改授权字段去凑条件 = 伪造授权证据，是这个项目的红线行为。

---

## 步骤 1 · 登记（`papers.toml`）

**先登记，再写稿。** 论文页的 `paper` 字段指向未登记的 key 会直接 ERROR（spec §6.9）。

```toml
[[paper]]
key = "mapreduce"                 # 必填，唯一；只允许小写字母、数字与连字符
title = "MapReduce: Simplified Data Processing on Large Clusters"
authors = ["Jeffrey Dean", "Sanjay Ghemawat"]   # 必填，**非空数组**
venue = "OSDI 2004"               # 必填
year = 2004                       # 可选
publisher = "USENIX"              # 可选但强烈建议（决定去查谁的政策页）
url = "https://..."               # 必填：论文的**官方条目页**，不是作者主页的 PDF
pdf_url = ""                      # 可选

[paper.license]
verified = false                  # ★ 未核实就是 false，别猜
terms = ""
evidence_url = ""
checked_at = ""
allows_translation = false        # ★ 与 verified 相互独立
allows_commercial = false
share_alike = false
notes = "未核实。核实方法与结论见 docs/paper-licensing.md"
```

规则：

- **先一律写 `false`**。占位是诚实的，「猜一个 true」不是。
- `key` 定下就不要改：它同时是目录名 `content/papers/<key>/` 与站点 URL `site/papers/<key>/`。
- `authors` 必须是**数组**，写成字符串会 ERROR。
- `venue` / `url` 缺一个就 ERROR；`url` 要官方条目页（USENIX / ACM DL / IEEE Xplore），不是镜像、不是作者主页的 PDF。
- `publisher` 不是必填，但它直接决定步骤 2 去查谁的政策 —— 填上。
- **每篇都要有自己的 `[paper.license]` 块**，不要复制粘贴另一篇的 `terms` / `evidence_url`。

### 讲座与本篇交叉链接（可选）

讲座 front matter 可以声明它涉及哪些论文：

```toml
papers = ["mapreduce", "gfs"]     # 必须是 papers.toml 中已登记的 key
```

key 必须**已经登记**，否则该讲座 ERROR（spec §6.11）。这比在正文里写一句「详见 MapReduce 那篇」有用得多 —— 它成了结构化数据。

---

## 步骤 2 · 核实授权（四步，spec §10.6 的方法论）

> **这一步没有命令。** spec 不提供、也不应有「核实授权」的脚本 —— 授权是**读原文并记录**的人工动作。用记忆填 `terms` 比留空**更危险**。

1. **抓原始 HTML，不要过滤标签后再搜文本。**
   许可常常只是一个 `rel="license"` 属性或图片徽章的 `href`。本项目就因此误判过一次：6.824 的 CC BY 3.0 US 徽章**是纯图片链接、没有任何可见文字**，只扫文本会得出「未声明许可 = 保留所有权利」的相反结论（见 `docs/course-catalog.md`）。
   → 把原始页面**落盘**再搜（`curl -o`），并留证。
2. **「能免费下载」≠「允许翻译」。**
   作者把 PDF 挂在自己主页上**没有授予任何许可**，法律状态仍是保留所有权利。URL 打得开 ≠ 有授权。
   → PDF 链接只能进 `url` / `pdf_url`，**不能进 `evidence_url`**。
3. **查出版社的政策，不只看论文页。**
   多数经典系统论文的版权在 **ACM / IEEE / USENIX**。ACM 有**明确的翻译授权流程** —— 那意味着「默认不可翻译，须先申请」。论文页上没有许可声明时，下一步就是看出版社的 copyright / permissions 页。
4. **逐篇记录 `evidence_url` 与 `checked_at`；核不出来就标未核实。**
   无法核实 → `verified = false`、`allows_translation = false`，`notes` 写「未确认」。**不要推测**，也不要用「大家都这么用」补空白。

⚠️ **同一篇论文的「会议版 / 技术报告 / 扩展版」条款可能不同**（Raft 的会议版与技术报告版就是常见例子）。`url` 必须与 `evidence_url` 指向**同一版**。

### 记录到两处

| 位置 | 填什么 |
| --- | --- |
| `papers.toml` 的 `[paper.license]` | `terms`（**原文照抄**的条款名）/ `evidence_url` / `checked_at`（ISO 日期）/ `allows_translation` / `allows_commercial` / `share_alike` / `notes` |
| `docs/paper-licensing.md` | 该篇的结论行，含原文引用与访问日期（**权威来源**） |

### `verified = true` 的四条前置（缺一不可）

- [ ] `terms` 非空，且是原文照抄的条款名
- [ ] `evidence_url` 非空，且**复核者本人打开过**
- [ ] `checked_at` 为 ISO 日期
- [ ] `allows_translation` 已明确判断（论文这边「能不能改编」被收窄成更具体的「能不能翻译」）

`verified = true` 而 `terms` / `evidence_url` / `checked_at` 任一为空 → `validate.py` **exit 1**（spec §6.8）。

### 人工闸门（**逐篇**双人签字）

- [ ] 证据由**第二人独立复核**（自己再看一遍不算复核）
- [ ] `evidence_url` 指向的是**该论文**的条款或**其出版社**的政策页，不是聚合站 / 仿制页
- [ ] 判定只依据 `evidence_url` 的原文，不依据「大家都这么用」「课表上就挂着 PDF」
- [ ] **不拿别的论文的条款顶替** —— 同一门课里 MapReduce（USENIX）与 GFS（ACM）各不相同
- [ ] **不拿课程的 `[license]` / `[license.materials]` 顶替** —— 那是课程材料的授权，与论文无关
- [ ] 未核实 → 结论就是 `false`，**照常开工导读，不照常开工翻译**

---

## 步骤 3 · 建目录与 front matter

> ⚠️ **没有论文骨架脚本。** `new_lecture.py` 只生成讲座（spec §1 也只列了它），论文页要**手工建**（见 `docs/SOP.md` §14-15）。手工建最容易漏 `kind = "paper"` 或把 `paper` 的 key 拼错，这两条都直接 ERROR —— 建完立刻跑一次 `validate.py`。

```
content/papers/<key>/index.md
content/papers/<key>/figures/*.svg      # 需要配图时
```

front matter 只有 **5 个字段**（spec §10.2）：

```markdown
+++
kind = "paper"
paper = "mapreduce"
title = "MapReduce 导读"
status = "draft"
output_mode = "guide"
+++
```

| 字段 | 规则 |
| --- | --- |
| `kind` | 固定 `"paper"`，写错直接 ERROR |
| `paper` | `papers.toml` 里的 key，**逐字符一致**；全课程不重复（一篇论文只允许一个论文页） |
| `title` | 中文标题（导读就叫「X 导读」，翻译就叫「X」或「X（中文翻译）」） |
| `status` | 新写的永远是 `"draft"` |
| `output_mode` | `guide` 或 `translation`，与步骤 0 的结论一致 |

**论文页没有 `lecture` / `slug` / `source_kind` / `source_url`** —— 作者、出处、来源链接全部由 `papers.toml` 提供，**同一事实不要写两处**。写了不算错，但它们不生效、只会误导后来人。

---

## 步骤 4 · 写导读（`guide`，默认档）

导读要**真的教这篇论文**，不是复述摘要。**七块缺一不可**：

### 4.1 它要解决什么问题
具体到当时的**具体麻烦**：什么任务、什么量级、旧办法为什么不行。
❌「随着互联网的发展，数据量越来越大」 ✅「每一类任务都要重写一遍分布式代码：怎么切分输入、怎么在机器挂掉时重试、怎么把中间结果送到该去的地方 —— 而且每次都容易写错」

### 4.2 核心主张 / 核心抽象
论文真正贡献的那个想法，并用一句话说清**它把什么变成了不用再想的前提**。
（例：MapReduce 把「怎么并行」抽出来做成框架，业务逻辑只写两个函数 —— 于是「分布式」从一个每次都要重新解决的问题，变成了一个不用再想的前提。）

### 4.3 机制走查
关键路径**按顺序**讲清楚：数据怎么流、谁做什么决定、哪一步是设计的枢纽。
**讲「为什么这么设计」，不只讲「设计成什么样」。** 找到那个枢纽步骤，说清它换来了什么、牺牲了什么。

### 4.4 边界与代价
论文**自己承认**的限制（不适合迭代式算法、单点、磁盘布局……）。
这一段最能区分「真读过」和「抄了摘要」—— 摘要里不会有代价。

### 4.5 与课程的关系
它是后面哪几讲的直觉前置；讲座那边用 `papers = ["<key>"]` 做交叉链接（步骤 1）。正文里可以用 `[[term:key]]` 交叉引用已冻结术语。

### 4.6 读完应该能回答
3 个左右的**判断力**问题（「为什么中间结果要写本地磁盘？」），不是知识问答（「MapReduce 是哪一年提出的？」）。

### 4.7 溯源
`papers.toml` 的 `url` + 本文对应的章节位置。**给位置，不给文本。**

### 写作纪律

- **术语**：用 `[[term:<key>]]` 标记已冻结术语，key 由 glossary 的 `en` 派生（小写、空格与下划线转连字符）。不要用中文替代词绕过标记，也不要直接写英文原词。需要新术语 → 回 `course-init` 走评审加词。
- **不转载**：不复制论文的句子、图表、图片、公式排版。**导读里一段原文都不放**（论文页同样走「几乎全为 ASCII 且 > 400 字符」的转载探测）。
- **配图自己画**（走 `course-diagram`）：`content/papers/<key>/figures/<key>-<n>.svg`，正文用**相对路径**引用，**alt 必写中文结论**。图里术语必须与 `glossary.toml` 一致。
- **不编数字**：只依据论文本身与公开官方信息；拿不准就写「论文给出的数字是 X（原文 §N）」，不要自己推算，不要凭记忆补年份、机构名、实验结论。
- **篇幅**：一篇导读 = 一次课读得完，主题收敛。
- **语气**：像助教不像营销号；用「你」；无「全网最全 / 颠覆 / 封神」（`docs/brand.md`）。

可粘贴的提示词见 `docs/SOP.md` §9.4。

### 导读交付清单

- [ ] front matter 5 字段齐全，`+++` 成对；`output_mode = "guide"`
- [ ] `paper` 与登记表的 `key` 逐字符一致，且未被另一个论文页占用
- [ ] 没写 `lecture` / `slug` / `source_kind` / `source_url`
- [ ] 七块俱全（问题 / 主张 / 机制 / 代价 / 与课程的关系 / 检查问题 / 溯源）
- [ ] 每个 `[[term:key]]` 都在 `glossary.toml`；glossary 的 `en` 原词都已打标记
- [ ] 无「几乎全为 ASCII 且 > 400 字符」的段落；无原文段落、无复制的图表
- [ ] 配图自己画的，alt 是中文结论
- [ ] `status = "draft"`
- [ ] `python scripts/validate.py` **exit 0**

---

## 步骤 5 · 如果翻译**确实**被允许，会多什么

前置：`verified = true` **且** `allows_translation = true`，且证据三件套非空、已入 `docs/paper-licensing.md`。
**开工前把 `terms` / `evidence_url` / `checked_at` 贴进 PR 描述** —— 复核者要看的不是「我确认过了」，而是**你依据的那一条条款**。

相比导读，翻译多了这些要求：

| 项 | 导读 | 翻译 |
| --- | --- | --- |
| front matter | 5 字段 | 同样 5 字段，但 `output_mode = "translation"` |
| 授权 | 不需要 | **两个 `true` + 证据三件套**，缺一不可 |
| 忠实度 | 讲清概念即可 | **不增、不删、不「润色」掉限定条件**；译者补充必须单独成小节并标注「译者注」 |
| 原文 | 一段都不放 | 除术语 / 代码 / 公式 / 专有名词外，也不放整段英文原文 |
| 图表 | 自己画 | **重画或转写**，不得截图、不得复制原始图片；重画的走 `course-diagram` |
| 开头 | 溯源位置 | 论文标题 / 作者 / venue / 年份 / 官方链接 / **版本与章节范围** / 授权依据（`terms` + `evidence_url`） |
| 复核 | 双人 | **授权复核人 ≠ 译者**；抽 3 处与原文逐句对照 |
| 复核问题 | 「这段是读出来的还是摘要的复述？」 | 「有没有漏译 / 增益 / 抹掉限定条件？」 |

⚠️ **机器兜底识别不了译文。** 转载探测只认「几乎全为 ASCII 的长段落」，而合规译文本来就是中文 —— `translation` 的**唯一防线是授权闸门 + 人工复核**（见 `docs/SOP.md` §14-18）。**别因为 `validate.py` exit 0 就以为译文安全。**

`build.py` 在论文翻译闸门上有**独立的第二道**检查：命中即 exit 1 且**不产出任何站点**（spec §7）。
和讲座一样，把它当**事后报警器，不是授权流程的替代品**。

可粘贴的提示词见 `docs/SOP.md` §9.5。

---

## 步骤 6 · 校验与复核

```bash
python scripts/validate.py            # 0=通过 1=有ERROR 2=用法/IO错误
python scripts/build.py --out site    # 看授权提示条与元数据，别只看 Markdown
```

论文相关 ERROR（spec §6.8–§6.11）：

| ERROR | 修法 |
| --- | --- |
| `papers.toml` 缺字段 / `key` 不合规或重复 / `verified = true` 但证据字段为空 | 补字段；`authors` 要是**数组**；**没证据就把 `verified` 改回 `false`**，别去「补」证据 |
| 论文页缺 `kind = "paper"` 或必填字段 / `paper` 未登记或重复 / `output_mode` 非法 | 补字段；`paper` 与登记表对齐；一篇论文只允许一个论文页 |
| **翻译闸门**：`translation` 而 `verified` 或 `allows_translation` 不为 `true` | **默认改回 `guide`** 写导读。要开翻译 → 回步骤 2 拿证据 |
| 讲座 `papers = [...]` 引用了未登记的 key | 回步骤 1 登记，或改掉写错的 key |

复核（`status` 的流转：`draft` → `reviewed` → `approved`）：

- `guide`：确认档位选得对（该篇确实不满足翻译条件，或我们主动选择只发导读）；元数据与 `papers.toml` 一致。
- `translation`：授权复核人独立打开 `evidence_url` 验证；确认 `allows_translation` 是**这一版**论文的结论；抽 3 处逐句对照。
- **授权判定有任何疑点 → 立刻退回 `guide`**（宁可只发导读，不发译文）。
- 一旦被指出超出授权范围 → 走 content-policy 的**立即下线**流程：不讨论、不等结论。

发布前打开 `site/papers/<key>/index.html` 目视验收：元数据正确、**授权提示条**与档位相符、`verified = false` 时页面上不得出现任何「已授权 / 已核实」措辞。

---

## 不要做

- ❌ **把「能免费下载」当成许可** —— 作者主页的 PDF 不是授权来源；`evidence_url` 必须是条款或出版社政策页
- ❌ **用一篇论文的条款顶替另一篇** —— 每篇各自抓、各自填、各自签字
- ❌ **拿课程的 `[license]` / `[license.materials]` 当论文授权** —— 课程笔记已核实推不出论文可翻译
- ❌ **把「已核实」当成「可以翻译」** —— `verified` 与 `allows_translation` 两个条件缺一不可
- ❌ **为了让 `translation` 过校验而改 `verified` / `allows_translation`** —— 伪造授权证据，红线行为
- ❌ **先写翻译、回头再补授权** —— 先把档位定下来（默认 `guide`）
- ❌ **在导读里放原文段落或复制图表** —— 导读的授权优势就来自「不复制表达」
- ❌ **翻译时截图论文的图 / 表** —— 重画或转写
- ❌ 修改 `papers.toml` 里**别的**论文的字段，或改 `glossary.toml` 的既有条目（→ 开 issue，走双人评审）
- ❌ 新增 spec 未定义的 `papers.toml` / 论文页 front matter 字段
- ❌ 使用 spec 未定义的脚本参数，或自己发明 `scripts/*.py` 的行为
