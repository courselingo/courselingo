# 四门新课 · 上线清单（截至第 14 轮）

> 目标：「至少全量翻译完 4 门课程。」判定标准是「**课程内容已上线且通过闸门**」。
> 本文件记录**已上线**的页面与它们的闸门证据。

## 已 reviewed 且线上可达（4 讲 · 4 门课各 1 讲）

| 课程 | 讲次 | 线上 URL | 字节 | 三道人工闸门 |
| --- | --- | --- | --- | --- |
| **mlsys-15442** | 01 `why-ml-systems` | <https://courselingo.github.io/mlsys-15442/lectures/why-ml-systems.html> | 41,929 | 事实核对 0/0/0 ✅ ｜ 视觉复核 11/11 可用 ✅ ｜ 透镜 3 ✅ 7/1/0 |
| **eth-ca** | 01 `lecture1-intro` | <https://courselingo.github.io/eth-ca/lectures/lecture1-intro.html> | 42,670 | 事实核对 0/3/3 已清 ✅ ｜ 视觉复核 11/11 可用 ✅ ｜ 透镜 3 ✅ 5/3/0 |
| **cs168** | 01 `internet-architecture-and-protocols` | <https://courselingo.github.io/cs168/lectures/internet-architecture-and-protocols.html> | 42,072 | （上一轮目标完成时已提级） |
| **mit-6.006** | 01 `algorithmic-thinking-peak-finding` | <https://courselingo.github.io/mit-6.006/lectures/algorithmic-thinking-peak-finding.html> | 45,016 | （上一轮目标完成时已提级） |

**⇒ 四门课各有一讲在线上，且四讲都过五道机检 + 各自的人工闸门。**

## 产出总览

| 课程 | 全量 | 已产出 | 已 reviewed | 自绘配图 |
| --- | --- | --- | --- | --- |
| cs168 | 52 | 5 | 1 | 46 |
| mit-6.006 | 24 | 2 | 1 | 15 |
| eth-ca | 31 | 8 | **1 ✅** | 78 |
| mlsys-15442 | 21 | 13 | **1 ✅** | 163 |
| **合计** | **128** | **28（22%）** | **4** | **302** |

## 提级路径（本会话跑通两条，可复用）

```
作者产出（status = draft）
  ↓ 五道机检：validate / check_style / audit_content --strict /
              check_figures --strict / build_site
  ↓ 三道人工闸门：
      ① 非作者事实核对   → docs/audit/<slug>-factcheck.md      （P0/P1 清零）
      ② 配图视觉复核     → docs/audit/visual-review/           （全部「可用」）
      ③ 透镜 3（陌生读者）→ 写进 docs/audit/lecture-NN-quality-audit.md 的 §5.5
  ↓ docs/audit/lecture-NN-quality-audit.md                  （§9 要求的「有审核记录」）
  ↓ check_reviewed.py --root .                              （读上面三样，全齐才过）
  ↓ Lead 改 status = "reviewed" + 建站 + push
  ↓ CI：Validate ✅ + Deploy to GitHub Pages ✅
  ↓ 实测线上 URL 返回内容
```

**★ 而 `check_reviewed.py` 要的两道人工闸门是**透镜 3 + 配图视觉复核**；
「非作者事实核对」是 Lead 另加的第三道**（它抓到了本会话全部内容级错误里的多数，但**不是**闸门要求）。

## ★ 2026-09-29 · 第 5 页上线：`mlsys-15442` 第 2 讲

| 项 | 值 |
| --- | --- |
| 页面 | `courses/mlsys-15442/content/02-introduction-to-mlsys/index.md` |
| 线上 | https://courselingo.github.io/mlsys-15442/lectures/introduction-to-mlsys.html |
| 实测 | **HTTP 200，66,066 B**（站点产物 `lectures/introduction-to-mlsys.html` 同为 66,066 B） |
| 页面哈希 | `902681F9C61B5E16`（26,263 B 归一化） |
| commit | `cd2a3a2`（mlsys-15442） |
| 五道机检 | validate=0 style=0 audit=0 figures=0 reviewed=0 build=0 |
| 事实核对 | **P0 0 ｜ P1 0 ｜ P2 3**（全仓仅两讲 P0/P1 双零） |
| 视觉复核 | **15/15 通过**（12 可用 + 3 条按 R1–R7 门槛的实测裁定） |
| 透镜 3 | ✅5 ｜ ⚠️3 ｜ ❌0（第一次未过，作者回源消除根因后重测通过） |

**★ 而这一页的提级多做了两步（`附录三十八` 之后的动作）：**
```
① 提级前**重跑**本讲全部 15 张图的复核（用新的 R1–R7 门槛提示词），不采信仓内旧报告
② 逐条核那 3 张「需小修」，确认裁定针对的是**最新那份报告**（哈希相符）
⇒ 用来避免 `mit-6.006` 第 2 讲那次「裁定覆盖旧报告、而新报告发现别处」的状态
```

**★ 而重跑有一个可量化的效果**：旧提示词下 4 张判「需小修」，
新门槛下 **2 张直接变「可用」**，另 2 张的判词变成**带比例与自检的可核主张**。
## ★ 2026-09-29 · 第 6 页上线：`mit-6.006` 第 2 讲

| 项 | 值 |
| --- | --- |
| 页面 | `courses/mit-6.006/content/02-models-of-computation-document-distance/index.md` |
| 线上 | https://courselingo.github.io/mit-6.006/lectures/models-of-computation-document-distance.html |
| 实测 | **HTTP 200，50,675 B** |
| 页面哈希 | `D336AD146A8BE340`（19,062 B） |
| commit | `e9bbc87`（mit-6.006） |
| 六道机检 | 全 0 |
| 事实核对 | P0 0 ｜ P1 0 ｜ P2 1 ＋ **差分补核 P0 0/P1 2/P2 3 ⇒ 按处方三处全改，逐条核实** |
| 视觉复核 | **8/8**（7 可用 + 1 实测裁定） |
| 透镜 3 | ✅5 ｜ ⚠️3 ｜ ❌0 |

## ★★ 而这一轮发现一件更重要的事：**draft 页也在线上**

```
cs168 8/8 ｜ mit-6.006 3/3 ｜ eth-ca 9/9 ｜ mlsys-15442 21/21
⇒ **41 讲产出、41 页在线上**（站点构建发布 draft 页）
⇒ 所以「上线」不是缺口，**「产出」才是**（41/128 = 32%）
★ 判据见 `docs/quality-audit.md` 附录三十九：**自己加的质量标准不能变成产出的前置条件。**
```