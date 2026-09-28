# 操作手册 · SOP（从零到一篇已发布讲座）

> **本手册的位置**：[pipeline-spec.md](./pipeline-spec.md) 是**冻结的接口契约**，本手册是**执行手册**。
> 两者冲突时，以 spec 为准；本手册不新增、不修改任何接口。若发现 spec 有缺口，写进本文 [§14 待决事项](#14-待决事项spec-缺口)，**不要私自发明约定**。
>
> 适用对象：驱动 Agent 干活的人（或 Agent 自己）。
>
> **命令的执行位置**：阶段 ① 的 `new_course.py` 在**平台主仓库**根目录执行（它负责**生成**课程仓库）；其余命令（`new_lecture.py` / `validate.py` / `build.py`）都在**课程仓库**根目录执行。

---

## 0. 四条不变量（任何阶段都不得违反）

| # | 不变量 | 机器兜底 | 违反的后果 |
| --- | --- | --- | --- |
| 1 | **授权优先**：`course.toml` 的 `[license].verified != true` 时，禁止产出 `output_mode = "transcript"` | `validate.py` 硬失败（exit 1） | 侵权。这是项目最大的敌人，比翻译质量更能决定生死 |
| 2 | **术语先行**：术语在写正文**之前**冻结；同一概念全课程同一个中文词 | `[[term:key]]` 引用不存在 → ERROR；glossary 的 `en` 出现在正文却没打标记 → WARN | 术语漂移，全课程返工，核心资产作废 |
| 3 | **不转载**：不把英文原文、幻灯片、视频、作业答案写进仓库 | 「几乎全为 ASCII 且 > 400 字符」的段落 → ERROR | 仓库变成原课程的复制品，授权风险最高 |
| 4 | **论文逐篇授权**：论文的授权与课程授权**完全无关**；`output_mode = "translation"` 必须 `verified = true` **且** `allows_translation = true` | `validate.py` 硬失败（exit 1）；`build.py` 另有**第二道独立闸门**（同样 exit 1，且**不产出任何站点**） | 发布我们无权翻译的论文全文。这比不变量 1 更容易发生 —— 同一门课的论文来自不同出版社，条款各不相同 |

**默认产出永远是「原创中文讲解」，不是翻译。** 逐句翻译 / 字幕 / 作业答案翻译是**默认关闭**的能力，开启它需要该课程该**材料类型**的书面授权。

**论文同理，而且更严。** 论文的默认产出是**我们自己写的导读**（`output_mode = "guide"`，**不设闸门** —— 思想与概念不受著作权保护）；全文翻译（`output_mode = "translation"`）必须**逐篇**拿到明确许可。课程授权再宽松，也推不出论文授权 —— 这是本项目最容易犯、后果最直接的一类错误。

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

论文（经典论文课的另一半）走一条**并行轨道**，入口在 ② 授权核实，闸门独立：

```
②P 论文登记 ──► ②Q 逐篇授权核实（★闸门）──► ④P 逐篇产出（guide 默认 / translation 需闸门）
  papers.toml      verified + allows_translation              │
                                                             ▼
                                          ⑤ 校验（同一个 validate.py；ERROR 8–11）
                                                             │
                                                             ▼
                                          ⑥P 人工复核（★闸门，双人签字）
                                                             │
                                                             ▼
                                          ⑦P 发布（site/papers/<key>/index.html）
```

> 论文轨道的**详细流程在阶段②（§3 的 ②P/②Q）、阶段④（§5 的论文产出）、阶段⑤（§6）、阶段⑥（§7 的 ⑥P）** 里，与讲座轨道同一处展开，不再另设章节。

| # | 阶段 | 命令 | 主输入 | 主输出 | 人工闸门 | 可并行 |
| --- | --- | --- | --- | --- | --- | --- |
| ① | 课程立项 | `python scripts/new_course.py` | `docs/course-catalog.md` | `course.toml` / `glossary.toml` / `papers.toml` / `content/` / `scripts/` | 课程 id 与中文名已登记在 catalog | — |
| ② | 授权核实 | *（无脚本，人工动作）* | `docs/content-policy.md` 的 9 项复核清单 | `[license]` 字段 + 核实记录 | **双人签字**；未核实则保持 `verified = false` | ❌ 串行，全局闸门 |
| ②P | 论文登记 | *（无脚本，人工动作）* | 课程大纲 / 阅读清单里的原文入口 | `papers.toml` 的 `[[paper]]` 条目（授权字段先一律 `false`） | `key` 唯一且合规；`authors` 非空数组 | ✅ 论文之间可并行 |
| ②Q | 论文逐篇授权核实 | *（无脚本，人工动作）* | 论文页**原始 HTML** + 出版社的 permission 政策页 | `[paper.license]` 字段 + `docs/paper-licensing.md` 的结论行 | **★双人签字**（逐篇）；未核实保持 `verified = false`、`allows_translation = false` | ❌ 串行，逐篇闸门 |
| ③ | 术语表冻结 | `python scripts/validate.py` | 官方材料（运行时只读） | 冻结版 `glossary.toml` | 术语评审 + 冻结声明 | ❌ 串行 |
| ④ | 逐讲产出 | `python scripts/new_lecture.py` | 讲座骨架 + 冻结 glossary + 源材料 | `content/<NN>-<slug>/index.md`（`status="draft"`） | 无（草稿），但须过 §5 清单自查 | ✅ 讲与讲之间可并行 |
| ④P | 论文逐篇产出 | *（**没有**论文骨架脚本，手工建目录，见 §14-15）* | 该篇的 `papers.toml` 条目 + 冻结 glossary + 论文原文（运行时只读） | `content/papers/<key>/index.md`（`status="draft"`） | 无（草稿），但须过 §5 的导读 / 翻译清单自查 | ✅ 篇与篇之间可并行 |
| ⑤ | 校验 | `python scripts/validate.py` | 全部 `content/**/index.md`（含 `content/papers/<key>/index.md`）+ `papers.toml` + `glossary.toml` | exit code + ERROR/WARN 列表 | 无 | ✅ 可重复跑 |
| ⑥ | 人工复核 | `python scripts/validate.py` → `python scripts/build.py --out site` | 校验通过的 draft | `status = "reviewed"` → `"approved"` | **双人签字**（术语/授权改动） | ✅ 讲与讲之间可并行 |
| ⑥P | 论文人工复核 | `python scripts/validate.py` → `python scripts/build.py --out site` | 校验通过的论文页草稿 | `status = "reviewed"` → `"approved"` | **★双人签字**（授权判定 + 导读/译文边界；`translation` 的授权复核人须≠译者） | ✅ 篇与篇之间可并行 |
| ⑦ | 发布 | `python scripts/build.py --out site` | `approved` 讲座 | `site/`（不入库）+ CI 部署 | 目视验收 + 「非官方」声明检查 | ❌ 串行 |
| ⑦P | 论文发布 | `python scripts/build.py --out site` | `approved` 论文页 | `site/papers/<key>/index.html` + 侧栏「论文」分组 + 首页「经典论文」列表 | 目视验收 + **授权提示条**核对 | ❌ 串行 |

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

> ⚠️ **执行位置注意**：spec §1 把 `new_course.py` 画在**课程仓库结构里**，而当前实现把它放在**平台主仓库**的 `scripts/` 下，并通过 `--out` 指定课程仓库位置。同时其 CLI 参数**不在冻结 spec 中**（见 §14-1、§14-9）。
> 若脚本行为与本节不符，按 spec §1 手工建目录、按 §2/§3/§4 手工写 `course.toml` / `glossary.toml` / `index.md`。

### 输出
```
course.toml      # 按 spec §2 填 [course] / [license] / [output]
glossary.toml    # 空表，等待阶段 ③
papers.toml      # 论文登记表（模板自带），条目等待阶段 ②P
content/         # 空目录
scripts/         # new_lecture.py / validate.py / build.py
```

必填字段（缺一个 → `validate.py` exit 1）。
spec §2 只把 `id` / `title` / `title_zh` 标为必填；**当前实现要求更多**（见 §14-9）：

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

# 可选但推荐：按材料类型逐项核实（「笔记已授权」不等于「视频也已授权」）。
# 一旦存在 [license.materials]，授权闸门就只认它，不再看上面的 verified。
# 没逐项核实过就【不要】加这个表 —— 别用一堆 false 假装核实过。
# [license.materials]
# notes = false
# video = false
# textbook = false
# other = false

[output]
default_mode = "explanation"
```

### 验证
```bash
# 在【课程仓库】根目录
python scripts/validate.py
```

⚠️ **此时还没有任何讲座（也没有论文页），校验会报「没有任何内容」而 exit 1 —— 这是预期的，不是配置错误。**
（spec §6.6 已明确这一条：`content/` 下既没有讲座也没有论文页 → ERROR。新建的课程仓库**故意**停在这里。）

因此阶段 ① 的验证方式改为：

1. 先只确认 `course.toml` 能被解析、`[course]` 必填字段齐全 —— 把「没有任何内容」之外的其他 ERROR 清零。
2. 建好第一讲骨架（步骤见 §5 / `course-init`；第一篇论文页见 §5 的论文产出）后，再跑一次 `validate.py`，此时应当 **exit 0**。

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
2. **按材料类型分别核实** —— 这是 content-policy 的要求，spec §2 已提供对应的表达方式 `[license.materials]`：
   - `notes` —— 讲座笔记 / 幻灯片
   - `video` —— 讲座视频（**许可可能与课件不同**，还叠加平台条款）
   - `textbook` —— 教材（独立作品）
   - `other` —— 其他
   - ⚠️ **作业 / Lab 题面与答案不属于以上任何一项**：作业答案翻译是**永久排除项**，不是「核实了就能开」的开关（spec §2、content-policy）。不要把作业答案塞进 `other`。
3. 把结论写回三处：
   - `course.toml` 的 `[license]` 字段（`terms` / `evidence_url` / `checked_at` / `allows_commercial` / `allows_derivatives` / `share_alike` / `notes`），并按类型填 `[license.materials]`
   - `docs/course-catalog.md` 的《记录格式》表（含原文引用与访问日期）
   - `docs/licensing-research-log.md` 的核实表

`checked_at` 用 ISO 日期（如 `2026-02-14`）。

#### 授权闸门的判定顺序（spec §2，`validate.py` 的 `license_allows()`）

```
1. 若 [license].materials 存在 → 只看 materials[该讲座的 source_kind] 是否为 true
2. 否则                       → 退回 [license].verified
```

**一旦你填了 `[license.materials]`，闸门就只认它，`verified` 被忽略。** 两个后果必须记住：

- 好处：能准确表达「笔记已授权、视频未授权」—— 这正是本项目最容易误解授权的地方。
- 风险：**别顺手加一个全 `false` 的 `materials` 表**，那会在 `verified = true` 的情况下把闸门收紧到「什么都不许」，或让人以为已经逐项核实过。**没逐项核实就不要写 `materials`**，让它退回 `verified` 总开关。

### 输出
- `[license]` 字段全部有据可依；（若逐项核实过）`[license.materials]` 与之一致
- 核实表一行，含**原文引用**
- 明确结论：`verified` / `materials[<kind>]` 的取值各是什么

### `verified = true`（或 `materials[<kind>] = true`）的四条前置（缺一不可）
- [ ] `terms` 非空，且是**原文照抄**的条款名
- [ ] `evidence_url` 非空，且**复核者本人真的打开过**
- [ ] `checked_at` 为 ISO 日期
- [ ] `allows_derivatives` 已明确判断（翻译属于衍生作品，这一项决定整门课能不能做）

> 用 `materials` 时，这四条前置**按类型分别满足**：`materials.video = true` 需要的是**视频**的条款证据，不能拿笔记的条款来顶。

### 人工闸门 ②（双人签字）
- [ ] 证据由**第二人独立复核**一次（自己看一遍不算复核）
- [ ] 判定**只依据 evidence_url 的原文**，不依据「大家都这么用」「MIT OCW 应该是 CC BY-NC-SA」
- [ ] 特别注意两个陷阱：MIT OCW 的 **NC / SA** 条款极易记错；6.824 / 6.1810 的讲座笔记历史上**未声明许可** —— 未声明的法律状态是**保留所有权利**
- [ ] **按类型分别签字**：`materials.notes = true` 只能说笔记可以用，**推不出**视频可以用
- [ ] 即便某项已核实为 `true`：**视频字幕翻译**仍默认关闭（平台条款叠加）；**作业答案翻译永久排除**（著作权 + 学术诚信）
- [ ] 未核实 → 该项保持 `false`，对应讲座一律 `output_mode = "explanation"`，**照常开工讲解，不照常开工翻译**

### 机器兜底
```bash
python scripts/validate.py
```
只要存在任一 `output_mode = "transcript"` 的讲座而 `verified != true`，**exit 1**（spec §6.2）。
把这条当成**事后报警器，不是授权流程的替代品** —— 一个已经写好的逐字稿被拦下来，意味着前面全白做且已经产生侵权风险。

### 阶段 ②P / ②Q · 论文登记与逐篇授权核实（★ 又一道独立的闸门）

**论文的授权与课程授权完全无关。** 一门课是 CC BY 3.0 US，**推不出**它课表上的 MapReduce（USENIX）或 GFS（ACM）可以翻译。所以论文**不用**课程级布尔，而是每篇一个 `[paper.license]`（spec §10.1）。

#### ②P 登记：先登记，再写内容

读课程大纲 / 阅读清单，把**要做的论文先全列出来**，逐篇写进课程仓库根目录的 `papers.toml`：

```toml
[[paper]]
key = "mapreduce"                 # 必填，唯一；只允许小写字母、数字与连字符
title = "MapReduce: Simplified Data Processing on Large Clusters"
authors = ["Jeffrey Dean", "Sanjay Ghemawat"]   # 必填，非空数组（不要写成一个字符串）
venue = "OSDI 2004"               # 必填
year = 2004                       # 可选
publisher = "USENIX"              # 可选但强烈建议：决定去查谁的政策页
url = "https://..."               # 必填：论文的官方条目页（不是作者主页的 PDF）
pdf_url = ""                      # 可选（可以填，但不构成任何授权）

[paper.license]
verified = false                  # ★ 未核实就是 false，别猜
terms = ""
evidence_url = ""
checked_at = ""
allows_translation = false        # ★ 与 verified 相互独立，见 ②Q
allows_commercial = false
share_alike = false
notes = "未核实。核实方法与结论见 docs/paper-licensing.md"
```

登记阶段的纪律：

- **一律先写 `verified = false` / `allows_translation = false`** —— 先占位，核实结论在 ②Q 才写。
- `key` 一旦定下就不要再改：它同时是目录名 `content/papers/<key>/` 与站点 URL `site/papers/<key>/`。
- `authors` 必须是**非空数组**，不要写成一个字符串；`venue` / `url` 缺一个就 ERROR（spec §6.8）。
- `url` 填论文的**官方条目页**（USENIX / ACM DL / IEEE Xplore）；作者主页上的 PDF **不是**授权来源。
- `publisher` 不是必填，但它直接决定 ②Q 要去查谁的政策页 —— 填上，省事的是自己。
- 逐篇的结论汇总在 [paper-licensing.md](./paper-licensing.md)：它是**逐篇授权的权威来源**，`notes` 里指向它。

#### ②Q 核实：四步方法（spec §10.6，都是踩过的坑）

> **这一阶段没有命令。** 授权是**读原文并记录**的人工动作；用记忆填 `terms` 比留空**更危险**。

1. **抓原始 HTML，不要过滤标签后再搜文本。** 许可常常只是一个 `rel="license"` 属性或图片徽章的 `href`。本项目就因此误判过一次：6.824 主页的 CC BY 3.0 US 徽章**是纯图片链接、没有任何可见文字**，只扫文本会得出「未声明许可 = 保留所有权利」的相反结论（见 [course-catalog.md](./course-catalog.md)）。把原始页面落盘留证再搜。
2. **「能免费下载」≠「允许翻译」。** 作者把 PDF 挂在自己主页上**没有授予任何许可**，法律状态仍是保留所有权利。URL 可达 ≠ 有授权。
3. **查出版社政策，不只看论文页。** 多数经典系统论文的版权在 **ACM / IEEE / USENIX**。ACM 有**明确的翻译授权流程** —— 那意味着「默认不可翻译，须先申请」。论文页上没有许可声明时，下一步就是看出版社的 copyright / permissions 页。
4. **逐篇记录 `evidence_url` 与 `checked_at`。** 无法核实的保持 `verified = false`，在 `notes` 写「未确认」，**不要推测**。

⚠️ **同一篇论文的「会议版 / 技术报告 / 扩展版」条款可能不同**（Raft 的会议版与技术报告版就是常见的例子）。`papers.toml` 的 `url` 必须与 `evidence_url` 指向**同一版**。

#### `[paper.license]` 的判定口径（spec §10.3）

| 字段 | 含义 | 谁在用 |
| --- | --- | --- |
| `verified` | 是否**已经实际核实过**这篇论文的条款 | 与 `allows_translation` 一起构成翻译闸门 |
| `allows_translation` | 条款是否**明确允许翻译** | 同上；「已核实」而这里为 `false` = **仍然不能翻译** |
| `allows_commercial` | 是否允许商用 | 商业使用决策 |
| `share_alike` | 是否有 SA 传染（产出须以同协议发布） | 授权边界（content-policy） |

- **`verified = true` 的四条前置**（缺一不可，与讲座 `[license]` 同级严格）：`terms` 非空且是**原文照抄**的条款名；`evidence_url` 非空且复核者**本人打开过**；`checked_at` 是 ISO 日期；`allows_translation` 已明确判断。
- `verified = true` 而 `terms` / `evidence_url` / `checked_at` 任一为空 → `validate.py` **exit 1**（spec §6.8）。
- **`verified` 与 `allows_translation` 是两件事。** 核实的结果完全可能是「查明有版权、须走授权流程」—— 那正是 `verified = true` + `allows_translation = false`，**翻译仍被闸门拦死**。这正是 `allows_translation` 独立存在的原因。
- 注意 `[paper.license]` **没有** `allows_derivatives` 字段：论文这边「能不能改编」被收窄成了更具体的「能不能翻译」，查那一项就够。

#### 人工闸门 ②Q（双人签字，**逐篇**）

- [ ] 证据由**第二人独立复核**（自己再看一遍不算复核）
- [ ] `evidence_url` 指向的是**该论文**的条款或**其出版社**的授权政策，而不是别处的仿制页、聚合站
- [ ] 判定只依据 `evidence_url` 的原文，不依据「大家都这么用」「课表上就挂着 PDF」
- [ ] **不拿别的论文的条款顶替** —— 同一门课里 MapReduce（USENIX）与 GFS（ACM）各不相同
- [ ] **不拿课程的 `[license]` / `[license.materials]` 顶替** —— 那是课程材料的授权，与论文无关
- [ ] 未核实 / 无法核实 → `verified = false`、`allows_translation = false`，并在 `notes` 写明「未确认」
- [ ] 结论一行已落到 [paper-licensing.md](./paper-licensing.md)（含原文引用与访问日期）

#### 机器兜底

```bash
python scripts/validate.py
```

论文相关的 ERROR（spec §6.8–§6.11）：`papers.toml` 缺字段 / `key` 不合规或重复 / `verified = true` 但证据字段为空；论文页缺 `kind = "paper"` 或必填字段 / `paper` 未登记或重复 / `output_mode` 不是 `guide` / `translation`；**`translation` 而该篇授权不允许翻译**；讲座 `papers = [...]` 引用了未登记的 key。

`build.py` 在论文翻译闸门上有**第二道独立检查**：命中即 exit 1，**且不产出任何站点**（spec §7）。
和讲座一样，把它当**事后报警器，不是授权流程的替代品**。

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
# key = "replication"          # 可选；默认由 en 推导，一般不用写
aliases = ["replica", "replicas"]
notes = "此处指数据副本机制"
```
- `en` / `zh` 必填且非空
- `en` 唯一（**大小写不敏感**去重）；**key 也必须在课程内唯一**（重复即 ERROR）
- `key` 可选，默认由 `en` 推导；需要与 `en` 不同的 key 时才显式写
- `aliases` 收异体/复数
- `notes` 只在有歧义时写

#### 标记 key 怎么来（★ 写正文时最容易错的一处）

spec §3 定义了 key 推导规则：**`key` 默认由 `en` 生成 —— 转小写、空格与下划线转连字符、去掉其他非法字符**。
正文标记必须用 **key**，不是 `en` 原文。

| `en` | 正文里必须写的标记 |
| --- | --- |
| `replication` | `[[term:replication]]` |
| `leader election` | `[[term:leader-election]]` |
| `primary-backup replication` | `[[term:primary-backup-replication]]` |

**写成 `[[term:leader election]]`（带空格）会 ERROR：key 不存在。** 统一写小写。
需要在正文里写「标记写法示例」本身时，把它放进**行内 code**（`` `[[term:key]]` ``）或 **HTML 注释**（`<!-- -->`）——
spec §5 明确这两种情况**不算真实引用**，不会被判 ERROR。

> `en` 里尽量别写括号、斜杠、逗号：它们会在派生时被去掉，导致你按 `en` 猜的 key 和实际 key 对不上。
> 真需要特殊 key 时，按 spec §3 显式写 `key = "..."`。

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
- [ ] 在 PR 描述中写明 **「glossary frozen @ `<commit short sha>`」**（冻结声明，见 §14-4：spec 没有专门的冻结字段）

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
| `slug` | 字符串 | **全课程唯一**；与目录名 `<NN>-<slug>` 的 slug 一致（见 §14-7） |
| `status` | `draft` / `reviewed` / `approved` | 新写的永远是 `draft` |
| `source_kind` | spec §4：`notes` / `video` / `textbook` / `other` | 如实填。**它还决定授权闸门查哪一项** —— 填错 `source_kind` 会拿到错误的授权结论（spec §2）。注意当前实现额外接受 `slides`（spec 未定义，见 §14-9），而 `[license.materials]` 只认上面四类；**按 spec 只用这四个值** |
| `output_mode` | `explanation` / `transcript` | **`verified = false` 时只能是 `explanation`** |

> `source_title` 在 spec §4 的示例里存在，但**当前实现不把它列为必填**（见 §14-9）。仍然建议填 —— 它是署名与可溯源的一部分。

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

### 论文产出（④P）· 导读（默认）与全文翻译

**一篇论文 = 一个 `content/papers/<key>/index.md`**，`<key>` 必须与 `papers.toml` 中已登记的 `key` **逐字符一致**（它同时是目录名与站点 URL）。

> ⚠️ **没有骨架脚本。** `new_lecture.py` 只生成讲座，论文页的目录与 front matter 目前要**手工建**（见 §14-15）。手工建最容易漏 `kind = "paper"` 或把 `paper` 的 key 拼错 —— 这两条都是 ERROR。建完目录立刻跑一次 `validate.py`。

#### 第 1 步 · 确认登记（②P / ②Q 已完成）

`papers.toml` 里必须有这篇，且 key 拼写一致。**没登记就先回阶段 ②P**：论文页的 `paper` 指向未登记的 key 会直接 ERROR（spec §6.9）。

#### 第 2 步 · 先决定档位（本轨道最关键的一次判断）

| 情况 | 档位 | 为什么 |
| --- | --- | --- |
| 未核实 / 核实为「不允许翻译」 / 还没核实完（**默认情况**） | `output_mode = "guide"` | 导读是我们自己写的，概念与思想不受著作权保护，**不需要任何授权** |
| `verified = true` **且** `allows_translation = true`（两条都成立，且证据已入库） | `output_mode = "translation"` | 只有此时全文翻译才被允许 |

**默认答案永远是 `guide`。** 遇到「不确定能不能翻译」，不要卡在那里等结论 —— **写导读，然后开工**。
`guide` 不是妥协品：一篇讲清「要解决什么问题、怎么解、代价是什么」的导读，对读者比一篇没人校对的全译更有用。范式见 `template/content/papers/mapreduce/index.md`。

**只「核实了」不够**：`verified = true` + `allows_translation = false` = 仍然**只能写 `guide`**。

#### 第 3 步 · front matter（spec §10.2，5 个字段，不加字段）

```markdown
+++
kind = "paper"
paper = "mapreduce"
title = "MapReduce 导读"
status = "draft"
output_mode = "guide"
+++
```

- `kind` 固定为 `"paper"`；`paper` 是 `papers.toml` 的 key；`status` 新写的永远是 `"draft"`；`output_mode` 只能是 `guide` 或 `translation`。
- **论文页没有 `lecture` / `slug` / `source_kind` / `source_url`** —— 作者、出处、来源链接全部由 `papers.toml` 提供，**同一事实不要写两处**。写了也不算错，但它们不生效、只会误导后来人，别写。
- 论文页与讲座**共享** `glossary.toml`：正文里的术语同样要打 `[[term:key]]`，glossary 的 `en` 原词出现却没打标记同样 WARN（spec §6.12）。

#### 第 4 步 · 写导读（`guide`，默认档）

导读要**真的教这篇论文**，而不是复述摘要。合格的导读至少包含这七块：

1. **它要解决什么问题** —— 具体到当时的具体麻烦（什么任务、什么量级、旧办法为什么不行）。不要写「随着互联网的发展」。
2. **核心主张 / 核心抽象** —— 论文真正贡献的那个想法（MapReduce 是两个函数 + 框架接管并行），并用一句话说清「它把什么变成了不用再想的前提」。
3. **机制走查** —— 关键路径按顺序讲清楚：数据怎么流、谁做什么决定、哪一步是设计的枢纽。讲**「为什么这么设计」**，不只讲「设计成什么样」。
4. **边界与代价** —— 论文自己承认的限制（不适合迭代式算法、单点、磁盘布局……）。这一段最能区分「真读过」和「抄了摘要」。
5. **与课程的关系** —— 它是后面哪几讲的直觉前置；可以在讲座 front matter 里用 `papers = ["<key>"]` 做成结构化交叉链接（spec §10.4）。
6. **读完应该能回答** —— 3 个左右的**判断力**问题（不是知识问答）。
7. **溯源** —— `papers.toml` 的 `url` + 本文对应的章节位置；**给位置，不给文本**。

配图放 `content/papers/<key>/figures/`，命名 `figures/<key>-<n>.svg`（沿用讲座的约定，见 §14-8 / §14-17）；正文用**相对路径**引用，**alt 必写中文结论**；需要画图走 `course-diagram`。

#### 论文导读交付清单（`guide`）

**契约层**
- [ ] front matter 5 字段齐全（`kind` / `paper` / `title` / `status` / `output_mode`），`+++` 成对
- [ ] `paper` 与 `papers.toml` 的 `key` 逐字符一致，且该 key 没有被另一个论文页用过
- [ ] `output_mode = "guide"`；**没有**写 `lecture` / `slug` / `source_kind` / `source_url`
- [ ] 每个 `[[term:key]]` 的 key 都在 `glossary.toml` 中；glossary 的 `en` 原词都已打标记
- [ ] 没有任何「几乎全为 ASCII 且 > 400 字符」的段落 —— **导读里一段原文都不放**（论文页走同一套正文检查）

**内容层**
- [ ] 问题、主张、机制、代价四块俱全，且都能指到论文的具体位置
- [ ] 机制部分讲了「为什么这么设计」，不只是「设计成什么样」
- [ ] 有「读完应该能回答」的检查问题（3 个左右）
- [ ] 有溯源位置，且与 `papers.toml` 的 `url` 一致
- [ ] 配图是自己画的；alt 是中文结论
- [ ] 语气像助教不像营销号；无禁用词（`docs/brand.md`）

#### 第 5 步 · 写全文翻译（`translation`，默认关闭）

**只有在 ②Q 已经记录，且 `verified = true` 与 `allows_translation = true` 两条都成立时**才动这一步。
开工前把该篇 `[paper.license]` 的原文（`terms` / `evidence_url` / `checked_at`）贴进 PR 描述 —— 复核者要看的不是「我确认过了」，而是**你依据的那一条条款**。

译文与我们的原创讲解**混在同一页里**，因此它继承与逐字稿翻译同级的风险。要求：

1. **遵守 `glossary.toml`**：术语译法与全课程一致，首现给「中文（English）」，之后统一用中文；已冻结术语照样打 `[[term:key]]`。
2. **忠实**：不增、不删、不「润色」掉作者的限定条件；译者的补充必须**单独成小节**并显式标注「译者注」。
3. **不夹带原文**：正文里不放整段英文原文（必要的术语、代码、公式、专有名词除外）。想做中英对照 → 那是另一个决定，需要单独的授权判断。
4. **图 / 表 / 公式自己重画或转写**，不得截图、不得复制原始论文的图片 —— 原图同样受著作权保护。
5. **署名与出处交给 `papers.toml`**：标题、作者、venue、官方链接由页面自动渲染，正文不要再抄一遍；正文只补「本译文对应的版本与章节范围」。
6. **开头写明这是译文**：论文标题、作者、venue、年份、官方链接、版本与章节范围、授权依据（`terms` + `evidence_url`），并保留页面自动生成的授权提示条。

#### 论文翻译交付清单（`translation`，比导读更严）

> **这份清单里任何一项 fail，都必须退回 `guide`** —— 而不是「先发出去再补」。

**闸门层（先过这四条，其他都是次要的）**
- [ ] `papers.toml[key].license.verified == true`，且证据三件套（`terms` / `evidence_url` / `checked_at`）非空
- [ ] `papers.toml[key].license.allows_translation == true`
- [ ] 证据针对的是**这一版**论文（会议版 / 技术报告 / 扩展版不要混）
- [ ] `evidence_url` 已由**第二人**独立打开复核过，结论落到 [paper-licensing.md](./paper-licensing.md)

**契约层**
- [ ] front matter 5 字段齐全；`paper` 与登记的 `key` 一致
- [ ] `output_mode = "translation"`
- [ ] 术语全部走 `glossary.toml`；`[[term:key]]` 无未登记 key、无漏标
- [ ] `python scripts/validate.py` **exit 0**（论文翻译闸门通过）

**译文层**
- [ ] 术语与全课程一致（抽 5 个术语全文搜索）
- [ ] 无漏译、无整段跳过、无「译者补充」混进正文
- [ ] 无原文段落夹带；图 / 表是**重画或转写**，不是截图或复制
- [ ] 版本与章节范围已在开头写明
- [ ] 抽读 3 段与原文逐句对照：有无添油加醋、有无抹掉限定条件

**复核层**
- [ ] 复核者与译者**不是同一人**（译文尤其不能自审）
- [ ] 复核意见落到**行号 + 原句 + 最小修改建议**，不允许「再打磨一下」

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
| 8 | **论文登记表**：`papers.toml` 的 `[[paper]]` 缺 `key` / `title` / `authors`（非空数组）/ `venue` / `url`，或缺 `[paper.license]` 段，或 `verified = true` 而 `terms` / `evidence_url` / `checked_at` 为空 | 补字段；`authors` 写成**数组**（`authors = ["A", "B"]`）而不是字符串；`verified = true` 必须有证据三件套，**没证据就把 `verified` 改回 `false`** —— 反过来「补」证据字段去凑，就是伪造授权 |
| 9 | **论文页**：缺 `kind = "paper"` 或 `title` / `paper` / `status` / `output_mode`；`paper` 未在 `papers.toml` 登记或重复；`output_mode` 不是 `guide` / `translation` | 补字段；`paper` 与登记表的 `key` 逐字符对齐；**一篇论文只允许一个论文页**（`content/papers/<key>/index.md`） |
| 10 | **论文翻译闸门**：`output_mode = "translation"` 而该篇 `verified` 或 `allows_translation` 不为 `true` | **默认改回 `guide`**，照常写导读。**绝对不要为了过校验去改 `verified` / `allows_translation`** —— 那是伪造授权证据。真要开翻译，先回阶段 ②Q 拿到并记录该篇的明确许可 |
| 11 | 讲座 front matter 的 `papers = [...]` 引用了 `papers.toml` 中未登记的 key | 回阶段 ②P 登记该论文，或改掉写错的 key；引用的必须是登记表里的 `key` |

> **编号说明**：本表 #1–#6 沿用**实现侧的旧编号**（它们对应 spec §6 的 ERROR 1–4、6、7）；#8–#11 直接用 **spec §6 的编号**。spec §6.6「`content/` 下既没有讲座也没有论文页」不单列 —— 它是空仓库的正常现象，见 §2。

**论文轨道的三条提醒**

- **转载探测管不了译文。** 它只识别「几乎全为 ASCII 的长段落」，而合规的译文本来就是中文 —— 所以 `translation` 的**唯一防线是 ②Q 的逐篇授权闸门 + 阶段 ⑥P 的加严复核**。机器既拦不住一篇没授权的译文（只要它是中文写的），也拦不住一篇译错的译文。**别因为 exit 0 就以为译文安全。**
- **论文页与讲座走同一套正文检查**（术语引用、漏标 WARN、转载探测）。导读里粘原文段落，一样会被拦下。
- `build.py` 的论文翻译闸门是**独立的第二道**：即使有人绕过 `validate.py`，构建仍会 exit 1 且**不产出 `site/`**（spec §7）。

**关于 ERROR 6 的判定口径**（当前实现，spec §6.7 未写细节，见 §14-5）：段落需同时满足
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

> **WARN 的编号**同样沿用实现侧的旧编号（#7 / #8 对应 spec §6 的 WARN 12 / 13）。上表 ERROR 的 #8–#11 用的是 **spec 编号**，与这里的 #8 **不在同一序列**里 —— 看编号时先看表头。
> 论文页的草稿标记还有一个口径问题（导航里显示的是「导读 / 全文翻译」档位标签，不是草稿标记），见 §14-16。

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

### 阶段 ⑥P · 论文复核（★ 闸门，双人）

论文页与讲座同样走 `draft` → `reviewed` → `approved`，但复核的问题**多一条，而且是最重要的一条**：这篇的**档位对不对**（该不该是 `translation`）。

```bash
python scripts/validate.py
python scripts/build.py --out site      # 论文页要看授权提示条与元数据，别只看 Markdown
```

#### `guide` 的复核（引用行号 + 原句 + 最小修改建议）
- [ ] §5 的《论文导读交付清单》全部 pass
- [ ] 抽读「机制」与「代价」两段，问一句：「这段是我们读出来的，还是摘要的复述？」有疑虑就驳回
- [ ] 页面元数据正确：标题 / 作者 / venue / 出版社 / 原文链接都来自 `papers.toml`，且与登记表一致
- [ ] **档位复核**：确认该篇的 `[paper.license]` 确实不满足翻译条件（或即使满足、我们仍选择只发导读）
- [ ] 若有相关讲座声明了 `papers = ["<key>"]` → 交叉链接双向可用

#### `translation` 的复核（**加严**）
- [ ] §5 的《论文翻译交付清单》全部 pass
- [ ] **授权复核人 ≠ 译者**，且授权结论由第二人**独立打开 `evidence_url` 验证过**
- [ ] 确认 `allows_translation = true` 是**这一版论文**的结论（会议版 vs 技术报告版不要混）
- [ ] 抽 3 处与原文逐句对照：有无漏译、有无增益、限定条件有没有被抹掉
- [ ] 图 / 表是**重画或转写**，不是截图、不是原始图片的复制
- [ ] 版本号与章节范围已在译文开头写明

#### 人工闸门 ⑥P
- [ ] 只有 `status = "approved"` 的论文页才能进阶段 ⑦P
- [ ] **授权判定有任何疑点 → 立刻退回 `guide`**（宁可只发导读，不发译文）
- [ ] 一旦被指出超出授权范围 → 走 content-policy 的**立即下线**流程，不讨论、不等结论

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

### 构建产物（spec §7 / §10.5）
```
site/index.html                课程首页 + 讲座目录 + 「经典论文」列表
site/<slug>/index.html         每篇讲座
site/papers/<key>/index.html   每篇论文页（导读或全文翻译；相对根目录两层，故 base="../../"）
site/glossary/index.html       术语表
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

#### 论文页专项验收（⑦P，必须逐篇打开看）

- [ ] 打开 `site/papers/<key>/index.html`：元数据（标题 / 作者 / venue / 出版社 / 原文链接）与 `papers.toml` 一致
- [ ] **授权提示条**存在且与档位相符：`guide` 显示「本篇为我们自己撰写的导读，不含原文段落」；`translation` 显示「已核实、允许翻译」并带 `terms`
- [ ] 该篇 `verified = false` 时，页面**不得**出现任何「已授权 / 已核实」措辞（提示条应显示「未核实，或条款未明确允许全文翻译」）
- [ ] 侧栏出现「**论文**」分组，首页出现「经典论文」列表；论文页的相对路径都对（`base="../../"`）
- [ ] `translation` 的论文页：**整页没有整段英文原文**；图 / 表是重画的，不是截图
- [ ] 论文页与相关讲座之间的交叉链接（`papers = [...]`）可来回跳转

### CI（spec §8）
| 工作流 | 触发 | 行为 |
| --- | --- | --- |
| `validate.yml` | push / PR | 跑 `validate.py`，有 ERROR 即失败 |
| `deploy.yml` | push to `main` | `validate.py` → `build.py` → 部署 `site/` 到 GitHub Pages |

### 人工闸门 ⑦
- [ ] 上面的目视验收全过
- [ ] `site/` **不入库**（检查 `.gitignore`）—— 构建产物不进版本历史
- [ ] 提交信息用祈使句 + 范围前缀（CONTRIBUTING §4），如 `6.824: 讲解 Lecture 3 主从复制`
- [ ] 发布范围只含 `approved` 的讲座与**论文页**；`translation` 的论文页还要在 PR 描述里附 `evidence_url` 的原文引用（授权依据不是「我确认过」，而是那一条条款）

---

## 9. 可直接粘贴的 Agent 提示词

> 用法：把 `<尖括号>` 换成真实值。提示词里已经内联了硬约束 —— **不要删减约束段**，它们对应 `validate.py` 的 ERROR 类。

### 9.1 建术语表（阶段 ③）

```text
你是 CourseLingo（译课 AI）的术语工程师。任务：为课程《<课程中文名>》（course.id = <id>）建立术语表首版。

先读：docs/pipeline-spec.md §3（字段契约）、docs/content-policy.md、.github/CONTRIBUTING.md §1。

硬约束：
1. 产出只能是 TOML 的 [[term]] 列表，字段仅限 en / zh / key / aliases / notes（spec §3）。不得新增其他字段。key 一般不用写 —— 它默认由 en 推导（小写、空格与下划线转连字符）。
2. 术语来源只能是课程官方材料（大纲、讲座列表、页面标题）。不得凭记忆编造官方术语。
3. 只输出术语条目，不得输出任何英文原文段落、幻灯片内容或视频内容。
4. 业界有通行译法的优先沿用（consensus → 共识，replication → 副本）；无通行译法的保留英文并在 notes 写明「无通行译法，暂译 X」。
5. 同一概念只能有一个 en；复数与异体写进 aliases。同一课程内 key 必须唯一。正文标记 key 由 en 派生（小写、空格转连字符：leader election → [[term:leader-election]]），所以 en 里不要用括号、斜杠等符号。

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
1. 本课程授权状态：license.verified = <true|false>，[license.materials] = <未填 / 各项取值>。为 false 时 output_mode 只能是 "explanation"：禁止逐句对照翻译，禁止在正文保留英文原句或整段英文。
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
 3. 每个 [[term:key]] 的 key 都在 glossary 中存在（列出不存在的 key；注意多词术语要连字符化）
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

### 9.4 写一篇论文导读（阶段 ④P，`output_mode = "guide"`，默认档）

```text
你是 CourseLingo（译课 AI）的论文导读作者。你写的是**我们自己写的导读**，不是翻译，也不包含原文段落。

任务：为课程 <course.id> 的论文 <papers.toml 里的 key>（《<论文标题>》，<venue> <year>）产出 content/papers/<key>/index.md。

先读：papers.toml 中该篇的条目、glossary.toml（必须遵守）、docs/pipeline-spec.md §10、docs/content-policy.md、docs/brand.md，以及 template/content/papers/mapreduce/index.md（导读的范式）。

硬约束：
1. output_mode 只能是 "guide"。禁止逐句翻译、禁止摘译、禁止在正文里放英文原文段落 —— 连"引用一句原文"都不要做。
2. front matter 只有 5 个字段：kind = "paper" / paper = "<key>" / title = "<中文标题>" / status = "draft" / output_mode = "guide"。不要写 lecture / slug / source_kind / source_url —— 作者、出处、链接由 papers.toml 提供，同一事实不写两处。
3. 术语：正文出现已冻结术语时用 [[term:<key>]] 标记（key 由 glossary 的 en 派生：小写、空格与下划线转连字符）；不要用中文替代词绕过标记，也不要直接写英文原词。需要新术语 → 回 course-init 走评审加词。
4. 不转载：不得复制论文的句子、图表、图片、公式排版。图必须自己画（走 course-diagram），放 content/papers/<key>/figures/<key>-<n>.svg，正文用相对路径引用，alt 写中文结论。
5. 不得出现成段的英文散文（「几乎全为 ASCII 且长度 > 400 字符」的段落会 ERROR；论文页也走这条检查）。
6. 只依据论文本身与公开的官方信息。不得凭记忆编造实验数字、年份、机构名；拿不准就写"论文给出的数字是 X（原文 §N）"，不要自己推算。

正文结构（必须齐全，七块）：
- 它要解决什么问题（具体的麻烦、量级、旧办法为什么不行）
- 核心主张 / 核心抽象（一句话说清它把什么变成了不用再想的前提）
- 机制走查（关键路径按顺序；讲"为什么这么设计"，不只讲"设计成什么样"）
- 边界与代价（论文自己承认的限制）
- 与课程的关系（它是后面哪几讲的直觉前置）
- 读完应该能回答（3 个左右判断题，不是知识问答）
- 溯源（论文官方入口 + 本文对应的章节位置；给位置，不给文本）

输出：一个完整的 index.md，然后附一张自查表（逐项 pass/fail，fail 的给出修改）。
```

### 9.5 写一篇论文全文翻译（阶段 ④P，`output_mode = "translation"`，**默认关闭**）

> **先停下来核对闸门。** 本提示词只在前置条件成立时才可用：
> `papers.toml[key].license.verified == true` **且** `allows_translation == true`，且 `terms` / `evidence_url` / `checked_at` 都有值。
> 任一不成立 → **改用 9.4 写导读**，不要翻译，也不要先去改授权字段。

```text
你是 CourseLingo（译课 AI）的论文译者。任务：把论文《<标题>》（<venue> <year>）全文翻译为中文，产出 content/papers/<key>/index.md，output_mode = "translation"。

前置（已在 papers.toml 中记录，你必须先读，并在输出开头复述一遍）：
- terms = "<条款名>"；evidence_url = "<核实依据>"；checked_at = "<ISO 日期>"
- 若这三项任一为空，或 allows_translation 不为 true → 立即停止，改产出导读（见 9.4），不要翻译。

硬约束：
1. front matter 只有 5 个字段：kind = "paper" / paper = "<key>" / title = "<中文标题>" / status = "draft" / output_mode = "translation"。
2. 术语一律用 glossary.toml 的译法，首次出现给「中文（English）」，之后统一用中文；已冻结术语用 [[term:<key>]] 标记。
3. 忠实：不增、不删、不"润色"掉作者的限定条件；译者的补充必须单独成小节并显式标注「译者注」。
4. 正文不夹带整段英文原文（术语、代码、公式、专有名词除外）。若确需中英对照，另起小节并说明理由。
5. 图 / 表 / 公式：重画或转写，不得截图、不得复制原始图片；重画的图走 course-diagram，存 content/papers/<key>/figures/。
6. 开头写明：论文标题、作者、venue、年份、官方链接、本文对应的版本与章节范围、授权依据（terms + evidence_url）。
7. 不复制论文的排版与版式；不加入任何出版社 / 学校的 Logo。

输出：一个完整的 index.md + 一张自查表（逐项 pass/fail），并在最后单列一节「不确定译法」，列出拿不准的 5 处及候选译法与理由。
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
| **把「能免费下载」当成许可**（论文） | `papers.toml` 的 `evidence_url` 填的是作者主页的 PDF 链接或镜像站 | 「PDF 能公开打开」≠「授予翻译权」；法律状态仍是保留所有权利 | `evidence_url` 必须指向**条款本身**（许可声明 / 出版社的 permission 政策页）；PDF 链接只能进 `url` / `pdf_url`；②Q 四步方法第 2 条 |
| **用一篇论文的条款顶替另一篇** | GFS（ACM）沿用了 MapReduce（USENIX）的 `terms`，或整门课的论文填了同一个 `evidence_url` | 同一门课的论文来自不同出版社，条款各不相同 —— 这正是 `papers.toml` 逐篇一个 `[paper.license]` 的原因 | 每篇单独抓、单独填、单独签字；发现两篇的 `evidence_url` 完全相同就当成红灯复查 |
| **拿课程授权当论文授权** | `course.toml` 是 `verified = true`（甚至 `[license.materials].notes = true`），于是顺手把论文的 `verified` 也置 `true` | 课程材料的授权与论文**完全无关**；「课程笔记已核实」推不出「论文可以翻译」 | 论文的 `verified` / `allows_translation` 只依据 `[paper.license].evidence_url`，课程字段一个字都不看（②Q 清单里有这一条） |
| **「已核实」被当成「可以翻译」** | `verified = true` 但 `allows_translation = false`，仍有人把论文页设成 `translation` | `verified` 只表示「查清楚了」；查清楚的结果可能是「有版权、须走授权流程」 | 两个条件缺一不可（spec §10.3）；`validate.py` ERROR 10 与 `build.py` 的独立闸门各拦一次；默认答案永远是 `guide` |
| **为过校验改授权字段** | 为了让 `translation` 通过校验，把 `verified` / `allows_translation` 改成 `true` | 把「希望」写成了「事实」 | **红线行为**（等于伪造授权证据）。证据字段只允许**在拿到 `evidence_url` 支撑、并经第二人复核后**从 `false` 改成 `true` |
| **「大家都分享 PDF」** | 付费墙后的论文也有人贴 PDF，于是认为可以翻译 | 灰色流通 ≠ 授权；反而说明该篇很可能**没有**开放许可 | ACM DL / IEEE Xplore / 付费墙上的论文默认「不可翻译」，除非出版社政策或书面许可明确允许 |
| **导读里夹带原文** | 导读为了「忠实」贴了一大段英文原文与图表 | 导读的授权优势来自「只讲概念、不复制表达」，夹带就把它抹掉了 | 导读不放原文段落、不复制图表（机器能以 ASCII 长段落拦下一部分，但**拦不住图片**） |
| **译文没人对照原文复核** | 译文推到 `approved`，而 `validate.py` 全程 0 ERROR | 转载探测只看 ASCII 长段落，**合规译文本来就是中文 —— 机器识别不了译得好不好，也识别不了有没有授权**（见 §14-18） | `translation` 的唯一防线是 ②Q 的逐篇授权 + ⑥P 的加严清单（译者与授权复核人分离、抽 3 处逐句对照） |
| **论文档位定错（该导读却做了翻译）** | 没有任何报错，但论文页是 `translation`，而该篇其实只有「可下载」没有「可翻译」 | 把「先做着，回头补授权」当成了流程 | ②Q 的结论落进 `papers.toml` 之后才允许动 ④P；`translation` 的开工前置是**两个 true + 证据三件套**，缺一个就写导读 |

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
| 不同论文的**导读初稿** | 每篇一个 subagent | 该篇已在 `papers.toml` 登记；每篇都必须要求「不复制原文」 |
| 不同论文的**授权核实** | 每篇一路 | 但**证据与签字是逐篇的**：每篇各自抓 `evidence_url`、各自签字，不许把一批结论糊成一行 |

并行时每个 subagent 的输入必须完全相同地包含：**冻结 glossary 全文 + 同一份提示词（§9.2）+ 本讲编号/slug**。

### 必须串行
| 工作 | 为什么 |
| --- | --- |
| 阶段 ② 授权核实 | 全局闸门，结论决定所有讲座的 `output_mode` |
| 阶段 ③ 术语冻结 | 它是并行的前提 |
| **glossary 的任何变更** | 会让所有已产出讲座的 WARN 结果失效 → 变更后**全课程重跑** `validate.py` |
| 讲座编号 / slug 分配 | 多路并行下唯一性靠事前分配，不能靠事后查重 |
| 论文 `translation` 的开工 | 前置是该篇 ②Q 的结论（`verified` + `allows_translation` 两个 true）；闸门不成立时**只能写 `guide`** |
| `papers.toml` 里论文 `key` 的分配 | `key` 同时是目录名 `content/papers/<key>/` 与站点 URL `site/papers/<key>/`，事后改 = 改 URL（同「讲座编号 / slug 分配」） |
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

### 13.1 每篇论文一页的速查

```bash
# 1. 登记（先做，否则论文页的 paper 字段必然 ERROR）
#    在 papers.toml 里加 [[paper]]：key 用小写连字符，authors 是非空数组
#    [paper.license] 先一律 false —— 别猜

# 2. 逐篇核实授权（人工，无脚本）—— 四步见 §3 的 ②Q
#    抓原始 HTML → 看出版社政策 → 记录 evidence_url + checked_at
#    结论一行落到 docs/paper-licensing.md

# 3. 建目录（没有骨架脚本，手工建，见 §14-15）
#    content/papers/<key>/index.md

# 4. 写稿：默认写导读（guide）；front matter 5 字段
#    kind = "paper" / paper = "<key>" / title / status = "draft" / output_mode
#    translation 只在前置「两个 true + 证据三件套」都成立时才写

# 5. 校验（同一脚本；论文相关 ERROR 见 §6 的 8–11）
python scripts/validate.py          # 0=通过 1=有ERROR 2=用法/IO错误

# 6. 本地看授权提示条与元数据
python scripts/build.py --out site
#    → site/papers/<key>/index.html

# 7. 复核通过后把 status 推到 reviewed / approved
#    translation 必须双人：授权复核人 ≠ 译者
```

---

## 14. 待决事项（spec 缺口）

> 以下都是**冻结契约未定义**、而执行中确实会撞到的问题。**在 spec 补齐之前，按「本手册的临时约定」执行，并保持与 spec 不冲突**；不要在多处各自发明不同做法。
>
> **已由 spec 更新消化的三项**（曾在本节，现已写入契约，不再列为缺口）：
> - ~~`[license]` 只有一个 `verified` 布尔，无法表达「笔记已授权、视频未授权」~~ → spec §2 已新增 **`[license.materials]`**，按 `source_kind` 逐项核实，且「一旦存在 `materials`，闸门只认它，不再看 `verified`」。本手册 §3 已按此更新。
> - ~~多词术语的 key 派生规则未定义~~ → spec §3 已明确 **key 推导规则**，并允许显式 `key = "..."` 覆盖。本手册 §4 已按此更新。
> - ~~空课程仓库「没有任何讲座」是否算 ERROR~~ → spec §6.6 已明确：**`content/` 下既没有讲座也没有论文页 → ERROR**。本手册 §2 与 §14-10 已按此更新。
>
> **下表第 9–19 项**是**对照当前实现（`template/scripts/`）核对后发现的 spec 缺口或分歧** —— 实现可能仍在演进，遇到不一致时**以 spec 为准并回报**。
> **第 14–19 项是论文轨道引入的新缺口**（spec §10 已冻结论文契约，但下表的这些边角没有定义）。

| # | 缺口 | 影响 | 临时约定 |
| --- | --- | --- | --- |
| 1 | `new_course.py` / `new_lecture.py` 的 **CLI 未定义**（spec §1 只给脚本名与作用）；且 spec §1 把 `new_course.py` 画在**课程仓库内**，而实现放在**平台主仓库** `scripts/` 下 | 无法从 spec 写出确定的开工命令 | 按实现的 `--help` 为准（已记录于 §2/§5）；若行为与 §1 结构不符，**按 spec §1/§2/§3/§4 手工建目录与文件**。绝不臆造参数 |
| 2 | `validate.py` 的 **CLI 未定义**（只冻结了退出码） | 无法「只校验单篇」；大仓库全量跑变慢 | 统一全量 `python scripts/validate.py`。实现另有 `--root` / `--quiet`，属实现细节（见 §14-9） |
| 3 | `[output].default_mode` 与逐讲 `output_mode` 的**优先级未定义** | 授权闸门判定口径含糊 | 闸门判定**以逐讲 `output_mode` 为准**（spec §6.2 即如此检查）；`default_mode` 在阶段 ② 出结论前恒为 `explanation` |
| 4 | 讲座 **front matter 无复核人 / 复核日期字段**（spec §4 字段已冻结） | 复核证据无处存放 | 用 PR 描述 + `status` 字段承载（CONTRIBUTING §3 已要求 PR 写明授权依据与术语变更）；不新增 front matter 字段 |
| 5 | **ASCII 长段落探测的判定细节未定义**（阈值、是否豁免代码块、是否剥离 Markdown 标记） | 合法代码块可能被误判，或作者不清楚什么会被拦 | 当前实现：`>400 字符` 且 `ASCII ≥ 90%` 且 `空格 ≥ 40` 才算可疑，且**跳过围栏代码块 / 标题 / 表格行**、判定前剥离行内代码与链接。**建议 spec 补齐这些细节**；本手册仍要求代码块加中文注释并保持短小（可读性 + 保守） |
| 6 | 一个讲座只有**一个** `source_url` / `source_title` / `source_kind` | 多源讲座（笔记 + 视频 + 教材）无法如实署名 | 填**主讲**来源，其余来源在正文「溯源」小节列出；如长期需要多源，提请 spec 扩展 |
| 7 | 目录名 `content/<NN>-<slug>/` 与 front matter `slug` 的**一致性未被校验**（§6.3 只查 slug 唯一） | 目录名与 slug 不一致时站点 URL 与目录错位 | 人工检查：目录名 `<NN>` 用两位补零，`<slug>` 与 front matter 完全相同 |
| 8 | `course-diagram` 的**产出契约未定义**（SVG 尺寸 / 命名 / alt 文本 / 是否内联） | 配图风格与可访问性靠自觉 | 图放 `content/<NN>-<slug>/figures/<slug>-<n>.svg`；正文用 `![<中文说明>](figures/...)`，alt 文本必须写 |
| 9 | **同一实现的多个 CLI / 字段超出冻结 spec** | 契约与实现漂移，消费方按 spec 写会失败或按实现写会与 spec 冲突 | 已观察到的分歧：① `validate.py` 有 `--root` / `--quiet`；② `build.py` 有 `--root`，且 `--base-url` 默认 `"./"` 而 spec §7 写 `/`；③ `validate.py` 实际要求 `[course]` 多填 `institution` / `source_language` / `target_language`（spec §2 只标 3 个必填）；④ `source_kind` 实际接受 `slides`（spec §4 只有 4 个值，且新增的 `[license.materials]` 也按这 4 类匹配，`slides` 永不匹配）；⑤ `source_title` 实际不是必填。**本手册一律按 spec 写**；分歧请回报给脚本维护者，由 spec 定夺 |
| 10 | ~~**`content/` 下没有任何讲座时 `validate.py` 报 ERROR**~~ → **spec §6.6 已明确这一条**（讲座与论文页**都没有**才算 ERROR） | 新生成的空课程仓库跑校验仍会 exit 1（这是刻意设计），容易被误判成配置错误；报错文案是「没有任何内容」，别拿它当「讲座缺失」来解 | 阶段 ① 只要求「除『没有任何内容』外无其他 ERROR」；建好**第一讲骨架或第一篇论文页**后再跑一次应当 exit 0 |
| 11 | `build.py` 对 `status = "draft"` 的讲座**是否发布**未定义（§6 WARN 8 只说会标注「草稿」） | 可能把草稿推到线上 | **发布闸门靠人工**：只发布 `approved` 的讲座，不依赖 `build.py` 过滤 |
| 12 | **spec §6.2 的措辞未与 §2 的 `[license.materials]` 同步**：§6.2 仍写「`license.verified != true` → ERROR」，而 §2 规定「存在 `materials` 时只认 `materials`，不看 `verified`」 | 只读 §6 的人会误以为 `verified` 是唯一闸门，可能据此把 `verified = true` 当成万能开关 | 以 §2 的判定顺序为准：**有 `materials` 就只认 `materials[source_kind]`**；建议把 §6.2 改写成引用 §2 的 `license_allows()` |
| 13 | spec §9 规定首批 **5** 个 skill（含 `course-diagram`），但本手册只覆盖 4 个（`course-diagram` 由其他产出负责） | 交叉引用可能指向尚不存在的 skill | `course-explain` 中「交给 `course-diagram`」的引用在 `skills/course-diagram/SKILL.md` 落地前，暂时手绘 SVG 按 §14-8 的约定存放 |
| 14 | spec §9 的 skill 清单仍是 **5 个**，**未包含论文技能** | `skills/` 现在有 6 个（新增 `course-paper`），与 spec §9 的清单不一致；`template/README.md` 已经引用 `course-paper` | 按本手册与 [skills/README.md](../skills/README.md) 执行：论文相关动作交给 `course-paper`。建议 spec §9 把清单更新为 6 个，并在 §10 末尾引用它 |
| 15 | **没有论文页骨架脚本**：`new_lecture.py` 只生成讲座（spec §1 也只列了它），论文页的目录与 front matter 要**手工建** | 手工建最容易漏 `kind = "paper"`、或把 `paper` 的 key 拼错 —— 这两条都直接 ERROR | 按 §5「论文产出」第 3 步的模板逐字填，建完立刻跑 `validate.py`。若将来加脚本（或给 `new_lecture.py` 加论文模式），参数同样必须先写进 spec 再实现 |
| 16 | 论文页 `status = "draft"` 的**标记口径**：`build.py` 在**侧栏导航**里给 `output_mode = "guide"` 的论文打「导读」标签（复用了 `draft` 这个 CSS 类），而「草稿」提示只在**论文页正文**里按 `status` 显示 | 只看导航会以为「导读」= 已复核状态；反过来 `translation` 的草稿在导航里**没有任何标记** | 发布闸门**不依赖导航标记**：只发布 `status = "approved"` 的论文页（与讲座同口径，见 §14-11）；导航里的「导读 / 全文翻译」只当**档位**提示看 |
| 17 | 论文页配图的**命名与尺寸契约未定义**（spec §1 只给了 `content/papers/<key>/figures/*.svg`） | 图会各写各的名字，正文引用也不统一 | 沿用讲座的约定（§14-8）：`figures/<key>-<n>.svg`，`n` 从 1 递增、本篇内唯一；正文用**相对路径**引用，alt 必须写中文结论；画图走 `course-diagram` |
| 18 | **机器兜底识别不了译文**：转载探测只在「几乎全为 ASCII 且 > 400 字符」时报警，而合规译文本来就是中文；spec §6 也没有任何针对译文的检查项 | 「校验通过」被误当成「译文安全」—— 没授权但译成中文的稿子同样能过 `validate.py` | `translation` 的唯一防线是 ②Q 的逐篇授权闸门 + ⑥P 的加严复核清单（译者与授权复核人分离、抽 3 处逐句对照）。**不要因为 exit 0 就认为译文可以发** |
| 19 | 没有 `site/papers/index.html` **论文索引页**（spec §10.5 只说首页加「经典论文」列表 + 侧栏「论文」分组） | 论文多了以后首页列表会很长，且没有可分页/可筛选的入口 | 按 spec 现状执行（首页列表 + 侧栏分组）；确实需要独立索引页时，**先提 spec 扩展再实现** |
