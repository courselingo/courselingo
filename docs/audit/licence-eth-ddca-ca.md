# 授权核实：ETH Zurich DDCA → Computer Architecture（safari.ethz.ch wiki）

> 核实日期 **2026-09-28**。方法：全部经 `-x socks5h://127.0.0.1:7892` 抓**原始 HTML**（失败重试 5–12 次；`000` ≠ 404）。
> 状态：**逐页 + 逐材料（含讲义 PDF 内部）核实完成**。
> 结论：**A 级（可翻译）—— 但仅限 wiki 托管内容**；四类排除项见 §4。

## 0. 一句话结论

两门课**每一个 wiki 页面**的页脚都带同一份站点级许可块：
`Except where otherwise noted, content on this wiki is licensed under the following license:` +
`rel="license"` → **CC BY-NC-SA 4.0**。
⇒ **wiki 文本 + 课程自制的 `onur-*` 讲义 PDF/PPTX** 可以翻译（**非商业 + 署名 + 同协议 BY-NC-SA 4.0 发布**）；
⛔ **第三方客座报告 / 会议论文 / YouTube 视频 / 作业解答** 一律不碰。

## 1. 核对清单

| 复核项 | 结果 |
| --- | --- |
| 许可声明位置 | ✅ **每个页面的页脚**（DokuWiki 站点级许可，逐页出现 —— 与 6.824「徽章只在主页」形成对照） |
| 覆盖范围是否明确 | ✅ 文本自述 `content on **this wiki**` ⇒ 覆盖 wiki 页 + **wiki 托管的媒体文件**（`lib/exe/fetch.php?media=…`） |
| ⚠️ 例外条款 | 有：`Except where otherwise noted` ⇒ **逐件复核**第三方材料（这正是本轮排除客座/论文材料的依据） |
| 我们实际依据的文件（讲义 PDF） | ✅ 抽样 3 份讲义 PDF 内部**无任何自有版权/许可声明**，只有内嵌字体声明（§3.3） |
| 是否有 ND（禁止翻译） | ❌ **无 ND**（BY-NC-**SA**）⇒ 翻译被允许 |
| 是否有 SA（传染） | ⚠️ **有** ⇒ 我们的译文**必须**同样以 CC BY-NC-SA 4.0 发布（copyleft 传染） |
| 商用 | ⛔ **不可**（NC） |
| YouTube 视频 | ⛔ 不在范围内（CA 排期页有 43 个 YouTube 链接；视频受平台条款） |
| 作业 / Lab | ⛔ 不进翻译（本项目红线）；wiki 本身**没有**「禁止公开解答」条款（见 §4.4，这是政策选择而非法律被动） |

## 2. 逐页取证（页脚许可块计数，全部 200）

| 课程实例 | 页面 | URL | `rel="license"` | `by-nc-sa/4.0` |
| --- | --- | --- | --- | --- |
| **DDCA Spring 2023**（路线图指定的目标版本） | start | <https://safari.ethz.ch/digitaltechnik/spring2023/> | 2 | 2 |
| DDCA Spring 2023 | schedule | <https://safari.ethz.ch/digitaltechnik/spring2023/doku.php?id=schedule>（72,137 B） | 2 | 2 |
| DDCA Spring 2023 | **labs**（材料页） | <https://safari.ethz.ch/digitaltechnik/spring2023/doku.php?id=labs>（34,961 B） | 2 | 2 |
| DDCA Spring 2023 | lectures | `…?id=lectures`（页面不存在，但页脚许可块仍在） | 2 | 2 |
| **CA Fall 2022** | start | <https://safari.ethz.ch/architecture/fall2022/doku.php?id=start>（32,982 B） | 2 | 2 |
| CA Fall 2022 | lectures | `…?id=lectures`（15,178 B） | 2 | 2 |
| CA Fall 2022 | **schedule**（材料页） | `…?id=schedule`（82,348 B） | 2 | 2 |
| **DDCA 当前实例（Spring 2026）** | start / lectures / schedule | <https://safari.ethz.ch/digitaltechnik/doku.php?id=start> 等 | 2 | 2 |

> ⚠️ **版本漂移（重要，影响后续取材料）**：`/digitaltechnik/doku.php?id=*` 现在服务的是 **Spring 2026** 实例
> （页脚徽章路径为 `/ddca/spring2026/lib/images/license/button/cc-by-nc-sa.png`），
> 而 `/digitaltechnik/spring2023/` 是**独立的存档实例**（徽章路径 `/digitaltechnik/spring2023/lib/…`），
> 两者**各自都带许可块**。取材料时**必须写清版本前缀**，不要用不带版本的 `/digitaltechnik/` 根路径。

## 3. 逐字证据

### 3.1 许可块（逐字，来自原始 HTML 页脚）

```html
<div class="license">Except where otherwise noted, content on this wiki is licensed under the following license:
  <bdi><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en" rel="license" class="urlextern">CC Attribution-Noncommercial-Share Alike 4.0 International</a></bdi></div>
<div class="buttons">
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en" rel="license">
    <img src="/digitaltechnik/spring2023/lib/images/license/button/cc-by-nc-sa.png"
         alt="CC Attribution-Noncommercial-Share Alike 4.0 International" /></a>
```

**它为什么比 6.824 的徽章强**：6.824 的徽章只在主页、且**没有说明覆盖哪些文件**；
这份声明**逐页出现**，而且**明文限定范围为 `content on this wiki`** —— 覆盖范围是条款自述，不是我们的推断。

### 3.2 材料规模（wiki 托管文件，从渲染页抽取 `lib/exe/fetch.php?media=` 链接）

| 实例 | 媒体文件数 | 构成 |
| --- | --- | --- |
| DDCA Spring 2023 | **92** | `onur-ddca-2023-lecture*`（讲义 1–26，PDF+PPTX）+ `ddca-2023-intro-labs-fpgas`（实验介绍）+ 5 份 problem-solving 讲义 |
| CA Fall 2022 | **107** | `onur-comparch-fall2022-*`（讲义 1–29）+ **第三方报告/论文**（见 §4.1） |
| DDCA Spring 2026（当前实例） | **84** | `onur-ddca-2026-*` + `ataberk-*`（助教制作） + `kanellok-*`（助教制作） |

### 3.3 讲义 PDF **内部**是否有独立声明（抽样取证）

对 3 份 PDF 做文本抽取后匹配 `rel="license"|creativecommons|licen[cs]e|all rights reserved|
adapted from|courtesy of|used with permission|copyright`：

| PDF | 结果 |
| --- | --- |
| `onur-ddca-2026-lecture1-intro-afterlecture.pdf`（16,969,483 B） | 命中**全部是内嵌字体/证书声明**，例如<br>`© 2018 Microsoft Corporation. All Rights Reserved. Hebrew OpenType Layout logic copyright © 2003 & 2007, ...`<br>`This layout logic for Biblical Hebrew is open source software under the MIT License ...`<br>**没有任何课程自己的版权或许可声明** |
| `onur-comparch-fall2022-lecture2b-courselogistics-afterlecture.pdf`（490,625 B，课程信息讲义） | 唯一命中：`Digitized data copyright Monotype Typography, Ltd 1991-1995. All rights reserved.`（字体）+ Microsoft 代码签名证书串；**无课程声明** |
| `adeeperlookintorowhammer_micro21-talk.pdf`（5,624,826 B，第三方报告） | 无自有版权声明（只有苹果 ICC profile 与字体串） |

⇒ 讲义 **没有**「otherwise noted」式声明 ⇒ 默认继承 wiki 的 CC BY-NC-SA 4.0。
（同时这也说明：**PDF 内的 `MIT License` 命中不能当课程许可** —— 坑九在 PDF 层面的复现。）

### 3.4 ★ 但「otherwise noted」**不是空话**：讲义内图注逐字点名了第三方来源

对 Spring 2023 的三份讲义做「图注/来源行」扫描（`Image source` / `Source:` / `Adapted from` / `Courtesy of`），
逐字命中如下（**这些是判定范围的决定性证据**）：

| 讲义 | 逐字图注 |
| --- | --- |
| `lecture2b-combinational-logic-i.pdf` | `Image source: Harris and Harris, Digital Design and Computer Architecture, 2nd Ed., p.110.`（同类命中另一份） |
| `lecture4-sequential-logic.pdf` | `Image source: Harris and Harris, Digital Design and Computer Architecture, 2nd Ed., p.110.`<br>`Image source: Patt and Patel, "Introduction to Computing Systems", 2nd ed., page 78.`<br>（另有 page 76 / page 95 两处同书图注） |
| `lecture2b / lecture4` | `Source: https://www.apple.com/mac/m1/`、`Source: https://www.anandtech.com/show/16252/mac-mini-apple-m1-tested`、`Source: https://en.wikichip.org/wiki/nvidia/tegra/xavier`、`Source: https://www.mouser.ch/…`、`Source: https://dl.acm.org/doi/pdf/10.1145/3445814.3446723`、`Image source: https://lbsitbytes2010.wordpress.com/…` |

⇒ **结论（必须写进写作规范）**：
- 讲义**文字**（Onur Mutlu 自撰）落在 wiki 的 CC BY-NC-SA 4.0 内，**可译**；
- 但**图/表**被逐字标注为**商业教材**（Harris & Harris；Patt & Patel）或**第三方网站 / ACM DL** 来源，
  这些**属于「otherwise noted」**，**不在课程方的授权范围内** ⇒ ⛔ **不复制、不重绘同图、不把图内文字当课程文本翻译**；
  需要图示时由 CourseLingo **自绘原理图**，并在图注中标明「概念来源：ETH DDCA 讲义」。
- 图注里的书名/页码**可以引用**（事实性出处信息），但**不要**把它当作「该图已获授权」的依据。

## 4. 排除项（`Except where otherwise noted` 的实际适用）

### 4.1 ⛔ 第三方客座报告与会议论文（CA Fall 2022 wiki 上）

从 107 个媒体链接中识别出**非 `onur-*`** 的一批，并逐条归类：

| 文件 | 性质 |
| --- | --- |
| `adeeperlookintorowhammer_micro21-talk.pdf/.pptx` | **MICRO'21 会议报告**（论文发表物演讲，非课程讲义） |
| `pluto_micro2022_final.pdf/.pptx`、`segram_comparch2022.pdf/.pptx`、`flash_cosmos.pdf/.pptx`、`hermes-comparch2022-final.*`、`morpheus_comparch_2022.*`、`pythia_comparch_fall2022.*`、`polynesia_comparch_fall2022_beforelecture.*`、`mensa_comparch_fall2022_beforelecture.*`、`pidram.*`、`genpip-before.*`、`dr-strange-afterlecture.*`、`alser-comparch-fall2022-lecture5-*`、`giray-comparch-fall2022-lecture23d-*`、`quac-trng-comparch-10.11.22.*` | 组内/客座研究报告，底稿是**已发表论文** |
| **`(Paper)` 标记的三份**：`genstore.pdf`、`quactrng.pdf`、`segram.pdf` | **原始论文 PDF** —— 完全走 `paper-licensing.md` 那条线（出版社权利，默认不译不转载） |

> 判断依据：这些是**会议发表物**，其权利层在 **ACM / IEEE**，不在 ETH 课程方。
> `paper-licensing.md` §0 的规则「**课程采用 CC，不等于它推荐的论文也是 CC**」在这里直接适用。
> ⇒ **不译、不转载、不入双语对照**；需要讲这些工作时，写**我们自己的原创导读**并链接原论文。

### 4.2 ⛔ YouTube 视频

CA Fall 2022 排期页含 **43 个 YouTube 链接**（本轮实测计数；另有 "Lecture Video Playlist"、"Livestream Lecture Playlist" 等）；
DDCA Spring 2023 排期页更多，**56 处** `youtube.com|youtu.be` 命中；
视频本体受**平台条款 + 独立权利层**约束，与 6.824 的 2020 视频同处理：**不转载、不做字幕翻译**。

### 4.3 ⛔ 助教制作材料需逐件标注来源

`ataberk-ddca-2026-*`（实验/FPGA 讲义）、`kanellok-ddca-2026-*`（虚拟内存讲义）由助教制作，
wiki 许可块在原则上覆盖，但**内容里常含第三方来源**（教材图、论文图、厂商资料）。
⇒ 若使用，需**逐件**确认无 "otherwise noted"；本轮只抽样，**未逐件核**（见 §6）。

### 4.4 ⛔ 作业 / Lab / 考试材料 —— 本项目红线

DDCA Spring 2023 wiki 的 `labs` 页含 **9 个实验手册 + 报告模板 + 实验补充材料**；
CA Fall 2022 侧栏有 `HWs` / `Labs` / `Exams`。
按 `content-policy.md`「以下内容一律不产出」（作业/Lab 题面与答案的翻译、原始课件转载）：
⛔ **实验手册与作业题面不翻译、原始 PDF 不转载**，只链接。

> 注意一个**诚实性要点**：与 MIT 6.824 / Berkeley CS 61A / CS 162 不同，
> ETH 这个 wiki **没有**「禁止公开解答」的明文条款（本轮已读 `labs` 页全文，未出现此类表述）。
> 因此这条排除是**我们自己的政策选择**（红线），**不是** ETH 条款的要求 —— 不要对外写成「ETH 禁止」。

## 5. 我们能发布什么

| 动作 | 判定 | 依据 |
| --- | --- | --- |
| 翻译 **wiki 页面文本**（讲义索引、排期、课程说明、labs 页说明文字） | ✅ 可做 | 页脚 CC BY-NC-SA 4.0 |
| 翻译 **`onur-*` 课程自制讲义 PDF/PPTX** + 双语原文对照 | ✅ 可做（抽样已确认无内部例外声明） | `content on this wiki` + §3.3 |
| 发布协议 | ⚠️ **必须 CC BY-NC-SA 4.0**（SA 传染，且非商业） | `ShareAlike` + `NonCommercial` |
| 署名义务 | ✅ 必须：作者（Onur Mutlu / 课程）、来源 URL、许可名称与链接；标注已翻译/修改 | CC BY-NC-SA 4.0 §3(a) |
| 译文与 6.824 / MLSys 内容**混进同一仓库** | ⛔ 不可 | SA 会把整个仓库拖成 BY-NC-SA；按 `content-policy.md`「一课程一仓库 + 授权边界隔开」 |
| 翻译第三方报告/论文、转载论文 PDF | ⛔ 不可 | §4.1 |
| 视频字幕 / 视频转载 | ⛔ 不可 | §4.2 |
| 复制讲义内原图 | ⛔ **不做（有逐字证据）** | §3.4：图注逐字点名 `Harris and Harris` / `Patt and Patel` / 第三方 URL / `dl.acm.org` ⇒ 属「otherwise noted」；改为**自绘**并注明概念来源 |

## 6. 仍存疑 / 未闭环

| # | 未闭环项 | 缺什么 |
| --- | --- | --- |
| 1 | **助教制作材料**（`ataberk-*` / `kanellok-*`）是否含 "otherwise noted" 的三方内容 | 需逐件打开 PDF/PPTX 做与 §3.3 同样的内部声明扫描（本轮只抽了 3 份 Onur 讲义 + 2 份 2026 讲义） |
| 2 | 讲义**图表级**出处 | ✅ **已部分解答**：Spring 2023 三份讲义里已抓到逐字图注（§3.4）⇒ 规则是「**图一律不用**」。仍未逐图穷举，但该规则已覆盖风险 |
| 3 | CA Fall 2022 的 `HWs` / `Labs` / `Exams` 页面 URL | 侧栏条目对应的 DokuWiki 页面名未逐个定位（`?id=homework`、`?id=project` 均为 NO-TOPIC-PAGE）；**不影响主结论**，因为这些材料本项目一律不做 |
| 4 | 更早学期实例（SS18–SS22、FS21）是否同许可 | 本轮只覆盖 **DDCA Spring 2023 / CA Fall 2022 / DDCA Spring 2026** 三个实例；若要复用旧版本讲义（例如 SS18 视频课对应的 PDF），需单独核 |

## 7. 复现方式

```powershell
# 页脚许可块（所有页面均可 grep）
& "C:\Windows\System32\curl.exe" -s -L --max-time 25 -x socks5h://127.0.0.1:7892 `
  "https://safari.ethz.ch/digitaltechnik/spring2023/doku.php?id=schedule" |
  Select-String -Pattern 'rel="license"'
# 材料清单（从渲染页抽 lib/exe/fetch.php?media=…）
python _sources\_audit\media_links.py <页面.html>
# 讲义 PDF 内部声明扫描
python _sources\_audit\pdftext.py <deck>.pdf
python _sources\_audit\ctx.py <deck>.pdf.text.txt
```

**落盘证据**：`_sources/eth-ddca-ca/evidence/`（各页原始 HTML + 纯文本、材料清单 `eth-media-links.txt` / `eth-sp2023-media.txt`、4 份讲义 PDF）
与 `_sources/eth-ddca-ca/text-clean/`（讲义可读文本）。
