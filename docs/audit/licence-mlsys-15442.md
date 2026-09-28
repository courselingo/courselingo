# 授权核实：CMU 15-442 / 15-642 Machine Learning Systems（mlsyscourse）

> 核实日期 **2026-09-28**。方法：`curl.exe` 直连 GitHub（`raw.githubusercontent.com` 直连可用），
> 课程站页面经 `-x socks5h://127.0.0.1:7892` 抓**原始 HTML**。
> 状态：**逐页 + 逐材料核实完成**。本文件不写课程正文，只给判定与最短逐字证据。
> 结论：**A 级（可翻译）**，但**仅限课程自制材料**；三条排除项见 §4。

## 0. 一句话结论

仓库根 `LICENSE` = **CC BY-NC 4.0**（全文 19,342 B，**无 ShareAlike、无 NoDerivatives**）
⇒ 课程自制讲义与网页文本**可以翻译**（非商业 + 署名 + 标注改动）；
但 **`slides/` 里混放了三份第三方客座/业界演讲**，**作业仓库另有 4 个连 `LICENSE` 都没有** —— 这两块一律不碰。

## 1. 核对清单（对应 `content-policy.md` 的逐课程复核清单）

| 复核项 | 结果 |
| --- | --- |
| 网页页面是否有许可声明 | ❌ **0 命中**（首页 / schedule / materials 均 0；logistics 唯一命中是**被注释掉**的旧版本语，见 §3.2） |
| **源码仓库根 `LICENSE`** | ✅ **CC BY-NC 4.0**（这是本课程唯一的有效授权声明 —— 坑八的又一次命中） |
| 我们实际依据的那份文件（`slides/*.pdf`） | ✅ 与 `LICENSE` 同仓库（`mlsyscourse/mlsyscourse.github.io`），就课程自制讲义而言授权成立 |
| 是否有 ND（禁止翻译） | ❌ 无。全文 `NoDerivatives` **0 命中** ⇒ 翻译（衍生作品）被允许 |
| 是否有 SA（传染） | ❌ 无。全文 `ShareAlike` **0 命中** ⇒ 不必以同一协议发布 |
| 是否有 NC | ⚠️ **有** ⇒ 我们的译文**不得商用**（详见 §5，这里修正了路线图的一处措辞） |
| 讲义 PDF 内部是否另有声明 | ❌ 抽样 2 份自制讲义：只有**内嵌字体许可**（Monotype/Microsoft/Calibri），见 §3.4 |
| 作业 / Lab 题面与答案 | ⛔ 见 §4.2：3 个作业仓库 `LICENSE` **真 404**；且本项目红线永久排除解答 |
| 讲义视频 | — 本课程 schedule 不含视频链接（客座场次无 slides 链接） |

## 2. 逐材料判定表

| 材料 | URL | 逐字证据 | 判定 | 我们能发布什么 |
| --- | --- | --- | --- | --- |
| **仓库根 LICENSE**（唯一有效声明） | <https://raw.githubusercontent.com/mlsyscourse/mlsyscourse.github.io/main/LICENSE>（19,342 B，200） | 第 1 行：`Attribution-NonCommercial 4.0 International`；正文：`Creative Commons Attribution-NonCommercial 4.0 International Public License`；`ShareAlike` 0 命中 / `NoDerivatives` 0 命中 | **allowed（带 NC）** | 译文 + 原文对照，**非商业**，署名 + 标注改动 |
| 课程首页 | <https://mlsyscourse.org/>（200，10,945 B） | 许可/版权类关键词 **0 命中** | unknown（页面本身） | 页面文本可随仓库 LICENSE 使用；页面本身无独立声明 |
| 课程 schedule | <https://mlsyscourse.org/schedule>（200，22,941 B） | **0 命中** | unknown（页面本身） | 同上 |
| 课程 materials | <https://mlsyscourse.org/materials>（200，4,816 B；源文件 `materials.md` 785 B） | **0 命中** | unknown（页面本身） | 链接第三方教材（d2l.ai / mlsysbook.ai）≠ 转载授权，只链接 |
| 课程 logistics | <https://mlsyscourse.org/logistics>（200，25,111 B；源文件 `logistics.md` 18,359 B） | 唯一命中是 **HTML 注释**（已停用）：`<!-- Please feel free to reuse any of these course materials that you find of use in your own courses. We ask that you retain any copyright notices, and include a written notice indicating the source of any materials you use. -->` | unknown（**注释 = 非生效声明**） | 不作为授权依据；仅作「课程方历史上曾欢迎复用」的旁证 |
| **课程自制讲义**（`slides/01…19*.pdf`、`data_layout/`、`modern-gpu-gemm/`、`tirx-gemm/`） | 例 <https://raw.githubusercontent.com/mlsyscourse/mlsyscourse.github.io/main/slides/01-course-introduction.pdf> | 与 LICENSE 同仓库（`git/trees/main?recursive=1` 可见 `blob 1624658 slides/01-course-introduction.pdf`）；schedule 页 `href="/slides/01-course-introduction.pdf"` | **allowed（带 NC）** | **译文 + 双语原文对照**；须署名 + 非商业 + 标注改动 |
| ⛔ 客座/业界讲义 1 | `slides/HaibinLinTalk.pdf`（5,045,323 B） | 首屏逐字（去字距后）：`Haibin Lin, Bytedance Seed - MLSys Building LLM Training Systems at Scale`；**`_data/lectures.yml` 与 schedule 均未收录** | **forbidden-by-third-party（排除）** | 不译、不转载（权利人非课程方，课程方无权以 CC 授权） |
| ⛔ 客座/业界讲义 2 | `slides/tim_quantization.pdf`（5,437,889 B） | 首屏逐字（PDF 内按 -3 偏移编码，解码后）：`EFFICIENT FOUNDATION MODELS VIA QUANTIZATION TIM DETTMERS`；未收录于 schedule | **排除** | 不译、不转载 |
| ⛔ 客座/业界讲义 3 | `slides/FlashInferCMU.pdf`（2,371,726 B） | 首屏逐字：`Efficient and Customizable Kernel Generation for LLM Inference Serving / Zihao Ye / Apr 9th, 2025 / Guest Lecture at @CMU Machine Learning Systems / University of Washington & NVIDIA` | **排除** | 不译、不转载 |
| 作业仓库 `assignment1` / `assignment2` / `assignment-distributed-training` | `…/mlsyscourse/assignment1/main/LICENSE` 等 | **真 404**（响应体 14 B `404: Not Found`）；GitHub API `license.spdx_id = null` | **unknown** | 题面/代码均不转载、不翻译（叠加红线 §4.2） |
| 作业仓库 `assignment-tirx-gemm` | `…/mlsyscourse/assignment-tirx-gemm/main/LICENSE`（11,357 B，200） | 首行 `Apache License Version 2.0` | allowed（限**该仓库**代码） | 可引用其代码思路；仍**不做**题面翻译（红线） |
| 笔记本仓库 `public-notebooks` | `…/mlsyscourse/public-notebooks/main/LICENSE` | **真 404**；API `license = null` | **unknown** | 不转载、不翻译 |
| 课程站另存的三方文档 `docs/PSC-machines.docx` | 仓库内 122,060 B | 文件名与内容指向匹兹堡超算中心（PSC）机器手册 | **排除**（第三方文档） | 只链接官方来源 |

## 3. 逐字证据（最短必需）

### 3.1 仓库根 LICENSE（授权文本）

```text
Attribution-NonCommercial 4.0 International
=======================================================================
Creative Commons Corporation ("Creative Commons") is not a law firm, ...
```

同一文件内：`Creative Commons Attribution-NonCommercial 4.0 International Public License`。
计数（对**落盘文件**计数，非记忆）：`ShareAlike` = **0**，`NoDerivatives` = **0**，`NonCommercial` > 0。

### 3.2 页面层面的 0 命中（坑八复现）

对 4 个渲染后页面做 `rel="license" | creativecommons | licen[cs]e | copyright | all rights reserved | ©` 计数：

| 页面 | 命中数 |
| --- | --- |
| `mlsyscourse.org/` | **0** |
| `mlsyscourse.org/schedule` | **0** |
| `mlsyscourse.org/materials` | **0** |
| `mlsyscourse.org/logistics` | **1**（仅 §2 表中那条 **HTML 注释**） |

⇒ 只看页面会得出「未声明许可」的**完全相反**结论。**必须看仓库根 `LICENSE`。**

### 3.3 `slides/` 里混放的第三方讲义（**本轮最重要的范围发现**）

`_data/lectures.yml`（30 行讲义表）里 `lecturer:` 只有 `Tianqi Chen` / `Zhihao Jia`；
三份客座讲义**一次都没出现**，schedule 渲染页的 17 个 PDF 链接里也没有它们：

```
/slides/01-course-introduction.pdf …… /slides/advanced-topic-mlc.pdf   # 共 17 个，全部为课程自制
```

而仓库里实际存在 `HaibinLinTalk.pdf`、`tim_quantization.pdf`、`FlashInferCMU.pdf`（+ 可能的其他遗留文件）。
⇒ 这三份是**堆在仓库里的第三方作品**，**不随课程 LICENSE 流转**。

### 3.4 讲义 PDF 内部的「许可命中」全部是内嵌字体（坑九的 PDF 版）

对 `slides/01-course-introduction.pdf` 与 `slides/04-automatic-differentiation.pdf` 做文本抽取后匹配：

> `© 2018 Microsoft Corporation. All Rights Reserved. Hebrew OpenType Layout logic copyright © 2003 & 2007, ...`
> `This layout logic for Biblical Hebrew is open source software under the MIT License; see embedded license description for details.`
> `Copyright (c) 2011-2015 by tyPoland Lukasz Dziedzic ... Licensed under the SIL Open Font License, Version 1.1`

⇒ 这些 `MIT License` / `copyright` **全部属于字体文件**（Calibri / Arial / Cambria / Lato），
**不是**课程许可。任何「PDF 里有 MIT ⇒ 这份讲义是 MIT」的推论都是错的。

### 3.5 ★ 自制讲义内部**含第三方改编页**（逐字证据 → 必须逐页排除）

对第一教学单元的自制讲义做「改编/来源行」扫描：

| 讲义 | 逐字命中 | 处理 |
| --- | --- | --- |
| `slides/08-ML-parallelization-part1.pdf` | **`Adapted from Minjia Zhang, DeepSpeed Presentation`（同一句命中 30 次，整组讲 GPU 内存/ZeRO 的页都在用）** | ⛔ **这些页不翻译**：改编内容的权利不在课程方，课程方的 CC BY-NC 4.0 只能覆盖**它自己的贡献** |
| `slides/02-introduction-to-MLSys.pdf` | `*Slides from Tianqi Chen`（同一作者自署） | ✅ 可用（课程作者本人） |
| `slides/06-CUDA-programming.pdf` | `Recall: An SM on a NVIDIA GTX 980 (2014)` | ✅ 事实性引用，不是改编声明 |
| `slides/01` / `04` | 无改编声明（仅字体内嵌许可） | ✅ 可用 |

⇒ **规则**：拿一份讲义来翻译之前，**先跑一次来源行扫描**（`Adapted from` / `Slides from` / `Courtesy of` / `Source:` / `Image source:`），
命中第三方署名的**整页/整组页**从翻译范围里剔掉，只译课程自撰页。这条规则同样适用于后续要取的其余 12 份讲义。

## 4. 三条排除项（硬规则，不因为「课程整体是 CC BY-NC」而放开）

### 4.1 第三方客座/业界讲义 —— 排除

课程方**无权**对 ByteDance / 外部讲者的作品授予 CC 许可；CC 授权由「有权授予的人」作出。
⇒ 三份客座讲义（§2 表）**不译、不做双语对照、不转载**，只允许链接仓库内的原始 PDF 路径。

### 4.2 作业 / Lab 题面与答案 —— 永久排除（本项目红线）

`assignment1` / `assignment2` / `assignment-distributed-training` **连 LICENSE 都没有**（真 404）⇒ 默认保留所有权利。
且按 `content-policy.md`「以下内容一律不产出」与 `paper-licensing.md` §4.1(c)：
**官方作业 / Lab 题面与答案的翻译在任何课程上都不做。**

### 4.3 课程方无法覆盖的三方内容（图/表/**改编页**）

CC BY-NC 4.0 §2(b)(2) 明确不授予「其他权利」，第三方素材（教科书图、论文图、厂商截图）不因课程的 CC 声明而开放。
⇒ **不复制原图**；需要图示时由 CourseLingo **自行重画**，并注明概念来源。
⇒ 更实际的一类：**整页改编内容**（§3.5 的 `Adapted from Minjia Zhang, DeepSpeed Presentation`）——
这类页**连同文字一起**排除，不能因为「LICENSE 是 CC BY-NC」就整份讲义照译。

## 5. 我们能发布什么（可执行的边界）

| 动作 | 判定 | 依据 |
| --- | --- | --- |
| 翻译课程自制讲义 + 双语原文对照 | ✅ **可做** | 仓库根 CC BY-NC 4.0；无 ND |
| 发布协议 | ⚠️ **必须保持非商业** | NC 条件随衍生作品传递：**不能**用 CC BY 4.0 发布译文（那会向下游授予商用权，违反上游 NC） |
| 署名义务 | ✅ 必须 | CC BY-NC 4.0 §3(a)：保留作者标识、版权声明、许可声明、免责声明、许可链接；并**标注已作修改**（翻译即为修改） |
| 商用（付费墙 / 广告 / 卖课 / 企业内训） | ⛔ **不可** | `NonCommercial` |
| 翻译客座讲义 / 作业题面 / 作业解答 | ⛔ 不可 | §4.1、§4.2 |
| 翻译**含第三方改编页**的讲义整份 | ⛔ 按页剔除 | §3.5（`08-ML-parallelization-part1.pdf` 已有 30 处 `Adapted from Minjia Zhang, DeepSpeed Presentation`） |
| 复制讲义原图 | ⛔ 不做 | §4.3；改为自绘并链接 |

> ⚠️ **对路线图的一处措辞修正（`course-selection.md` §3.3「无 SA ⇒ 我们的产出不必被拖成 CC」）**：
> 「无 SA」成立的只是「**不必用同一协议**」，**不等于**「可以用我们默认的 CC BY 4.0」。
> **NC 条款照样传递到衍生作品上**：MLSys 的译文必须非商业，且不得附加限制。
> 因此 MLSys 的译文产出应当**单独隔离**（独立子目录/仓库），协议建议直接沿用 **CC BY-NC 4.0**。
> 这一点不改变 A 级结论，但改变**发布协议**的选择 —— 若项目要商业化，MLSys 的译文线必须先解决 NC。

## 6. 仍存疑 / 未闭环（诚实清单）

| # | 未闭环项 | 缺什么 |
| --- | --- | --- |
| 1 | CC 授权文本**未逐字列举**覆盖哪些文件 | 覆盖范围来自「LICENSE 置于仓库根」这一仓库级事实，而非条款明文。若要更保险，可发信 `mlsyscourse` 维护者确认 slides 在授权范围内 |
| 2 | `slides/` 里是否还有**其他**未列入 schedule 的遗留文件 | 本轮只对 3 份可疑文件做了首屏取证；`git/trees?recursive=1` 的完整列表已落盘，可由列表中「不在 schedule 的 PDF」逐一复核 |
| 3 | 讲义内**图表的原始出处** | ✅ **已部分解答**：`08-ML-parallelization-part1.pdf` 含 30 处 `Adapted from Minjia Zhang, DeepSpeed Presentation`（§3.5）⇒ 规则是「**逐页扫来源行，命中即剔除**」。其余讲义需在取用时各跑一次 |
| 5 | 其余 12 份讲义（03/05/07/09/11/14/15/16/17/18/19/advanced-topic-mlc）的改编页比例 | 未逐份扫描；取用时按 §3.5 的规则先扫再用 |
| 4 | `assignment-tirx-gemm` 的 Apache-2.0 是否覆盖其**作业说明文本** | Apache-2.0 是软件许可；本轮只确认该仓库有此文件，未逐文件判断 |

## 7. 复现方式

```powershell
# 1) 仓库根 LICENSE（直连，不走代理）
& "C:\Windows\System32\curl.exe" -s -L -o LICENSE https://raw.githubusercontent.com/mlsyscourse/mlsyscourse.github.io/main/LICENSE
# 2) 页面（走 socks5 代理，失败重试 5–12 次；000 ≠ 404）
& "C:\Windows\System32\curl.exe" -s -L --max-time 25 -x socks5h://127.0.0.1:7892 https://mlsyscourse.org/logistics
# 3) 仓库文件清单
gh api "repos/mlsyscourse/mlsyscourse.github.io/git/trees/main?recursive=1" --jq '.tree[].path'
# 4) 讲义文本抽取（本机无 pypdf，用自带脚本）
python _sources\_audit\pdftext.py <deck>.pdf
```

**落盘证据**：`_sources/mlsys-15442/evidence/`（LICENSE、仓库树、页面源码与渲染 HTML、讲义 PDF、作业仓库 LICENSE 探针）
与 `_sources/mlsys-15442/text-clean/`（讲义可读文本，供后续写作）。
