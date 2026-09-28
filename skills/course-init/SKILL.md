---
name: course-init
description: Bootstrap a new CourseLingo course repository from the template — course metadata, the license-verification gate and how to record evidence, glossary seeding, and the first lecture skeleton. Use when starting a new course, setting up course.toml or glossary.toml, verifying a course license, or before any lecture content is produced.
---

# course-init · 课程立项与授权核实

把一个还没开始的课程，变成**可开工、且授权有据**的仓库骨架。

**本 skill 不产出任何讲座正文。** 正文属于 `course-translate` / `course-explain`。

## 前置阅读（先读，再动手）

| 文件 | 你从中取什么 |
| --- | --- |
| `docs/pipeline-spec.md` §1/§2/§3/§4 | 目录结构、`course.toml`、`glossary.toml`、front matter 的**冻结字段** |
| `docs/content-policy.md` | 9 项逐课程复核清单、署名规范、下线机制 |
| `docs/course-catalog.md` | 课程是否已登记、待抓取 URL 清单、记录格式表 |
| `docs/licensing-research-log.md` | 已发起过的核实动作与结论（当前：**全部未核实**） |
| `docs/SOP.md` §2/§3/§4 | 阶段 ①–③ 的完整流程与闸门 |

---

## 步骤 1 · 确认课程已登记

`docs/course-catalog.md` 里**必须已有这门课**。没有就先加一行（课程、学校、主题、语言、授权状态、官方入口）。

**不要在 catalog 之外另开课程** —— 否则课程 id、中文名会各处不一致。

## 步骤 2 · 生成仓库骨架

```bash
# 注意：在【平台主仓库】根目录执行；它从 template/ 生成一个新的课程仓库
python scripts/new_course.py --id mit-6.5840 --out ../courses/mit-6.5840 \
    --title "Distributed Systems" --title-zh "分布式系统" \
    --institution MIT --course-number "6.5840 / 6.824" \
    --homepage "https://pdos.csail.mit.edu/6.824/"
```

默认会移除模板自带的演示讲座；`--keep-demo` 可保留演示内容（用于验证流水线）。

> ⚠️ spec §1 把 `new_course.py` 画在**课程仓库内**，并把 CLI 留空；当前实现把它放在**平台主仓库**的 `scripts/` 下，用 `--out` 指定课程仓库位置。
> **参数以 `--help` 为准，不要臆造。** 若行为与本节不符，按 spec §1 手工建：

```
course.toml
glossary.toml
content/
scripts/          # new_lecture.py / validate.py / build.py
```

## 步骤 3 · 填 `course.toml`（严格按 spec §2，不加字段）

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
verified = false                  # ★ 授权闸门，见步骤 4
terms = ""
evidence_url = ""
checked_at = ""
allows_commercial = false
allows_derivatives = false
share_alike = false
notes = ""

# 可选但推荐：按材料类型逐项核实（「笔记已授权」不等于「视频也已授权」）。
# 一旦存在 [license.materials]，闸门就只认它，不再看上面的 verified（spec §2）。
# 没逐项核实过就【不要】加这个表 —— 别用一堆 false 假装核实过。
# [license.materials]
# notes = false
# video = false
# textbook = false
# other = false

[output]
default_mode = "explanation"
```

规则：
- `title_zh` 用课程**通用中文名**，不造品牌名。
- `homepage` 填**官方**入口，不填镜像或聚合站。
- `[output].default_mode` 在步骤 4 出结论前**恒为 `explanation`**。
- 缺 `id` / `title` / `title_zh` 任一 → `validate.py` exit 1。
- **当前实现比 spec 更严**：`validate.py` 还要求 `institution` / `source_language` / `target_language` 非空（spec §2 只把前三个标为必填）。
  所以**全部填上**，一次到位。详见 `docs/SOP.md` §14-9。

```bash
python scripts/validate.py    # 此时会报「没有任何讲座」→ exit 1，属预期（见下）
```

⚠️ **新建的空课程仓库还没有讲座，校验会因「没有任何讲座」而 exit 1 —— 这是预期的。**
（spec §6 的 ERROR 清单里没有这一项；当前实现会这么报。详见 `docs/SOP.md` §14-10。）

所以本步骤只要求：**除「没有任何讲座」之外没有其他 ERROR**（尤其是 `[course]` 必填字段相关的）。
建好第一讲骨架（步骤 6）后再跑一次，那时应当 **exit 0**。

---

## 步骤 4 · 授权核实（★ 最硬的闸门）

**这一步没有命令可跑。** spec 不提供、也不应有「核实授权」的脚本 —— 授权是**读原文并记录**的人工动作。用记忆或推测填 `terms` 比留空**更危险**。

### 4.1 实际访问并按材料类型分别核实

content-policy 要求**逐类型**确认，因为许可可能不同：

| 材料类型 | 必须确认 |
| --- | --- |
| 讲座笔记 / 幻灯片 | 条款、是否允许衍生、是否 ShareAlike |
| 讲座视频 | **可能与课件不同**，且叠加视频平台条款 |
| 作业 / Lab 题面与答案 | 著作权 + 学术诚信；**答案默认无授权** |
| 教材（如有） | 独立作品，另有条款 |
| 课程 reuse / citation 声明 | 署名要求的具体形式 |

逐字摘录许可文本 + 记录访问日期。**不可达就写「不可达」，不得推断。**

### 4.2 两个必须避开的陷阱

1. **MIT OCW 的许可极易记错。** 其中的 `NC`（非商业）与 `SA`（相同方式共享）直接决定「能否商用」和「翻译改编是否被允许」—— 必须读官方 terms 原文。
2. **6.824 / 6.1810 的讲座笔记历史上没有声明许可。**「未声明」的法律状态是**保留所有权利**，与宽松开源许可完全不同。课件公开可访问 ≠ 可以自由改编。

### 4.3 证据记录到三处

| 位置 | 填什么 |
| --- | --- |
| `course.toml` `[license]` | `terms`（原文照抄的条款名）/ `evidence_url` / `checked_at`（ISO 日期）/ `allows_commercial` / `allows_derivatives` / `share_alike` / `notes` |
| `course.toml` `[license.materials]` | **逐项核实过的**类型填 `true`（`notes` / `video` / `textbook` / `other`） |
| `docs/course-catalog.md` | 《记录格式》表一行，含**原文引用**与访问日期 |
| `docs/licensing-research-log.md` | 核实表对应的行 |

#### 授权闸门的判定顺序（spec §2）

```
1. 若 [license].materials 存在 → 只看 materials[该讲座的 source_kind] 是否为 true
2. 否则                       → 退回 [license].verified
```

**一旦你填了 `[license.materials]`，闸门就只认它，`verified` 被忽略。**

- 好处：能准确表达「笔记已授权、视频未授权」—— 许可常按材料类型不同。
- 风险：**没逐项核实过就不要写 `materials`**，让它退回 `verified` 总开关。
  **别顺手加一个全 `false` 的表**，那会让人以为已经逐项核实过，或把闸门莫名收紧。
- ⚠️ **作业 / Lab 答案不属于这四个类型中的任何一个**：作业答案翻译是**永久排除项**，不是开关。不要塞进 `other`。

### 4.4 `verified = true`（或 `materials[<kind>] = true`）的四条前置（缺一不可）

- [ ] `terms` 非空，且是原文照抄
- [ ] `evidence_url` 非空，且**复核者本人真的打开过**
- [ ] `checked_at` 为 ISO 日期
- [ ] `allows_derivatives` 已明确判断（翻译属于衍生作品）

> 用 `materials` 时，四条前置**按类型分别满足**：`materials.video = true` 需要的是**视频**的条款证据，不能拿笔记的条款来顶。

### 4.5 闸门的后果

| 授权状态 | 允许的 `output_mode` |
| --- | --- |
| 该项为 `false`（或 `verified = false` 且无 `materials`） | **只有 `explanation`** —— 写我们自己的原创中文讲解 |
| 该项为 `true` | `explanation` 或 `transcript`，且仅限**已核实授权的那种材料** |

即便某项已核实为 `true`：
- **视频字幕翻译**仍默认关闭（平台条款叠加）
- **作业答案翻译永久排除**

`validate.py` 会在「存在 `transcript` 讲座 + 该讲座 `source_kind` 对应的授权不为 `true`」时 **exit 1**。
这是**事后报警器**，不是流程的替代品 —— 被拦住意味着前面已经白做且产生了侵权风险。

### 人工闸门（双人签字）

- [ ] 证据由**第二人独立复核**（自己再看一遍不算复核）
- [ ] 判定只依据 `evidence_url` 的原文，不依据「大家都这么用」
- [ ] **按类型分别签字**：`materials.notes = true` 推不出视频也能用
- [ ] 分清材料类型；部分材料未核实 → 该项为 `false`
- [ ] 未核实 → 结论就是 `false`，**照常开工讲解，不照常开工翻译**

---

## 步骤 5 · 术语表播种（术语先行）

术语表是项目**核心资产**，独立于模型。目标是首版 **60–100 条**，覆盖已排期的前 3 讲。

严格按 spec §3：

```toml
[[term]]
en = "replication"
zh = "副本"
aliases = ["replica", "replicas"]
notes = "此处指数据副本机制"
```

| 字段 | 规则 |
| --- | --- |
| `en` | 必填、非空、**唯一（大小写不敏感）** |
| `zh` | 必填、非空 |
| `aliases` | 收复数与异体（`replica` → 进 `replication` 的 aliases） |
| `notes` | 只在有歧义时写 |

### 标记 key 怎么来（写正文时最容易错的一处）

spec §3 定义了 key 推导规则：**`key` 默认由 `en` 生成 —— 转小写、空格与下划线转连字符、去掉其他非法字符**。
正文标记必须用 **key**，不是 `en` 原文。

| `en` | 正文里必须写 |
| --- | --- |
| `replication` | `[[term:replication]]` |
| `leader election` | `[[term:leader-election]]` |

`en` 里不要写**括号、斜杠、逗号** —— 它们会在派生时被去掉，导致作者按 `en` 猜的 key 和实际 key 对不上。
正文写 `[[term:leader election]]`（带空格）会 ERROR：key 不存在。
需要与 `en` 不同的 key 时，按 spec §3 显式写 `key = "..."`（可选字段，一般用不到）。
同一课程内 **key 也必须唯一**（重复即 ERROR）。

> 想展示「标记怎么写」时，把它放进**行内 code**（`` `[[term:key]]` ``）或 **HTML 注释**（`<!-- -->`）——
> spec §5 明确这两种情况**不算真实引用**，不会被判 ERROR。

译法决策：
- 业界有通行译法 → **优先沿用**（`consensus` → 共识）
- 无通行译法 → 保留英文并在 `zh` / `notes` 给出译名
- 一词多义（如 `thread`）→ 每个义项一个条目，用 `notes` 区分；**禁止同 key 两译**
- 想改已有译法 → **开 issue 说明理由，不静默改动**（CONTRIBUTING §1）

生成术语表的提示词见 `docs/SOP.md` §9.1。

### 冻结

- [ ] 每条 `en` 唯一、`zh` 非空
- [ ] 没有「同一概念两个 key」（`replica` 与 `replication` 要分清）
- [ ] 都是**真术语**，不是普通词
- [ ] `python scripts/validate.py` **exit 0**
- [ ] PR 描述写明 **「glossary frozen @ `<commit short sha>`」**

冻结后：新增术语走同样流程（**两名维护者**确认）；**任何 glossary 变更后必须全课程重跑 `validate.py`**（旧讲座的 WARN 结果会失效）。

---

## 步骤 6 · 第一讲骨架

```bash
python scripts/new_lecture.py
```

产出 `content/<NN>-<slug>/index.md`，front matter **8 个字段全填**（spec §4）：

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

- `lecture` / `slug` **全课程唯一**；多路并行前先由一人**分配编号表**
- 目录名 `<NN>-<slug>` 与 front matter `slug` 保持一致（spec 未校验此项，靠人工）
- `slug` 只允许小写字母、数字与连字符（当前实现会校验格式）
- `source_kind` 按 spec §4 只用 `notes` / `video` / `textbook` / `other`
  （当前实现额外接受 `slides`，但 spec 未定义该值，见 `docs/SOP.md` §14-9）
- `output_mode` 与步骤 4 的结论一致
- 配图目录 `content/<NN>-<slug>/figures/`（需要图时走 `course-diagram`）

```bash
python scripts/validate.py
```

---

## 完工检查

- [ ] 课程已在 `docs/course-catalog.md` 登记，id / 中文名一致
- [ ] `course.toml` 三个必填字段齐全，`default_mode = "explanation"`
- [ ] `[license]` 每个字段都有据可依；无据则留空且 `verified = false`
- [ ] 若逐项核实过，`[license.materials]` 与证据一致；**没核实过就别写这个表**
- [ ] 证据落到了三处（toml / catalog / research-log），含原文引用与访问日期
- [ ] `glossary.toml` 60–100 条，`en` 唯一、**key 唯一**，PR 中有冻结声明
- [ ] 第一讲骨架存在，front matter 8 字段齐全，`lecture` / `slug` 唯一
- [ ] `python scripts/validate.py` **exit 0**
- [ ] **仓库里没有任何课程原料**（PDF / 视频 / 逐字稿 / 幻灯片）
- [ ] 下一步：正文交给 `course-translate` + `course-explain`

## 不要做

- ❌ 凭记忆或推测填 `[license]` 的任何一个字段
- ❌ 在 `verified = false` 时把任何讲座设成 `output_mode = "transcript"`
- ❌ 新增 spec 未定义的 `course.toml` / `glossary.toml` / front matter 字段
- ❌ 把英文原文、课件、视频、作业答案写进仓库
- ❌ 在 glossary 冻结前开始写正文
