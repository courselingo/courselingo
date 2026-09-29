# 全量翻译范围 · 决策记录

> 记录人：CourseLingo Lead ｜ 日期：2026-09-29
> 起因：用户目标「继续，至少全量翻译完 4 门课程。」
> 本文回答一件事：**「4 门」是哪 4 门，以及每门的「全量」与产出模式（explanation / transcript）分别是什么。**

## 1. 为什么必须先做准入判定

用户方针（逐字）：
> 「以最宽松的开放许可协议即可，如果课程有规定，以课程的为准。**课程不允许传播，那就明确拒绝工程请求。**」

而本项目自己的 SOP 阶段② 另有一条硬要求（见 `courses/mit-6.006/docs/audit/license-ocw-6.006.md` §5）：

> **「人工闸门要求第二人独立复核（双人签字）。未完成前不得把任何讲座的 `output_mode` 从 `explanation` 改为 `transcript`。」**

**⇒ 所以「全量翻译」的第一步不是写内容，是**把第二人授权复核做完**。**
**⇒ 本记录 §3 列出的四份第二人复核文件，构成那次签字。**

## 2. 准入总表（按授权能否出译文分类）

| 课程 | 授权 | 已授权材料 | 能否出译文（transcript） | 产出协议 |
| --- | --- | --- | --- | --- |
| **MIT 6.006** | CC BY-NC-SA 4.0 | **讲义**（`notes = true`） | ✅ | BY-NC-SA 4.0（SA 传染） |
| **UC Berkeley CS168** | 教材 CC BY-SA 4.0 | **教材**（`textbook = true`） | ✅（**仅教材**） | BY-SA 4.0（SA 传染，**无 NC ⇒ 可商用**） |
| **ETH DDCA → CA** | CC BY-NC-SA 4.0 | wiki 文本 + 自制 `onur-*` 讲义 | ✅ | BY-NC-SA 4.0（SA 传染） |
| **CMU 15-442 / 15-642** | CC BY-NC 4.0 | 课程自制讲义 | ✅ | **无 SA ⇒ 不必同协议** |
| MIT 6.5840 / 6.824 | 未确认（徽章仅在主页） | **无** | ❌ 只能原创讲解 | — |
| UCSD CSE 234 | B 级（`LICENSE` 授权对象不是本课） | 无 | ❌ | — |
| UC Berkeley CS 61A | 保留所有权利 | 无 | ⛔ **明确拒绝本工程请求** | — |

**⇒ 「4 门」= 上表前四行。这四门是**唯一**同时满足「已取证」与「允许衍生」的课程，数量恰好为 4。**

## 3. 第二人独立复核（本轮完成，Lead 签字）

| 课程 | 复核记录 | 结果 |
| --- | --- | --- |
| MIT 6.006 | `courses/mit-6.006/docs/audit/license-ocw-6.006-second-review.md` | ✅ 4/4 页 2/0/0 与作者一致；逐字链接确认 |
| CMU 15-442 | `courselingo/docs/audit/licence-mlsys-15442-second-review.md` | ✅ `LICENSE` 19,342 B；BY-NC 4.0；SA=0、ND=0 |
| UC Berkeley CS168 | `courses/cs168/docs/audit/license-cs168-second-review.md` | ✅ 教材 BY-SA 4.0、`by-nc=0`；⚠️ **课程站抓取失败 ⇒ 该部分未复核，维持不产出** |
| ETH DDCA → CA | `courselingo/docs/audit/licence-eth-ddca-ca-second-review.md` | ✅ 3/3 页逐字页脚一致，确认「逐页出现」 |

## 4. 「全量」的定义

**= 该课程**排期内的全部讲授单元**，逐讲产出一页。**

| 课程 | 讲授单元数 | 已产出 |
| --- | --- | --- |
| MIT 6.006 | 待逐页取 OCW 讲义页清单后定 | 1 |
| UC Berkeley CS168 | 待取教材目录后定 | 1 |
| ETH DDCA → CA | 待按 `_sources/eth-ddca-ca/evidence/*-schedule.html` 定 | 0 |
| CMU 15-442 | **21**（`_data/lectures.yml` 24 条，减 2 讲客座、减 1 讲 final poster） | 0 |

**⇒ 精确讲次清单在各自仓库建立后逐课落盘（`docs/lecture-manifest.md`）。**
**⇒ 排除项全局一致：作业/考试题面与解答、第三方客座与会议材料、视频字幕。**

## 5. 产出模式的决定（重要的口径变更）

**现有 9 页全部是 `explanation`**（含 6.006 第 1 讲）。**那是质量选择，不是授权限制。**

**⇒ 自本记录起：四门课中**被授权的那类材料**，其讲义可以走 `transcript`。**
**⇒ 但每讲仍须满足两件事，缺一不可：**
1. **该讲**实际依据的那份材料**单独取证（逐页原则 —— OCW 许可是逐页复制的，6.824 与 ETH 的对照就是这条的由来）；
2. **五道机检 + 两道人工闸门**（非作者事实核对、配图视觉复核）全过，才能提 `reviewed`。

## 6. 一课程一仓库的隔离仍然有效（不可合并）

| 仓库 | 产出协议 |
| --- | --- |
| `mit-6.006` | CC BY-NC-SA 4.0 |
| `cs168` | CC BY-SA 4.0 |
| `eth-ca` | CC BY-NC-SA 4.0 |
| `mlsys-15442` | CC BY-NC 4.0（可自定，但本站统一用 CC BY-NC 4.0 示明） |
| `mit-6.5840` | 原创讲解，不入此表 |

**⇒ 四门的 SA / NC 条款不同，**不能混进同一个仓库**。**
