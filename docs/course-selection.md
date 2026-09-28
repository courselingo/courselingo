# 课程选择路线图 · Course Selection Roadmap

> **本文件是一份决策记录，不是愿望清单。** 它回答一个问题：**下一批翻译/讲解哪些课。**
> 判断只由两个已取证的输入相乘得出 ——（a）CS 自学指南社区实际推荐的课程，（b）**我们法律上能发布什么**。
> 核验日期：**2026-09-28**。本轮共抓取 **64 个页面 URL**（含子页面；另有 1 次 git tree API 调用与 1 次仓库归档下载），
> 全部用 `curl -x socks5h://127.0.0.1:7892`（方法沿用 [course-catalog.md](./course-catalog.md)，本机 DNS 为 Clash fake-IP，
> 必须走 SOCKS5；`000` 一律重试，从不当成「不存在」）。
> **本轮抓取物留在本机临时目录（未入库）**，因此每条结论都在正文里保留**逐字引用 + URL**，以便独立复现。
>
> 既有结论（6.824/6.5840、6.1810/6.S081、MIT OCW、CS 61A、15-445、CS 144）**原样复用**
> [course-catalog.md](./course-catalog.md)，本轮不重新推导，只在需要的地方引用。

---

## 1. 方法论

### 1.1 两个独立输入

**输入 A · 需求（社区推荐）= CS 自学指南**

<https://github.com/pkuflyingpig/cs-self-learning>（site: <https://csdiy.wiki/>，75,894 stars，**MIT License**）。
它是 `docs/<分类>/<课程>.md` 的结构。本轮用 GitHub git tree API **全量抓取**（`200`，99,821 B）：

| 项 | 实测值 |
| --- | --- |
| 分类数 | **25** |
| 课程页数（不含 `*.en.md`、不含 5 个非课程文档） | **131** |
| 文件组织 | `docs/操作系统/MIT6.S081.md` 形式，共 276 个 blob |

> **需求信号 = 「它被收录」＋「它被排在哪个分类」＋「它自己的难度/学时标注」，不是我们自己猜的热度。**
> 本文件引用的「社区为何看重」全部来自 csdiy 页面自身的文字或它给出的链接，一律标注来源。

**输入 B · 许可（我们能发布什么）= 我们实际要用的那份文件**

规则沿用 [content-policy.md](./content-policy.md)：**课程条款优先；未声明 = 保留所有权利；只有许可允许时才发布译文。**
本轮**不接受任何记忆或推断**，每条授权结论都必须落到「URL + 逐字原文 + 该原文出现在哪个页面」。

### 1.2 可发布形式分级（这是本文件的主轴）

| 级别 | 条件 | 我们能发布什么 |
| --- | --- | --- |
| **A · 翻译可做** | 许可**已核实**允许衍生（CC BY / BY-SA / BY-NC / BY-NC-SA / MIT 等） | 译文 + **双语原文对照** + 转载许可范围内的材料；须履行署名等义务 |
| **B · 仅讲解** | 未声明 / 保留所有权利 | **只发布我们自己独立撰写的原创讲解**；不产出逐字稿，不注入原文对照 |
| **C · 拒绝执行** | 课程**明确禁止传播** | 什么都不做（对应 `redistribution = "forbidden"`，`validate.py` 退出码 3） |

> **★ 本路线图最重要的一条结构性结论：**
> 在 9 个优先分类的英文课程里，**绝大多数是 B 级**。
> 「A 级」是一个**很小的集合**，而且几乎全部来自 **MIT OCW、ETH 的 DokuWiki、Berkeley CS168 的在线教材、以及两份 GitHub Pages 课程站的仓库 `LICENSE`**（外加 Nand2Tetris 的许可专页）。
> 这与既有结论同构：**6.824 也只能走讲解路线**（主页有徽章、讲义无声明）。
> **下一批的真正机会，就在这 10 来个 A 级来源里挑，而不是在 131 门课里平铺。**

### 1.3 优先级 = 需求 × 授权等级 × 差异化

**优先级 = 社区需求（csdiy 收录强度） × 授权等级（A 级加分） × 中文空白程度。**

第三条经常被忽略，但本轮取了证：csdiy 页面**自己**就列出了大量中文资源，例如

- CSAPP：「英语有困难的同学可以参考B站UP主九曲阑干对 CSAPP 的中文讲解」
- CS61B：「原版视频参见课程网站，B站有中文翻译搬运。」
- MIT 6.5940（EML）：「B站也有生肉和熟肉搬运」
- DDCA：「中文译本为《数字设计和计算机体系结构(原书第2版)》」（**指教材**，不是课程材料）

**已有成熟中文资源的课，翻译的边际价值低；中文完全空白的课，同一个工时值更多。**

### 1.4 本轮核验范围与动作

- 候选筛选：9 个优先分类（并行与分布式系统 / 操作系统 / 计算机网络 / 数据库系统 / 编译原理 /
  计算机系统基础 / 数据结构与算法 / 体系结构 / 机器学习系统）中的**全部英文授课课程 = 24 门**
  （另经 MIT OCW 补充核验 5 门跨分类课程）。
- 每门课**至少核两个页面**：入口页 + 一个真正承载材料的子页面（schedule / notes / labs / policies / assignments）。
- 补充核验 **第三方材料页**：教科书站（`textbook.cs168.io`）、许可专页（`nand2tetris.org/license`）、
  **GitHub Pages 课程站的源码仓库根 `LICENSE`**（这是本轮最大的方法论收益，见 §1.5 坑八）。
- 搜索词覆盖：`creativecommons`、`rel="license"`、`Copyright`、`licen[cs]e`、`MIT`、`CC BY`、`Apache`、
  `all rights reserved`、`terms of use`、`licenses/by*`；**一律抓原始 HTML，从不过滤标签后再搜**。
- 真 404 与抓取失败的区分：本轮唯一一次 404 结论（OCW 无 6.5940）是通过**读响应正文**
  确认的 —— `Page Not Found` / `Sorry, the page you requested was not found.`。

### 1.5 本轮新增的四个坑（补在既有七条之后）

| # | 坑 | 本轮实例 |
| --- | --- | --- |
| **八** | **GitHub Pages 类课程站，许可写在源码仓库的 `LICENSE` 里，页面本身一个字都没有。** 只抓页面 = 100% 假阴性 | **CSE 234**（`hao-ai-lab/cse234-w25` 根 `LICENSE` = **MIT**）与 **CMU 15-442/642**（`mlsyscourse.github.io` 根 `LICENSE` = **CC BY-NC 4.0**）**两条 A 级结论都是这样挖出来的** |
| **九** | 页面上出现的「MIT License」经常**不是**课程许可，而是模板自带的**图标库注释** | CS168 课程站命中 `MIT` 2 次 / `license` 4 次，逐字看全是 `<!-- Feather. MIT License … -->`、`<!-- Bootstrap Icons. MIT License … -->`；CS61B 同款。**这两门课的「MIT 命中数」一个都不能用**（既有结论里 CS 61A 也是同一现象） |
| **十** | OCW 的许可是**逐页复制**的；6.824 的徽章**只在主页**。两者不能互推 | OCW 6.006 / 6.858 的**课程页与讲义页**都带 `"license": "https://creativecommons.org/licenses/by-nc-sa/4.0/"`；而 6.824 讲义 0/0/0 |
| **十一** | 「有 CC 徽章」≠「可以做翻译」：**ND（NoDerivatives）明文禁止翻译** | MIT 6.1600 的 notes 仓库是 **CC BY-NC-ND 4.0**（既有结论）⇒ 该材料的**翻译路线被直接禁止**。这是开放许可里最反直觉的一类 |

---

## 2. 候选总表（24 门优先分类课程 + 5 条 OCW 补充）

> 语言一栏指**授课语言**。所有 24 门均为英文授课 —— 中文授课的课程不进入本表，见 §7。
> 「可发布形式」按 §1.2 的分级；`待核实` 表示某一部分未取得证据，见 §5。

| 课程 | 分类 | 学校 | 语言 | 授权结论 | 证据 URL | 可发布形式 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **CS168: Introduction to the Internet** | 计算机网络 | UC Berkeley | 英文 | ✅ **教材 CC BY-SA 4.0**（无 NC）；**课程站未声明** | <https://textbook.cs168.io/> · <https://sp25.cs168.io/> | **A（教材）** 译文＋原文对照，**可商用**，须 BY-SA；课程站按 B | **P0** |
| **CMU 15-442/15-642 ML Systems** | 机器学习系统 | CMU | 英文 | ✅ **CC BY-NC 4.0**（网站仓库根 LICENSE，无 SA） | <https://raw.githubusercontent.com/mlsyscourse/mlsyscourse.github.io/main/LICENSE> | **A** 译文＋原文对照（非商业、署名；**不传染**） | **P0** |
| **CSE 234: ML Systems / LLM Systems** | 机器学习系统 | UCSD | 英文 | ✅ **MIT License**（网站仓库根 LICENSE） | <https://raw.githubusercontent.com/hao-ai-lab/cse234-w25/main/LICENSE> | **A** 译文＋原文对照（**无 NC、无 SA，可商用**） | **P0** |
| **MIT 6.006 Introduction to Algorithms** | 数据结构与算法 | MIT（OCW） | 英文 | ✅ **CC BY-NC-SA 4.0**（课程页＋讲义页双重出现） | <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/> | **A** 译文＋原文对照（NC＋SA） | **P0** |
| **DDCA: Digital Design and Computer Architecture** | 体系结构 | ETH Zurich | 英文 | ✅ **CC BY-NC-SA 4.0**（wiki 的 start / lectures / schedule 三页一致） | <https://safari.ethz.ch/digitaltechnik/spring2023/> | **A（wiki 内容）** 译文＋原文对照（NC＋SA）；⚠️ YouTube 视频不做 | **P0** |
| **CA: Computer Architecture** | 体系结构 | ETH Zurich | 英文 | ✅ **CC BY-NC-SA 4.0**（同上，同一 DokuWiki 许可块） | <https://safari.ethz.ch/architecture/fall2022/doku.php?id=schedule> | **A（wiki 内容）** 同 DDCA；⚠️ 客座讲者材料须逐件复核 | **P0** |
| MIT 6.046J Design and Analysis of Algorithms | 数据结构与算法 | MIT（OCW） | 英文 | ✅ CC BY-NC-SA 4.0 | <https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/> | A（NC＋SA） | P1 |
| MIT 6.858 Computer Systems Security | 系统安全 | MIT（OCW） | 英文 | ✅ CC BY-NC-SA 4.0（课程页＋讲义页） | <https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/> | A（NC＋SA） | P1 |
| MIT 6.828 Operating System Engineering | 操作系统 | MIT（OCW，2012） | 英文 | ✅ CC BY-NC-SA 4.0，⚠️ **部分第三方图片被明确排除在 CC 之外** | <https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/> | A（NC＋SA），图片须逐件复核；内容偏旧 | P1 |
| MIT 6.035 Computer Language Engineering | 编译原理 | MIT（OCW，2010） | 英文 | ✅ CC BY-NC-SA 4.0，⚠️ **csdiy 未收录 ⇒ 无需求信号** | <https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/> | A（NC＋SA），仅作编译原理的许可明确替代品 | P1 |
| **Nand2Tetris** | 体系结构 | 希伯来大学 | 英文 | ✅ **CC BY-NC-SA 3.0 Unported**（专页，覆盖「all materials and tools」） | <https://www.nand2tetris.org/license> | A（NC＋SA），⚠️ **官方中文版已存在 ⇒ 暂缓** | P1（暂缓） |
| CS149 / CMU 15-418 Parallel Computing | 并行与分布式系统 | CMU + Stanford | 英文 | 🔴 未声明 → 保留所有权利（页脚 `Copyright 2021 Stanford University`） | <https://gfxcourses.stanford.edu/cs149/fall21> | B 仅讲解 | P1 |
| CS186 Introduction to Database Systems | 数据库系统 | UC Berkeley | 英文 | 🔴 未声明（主页＋syllabus 均 0 命中） | <https://cs186berkeley.net/syllabus/> | B 仅讲解 | P1 |
| CS143 Compilers | 编译原理 | Stanford | 英文 | 🔴 未声明（主页＋course_info 均 0 命中） | <http://web.stanford.edu/class/cs143/course_info.html> | B 仅讲解 | P1 |
| CS110 Principles of Computer Systems | 计算机系统基础 | Stanford | 英文 | 🔴 未声明（主页＋assign1 均 0 命中） | <https://web.stanford.edu/class/archive/cs/cs110/cs110.1204/assign1/> | B 仅讲解 | P1 |
| CS170 Efficient Algorithms and Intractable Problems | 数据结构与算法 | UC Berkeley | 英文 | 🔴 **保留所有权利**：`Copyright ©2026, Regents of the University of California and respective authors.` | <https://cs170.org/policies/> | B 仅讲解 | P1 |
| CS61B Data Structures | 数据结构与算法 | UC Berkeley | 英文 | 🔴 未声明（主页＋policies 仅图标库 MIT 注释） | <https://sp24.datastructur.es/policies/> | B 仅讲解 | P1 |
| CS61C Great Ideas in Computer Architecture | 体系结构 | UC Berkeley | 英文 | 🔴 未声明（主页＋当前学期页均 0 命中） | <https://cs61c.org/fa26/> | B 仅讲解 | P1 |
| CMU 10-414/714 Deep Learning Systems | 机器学习系统 | CMU | 英文 | 🔴 未声明（主页＋assignments 仅 Jekyll 主题版权行） | <https://dlsyscourse.org/assignments/> | B 仅讲解 | P1 |
| MIT 6.5940 TinyML / Efficient DL Computing | 机器学习系统 | MIT | 英文 | 🔴 未声明开放许可：`Copyright © MIT Han Lab.`；**OCW 无此课** | <https://hanlab.mit.edu/courses/2023-fall-65940> | B 仅讲解（B 站已有熟肉，差异化中） | P1 |
| CMU 15-799 Self-Driving DBMS | 数据库系统 | CMU | 英文 | 🔴 未声明（主页＋schedule 均 0 命中） | <https://15799.courses.cs.cmu.edu/spring2022/schedule.html> | B 仅讲解 | P1 |
| CS122 Database System Implementation | 数据库系统 | Caltech | 英文 | 🔴 未声明（主页＋lectures 均 0 命中） | <http://courses.cms.caltech.edu/cs122/lectures> | B 仅讲解 | P1（低） |
| CS346 Database System Implementation | 数据库系统 | Stanford | 英文 | 🔴 未声明（主页＋notes 均 0 命中） | <https://web.stanford.edu/class/cs346/2015/notes/old/buffer.html> | B 仅讲解 | P1（低） |
| Neural Networks: Zero to Hero | 人工智能 | Andrej Karpathy | 英文 | 🔴 未声明（主页 0 命中） | <https://karpathy.ai/zero-to-hero.html> | B 仅讲解；视频另受 YouTube 条款 | P1（低） |
| **CS162 Operating Systems** | 操作系统 | UC Berkeley | 英文 | ⛔ **明确禁止传播** | <https://cs162.org/policies/> | **C 拒绝执行** | **P2** |
| **KAIST CS420 Compiler Design** | 编译原理 | KAIST | 英文 | 🔴 **无 LICENSE**（`main`/`master` 均 404，README 无许可措辞） | <https://github.com/kaist-cp/cs420> | C/B —— 翻译不做；走 OCW 6.035 替代 | **P2** |
| **Algorithms 4th ed.（Algo）** | 数据结构与算法 | Princeton | 英文 | ⛔ **明文 `All rights reserved.`** | <https://algs4.cs.princeton.edu/home/> | P2（不做） | **P2** |
| **CS:APP（CSAPP）** | 计算机系统基础 | CMU | 英文 | ⛔ 商业教材（页脚 `Copyright © 2015,` Pearson）；站点无 CC | <http://csapp.cs.cmu.edu/> | P2（不做翻译） | **P2** |
| **Kurose & Ross《计算机网络：自顶向下方法》（topdown）** | 计算机网络 | UMass | 英文 | ⛔ 商业教材 `Copyright © 2010-2025 J.F. Kurose, K.W. Ross` | <https://gaia.cs.umass.edu/kurose_ross/index.php> | P2（不做） | **P2** |

> 表中 6.006 / 6.046J / 6.858 / 6.828 / 6.035 五行是**跨分类补充核验**：csdiy 的分类里只有
> 6.006 与 6.046 被收录（「数据结构与算法」），其余三门是**同许可等级的可用来源**，
> 但它们的需求信号强弱不同，已在表中注明。

---

## 3. 第一梯队（建议紧接着做）

**入选条件（三条同时满足）**：① 授权**已核实为 A 级**（可做真正的翻译，这是与 B 站搬运的核心差异）；
② 社区需求由 csdiy 收录与标注证实；③ **中文空白**或中文资源明显不足。

### 3.1 MIT 6.006 Introduction to Algorithms · 数据结构与算法

| 项 | 内容 |
| --- | --- |
| 是什么 | MIT OCW **Fall 2011** 版，**24 讲**（讲义页表格 33 行），配套作业与考试；教材 CLRS |
| 社区为何看重 | csdiy「数据结构与算法」分类收录，标注**难度 5 星、预计 100h+**，先修「计算机导论(CS50/CS61A)」——它是社区算法自学的第一站 |
| 中文空白 | csdiy 页面只给出 B 站视频搬运链接（`BV1b7411e7ZP`），**没有中文讲义或中文讲解** |
| 授权 | ✅ **CC BY-NC-SA 4.0**（已核实两处） |
| 证据（逐字） | 课程页与讲义页**都**含：`"license": "https://creativecommons.org/licenses/by-nc-sa/4.0/"` 与 `<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">Creative Commons License</a>` |
| 证据 URL | <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/> · <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/pages/lecture-notes/>（2026-09-28 访问） |
| 可发布 | **A 级**：译文、双语原文对照、术语表、学习路径。义务：**署名 + 非商业 + 相同方式共享（产出必须以 CC BY-NC-SA 4.0 发布）** |
| 工时（推断，非核实） | 先行 **8 讲**，参照现有单位产出（6.824 的 3 讲 + 2 篇导读 = 3.6 万字）估算 **6–8 万字**，3–4 周 |
| 备注 | ⚠️ OCW 材料里可能夹带**被明确排除在 CC 许可之外**的第三方内容：6.828 页面即有 `All rights reserved. This content is excluded from our Creative Commons license.` 的标注（6.006 页面本轮**未见**同类标注，但这不等于没有）⇒ **配图一律逐件复核，不直接搬运** |

### 3.2 UC Berkeley CS168 Introduction to the Internet · 计算机网络（教材 CC BY-SA 4.0）

| 项 | 内容 |
| --- | --- |
| 是什么 | Berkeley 本科网络课（`sp25.cs168.io`），配套**在线教材** `textbook.cs168.io`：**8 大章、52 个章节页**，源码在官方仓库 `berkeley-cs168/textbook`，**截至 2024 Fall 学期仍在维护** |
| 社区为何看重 | csdiy「计算机网络」分类收录，标注**难度 3 星、约 140 小时**，描述为「Internet 的设计原则与核心协议……结合理论与实践」（traceroute / 路由 / TCP 三个项目） |
| 中文空白 | csdiy 页面**没有给出任何中文资源**（对比 CSAPP/CS61B 都有） |
| 授权 | ✅ **CC BY-SA 4.0** —— **这是本轮唯一「允许商用」的课程级开放许可（无 NC）** |
| 证据（逐字） | 教材页面 License 段：`This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.`；同页 `rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"` 与 `i.creativecommons.org/l/by-sa/4.0/88x31.png` 徽章 |
| 证据 URL | <https://textbook.cs168.io/>（2026-09-28 访问） |
| 可发布 | **A 级（仅教材）**：译文 + 原文对照 + **可商用**；义务 = 署名 + **以 CC BY-SA 4.0 发布衍生作品（SA 传染，但无 NC）** |
| ⚠️ 范围限定 | **课程站 `sp25.cs168.io` 未声明任何许可**：主页与 `/policies/` 均 0 命中（`license` 的 4 次命中全部是图标库注释）。⇒ **课程站的讲义/项目仍按 B 级处理，只做讲解。** 教材与课程站是两套授权 —— 与「CS 61A 站 vs Composing Programs」同一模式 |
| 工时（推断） | 先做 **6 节**（分层与寻址 / 路由 / 可靠传输 / 拥塞控制 / TCP / 应用层）≈ **5 万字**，约 3 周 |
| 为什么排第一梯队 | 它是**唯一不受 NC 约束**的选择。商业化路径（会员、付费专栏）在 BY-SA 下不受阻，而其余 A 级全部带 NC |

### 3.3 CMU 15-442/15-642 Machine Learning Systems · 机器学习系统

| 项 | 内容 |
| --- | --- |
| 是什么 | CMU 研究生课，**Tianqi Chen / Zhihao Jia** 讲授；排期页 30 行，覆盖 ML 系统全栈：自动微分、线性代数优化、GPU 架构与 CUDA、Transformer、数据并行与 ZeRO、模型/流水线并行、内存优化、ML 编译器、TIRx 算子 |
| 社区为何看重 | csdiy「机器学习系统」分类收录，标注**难度 4 星、100h+**；且它是本仓库已有 **6.824（分布式）** 能力的直接延续 —— 分布式训练就是分布式系统的下游 |
| 中文空白 | csdiy 页面**无任何中文资源** |
| 授权 | ✅ **CC BY-NC 4.0** —— **约束最轻的课程级开放许可之一（有 NC、无 SA）** |
| 证据（逐字） | 网站源码仓库根 `LICENSE` 全文首行：`Attribution-NonCommercial 4.0 International`；正文：`Creative Commons Attribution-NonCommercial 4.0 International Public License` |
| 证据 URL | <https://raw.githubusercontent.com/mlsyscourse/mlsyscourse.github.io/main/LICENSE>（2026-09-28 访问）；课程站 <https://mlsyscourse.org/schedule> |
| 可发布 | **A 级**：译文 + 原文对照。义务 = **署名 + 非商业**；**无 SA ⇒ 我们的产出不必被拖成 CC**（这正是它的价值：不与 6.824 仓库的授权边界冲突） |
| ⚠️ 范围限定 | LICENSE 位于**网站仓库**，覆盖网站托管的内容；**作业代码在 `mlsyscourse/assignment*` 三个独立仓库，本轮未核** ⇒ 作业按 B 级/不产出处理（见 §5） |
| 工时（推断） | 先做 **5 讲**（ML 系统概览 / 自动微分 / GPU 与 CUDA / 数据并行与 ZeRO / 模型与流水线并行）≈ **5–6 万字**，约 4 周 |

### 3.4 ETH Zurich DDCA → Computer Architecture · 体系结构（两门一条线）

| 项 | 内容 |
| --- | --- |
| 是什么 | Onur Mutlu 的 ETH 课，**两门成链**：**DDCA**（Spring 2023）从布尔代数到 MIPS CPU，9 个实验；**CA**（Fall 2022）是其进阶（流水线、cache、内存系统）。CA 排期页含 **107 个 wiki 托管文件**与 **43 个 YouTube 链接** |
| 社区为何看重 | csdiy「体系结构」分类收录两门，并明确把 DDCA 标为 CA 的**先修**；页面反馈「从课程本身的难度上说，至少高于 CS61C，课程的部分内容十分前沿」 |
| 中文空白 | ⚠️ 页面里的「中文译本为《数字设计和计算机体系结构(原书第2版)》」指的是**教材**（Harris & Harris），**课程材料本身没有中文版** |
| 授权 | ✅ **CC BY-NC-SA 4.0**，**在 3 个页面上一致出现** |
| 证据（逐字） | `Except where otherwise noted, content on this wiki is licensed under the following license:` + `CC Attribution-Noncommercial-Share Alike 4.0 International`，并带 `rel="license"` ×2 与徽章图 |
| 证据 URL | <https://safari.ethz.ch/digitaltechnik/spring2023/> · <https://safari.ethz.ch/architecture/fall2022/doku.php?id=lectures> · <https://safari.ethz.ch/architecture/fall2022/doku.php?id=schedule>（2026-09-28 访问） |
| 可发布 | **A 级**：译文 + 原文对照 + wiki 托管文件（`lib/exe/fetch.php?media=…` 形式的 107 个 PDF/PPTX 属于「content on this wiki」）。义务 = **署名 + 非商业 + 相同方式共享** |
| ⛔ 明确不做 | **YouTube 视频**：CA 排期页有 43 个 YouTube 链接，视频本体受**平台条款**约束，与 6.824 的 2020 视频同一处理 —— **不转载、不做字幕翻译** |
| ⚠️ 逐件复核项 | 「Except where otherwise noted」不是空话：wiki 上托管了**客座/第三方讲者材料**（例：`adeeperlookintorowhammer_micro21-talk.pdf` 是 MICRO'21 论文报告）⇒ 这部分不能默认继承 wiki 许可 |
| 工时（推断） | 先做 **DDCA 前 6 讲**（布尔代数 → 组合逻辑 → 时序逻辑 → 指令集 → 单周期 CPU → 流水线）≈ **5 万字**，4–5 周；CA 作为下一阶段 |
| 方法学意义 | 这是本仓库**第一次把许可核到「材料页」而不是只核入口页**（`start` ＋ `lectures` ＋ `schedule` 三处一致），正是 6.824「坑二」的正面案例 |

### 3.5 第一梯队的排序理由（一句话版）

| 顺序 | 课程 | 一句话理由 |
| --- | --- | --- |
| 1 | CS168 | 唯一**可商用**（BY-SA，无 NC），中文完全空白 |
| 2 | MIT 6.006 | 受众最大（算法入门），许可链条最干净（课程页＋讲义页双重取证） |
| 3 | CMU 15-442 | 最热方向 × **无 SA**（不污染我们的发布协议）× 与 6.824 能力协同 |
| 4 | ETH DDCA→CA | 中文空白 × 系统纵深 × 许可核到材料页 |
| 备 1 | **CSE 234** | **MIT License（许可最宽松：无 NC、无 SA、可商用）**；因与第 3 项同属「机器学习系统」而暂列 §4，**一旦第 3 项的 NC 约束影响商业化，立即顶上** |

---

## 4. 第二梯队（可做，稍后）

### 4.1 A 级但本轮暂缓（许可已核实，理由逐条给出）

| 课程 | 授权 | 暂缓理由（不是许可问题） |
| --- | --- | --- |
| **UCSD CSE 234** | **MIT License** | 与第一梯队 3.3 **同分类**，避免同期双开；但它是全场**许可最宽松**的一项，且 csdiy 标注 120 小时、含 Triton/FlashAttention/推理系统等热点 ⇒ **第一顺位备选** |
| **MIT 6.046J** | CC BY-NC-SA 4.0 | 与 6.006 同许可、同义务，**建议与 6.006 打包成「算法双课」**，一次讲清 NC＋SA 的落地方式 |
| **MIT 6.858** | CC BY-NC-SA 4.0 | 材料完整（讲义页 25 行），但属**系统安全**分类（非本轮优先分类） |
| **MIT 6.828** | CC BY-NC-SA 4.0 | ⚠️ 版本为 **2012**，内容偏旧；且我们已有 6.1810/6.S081 在飞。页面显式标注部分第三方图片**被排除在 CC 许可之外** |
| **MIT 6.035** | CC BY-NC-SA 4.0 | ⚠️ **csdiy 未收录 ⇒ 需求信号缺失**。价值在于：当我们想覆盖「编译原理」时，它比 CS143 / CS420 有**明确的许可依据** |
| **Nand2Tetris** | CC BY-NC-SA 3.0 Unported | ⚠️ **官方中文版已在市面**（csdiy 页面直接链接了《计算机系统要素：从零开始构建现代计算机》周维译本的扫描 PDF）⇒ 逐字翻译差异化低；课程视频在 Coursera（平台条款） |

Nand2Tetris 授权原文（逐字，来自其**专门的许可页**）：

> "All Nand to Tetris materials and tools and every item appearing in this website are protected under a Creative Common Attribution-NonCommercial-ShareAlike 3.0 Unported License."

同页还有一条与我们的硬规则同向的请求（逐字）：

> "We believe that students and self-learners who set out to do the hardware and software projects should have the benefit and challenge of doing original work, without seeing published solutions."

⇒ **Lab 解答永久排除**，与 6.824 / CS 144 / CS 61A 同一处理。

### 4.2 B 级：只做原创讲解（需求在，但许可不允许译文）

这些课**法律上可做**（自己写讲解，不复制对方表达），但**不能**产出逐字稿与原文对照。
排序按「需求强度 ÷ 已有中文资源」：

| 课程 | 需求依据（csdiy） | 已有中文资源（差异化） | 建议 |
| --- | --- | --- | --- |
| **CS149 Parallel Computing** | 「并行与分布式系统」分类，难度 5 星、150h | 未见中文翻译 | **B 级里最优先**：与 6.824 同一知识域，可复用我们的术语表 |
| **CS186** | 「数据库系统」难度 5 星、150h | 仅 B 站视频搬运 | 数据库分类里**唯一需求与材料都够**的一门（15-445 已判红线） |
| **CS143 Compilers** | 「编译原理」难度 5 星、150h | 仅 B 站视频搬运 | 编译原理的 B 级首选；若坚持要 A 级，走 OCW 6.035 |
| **CS110** | 「计算机系统基础」难度 5 星、150h | 未见中文翻译 | 与 CSAPP 互为补充；CSAPP 因商业教材＋已有中文讲解而被判不做 |
| **CS170 / CS61B / CS61C** | 均为 Berkeley 热门课（3–4 星，60–100h） | CS61B 已有「B站中文翻译搬运」 | 均可做讲解；CS61B 因已有中文搬运而降序 |
| **CMU 10-414/714** | 「机器学习系统」难度 3 星、100h | 未见中文翻译 | 与第一梯队 3.3 同域，作为补充而非并行 |
| **MIT 6.5940 / EML** | 「机器学习系统」难度 4 星、50h | **B 站已有「生肉和熟肉搬运」** | 讲解仍可做，但翻译路线已被 B 站熟肉抢先 |
| **CMU 15-799 / Caltech CS122 / Stanford CS346** | 数据库系统分类 | 未见中文翻译 | 优先级低：需求与材料密度都不及 CS186 |
| **Karpathy: Zero to Hero** | 「人工智能」分类，约 19 小时 | 中文讲解较多 | 优先级低；且视频本体受 YouTube 条款 |

---

## 5. 待核实

> 规则：**未取证的一律写 `未确认`，并写清「查了什么、缺什么」。** 以下都不是「已确认无许可」。

| # | 对象 | 已查 | 缺什么 |
| --- | --- | --- | --- |
| 1 | **CS168 课程站其余材料**（讲义、三个项目、discussion） | 主页与 `/policies/` 均 0 命中（`license` 的命中全是图标库注释）；`/projects/` 取回 404 | 课程站**没有任何许可声明**；教材的 BY-SA 是否被课程站承接，**无依据**。⇒ 课程站按 B 级处理，除非找到书面依据 |
| 2 | **`mlsyscourse/assignment1`、`assignment-distributed-training`、`assignment-tirx-gemm`** | 未抓取 | 三个作业仓库各自的 LICENSE；课程站的 CC BY-NC 4.0 是否覆盖它们 |
| 3 | **CSE 234 的作业材料** | 网站仓库根 `LICENSE` = MIT License；`/assignments/` 页面 0 命中 | 作业是否托管在**另一个仓库**（若在网站仓库内，则随 MIT）；以及 `LICENSE` 里的 "Copyright (c) 2024 DSC 204A" 与 CSE 234 的对应关系 |
| 4 | **ETH wiki 上「otherwise noted」的客座讲者材料** | 确认 wiki 许可块在三页一致 | 逐个文件是否有独立声明（例：`adeeperlookintorowhammer_micro21-talk.pdf`、`2022.11.25_sibyl_before.pdf`） |
| 5 | **SEED Labs**（系统安全，csdiy 收录） | 站点与实验室索引页仅有 `Copyright © Wenliang Du, wedu@acm.org`，**0 处许可措辞** | 具体 lab 文档（PDF/网页）是否另有 CC 声明 —— **站点无声明不等于 lab 无声明**（CS 144 就是这样被漏掉的） |
| 6 | **OSTEP《Operating Systems: Three Easy Pieces》教材**（csdiy 的 NJUOS 页把它列为课程教材，`pages.cs.wisc.edu/~remzi/OSTEP/`） | 该页 **11 项关键词全部 0 命中** | 章节 PDF 内页是否含许可声明；网上常见「OSTEP 是 CC 授权」的说法**本轮未取到证据，不得引用** |
| 7 | **KAIST CS420** | `README.md` 无许可措辞；`LICENSE` 在 `main`/`master` 两个分支**均 404** | GitHub 的 404 对「仓库不存在」与「文件不存在」是二义的（既有坑五）；**结论只能是「无 LICENSE」，不能写成「作者拒绝授权」** |
| 8 | **MIT 6.1810 讲义文件的覆盖范围** | 沿用既有结论（主页有 CC BY 3.0 US 徽章，**其讲义文件未单独取证**） | 与 6.824 讲义同样的取证动作 |
| 9 | **MIT 6.5940 是否有 OCW 版本** | ✅ **已确认没有**：`https://ocw.mit.edu/courses/6-5940-tinyml-…-fall-2023/` 返回 404，且**正文**为 `Page Not Found` / `Sorry, the page you requested was not found.`（真 404，非抓取失败） | 无（此项已闭环，留档以示范「真 404 怎么确认」） |
| 10 | CS168 教材仓库根 `LICENSE` | `https://raw.githubusercontent.com/berkeley-cs168/textbook/main/LICENSE` 返回 **404 / 一次 000** | 默认分支名或文件路径未定。**不影响教材本体结论** —— 许可逐字写在渲染后的教材页上 |

---

## 6. 明确不做

> 这一节是**说「不」的地方**。理由只有两类：**课程条款不允许**，或**法律上没有依据**。

| 课程 | 结论 | 依据（逐字引用） |
| --- | --- | --- |
| **UC Berkeley CS162** | ⛔ **全站不做（含原创讲解）** —— C 级 | `/policies/` 页 Copyright 段：`All course materials are protected by US copyright law and by university policy. Under no circumstances are students permitted to upload course materials online or distribute these materials to anyone enrolled or not enrolled in the course. This policy will be enforced during and after the course.` |
| **Princeton Algorithms 4th ed.（Algo）** | ⛔ 不做 | 站点明文：`All rights reserved.` |
| **CS:APP / CMU 15-213** | ⛔ 不做翻译 | 教材为商业出版物（页脚 `Copyright © 2015,`），站点无 CC 声明；**且 csdiy 页面自己就在推荐 B 站中文讲解** ⇒ 差异化也不成立 |
| **Kurose & Ross《计算机网络：自顶向下方法》** | ⛔ 不做 | 商业教材：`Copyright © 2010-2025 J.F. Kurose, K.W. Ross` |
| **KAIST CS420** | ⛔ 不做翻译 | 无 `LICENSE`（两个分支均 404）⇒ 保留所有权利；**替代方案**：编译原理走 MIT OCW 6.035（CC BY-NC-SA 4.0，已核实） |
| **MIT 6.1600** | ⛔ **翻译路线被明文禁止** | notes 仓库 **CC BY-NC-ND 4.0**（既有结论）——**ND = NoDerivatives**，翻译即衍生作品。这是「有 CC 徽章」却不能翻译的唯一一类，务必记住 |
| **UC Berkeley CS 61A** | ⛔ 不做翻译（既有结论） | `Copyright ©2026, Regents of the University of California and respective authors.`；syllabus：`Do not post your solutions publicly during or after the semester.` |
| **CMU 15-445** | ⛔ 不做翻译（既有结论） | 全部核验页面**无任何许可标注** |
| **Stanford CS 144 站点** | ⛔ 不做翻译（既有结论） | 站点无声明；实验 README 自订条款仅授予「公开可读」 |
| **全部课程的 Lab / 作业解答** | ⛔ **永久排除（硬规则）** | 6.824、6.1810、CS 144、CS 61A、Nand2Tetris 五处**各自**都有禁发解答的条款；这是著作权与学术诚信的双重风险 |

> **保留的中间结论**（不要简化）：CS162 的条款**措辞面向学生**，严格讲它约束的是选课学生而非第三方；
> 但本项目 [content-policy.md](./content-policy.md) 的既定立场是「课程明确说了不要传播 ⇒ 我们不做，
> 这是比法律底线更保守的政策性选择」。**若将来要动 CS162，正确路径是先取得讲师/院系书面授权，而不是先发布。**

---

## 7. 不适用（中文授课，翻译无对象）

CS 自学指南的 131 门课里，有相当一部分**本身就是中文课**。**中文 → 中文不需要翻译**，
因此它们既不进授权核验流程，也不消耗任何许可调查工时。

| 分类 | 课程 | 为什么是「不适用」（而不是「不做」） |
| --- | --- | --- |
| 操作系统 | **HITOS**（哈尔滨工业大学）、**NJUOS**（南京大学，蒋炎岩） | 中文授课，视频与讲义均为中文（icourse163 / jyywiki.cn / B 站）；csdiy 原文即称「在 B 站观看了蒋老师的课程视频」 |
| 编译原理 | **NJU-Compilers**、**PKU-Compilers**、**SJTU-Compilers**、**USTC-Compilers** | 四门全部中文授课；其中三门有中文实验文档（Koopa IR 等） |
| 计算机网络 | **topdown_ustc**（中国科学技术大学，**授课教师：郑烇、杨坚**） | 中文授课＋中文课件（`staff.ustc.edu.cn/~qzheng/`）；csdiy 原文：「课程视频是郑烇老师本人在哔哩哔哩上上传的」 |
| 机器学习系统 | **AICS**（中国科学院大学）、**MLC**（机器学习编译） | AICS 为国科大中文课；**MLC 的官方站点本身就带中文版**（`mlc.ai/zh/`）—— 官方中文优先，我们再做一遍没有意义 |
| 编程语言设计与分析 | **NJU-SoftwareAnalysis**、**PKU-SoftwareAnalysis** | 两校中文课程 |
| 计算机图形学 | **GAMES101 / GAMES103 / GAMES202**、**USTC ComputerGraphics** | 三门前者的课程视频主入口是 **B 站**（csdiy 页面逐字：`课程视频：[bilibili](…)`）与中文平台 `games-cn.org`，即中文授课；USTC 那门是中文课 |
| 深度学习 | **LHY**（李宏毅，台湾大学） | 中文授课（课程页标注「國立台灣大學」） |
| 必学工具 | **翻墙 / 信息检索 / CMake / Docker / Emacs / Git / GitHub / GNU_Make / LaTeX / Scoop / thesis / tools / Vim / workflow**（14 篇） | **它们不是课程，是社区中文原创教程。** 既不构成翻译需求，其内容版权也属于 csdiy 作者本人（受该仓库 MIT 许可覆盖，与我们无关） |

**合计：中文授课课程 16 门 ＋ 必学工具 14 篇（非课程）。**

> 说明：把它们判为「不适用」**不是**贬低 —— 恰恰相反，这些课是我们做中文讲解时要**对标**的对象：
> 它们已经占据了「中文 × 这些主题」的位置，所以我们选择英文课做翻译，是**避让**而不是竞争。

---

## 8. 一个诚实的提醒

**CS 自学指南这个仓库是 MIT License 的，但这只能给我们一件东西：引用它的「选课清单」。**

已核实（本轮从仓库压缩包内直接读取）：

```
MIT License
Copyright © <2021> <copyright Yinmin Zhong>
```

站点头还另有一行 `copyright: Copyright © 2021-present PKUFlyingPig`（`mkdocs.yml`）。

**它允许的**：

- 复制、改编、再发布**它自己写的文字与结构** —— 也就是那 131 个课程页的**介绍、分类、推荐顺序**；
- 意味着我们可以正当地写「**我们按 CS 自学指南的分类与推荐顺序选课**」，并标明来源与许可。这也是本文件
  §1.1、§3、§4 能大量引用 csdiy 原文的原因。

**它不允许的（这是关键）**：

- **MIT 只覆盖仓库作者自己写的东西。它对仓库里那些链接指向的课程，授予我们零权利。**
  一个 MIT 的清单，指向的是一堆「保留所有权利」的课程网站 —— 清单的许可不能沿链接传染。
- 同理，csdiy 页面里推荐的**社区笔记仓库**（如 `PKUFlyingPig/MIT6.824`、`PKUFlyingPig/CS61B`）
  是**第三方作品**，各自的许可互不相同，**不能由 csdiy 的 MIT 推及**。
- 我们对 csdiy 的引用**仅限于「选择与推荐」这一个层面**。一旦开始翻译某门课，适用的是**那门课自己的条款**
  —— 也就是本文件全部授权核验工作的对象。

**推论（写给维护者）**：

1. **「CS 自学指南推荐了它」不是授权依据，只是需求依据。** 两者必须始终分开记账。
2. 我们的发布协议必须**按来源分层**：代码 MIT / 原创内容 CC BY 4.0（[content-policy.md](./content-policy.md)）；
   一旦改编了 NC 或 SA 材料，**该仓库的产出必须按上游条款发布**。
   **一课程一仓库的隔离设计正是为此而存在** —— 本路线图的第一梯队里既有 BY-SA（CS168）、
   BY-NC（15-442）、MIT（CSE 234）、也有 BY-NC-SA（OCW / ETH），**这四类绝不能混进同一个仓库**。
3. 任何一次「引用」，都要能回答：**我引用的是它的清单，还是它的内容？** 前者 MIT 覆盖，后者不覆盖。

---

## 附：本文件的证据强度自评

| 强度 | 含义 | 本文件中的例子 |
| --- | --- | --- |
| **已核实** | 抓取了确有该措辞的页面，留了逐字引用与 URL | CS168 教材 CC BY-SA 4.0；15-442 的 CC BY-NC 4.0；CSE 234 的 MIT License；OCW 五门；ETH 两门；Nand2Tetris；CS162 的禁止传播条款；CS170 的 UC 版权行；Algo 的 All rights reserved |
| **推断** | 由已核实事实推出的行为建议，**不是**许可结论 | 「A 级可做译文」；工时估算；优先级排序 |
| **头脑风暴** | 未取证的判断，明确标出 | 「一旦 NC 影响商业化，CSE 234 顶上」这类策略设想 |
| **未确认** | 查过但没拿到依据，见 §5 | CS168 课程站；三个 mlsyscourse 作业仓库；SEED Labs 的 lab 文档；OSTEP；KAIST CS420 的 `LICENSE` |

> **最后一条规则，比本文件全部内容都重要：条款未核实 = 不发布。**
> 需要逐字稿或字幕翻译的课程，正确路径是**先写信取得授权**，而不是先发布再说。
