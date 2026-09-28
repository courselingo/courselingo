# 操作手册 · SOP（从零到一篇已发布讲座）

> **本手册的位置**：[pipeline-spec.md](./pipeline-spec.md) 是**冻结的接口契约**，本手册是**执行手册**。
> 两者冲突时，以 spec 为准；本手册不新增、不修改任何接口。若发现 spec 有缺口，写进本文 [§14 待决事项](#14-待决事项spec-缺口)，**不要私自发明约定**。
>
> 适用对象：驱动 Agent 干活的人（或 Agent 自己）。
>
> **命令的执行位置**：阶段 ① 的 `new_course.py` 在**平台主仓库**根目录执行（它负责**生成**课程仓库）；其余命令（`new_lecture.py` / `validate.py` / `build.py`）都在**课程仓库**根目录执行。

---

## 0. 三条不变量（任何阶段都不得违反）

| # | 不变量 | 机器兜底 | 违反的后果 |
| --- | --- | --- | --- |
| 1 | **授权优先**：`course.toml` 的 `[license].verified != true` 时，禁止产出 `output_mode = "transcript"` | `validate.py` 硬失败（exit 1） | 侵权。这是项目最大的敌人，比翻译质量更能决定生死 |
| 2 | **术语先行**：术语在写正文**之前**冻结；同一概念全课程同一个中文词 | `[[term:key]]` 引用不存在 → ERROR；glossary 的 `en` 出现在正文却没打标记 → WARN | 术语漂移，全课程返工，核心资产作废 |
| 3 | **不转载**：不把英文原文、幻灯片、视频、作业答案写进仓库 | 「几乎全为 ASCII 且 > 400 字符」的段落 → ERROR | 仓库变成原课程的复制品，授权风险最高 |

**默认产出永远是「原创中文讲解」，不是翻译。** 逐句翻译 / 字幕 / 作业答案翻译是**默认关闭**的能力，开启它需要该课程该**材料类型**的书面授权。

---

## 1. 阶段地图

```
① 课程立项 ──► ② 授权核实（★闸门）──► ③ 术语表冻结（★闸门）
                                            │
                                            ▼
                              ④ 逐讲产出（可并行）
                                            │
                                            ▼
                              ⑤ 校验（机器，可重复）
                                            │
                                            ▼
                              ⑥ 人工复核（★闸门）
                                            │
                                            ▼
                              ⑦ 发布
```

| # | 阶段 | 命令 | 主输入 | 主输出 | 人工闸门 | 可并行 |
| --- | --- | --- | --- | --- | --- | --- |
| ① | 课程立项 | `python scripts/new_course.py` | `docs/course-catalog.md` | `course.toml` / `glossary.toml` / `content/` / `scripts/` | 课程 id 与中文名已登记在 catalog | — |
| ② | 授权核实 | *（无脚本，人工动作）* | `docs/content-policy.md` 的 9 项复核清单 | `[license]` 字段 + 核实记录 | **双人签字**；未核实则保持 `verified = false` | ❌ 串行，全局闸门 |
| ③ | 术语表冻结 | `python scripts/validate.py` | 官方材料（运行时只读） | 冻结版 `glossary.toml` | 术语评审 + 冻结声明 | ❌ 串行 |
| ④ | 逐讲产出 | `python scripts/new_lecture.py` | 讲座骨架 + 冻结 glossary + 源材料 | `content/<NN>-<slug>/index.md`（`status="draft"`） | 无（草稿），但须过 §5 清单自查 | ✅ 讲与讲之间可并行 |
| ⑤ | 校验 | `python scripts/validate.py` | 全部 `content/**/index.md` | exit code + ERROR/WARN 列表 | 无 | ✅ 可重复跑 |
| ⑥ | 人工复核 | `python scripts/validate.py` → `python scripts/build.py --out site` | 校验通过的 draft | `status = "reviewed"` → `"approved"` | **双人签字**（术语/授权改动） | ✅ 讲与讲之间可并行 |
| ⑦ | 发布 | `python scripts/build.py --out site` | `approved` 讲座 | `site/`（不入库）+ CI 部署 | 目视验收 + 「非官方」声明检查 | ❌ 串行 |

---

## 2. 阶段 ① 课程立项

**目的**：把一门课变成可开工的仓库骨架。**此阶段不写任何正文。**

### 输入
- `docs/course-catalog.md` 中已登记的课程（未登记的先登记，不要在 catalog 之外另开课程）
- 官方入口 URL（只填官方地址）

### 命令
```bash
# 在【平台主仓库】根目录执行：它从 template/ 生成一个新的课程仓库
python scripts/new_course.py --id mit-6.5840 --out ../courses/mit-6.5840 \
    --title "Distributed Systems" --title-zh "分布式系统" \
    --institution MIT --course-number "6.5840 / 6.824" \
    --homepage "https://pdos.csail.mit.edu/6.824/"
```
默认会移除模板自带的演示讲座，得到干净的课程仓库；`--keep-demo` 保留演示内容（用于验证流水线）。

> ⚠️ **执行位置注意**：spec §1 把 `new_course.py` 画在**课程仓库结构里**，而当前实现把它放在**平台主仓库**的 `scripts/` 下，并通过 `--out` 指定课程仓库位置。同时其 CLI 参数**不在冻结 spec 中**（见 §14-1、§14-11）。
> 若脚本行为与本节不符，按 spec §1 手工建目录、按 §2/§3/§4 手工写 `course.toml` / `glossary.toml` / `index.md`。

### 输出
```
course.toml      # 按 spec §2 填 [course] / [license] / [output]
glossary.toml    # 空表，等待阶段 ③
content/         # 空目录
scripts/         # new_lecture.py / validate.py / build.py
```

必填字段（缺一个 → `validate.py` exit 1）。
spec §2 只把 `id` / `title` / `title_zh` 标为必填；**当前实现要求更多**（见 §14-11）：

| 来源 | 必填字段 |
| --- | --- |
| spec §2 标注 | `id`、`title`、`title_zh` |
| 当前 `validate.py` 实际校验 | 上述三者 + `institution`、`source_language`、`target_language` |

建议全部填上（含 `course_number`、`homepage`），一次到位：

`[license]` 全部留空 / `verified = false`，**留给阶段 ②**：

```toml
[license]
verified = false
terms = ""
evidence_url = ""
checked_at = ""
allows_commercial = false
allows_derivatives = false
share_alike = false
notes = ""

[output]
default_mode = "explanation"
```

### 验证
```bash
# 在【课程仓库】根目录
python scripts/validate.py
```

⚠️ **此时还没有任何讲座，校验会报「没有任何讲座」而 exit 1 —— 这是预期的，不是配置错误。**
（当前实现把「`content/` 下没有任何讲座」也当作 ERROR；spec §6 的 ERROR 清单里**没有**这一项，见 §14-12。）

因此阶段 ① 的验证方式改为：

1. 先只确认 `course.toml` 能被解析、`[course]` 必填字段齐全 —— 把「没有任何讲座」之外的其他 ERROR 清零。
2. 建好第一讲骨架（步骤见 §5/`course-init`）后，再跑一次 `validate.py`，此时应当 **exit 0**。

### 人工闸门 ①
- [ ] `course.id`、`title_zh` 与 `docs/course-catalog.md` 一致（不允许各写各的）
- [ ] `title_zh` 是课程**通用中文名**，不是自创品牌名
- [ ] `homepage` 是官方入口，不是第三方镜像
- [ ] `[output].default_mode = "explanation"`（在阶段 ② 出结论前不得改成别的）
- [ ] **仓库里没有任何课程原料**（PDF / 视频 / 逐字稿 / 幻灯片）

---

## 3. 阶段 ② 授权核实（★ 最硬的闸门）

**这一阶段没有命令。** spec 没有也不会有一个「核实授权」的脚本 —— 授权是**读原文并记录**的人工动作。任何试图自动化它的做法都是在用记忆填补空白，而 content-policy 明确禁止这一点。

### 输入
- [content-policy.md](./content-policy.md) 的《逐课程复核清单》（9 项）
- [course-catalog.md](./course-catalog.md) 的《待抓取清单》与《记录格式》表
- [licensing-research-log.md](./licensing-research-log.md) 的现状（当前：**全部未核实**）

### 动作
1. **实际访问**官方页面，逐字摘录许可文本，记录访问日期。不可达就写「不可达」，**不得推断**。
2. **按材料类型分别核实**（这是 content-policy 的要求，而 spec 的 `course.toml` 只有一个布尔，见 §14-4）：
   - 讲座笔记 / 幻灯片
   - 讲座视频（**许可可能与课件不同**，还叠加平台条款）
   - 作业 / Lab 题面与答案
   - 教材（如有，是独立作品）
3. 把结论写回三处：
   - `course.toml` 的 `[license]` 字段（`terms` / `evidence_url` / `checked_at` / `allows_commercial` / `allows_derivatives` / `share_alike` / `notes`）
   - `docs/course-catalog.md` 的《记录格式》表（含原文引用与访问日期）
   - `docs/licensing-research-log.md` 的核实表

`checked_at` 用 ISO 日期（如 `2026-02-14`）。

### 输出
- `[license]` 字段全部有据可依
- 核实表一行，含**原文引用**
- 明确结论：`verified` 是 `true` 还是 `false`

### `verified = true` 的四条前置（缺一不可）
- [ ] `terms` 非空，且是**原文照抄**的条款名
- [ ] `evidence_url` 非空，且**复核者本人真的打开过**
- [ ] `checked_at` 为 ISO 日期
- [ ] `allows_derivatives` 已明确判断（翻译属于衍生作品，这一项决定整门课能不能做）

### 人工闸门 ②（双人签字）
- [ ] 证据由**第二人独立复核**一次（自己看一遍不算复核）
- [ ] `verified` 的判定**只依据 evidence_url 的原文**，不依据「大家都这么用」「MIT OCW 应该是 CC BY-NC-SA」
- [ ] 特别注意两个陷阱：MIT OCW 的 **NC / SA** 条款极易记错；6.824 / 6.1810 的讲座笔记历史上**未声明许可** —— 未声明的法律状态是**保留所有权利**
- [ ] 即便 `verified = true`：**视频字幕翻译**仍默认关闭（平台条款叠加）；**作业答案翻译永久排除**（著作权 + 学术诚信）
- [ ] 未核实 → 结论就是 `verified = false`，全课程 `output_mode = "explanation"`，**照常开工讲解，不照常开工翻译**

### 机器兜底
```bash
python scripts/validate.py
```
只要存在任一 `output_mode = "transcript"` 的讲座而 `verified != true`，**exit 1**（spec §6.2）。
把这条当成**事后报警器，不是授权流程的替代品** —— 一个已经写好的逐字稿被拦下来，意味着前面全白做且已经产生侵权风险。

---

## 4. 阶段 ③ 术语表冻结（★ 闸门）

**目的**：术语表是项目的**核心资产**，独立于模型。换模型不应导致术语漂移 —— 前提是术语在写正文之前就定死。

### 输入
- 官方材料（**运行时只读，不入库**）：课程大纲、讲座列表、术语密集页面
- [CONTRIBUTING.md](../.github/CONTRIBUTING.md) §1 术语一致性规则

### 命令
```bash
# 可选：先造 1–2 个讲座骨架，便于在真实上下文里试标术语
python scripts/new_lecture.py

# 每轮改完 glossary.toml 都跑
python scripts/validate.py
```

### 输出
`glossary.toml`，条目形态严格按 spec §3：
```toml
[[term]]
en = "replication"
zh = "副本"
aliases = ["replica", "replicas"]
notes = "此处指数据副本机制"
```
- `en` / `zh` 必填且非空
- `en` 唯一（**大小写不敏感**去重）
- `aliases` 收异体/复数
- `notes` 只在有歧义时写

#### 标记 key 怎么来（★ 写正文时最容易错的一处）

spec §5 只给了单词示例 `[[term:replication]]`，**没有定义多词术语的 key 派生规则**（见 §14-10）。
当前实现的规则是：**key = `en` 小写化、空白与下划线转连字符、去掉其他非 `[a-z0-9.-]` 字符**。

| `en` | 正文里必须写的标记 |
| --- | --- |
| `replication` | `[[term:replication]]` |
| `leader election` | `[[term:leader-election]]` |
| `primary-backup replication` | `[[term:primary-backup-replication]]` |

**写成 `[[term:leader election]]`（带空格）会 ERROR：key 不存在。** 正文匹配时 key 按小写比对，所以 `[[term:Leader-Election]]` 能通过，但**统一写小写**。

> 当前实现还允许在 `[[term]]` 里显式写一个 spec §3 未定义的 `key = "..."` 字段来覆盖派生结果 —— **不要用它**（不在冻结契约内，见 §14-10）。

规模基线：首门课首版 **60–100 条**（ROADMAP Phase 1），至少覆盖前 3 讲。

### 术语决策规则
| 情况 | 做法 |
| --- | --- |
| 业界已有通行译法 | **优先沿用**（`consensus` → 共识） |
| 无通行译法 | 保留英文，在 `zh` 或 `notes` 中给出译名并说明 |
| 一词多义（如 `thread`） | 每个义项一个独立条目，用 `notes` 区分；**不允许同 key 两译** |
| 想改已有译法 | **开 issue 说明理由，不静默改动**（CONTRIBUTING §1） |

### 人工闸门 ③
- [ ] 目标 60–100 条，覆盖已排期的前 3 讲
- [ ] 每条 `en` 唯一、`zh` 非空；没有「一条概念两个 key」（`replica` 与 `replication` 要分清）
- [ ] 每条术语都是**真的术语**，不是普通词（不要把 `the`、`system` 收进来）
- [ ] 分歧清单（拿不准的 5 条）已逐条给出候选译法与理由，并由**两名维护者**确认
- [ ] `python scripts/validate.py` **exit 0**
- [ ] 在 PR 描述中写明 **「glossary frozen @ `<commit short sha>`」**（冻结声明，见 §14-5：spec 没有专门的冻结字段）

### 冻结的纪律
冻结之后：
- 新增术语**必须**走同样的评审 + 双人确认流程
- 术语变更会**让所有已产出讲座的 WARN 结果失效** → 变更后必须**全课程重跑** `validate.py`
- **并行写正文的前提就是 glossary 不再变**。要加词 → 先停并行、加词、重跑校验、再恢复

---

## 5. 阶段 ④ 逐讲产出

**目的**：产出一篇**原创中文讲解**。不是翻译。

### 输入
- 讲座骨架 `content/<NN>-<slug>/index.md`（由 `new_lecture.py` 生成）
- **冻结版** `glossary.toml`
- 源材料（运行时读取，**绝不入库**）

### 命令
```bash
python scripts/new_lecture.py     # 每个讲座一次，生成骨架
```

### 输出
`content/<NN>-<slug>/index.md`，front matter 严格按 spec §4（`+++` 分隔，8 个字段）：

```markdown
+++
title = "主从复制"
lecture = 3
slug = "primary-backup-replication"
status = "draft"
source_kind = "notes"
source_url = "https://pdos.csail.mit.edu/6.824/notes/l03.txt"   # 必填，署名与可溯源
source_title = "Primary-Backup Replication"
output_mode = "explanation"
+++
```

| 字段 | 值域 | 注意 |
| --- | --- | --- |
| `lecture` | 整数 | **全课程唯一** |
| `slug` | 字符串 | **全课程唯一**；与目录名 `<NN>-<slug>` 的 slug 一致（见 §14-8） |
| `status` | `draft` / `reviewed` / `approved` | 新写的永远是 `draft` |
| `source_kind` | spec §4：`notes` / `video` / `textbook` / `other` | 如实填。注意当前实现额外接受 `slides`（spec 未定义，见 §14-11）；**按 spec 只用这四个值** |
| `output_mode` | `explanation` / `transcript` | **`verified = false` 时只能是 `explanation`** |

> `source_title` 在 spec §4 的示例里存在，但**当前实现不把它列为必填**（见 §14-11）。仍然建议填 —— 它是署名与可溯源的一部分。

配图放 `content/<NN>-<slug>/figures/*.svg`，正文用 `![说明](figures/xxx.svg)` 引用；需要画图时走 `course-diagram` skill。

### 每讲产出自查清单（Agent 自己先过一遍，再进阶段 ⑤）

**契约层**
- [ ] front matter 8 字段齐全，`+++` 成对
- [ ] `lecture` / `slug` 未与已有讲座重复
- [ ] `source_url` 非空、指向官方来源
- [ ] `output_mode` 与 `[license].verified` 不冲突
- [ ] 正文中每个 `[[term:key]]` 的 key 都存在于 `glossary.toml`（多词术语用连字符：`[[term:leader-election]]`，见 §4）
- [ ] 正文中出现的每个 glossary `en` 原词都已打标记（否则会 WARN，且是漂移前兆）
- [ ] 没有任何「几乎全为 ASCII 且 > 400 字符」的段落

**质量层**
- [ ] **概念前置**：本讲依赖但原文默认已知的背景已补
- [ ] **推导可见**：每个「因此 / 显然 / 可得」处都有中间步骤
- [ ] **代码有注释**：每个代码块关键行有**中文**注释；单块保持短小（≤ 400 字符为可读性基准，非校验要求）
- [ ] **可溯源**：结尾列出对应原文位置（讲座号 / 时间戳 / 页码）
- [ ] **术语一致**：同一概念全文同一个中文词
- [ ] **语气**：像助教不像营销号；面向读者写「你」；无「全网最全 / 颠覆 / 封神」
- [ ] **授权边界**：无逐句改写痕迹、无整段英文原句、无图片或幻灯片复制

### 人工闸门 ④
无。草稿阶段不设闸门，但要保证每讲都真的过了上面的清单 —— 把没自查的稿子丢给复核者是浪费复核者。

---

## 6. 阶段 ⑤ 校验

### 命令
```bash
python scripts/validate.py
```

### 退出码（spec §6）
| 退出码 | 含义 | 动作 |
| --- | --- | --- |
| `0` | 通过（可能有 WARN） | 读 WARN，判断是否要改；进阶段 ⑥ |
| `1` | **有 ERROR** | **不得进入复核**，按下面映射表逐条修复后重跑 |
| `2` | 用法 / IO 错误 | 检查工作目录是否是课程仓库根、文件是否齐全 |

### ERROR 修复映射表
| # | ERROR 类（spec §6） | 修法 |
| --- | --- | --- |
| 1 | `course.toml` 不可解析或缺 `[course]` 必填字段 | 补 `id` / `title` / `title_zh`；检查 TOML 引号与缩进 |
| 2 | 存在 `transcript` 讲座而 `license.verified != true` | **默认改回 `explanation`**；只有在阶段 ② 拿到**该材料类型**的书面授权后，才允许把 `verified` 改成 `true` |
| 3 | front matter 必填字段缺 / `lecture` 或 `slug` 重复 / `source_url` 为空 | 逐个补；重复的 `lecture` 重新编号；`slug` 改成唯一的；`source_url` 填官方地址 |
| 4 | `[[term:key]]` 的 key 不在 glossary | 拼写错误 → 改正；多词术语要连字符化（`leader election` → `[[term:leader-election]]`）；确实是新术语 → **回阶段 ③ 走评审加词**（不要就地写个中文替代） |
| 5 | glossary 的 `en` / `zh` 为空或 `en` 重复 | 补空值；`en` 重复 → 合并为一个条目，其余进 `aliases` |
| 6 | 正文有「几乎全为 ASCII 且 > 400 字符」的连续段落 | 十有八九是照抄原文：**删掉重写成中文讲解** |

**关于 ERROR 6 的判定口径**（当前实现，spec §6.6 未写细节，见 §14-6）：段落需同时满足
`长度 > 400 字符` **且** `ASCII 占比 ≥ 90%` **且** `空格数 ≥ 40` 才算可疑；
判定前会**剥离行内代码、链接与 Markdown 标记**，并且**跳过围栏代码块、标题行与表格行**。

所以：
- **代码块不会触发这条**（当前实现跳过围栏内的内容）——「单块 ≤ 400 字符」是**保险做法**，不是校验要求。
- 真正会被拦下的是**成段的英文散文**：这正是「整段照抄原文」的特征，必须删掉重写成中文讲解。
- 长 URL、无空格的长串不会被误判。

### WARN 的处理（不要习惯性忽略）
| # | WARN 类 | 处理 |
| --- | --- | --- |
| 7 | glossary 的 `en` 原词出现在正文但未打标记 | **必查**。要么是漏标术语（→ 补 `[[term:key]]`），要么是术语漂移（→ 改回 glossary 的 `zh`）。两者都是真实缺陷 |
| 8 | `status = "draft"` 的讲座在 `build` 时会被标注「草稿」 | 发布前把状态推到 `reviewed` / `approved` |

---

## 7. 阶段 ⑥ 人工复核（★ 闸门）

### 输入
校验通过（exit 0）的 `status = "draft"` 讲座

### 命令
```bash
python scripts/validate.py
python scripts/build.py --out site      # 本地预览，别只看 Markdown
```

### 输出
- 讲座 `status`：`draft` → `reviewed`（单审通过）→ `approved`（双审通过）
- PR 描述中写明：**对应课程与讲座、授权依据、术语表变更**（CONTRIBUTING §3）

### 复核者逐条判定（引用行号 + 原句 + 最小修改建议）
- [ ] 契约层 7 项（§5 清单前半）全部 pass
- [ ] 质量层 7 项（§5 清单后半）全部 pass
- [ ] 抽查术语一致性：随机挑 5 个术语，全文搜索确认**同一个中文词**、**都打了标记**
- [ ] 抽读 3 段，问一句：「这段话是**我们写的**，还是原文的改写？」有疑虑就驳回重写
- [ ] 术语表变更若在本 PR 中 → 需**两名维护者**确认（CONTRIBUTING §3）

### 人工闸门 ⑥
- [ ] 只有 `status = "approved"` 的讲座才能进阶段 ⑦
- [ ] 复核者的驳回意见必须落到**行号 + 具体修改**，不允许「再打磨一下」这种不可执行的评语
- [ ] 授权边界一经质疑，**立即下线，不讨论、不等结论**（content-policy 下线机制）

---

## 8. 阶段 ⑦ 发布

### 命令
```bash
python scripts/validate.py
python scripts/build.py --out site
# 部署到子路径时（GitHub Pages 项目站）：
python scripts/build.py --out site --base-url /courselingo/
```
> `build.py` 的 CLI 就是 spec §7 定义的两个选项：`--out`（默认 `site`）与 `--base-url`（默认 `/`）。**不要用未定义的参数。**

### 构建产物（spec §7）
```
site/index.html            课程首页 + 讲座目录
site/<slug>/index.html     每篇讲座
site/glossary/index.html   术语表
site/assets/style.css
```

### 本地目视验收（必须真的打开看）
- [ ] 打开 `site/index.html`：讲座目录顺序正确、`status = "draft"` 的讲座已标注「草稿」
- [ ] 打开 `site/<slug>/index.html`：侧边栏导航、面包屑、`<meta name="description">` 均存在
- [ ] 术语渲染正确：**首现**显示「中文（English）」，**后续**只显示中文
- [ ] 明暗色都看一遍；中文行高与字距可读（`lang="zh-CN"`）
- [ ] 页脚有**署名**与「**非官方 · 社区项目**」声明
- [ ] **站点里没有任何英文原文段落、课件、视频、作业答案**
- [ ] 无任何学校校徽 / 课程 Logo / 官方背书暗示（brand.md 禁止事项）

### CI（spec §8）
| 工作流 | 触发 | 行为 |
| --- | --- | --- |
| `validate.yml` | push / PR | 跑 `validate.py`，有 ERROR 即失败 |
| `deploy.yml` | push to `main` | `validate.py` → `build.py` → 部署 `site/` 到 GitHub Pages |

### 人工闸门 ⑦
- [ ] 上面的目视验收全过
- [ ] `site/` **不入库**（检查 `.gitignore`）—— 构建产物不进版本历史
- [ ] 提交信息用祈使句 + 范围前缀（CONTRIBUTING §4），如 `6.824: 讲解 Lecture 3 主从复制`
- [ ] 发布范围只含 `approved` 的讲座

---

## 9. 可直接粘贴的 Agent 提示词

> 用法：把 `<尖括号>` 换成真实值。提示词里已经内联了硬约束 —— **不要删减约束段**，它们对应 `validate.py` 的 ERROR 类。

### 9.1 建术语表（阶段 ③）

```text
你是 CourseLingo（译课 AI）的术语工程师。任务：为课程《<课程中文名>》（course.id = <id>）建立术语表首版。

先读：docs/pipeline-spec.md §3（字段契约）、docs/content-policy.md、.github/CONTRIBUTING.md §1。

硬约束：
1. 产出只能是 TOML 的 [[term]] 列表，字段仅限 en / zh / aliases / notes。不得新增字段（尤其不要写 key 字段）。
2. 术语来源只能是课程官方材料（大纲、讲座列表、页面标题）。不得凭记忆编造官方术语。
3. 只输出术语条目，不得输出任何英文原文段落、幻灯片内容或视频内容。
4. 业界有通行译法的优先沿用（consensus → 共识，replication → 副本）；无通行译法的保留英文并在 notes 写明「无通行译法，暂译 X」。
5. 同一概念只能有一个 en；复数与异体写进 aliases。正文标记 key 由 en 派生（小写、空格转连字符：leader election → [[term:leader-election]]），所以 en 里不要用括号、斜杠等符号。

执行步骤：
1. 列出该课程的高频术语概念，目标 60–100 条，至少覆盖前 3 讲。
2. 每条给出 en / zh / aliases / notes（notes 只在有歧义时写）。
3. 自查：en 是否唯一（大小写不敏感）、zh 是否为空、是否存在「同一概念两个 key」。
4. 输出可直接粘贴进 glossary.toml 的内容，并附一节「分歧清单」：你拿不准的 5 条，逐条给候选译法与理由。

不要做：不要给整段翻译；不要新增 TOML 字段；不要改动已有术语的 zh（如认为有误，单独列在「建议变更」并说明理由）。
```

### 9.2 写一篇讲解（阶段 ④）

```text
你是 CourseLingo（译课 AI）的讲解作者。你写的是**原创中文讲解**，不是翻译。

任务：为 <course.id> 第 <lecture> 讲《<讲座中文标题>》产出 content/<NN>-<slug>/index.md。

先读：glossary.toml（必须遵守）、本讲座骨架的 front matter、docs/content-policy.md、docs/brand.md。

硬约束：
1. 本课程 license.verified = <true|false>。为 false 时 output_mode 只能是 "explanation"：禁止逐句对照翻译，禁止在正文保留英文原句或整段英文。
2. 术语：正文出现每个已冻结术语时，用 [[term:<key>]] 标记，key 由 glossary 的 en 派生（小写、空格转连字符，如 leader election → [[term:leader-election]]）；不要用中文替代词绕过标记，也不要直接写英文原词。
3. 不转载：不得复制源材料的句子、幻灯片、图片、题面。用你自己的话讲。
4. 每个代码块的关键行必须有中文注释；代码块保持短小（单块 ≤ 400 字符，超长就拆分并用正文文字承接）。
5. 不得出现成段的英文散文（「几乎全为 ASCII 且长度 > 400 字符」的段落会 ERROR；围栏代码块不受此限，但也不要整段照抄）。

front matter（8 字段全填，值域见 spec §4）：
title / lecture = <N> / slug = "<slug>" / status = "draft" / source_kind = "<notes|video|textbook|other>" /
source_url = "<官方 URL>" / source_title = "<原标题>" / output_mode = "explanation"

正文结构：
- 读者画像与前置知识（1 段）
- 概念前置：本讲依赖、但原文默认读者已知的背景
- 主线推导：不跳步，把中间过程写出来
- 代码 / 伪代码走查：逐行中文注释解释「为什么这么写」
- 小结：3–7 条要点 + 常见误解
- 溯源：结尾列出本讲对应的原文位置（讲座号 / 时间戳 / 页码 / 章节名）

输出：一个完整的 index.md，然后附一张自查表（逐项 pass/fail，fail 的给出修改）。
```

### 9.3 自审草稿（阶段 ④ 收尾 / ⑤ 之前）

```text
你是 CourseLingo 的复核者。**只评审，不改文件。**

输入：content/<NN>-<slug>/index.md、glossary.toml、docs/pipeline-spec.md §4/§5/§6、.github/CONTRIBUTING.md §2、docs/brand.md。

逐项判定 pass/fail，每条给出「行号 + 原句 + 最小修改建议」：

A 契约层
 1 front matter 8 字段齐全；lecture 与 slug 全课程唯一；source_url 非空
 2 output_mode 与 license.verified 不冲突
 3 每个 [[term:key]] 的 key 都在 glossary 中存在（列出不存在的 key）
 4 正文出现的每个 glossary en 原词都已打标记（列出漏标的词与行号）
 5 无「几乎全为 ASCII 且 > 400 字符」的段落（列出可疑段落的首 40 字符与长度）

B 质量层
 6 概念前置：列出需要补背景的位置（未解释的默认已知前提）
 7 推导可见：列出跳步点（「因此 / 显然 / 可得」却没有中间步骤的地方）
 8 代码有注释：每个代码块关键行有中文注释；单块 ≤ 400 字符
 9 可溯源：结尾有原文位置
 10 术语一致性：同一概念是否全文同一中文词（列出漂移）
 11 语气：像助教不像营销号；无「全网最全 / 颠覆 / 封神」；面向读者用「你」
 12 授权边界：有无逐句改写痕迹、整段英文原句、图片或幻灯片复制

输出格式：
- 一张表：编号 / 判定 / 证据行号 / 修改建议
- 最后一节「必须修改才能进入 reviewed 的项」

禁止：不要重写全文；不要修改 glossary.toml；不要用「再打磨一下」这类不可执行的评语。
```

---

## 10. 质量基线（`reviewed` 的准入门槛）

| 维度 | 可检验的标准 | 检查方式 |
| --- | --- | --- |
| **概念前置** | 读者不看英文原文也能读懂；原文默认已知但本讲依赖的背景已补 | 找一段「直接开始用某个未解释概念」的地方，若存在则 fail |
| **推导可见** | 关键推导有中间过程；每个「因此 / 显然 / 可得」都能追溯到上一步 | 全文搜这些词，逐个回溯 |
| **代码有注释** | 每个代码块的关键行有中文注释；单块保持短小（≤ 400 字符为可读性基准） | 目视 + 字符计数 |
| **可溯源** | 结尾给出讲座号 / 时间戳 / 页码 | 有即 pass，无即 fail |
| **术语一致性** | 同一概念全课程同一中文词；正文出现的 glossary 词汇都已打 `[[term:]]` | 抽 5 个术语全文搜索；`validate.py` 的 WARN 7 归零或已解释 |
| **语气** | 像助教；承认复杂；不吹牛；用「你」不用「用户 / 学员」 | 搜禁用词：全网最全 / 颠覆 / 封神 / 用户 / 学员 |
| **授权边界** | 无逐句改写、无整段英文、无图片幻灯片复制 | ASCII 长段落检查 + 抽读 3 段自问「这是我们写的还是改写？」 |

**验收口径**（对齐 ROADMAP Phase 1）：**读者能不看英文原文读懂该讲，且术语零冲突。**

---

## 11. 常见失败模式

| 失败模式 | 症状 | 根因 | 预防 / 修法 |
| --- | --- | --- | --- |
| **术语漂移** | 同一概念前后用词不同（`leader` 一处「领导者」一处「主节点」） | 边写边定术语；不同讲座由不同 Agent 并行写却没喂同一份 glossary | 阶段 ③ 冻结；并行时**每讲都必须投喂同一份冻结 glossary**；`validate.py` WARN 7 归零 |
| **翻译而非讲解** | 一篇读起来是「中英对照」，句子结构与英文一一对应 | 把任务理解成「翻译」而不是「讲懂」 | 提示词里写死「原创中文讲解」；复核时抽读 3 段自问来源；禁止正文保留英文原句 |
| **转载原文** | `validate.py` ERROR 6；仓库里出现长英文段落 | 图省事直接粘贴源材料当「引用」 | 引用只给 URL 与位置，不给文本；长英文段落一律删掉重写 |
| **跳过授权闸门** | 有人把 `output_mode` 改成 `transcript`「先做着」 | 认为「公开可访问 = 可以自由改编」 | 阶段 ② 双人闸门；把 `validate.py` exit 1 当红线；记住「未声明许可 = 保留所有权利」 |
| **讲座过长** | 一篇讲座远超课堂讲得完的量，读者读不完 | 把整章教材塞进一讲；没有小节边界 | 一讲 = 一次课（或一个小节）。超长就拆成两讲，各自有独立 `lecture` / `slug`；拆完重跑 `validate.py`（`lecture` 要重编号且唯一） |
| **front matter 缺字段** | `validate.py` ERROR 3 | 手写骨架时漏了 `source_url` | 用 `new_lecture.py` 生成骨架再填，不要手搓 |
| **`slug` / `lecture` 撞车** | ERROR 3，并行写两讲时最常发生 | 多个 Agent 各自分配编号 | 开工前由一人**先分配编号表**，再分发任务 |
| **术语标记漏打** | WARN 7 刷屏 | 用中文替代词写了术语，没打 `[[term:]]` | 每讲自查清单第 6 项；WARN 7 不允许「忽略」 |
| **静默改术语** | 某讲里的中文词与 glossary 不一致，且 glossary 被改了 | 认为「我的译法更好」就直接改 | 开 issue 说明理由；术语改动需两名维护者（CONTRIBUTING §1/§3） |
| **代码块照抄无注释** | 代码块直接来自课件，无中文注释 | 把代码当「事实」而非「要讲的内容」 | 每个代码块关键行加中文注释解释「为什么」；保持短小并拆分 |
| **`site/` 进版本库** | 构建产物出现在 diff 里 | `.gitignore` 缺项 | 确认 `site/` 已忽略；发布只推源码 |
| **凭空发明接口** | 出现 spec 里没有的命令参数或 TOML 字段 | 想当然 | 只有 `validate.py` / `build.py` 的 CLI 是冻结的（§7）；其余脚本参数先查 spec，没有就进 §14 |
| **`default_mode` 与逐讲 `output_mode` 不一致** | 闸门判定含糊 | spec 未定义优先级（§14-3） | 闸门判定**以逐讲 `output_mode` 为准**（spec §6.2 就是这么查的）；保持 `default_mode = "explanation"` 直到阶段 ② 给出结论 |

---

## 12. 成本与规模化

### 批次
- **术语表先覆盖未来 3 讲的量**（60–100 条），不要一次抽全课程的术语 —— 后面一定会改。
- 正文按 **3–5 讲一批**推进：一批内的讲座共享同一份冻结 glossary，写完统一跑一次 `validate.py` 再进复核。
- 首批范围对齐 ROADMAP Phase 1：MIT 6.5840 / 6.824 的 Lecture 1–3。

### 可以并行（用 subagent）
| 工作 | 并行度 | 前提 |
| --- | --- | --- |
| 不同讲座的**正文初稿** | 每讲一个 subagent | glossary 已冻结且在本批内不变 |
| 同一讲的「正文」与「配图」 | 2 路 | 图的分工在写作前定好（哪些小节要图） |
| 第 N 讲的自审 与 第 N+1 讲的初稿 | 2 路 | 自审的输出只影响第 N 讲 |
| 不同讲座的**复核** | 每讲一个复核者 | 复核者与作者**不同**（自审不能替代复核） |

并行时每个 subagent 的输入必须完全相同地包含：**冻结 glossary 全文 + 同一份提示词（§9.2）+ 本讲编号/slug**。

### 必须串行
| 工作 | 为什么 |
| --- | --- |
| 阶段 ② 授权核实 | 全局闸门，结论决定所有讲座的 `output_mode` |
| 阶段 ③ 术语冻结 | 它是并行的前提 |
| **glossary 的任何变更** | 会让所有已产出讲座的 WARN 结果失效 → 变更后**全课程重跑** `validate.py` |
| 讲座编号 / slug 分配 | 多路并行下唯一性靠事前分配，不能靠事后查重 |
| `validate.py` → 复核 → `build.py` | 顺序不可颠倒：没校验的稿子复核是浪费 |
| `build.py` 与发布 | 构建产物是全局的 |

### 成本控制
- **一次只投喂一讲的源材料**，不要把整门课的上下文塞进去。
- 用 `glossary.toml` 作为固定前缀（对 prompt 缓存友好，也保证术语一致）。
- 先产出「大纲 + 本讲术语命中清单」，确认后再写正文 —— 比写完再返工便宜。
- 自审用同一模型即可；复核用不同模型或不同人，避免同源盲区。

---

## 13. 每讲一页的速查

```bash
# 1. 建骨架
python scripts/new_lecture.py

# 2. 写 index.md（front matter 8 字段 + 原创中文讲解 + [[term:key]]）

# 3. 校验
python scripts/validate.py          # 0=通过 1=有ERROR 2=用法/IO错误

# 4. 本地看效果
python scripts/build.py --out site

# 5. 复核通过后把 status 推到 reviewed / approved

# 6. 发布（CI 会做，本地仅验证）
python scripts/build.py --out site --base-url /<repo>/
```

---

## 14. 待决事项（spec 缺口）

> 以下都是**冻结契约未定义**、而执行中确实会撞到的问题。**在 spec 补齐之前，按「本手册的临时约定」执行，并保持与 spec 不冲突**；不要在多处各自发明不同做法。
>
> 第 10–14 项是**对照当前实现（`template/scripts/`）核对后发现的 spec 缺口或分歧** —— 实现可能仍在演进，遇到不一致时**以 spec 为准并回报**。

| # | 缺口 | 影响 | 临时约定 |
| --- | --- | --- | --- |
| 1 | `new_course.py` / `new_lecture.py` 的 **CLI 未定义**（spec §1 只给脚本名与作用）；且 spec §1 把 `new_course.py` 画在**课程仓库内**，而实现放在**平台主仓库** `scripts/` 下 | 无法从 spec 写出确定的开工命令 | 按实现的 `--help` 为准（已记录于 §2/§5）；若行为与 §1 结构不符，**按 spec §1/§2/§3/§4 手工建目录与文件**。绝不臆造参数 |
| 2 | `validate.py` 的 **CLI 未定义**（只冻结了退出码） | 无法「只校验单篇」；大仓库全量跑变慢 | 统一全量 `python scripts/validate.py`。实现另有 `--root` / `--quiet`，属实现细节（见 §14-11） |
| 3 | `[output].default_mode` 与逐讲 `output_mode` 的**优先级未定义** | 授权闸门判定口径含糊 | 闸门判定**以逐讲 `output_mode` 为准**（spec §6.2 即如此检查）；`default_mode` 在阶段 ② 出结论前恒为 `explanation` |
| 4 | `[license]` 只有**一个** `verified` 布尔，而 content-policy 要求**分材料类型**核实（笔记 / 视频 / 作业 / 教材许可可能各不相同） | 无法在 `course.toml` 表达「笔记已授权但视频未授权」 | 在 PR 描述与 `docs/licensing-research-log.md` 中**分类型**记录；`verified = true` 只在「本课程要用的**全部**材料都已核实」时才置位 |
| 5 | 讲座 **front matter 无复核人 / 复核日期字段**（spec §4 已冻结字段） | 复核证据无处存放 | 用 PR 描述 + `status` 字段承载（CONTRIBUTING §3 已要求 PR 写明授权依据与术语变更）；不新增 front matter 字段 |
| 6 | **ASCII 长段落探测的判定细节未定义**（阈值、是否豁免代码块、是否剥离 Markdown 标记） | 合法代码块可能被误判，或作者不清楚什么会被拦 | 当前实现：`>400 字符` 且 `ASCII ≥ 90%` 且 `空格 ≥ 40` 才算可疑，且**跳过围栏代码块 / 标题 / 表格行**、判定前剥离行内代码与链接。**建议 spec 补齐这些细节**；本手册仍要求代码块加中文注释并保持短小（可读性 + 保守） |
| 7 | 一个讲座只有**一个** `source_url` / `source_title` / `source_kind` | 多源讲座（笔记 + 视频 + 教材）无法如实署名 | 填**主讲**来源，其余来源在正文「溯源」小节列出；如长期需要多源，提请 spec 扩展 |
| 8 | 目录名 `content/<NN>-<slug>/` 与 front matter `slug` 的**一致性未被校验**（§6.3 只查 slug 唯一） | 目录名与 slug 不一致时站点 URL 与目录错位 | 人工检查：目录名 `<NN>` 用两位补零，`<slug>` 与 front matter 完全相同 |
| 9 | `course-diagram` 的**产出契约未定义**（SVG 尺寸 / 命名 / alt 文本 / 是否内联） | 配图风格与可访问性靠自觉 | 图放 `content/<NN>-<slug>/figures/<slug>-<n>.svg`；正文用 `![<中文说明>](figures/...)`，alt 文本必须写 |
| 10 | **多词术语的标记 key 派生规则未定义**（spec §5 只给单词示例 `[[term:replication]]`） | 作者可能写成 `[[term:leader election]]` → ERROR；key 写法全凭猜 | 当前实现的规则：`key = en 小写化、空白与下划线转连字符、去掉其他非 [a-z0-9.-] 字符`（`leader election` → `leader-election`）。**建议写入 spec §5**；正文统一用小写 key |
| 11 | **同一实现的多个 CLI / 字段超出冻结 spec** | 契约与实现漂移，消费方按 spec 写会失败或按实现写会与 spec 冲突 | 已观察到的分歧：① `validate.py` 有 `--root` / `--quiet`；② `build.py` 有 `--root`，且 `--base-url` 默认 `"./"` 而 spec §7 写 `/`；③ `validate.py` 实际要求 `[course]` 多填 `institution` / `source_language` / `target_language`（spec §2 只标 3 个必填）；④ `source_kind` 实际接受 `slides`（spec §4 只有 4 个值）；⑤ `source_title` 实际不是必填；⑥ glossary 实际支持 spec §3 未定义的 `key` 字段。**本手册一律按 spec 写**；分歧请回报给脚本维护者，由 spec 定夺 |
| 12 | **`content/` 下没有任何讲座时 `validate.py` 报 ERROR** | 新生成的空课程仓库跑校验会 exit 1，容易被误判为配置错误 | 阶段 ① 只要求「除『没有任何讲座』外无其他 ERROR」；建好第一讲骨架后再跑一次应当 exit 0。**建议 spec §6 明确这一条**（要么列入 ERROR，要么允许空课程） |
| 13 | `build.py` 对 `status = "draft"` 的讲座**是否发布**未定义（§6 WARN 8 只说会标注「草稿」） | 可能把草稿推到线上 | **发布闸门靠人工**：只发布 `approved` 的讲座，不依赖 `build.py` 过滤 |
| 14 | spec §9 规定首批 **5** 个 skill（含 `course-diagram`），但本手册只覆盖 4 个（`course-diagram` 由其他产出负责） | 交叉引用可能指向尚不存在的 skill | `course-explain` 中「交给 `course-diagram`」的引用在 `skills/course-diagram/SKILL.md` 落地前，暂时手绘 SVG 按 §14-9 的约定存放 |
