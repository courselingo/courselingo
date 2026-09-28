# 课程目录 · Course Catalog

> 授权状态已在 2026-09-28 经**实际抓取**核实（含**同日二次核实**）。每条都附逐字原文引用与来源 URL。
> **读本文件请先看下面两节修正记录**：6.824 的 CC BY 3.0 US 徽章**只在主页**，
> 讲义 `notes/l01.txt` 无任何声明 ⇒ 讲义授权 **`未确认`**，**只发布原创讲解**。
> 方法：本机 DNS 为 Clash fake-IP（学术域名解析到 `198.18.0.x`），`web_fetch` 会拒绝非公网地址、
> `web_search` 无 API key，因此统一用 `curl -x socks5h://127.0.0.1:7892` 抓取
> （**必须是 SOCKS5，`socks5h://`**；同端口的 HTTP 代理模式不可用）。抓取到的原始页面留证在 `docs/_fetch/`。

## ⚠️ 第一轮修正（2026-09-28）：更早一版结论有四处错误

本文件上一版把 6.824 判为「未声明许可」、把 Composing Programs 判为 CC BY-NC-SA 3.0。**两处都不对**，原因是只扫了可见文字、以及引用了过期版本。修正如下：

| 上一版结论 | 实测真相 | 错因 |
| --- | --- | --- |
| 6.824「未声明任何许可」 | **主页有 CC BY 3.0 US 徽章**（`rel="license"`） | 徽章是**纯图片链接，无任何可见文字**；只扫文字必然漏掉 |
| Composing Programs = CC BY-NC-SA **3.0** | 现行 `/3ed/` = CC BY-NC-SA **4.0** | 引用了旧版教材的措辞；站点现已 302 到 `/3ed/` |
| CS 144「未确认」 | 实验 README 有**明确自订条款** | 只试了 `LICENSE` 文件；授权写在同一仓库的 `README.md` 里 |
| 6.1810 未列 | **CC BY 3.0 US**，配套 xv6 教材 **MIT License** | 未抓取 |

> 教训：**`rel="license"` 徽章的授权信息全在 `href` 里，纯文本抽取会 100% 丢失这条证据。**

## ⚠️ 二次核实修正（2026-09-28）：6.824 徽章**只在主页**

上一轮把 6.824 从「无许可」改判为「开放授权」，**这一步是对的** —— 徽章确实存在。
但上一轮**由它推出了覆盖范围**（讲义、幻灯片可翻译可转载），而那个范围**从来没有取过证**。

**二次核实取了证，结论是反的：**

| 上一轮结论 | 二次核实真相 | 错因 |
| --- | --- | --- |
| 「主页有 CC BY 3.0 US ⇒ 讲座笔记 / 幻灯片可翻译、可转载」 | 徽章 `rel="license"` **全站只出现 1 次，就在主页**；**讲义 `notes/l01.txt`（我们实际依据的文件）无许可标注、无版权声明（0/0/0）** ⇒ 讲义授权 **`未确认`** | 核实范围覆盖了 `general / schedule / questions / labs / guidance / submit`，**唯独漏掉讲义文件本身**，把推断当成了原文 |

| URL | 大小 | `rel="license"` | CC 链接 | 版权声明 |
| --- | --- | --- | --- | --- |
| `https://pdos.csail.mit.edu/6.824/` | 3995 B | **1** | 1 | 0 |
| `https://pdos.csail.mit.edu/6.824/schedule.html` | 17414 B | 0 | 0 | 0 |
| `https://pdos.csail.mit.edu/6.824/labs/lab-mr.html` | 15394 B | 0 | 0 | 0 |
| `https://pdos.csail.mit.edu/6.824/general.html` | 8065 B | 0 | 0 | 0 |
| **`https://pdos.csail.mit.edu/6.824/notes/l01.txt`** | 10886 B | **0** | **0** | **0** |

> 取证留档：`docs/_fetch/6824-notes-l01.txt`。该文件在本轮被**独立重取一次**
> （`200`、10886 B，与首次一致），并连同首页/子页面的落盘副本一起**重新计数** —— 结果与上表一致。

> **中间结论保留**：6.824 **不是**「无许可」（徽章真实存在，这条上一轮没错），
> 但它是**主页范围的许可**，不是整站许可。**讲义没有许可依据 ⇒ 按 `未确认`（默认保留所有权利）处理。**
> **我们只发布原创讲解；不产出逐字稿，不做双语原文对照。**
> 代码侧已落地：`course.toml` 的 `verified = false` / `redistribution = "unknown"` / `[license.materials]` 全 false。

## 结论总表

| 课程 | 授权状态 | 对我们的含义 |
| --- | --- | --- |
| **MIT 6.5840 / 6.824** | ⚠️ **CC BY 3.0 US，但覆盖范围仅限主页；讲义无任何声明 ⇒ 讲义授权 `未确认`** | 徽章**只在主页**。讲义 `notes/l01.txt`（我们实际依据的文件）无许可标注、无版权声明 ⇒ **不做逐字稿、不做双语原文对照，只发布原创讲解**。Lab 代码另有禁发条款 |
| **UC Berkeley CS168** | 🟢 **教材站根页 CC BY-SA 4.0（已核实；Lead 独立二次复核）**；**课程站与讲义无任何声明** | 教材：可翻译、**可商用**、须 **SA 同协议** —— 第一梯队里**唯一不带 NC** 的一门。讲义/幻灯片/作业/视频未声明 ⇒ 只能**原创讲解**（`[license.materials]` 逐项表达） |
| **UC Berkeley CS 61A** | 🔴 **明确声明版权 = 保留所有权利**（`Copyright ©2026, Regents of the University of California`） | ⛔ **不做这门课**（用户方针：课程不允许传播即明确拒绝）；逐字稿 / 字幕 / 课件转载更是一律不可做 |
| MIT 6.1810 / 6.S081 | 🟢 **CC BY 3.0 US**（主页与 general 页有徽章）；xv6 教材 **MIT** | 就**已取证的页面**而言：可商用、可翻译、无 SA。⚠️ **但其讲义文件未单独取证**（沿用 6.824 的教训）⇒ 讲义的覆盖范围 **`未确认`**，逐字稿路线同样**未解锁** |
| MIT OpenCourseWare | 🟡 **CC BY-NC-SA 4.0** | 可改编，**禁止商用**且 **SA 传染** |
| Composing Programs（3ed） | 🟡 **CC BY-NC-SA 4.0** | 可改编，**禁止商用** + 相同方式共享 |
| CMU 15-445 | ⚠️ **未声明许可**（`unknown`：无人表态，默认保留所有权利） | 只做**原创讲解**；逐字稿 / 字幕 / 课件转载一律不可做 |
| Stanford CS 144 | ⚠️ **混合**：站点无声明；实验 README 自订「公开可读但禁发解答」 | 未授予明确的商用与衍生权 |

**关键判断（已修正）：6.824 的 CC BY 3.0 US 徽章是「主页范围的许可」，不是整站许可。**

上一版此处的表述「6.824 并非『无授权』而是『开放授权』，因此 Phase 1 的 6.824 逐字稿翻译在法律上可行」
**前半句仍然成立，后半句已作废**：徽章确实存在（所以不是「无授权」），
但**讲义文件 `notes/l01.txt` 没有任何许可声明** ⇒ 讲义授权 **`未确认`**。
**结论：6.824 的逐字稿翻译路线并未解锁。** 现行做法是只发布原创讲解（`output_mode = "explanation"`）。

至于「6.824 不是无授权」这一点本来是有价值的中间结论 —— 它避免了把一门**主页确已开放**的课程
误判成「保留所有权利」；只是它**不能**被延伸成「所以讲义也能翻」。**这是两次核实的合成结论。**
但 CS 61A 仍然是红线。

---

## 目标课程

### MIT 6.5840 / 6.824 · 分布式系统

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://pdos.csail.mit.edu/6.824/> |
| 许可 | ⚠️ **CC BY 3.0 US —— 但只出现在主页**（Creative Commons Attribution 3.0 United States） |
| 核实范围 | 主页、`/general.html`、`/schedule.html`、`/questions.html`、`/labs/lab-mr.html`、`/labs/collab.html`、`/labs/guidance.html`、`/labs/submit.html`、**`/notes/l01.txt`（二次核实新增）**、2020 与 2018 历史主页 |
| 出现位置 | **仅主页**（含 2018 / 2020 历史主页）；其余页面**均无**标注 |
| 讲义授权 | **`未确认`** —— `notes/l01.txt` 无许可标注、无版权声明（0/0/0） |

主页原文 HTML（逐字，这是**唯一**的授权证据）：

```html
<a rel="license" href="https://creativecommons.org/licenses/by/3.0/us/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/us/88x31.png" /></a>
```

**判读（务必连同范围限定一起读）**：`by/3.0/us` 是**只有 BY 一项**的许可 —— 无 NC、无 SA、无 ND。
**许可条款本身宽松；但它写在哪里、覆盖什么，是另一回事。**

- ⚠️ **该徽章只出现在主页。** 讲义 `notes/l01.txt`（**我们实际依据的材料**）与
  `schedule / lab-mr / general` 等子页面**均无任何声明** ⇒ 讲义授权 **`未确认`**。
- ⛔ **逐字稿翻译 / 双语原文对照：不产出。** 讲义没有许可依据，按「无声明 = 保留所有权利」处理；
  翻译是衍生作品。这一判定已由 `validate.py`（`output_mode = "transcript"` → **退出码 1** 拒绝）
  与 `build_site.py`（**不注入**原文对照块）各自独立落地。
- ✅ **原创中文讲解：可做** —— 不复制原文表达，讲概念，不受许可范围影响。**这是 6.824 现行唯一路线。**
- ⛔ **转载原始课件：不做** —— 与上一条同因（`redistribution = "unknown"`）。
- ~~✅ 翻译讲座笔记 / 逐字稿：可做（署名 + 链接许可 + 标明已修改）~~ **【已作废·2026-09-28】**
  该结论预设了徽章覆盖讲义，**从未取证，现予以撤回**。
- ~~✅ 商用：可做（无 NC）~~ → **`未确认`**：CC BY 3.0 US 本身无 NC，
  但**只有当它确实覆盖所引材料时**才能推出「可商用」；讲义覆盖范围未确立，故不能据此断言。
- ~~✅ 译文不必以相同许可发布（无 SA）~~ → 同上，**`未确认`**（许可文本无 SA 是确定的；
  不确定的是它是否适用于讲义）。
- ⛔ **Lab 代码不得公开** —— 这是与 CC 并行的另一层课程条款，来源 <https://pdos.csail.mit.edu/6.824/labs/collab.html>，逐字引用：
  > "Please do not publish your code or make it available to current or future 6.5840 students."
- ⚠️ **视频**：当前 2026 版无视频。2020 及更早是 **YouTube 嵌入**（<http://nil.csail.mit.edu/6.824/2020/video/1.html> 全文即一个 `youtube.com/embed/cQP8WApzIQQ` 的 iframe），**视频本体另受 YouTube 条款约束**。
- ⚠️ **golabs 发行包内是否另有 `LICENSE`：未核实。** Lab 代码走 MIT 自建 git（`git clone git://g.csail.mit.edu/6.5840-golabs-2026`），不在 GitHub；且 `g.csail.mit.edu` 实测**不可达**（4 次 `000`）。

### UC Berkeley CS168 · 计算机网络导论

| 项 | 内容 |
| --- | --- |
| 官方入口 | 课程站 <https://cs168.io/>（302 跳转到当学期，实测为 <https://fa26.cs168.io/>） |
| 教材站 | <https://textbook.cs168.io/> |
| 许可 | 🟢 **教材站根页 CC BY-SA 4.0**（`rel="license"` ×2、CC 链接 ×2） |
| 核实范围 | 教材根页 + **真实存在的三个章节页**（`/intro/layers.html`、`/intro/headers.html`、`/applications/http.html`）+ 课程站真站 `fa26.cs168.io` 根页 |
| 教材根页逐字 | `This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.` |
| 章节页 | **0 / 0 / 0 / 0**（`rel="license"`、CC 链接、`Copyright`、`all rights reserved` 全为 0） |
| 课程站 `fa26.cs168.io` 根页 | **0 / 0 / 0 / 0** —— 无任何许可声明 |
| 讲义 / 幻灯片 / 作业 / 视频 | **未声明** ⇒ 覆盖范围未获确认 |

**★ 本条目记录一次 Lead 独立复核（SOP 要求第二人复核，不橡皮图章）：**

第一次取证的**章节 URL 是猜的**，三页都返回同一个 **404**（各 18,034 B，且与一个故意编造的
URL 返回完全相同的页面）。**在 404 页面上数「许可声明 0 处」是没有意义的。**
第二轮从教材根页的导航链接取出**真实**章节 URL 重测，结论**不变**（真实章节 34–59 KB，仍全 0）。

> **教训（补进陷阱表）**：**同一个 404 页会被抓成「内容页」，字节数还完全相同** ——
> 多个不同 URL 返回**完全相同的字节数**时，几乎一定是 404 或空壳，必须先读 `<title>` 与正文确认。

**判读**：

- 教材根页有**权利人的明文授权**（"This work is licensed under…"），因此 `verified = true`。
  书在根页声明一次许可、章节页不重复，是**书籍的常态**（不同于课程站逐页复制许可），
  所以「章节页无声明」**不推翻**教材整体的 CC BY-SA 4.0。
- 课程站与讲义是**另一批作品**，实测 0 声明 ⇒ **`unknown` ⇒ 只做原创讲解**。
- 因此 `course.toml` 用 `[license.materials]` **逐项**表达：`textbook = true`，其余为 `false`；
  页面提示条会如实分列已核实与未核实的材料（见 `template/scripts/banners.py`）。

### UC Berkeley CS 61A · 计算机程序的构造与解释

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://cs61a.org/>（302 → <https://cs61a.org/fa26/>） |
| 许可 | **无任何许可声明 = 保留所有权利** |
| 原文引用 | "Copyright ©2026, Regents of the University of California and respective authors." |
| 出现位置 | 首页、`/fa26/syllabus/`、`/fa26/articles/contact/` 页脚 |

**判读**：版权归加州大学校董会，未授予改编或再发布的权利。

> 注意：页面里那 4 处 "License" 字样**全部是站点模板自带的图标库许可注释**（`Feather. MIT License`、`Bootstrap Icons. MIT License`），**与课程内容无关** —— 别被 grep 命中数误导。

- ⛔ 逐字稿翻译 / 字幕翻译：**不可做**
- ⛔ 转载课件 PDF：**不可做**
- ⛔ 作业与 Lab 解答：**永久排除**，来源 <https://cs61a.org/fa26/syllabus/>，逐字引用：
  > "Do not post your solutions publicly during or after the semester."
- ⚠️ **视频**：公开讲座在 **YouTube 播放列表**（如 `PL6BsET-8jgYVfI7chdrXciKy8CP10tOcl`），另有 bCourses 受限入口（需登录）。
- 说明：`cs61a.org/about.html`、`/faq.html`、`/articles/about.html` **均 HTTP 404**（页面不存在，不是抓取失败）。

### MIT OpenCourseWare

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://ocw.mit.edu/> · 条款 <https://ocw.mit.edu/terms/>（落点 `/pages/privacy-and-terms-of-use/`） |
| 许可 | **CC BY-NC-SA 4.0** |
| 许可定义 | "The following notices and licenses comprise together the MIT OpenCourseWare License." |
| 许可证名 | "Creative Commons License Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)" |
| 衍生授权 | "Adapt — remix, transform, and build upon the material" |
| 商用 | "Noncommercial — You may not use the material for commercial purposes." |
| MIT 的解释 | "Non-commercial use means that users may not sell, profit from, or commercialize OCW materials or **works derived from** them." |
| 相同方式共享 | "Share Alike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original." |
| 商标 | "you may not use MIT's names or logos, or any variations thereof, without prior written consent of MIT." |
| 版本日期 | 页面标注 `Last Updated: 08/11/2026` |

**判读**：唯一明确允许改编的目标来源，但代价是两条**传染性**约束：

1. **禁止商用** —— 一旦用了 OCW 材料（含其衍生作品），整个产出不得商业化。
2. **ShareAlike 传染** —— 我们的翻译/讲解必须以 CC BY-NC-SA 4.0 发布。

补充两点：

- **OCW 与校内课程站是两套授权**：`ocw.mit.edu` 上的课程版本带 CC BY-NC-SA 4.0，
  而 `pdos.csail.mit.edu/6.824/` 课程站带的是 CC BY 3.0 US。就**许可文本**而言课程站更宽松（无 NC、无 SA），
  **但这个比较在二次核实后已不能直接使用**：6.824 的徽章**只在主页**，讲义文件无声明 ⇒ 讲义 **`未确认`**。
  「走课程站更自由」这句话**只对主页本身成立**，不能推及讲义。
- **OCW 已无独立「引用/citation」页面**：`/citation/`、`/privacy/`、`/pages/how-to-cite-ocw/`、`/pages/attribution/`、`/pages/cite/` **全部 HTTP 404**。署名要求以 terms 页 `Attribution` 条款为准。

### Composing Programs（CS 61A 教材）

| 项 | 内容 |
| --- | --- |
| 入口 | <https://composingprograms.com/>（302 → <https://composingprograms.com/3ed/>） |
| 许可 | **CC BY-NC-SA 4.0** |
| 原文引用 | "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)." |
| 来源沿革 | "This online book is a derivative of Structure and Interpretation of Computer Programs (2nd ed.) … originally authored in 2011 under the CC BY-NC-SA 3.0 Unported license … (SICP was later relicensed under CC BY-SA 4.0 in 2016). As permitted under Section 4(b) of the original 3.0 license, this adaptation has been upgraded to CC BY-NC-SA 4.0, but remains non-commercial." |
| 版权 | "Copyright John DeNero." |
| 机器可读标注 | `aria-label` = "Content License: Creative Commons Attribution Non Commercial Share Alike 4.0 International (CC-BY-NC-SA-4.0)" |
| 生效范围 | 逐页生效（`/3ed/getting-started/` 内页带同一徽章） |

**判读**：教材本身允许改编，但同样禁止商用 + 相同方式共享。
**它与 CS 61A 课程站是两套授权** —— 教材开放 ≠ 课程幻灯片/作业开放。

> 版本澄清：现行第三版是 **4.0**。旧版文案曾写 "version 3"，但站点现只发布 `/3ed/`，**以 4.0 为准**。

### MIT 6.1810 / 6.S081 · 操作系统工程

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://pdos.csail.mit.edu/6.1810/> · <https://pdos.csail.mit.edu/6.S081/2023/general.html> |
| 许可 | **CC BY 3.0 US**（与 6.824 同一徽章、同一 href；出现在主页与 `6.S081/2023/general.html`） |
| 讲义授权 | ⚠️ **`未确认`** —— **其讲义文件未单独取证**（沿用 6.824 的教训：要核到实际使用的文件）⇒ **逐字稿路线同样未解锁** |
| 配套教材 | `xv6-riscv` / `xv6-book` / `xv6-public` 均为 **MIT License** |

课程自订条款（逐字，见 6.S081 general 页）：

> "Do not post your lab or homework solutions on publicly accessible web sites (such as GitHub) or file spaces (such as your Athena Public directory)."

### CMU 15-445 · 数据库系统

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://15445.courses.cs.cmu.edu/> |
| 许可 | **未声明 = 保留所有权利** |
| 核实范围 | 主页 + `/spring2024/`、`/fall2023/`、`/spring2023/`、`spring2024/syllabus.html`、`spring2024/faq.html` |
| 结果 | 全部页面**无任何许可标注**（无 Creative Commons、无 `rel="license"`、无授权措辞） |

唯一相关文本是学术诚信条款（`spring2024/syllabus.html`）：

> "Any violation of this policy is cheating. The minimum penalty for cheating (including plagiarism) will be a zero grade for the whole assignment"

### Stanford CS 144 · 计算机网络

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://cs144.github.io/> |
| 站点许可 | **未声明** |
| 实验代码许可 | ⚠️ **自订条款**（非标准开源许可） |

站点逐字引用：

> "Please don't post source code to lab solutions."

实验代码授权来自仓库 README（**不是 LICENSE 文件**），来源 <https://raw.githubusercontent.com/CS144/imp/master/README.md>，逐字引用：

> "These labs are open to the public under the (friendly, but also mandatory) condition that to preserve their value as a teaching tool, solutions not be posted publicly by anybody."

- `raw.githubusercontent.com/CS144/imp/master/LICENSE` → **HTTP 404**（无独立 LICENSE）
- `raw.githubusercontent.com/CS144/cs144.github.io/master/LICENSE` → **HTTP 404**
- `CS144` 组织下仅 `cs144.github.io` 与 `imp` 两个仓库

**判读**：只授予「公开可读」，**未明确授予商业使用或衍生权**。翻译其课件应视为需授权。

---

## 对 Phase 1 的直接影响

原计划「先做 6.824」。~~按核实结果，**6.824 可以按逐字稿翻译推进（CC BY 3.0 US）**，但 CS 61A 必须改走讲解路线。~~

**修正后（2026-09-28 二次核实）**：**6.824 只能走讲解路线**，
因为它的 CC BY 3.0 US 徽章**只在主页**，而讲义 `notes/l01.txt` 无任何声明 ⇒ 讲义授权 **`未确认`**；
**逐字稿翻译路线未解锁**，同时**双语原文对照不注入**。原文表述中「6.824 可翻译」的部分已作废。
**这不是「6.824 无授权」**（主页徽章真实存在）—— 是「**讲义那份文件没有许可依据**」。

⚠️ **第三次修正（同日）——CS 61A 与 6.824 并不相同，此前把它们并列是错的：**

| | 6.824 讲义 | CS 61A |
| --- | --- | --- |
| 站方表态 | **沉默**：没有许可，也没有版权声明 | **明确**：`Copyright ©2026, Regents of the University of California` |
| 分类 | `unknown`（未声明） | `forbidden`（明确保留） |
| 我们的做法 | 只做**原创讲解**（讲思想、不复制表达） | ⛔ **不做这门课** |

两者在法律默认状态上其实一样（都等于保留所有权利），
但**权利人是否表过态**决定我们的行为：
没人表态 ⇒ 我们谨慎地只做讲解；**权利人明确声明了版权 ⇒ 按项目方针直接拒绝**，
而不是「只做讲解」—— 那样容易让人以为我们在蹭一门明确不开放的课。

| 做法 | 6.824 | CS 61A | OCW / Composing Programs |
| --- | --- | --- | --- |
| 原创概念讲解（我们自己写） | ✅ **可做（唯一路线）** | ⛔ **不做该课程** | ✅ 可做 |
| 逐字稿翻译 | ⛔ **不产出**（讲义 `未确认`） | ⛔ 不可做 | ✅ 可做（NC + SA） |
| 视频字幕翻译 | ⚠️ 需先确认视频权利 | ⛔ 不可做 | ✅ 可做（NC + SA） |
| 转载课件 PDF | ⛔ **不做**（`redistribution = "unknown"`） | ⛔ 不可做 | ✅ 可做（NC + SA） |
| 术语表、学习路径、原创配图 | ✅ 可做 | ⛔ 不做 | ✅ 可做 |
| 作业 / Lab 解答翻译 | ⛔ **永久排除** | ⛔ **永久排除** | ⛔ **永久排除** |

**三条可行路线：**

1. **讲解路线（默认，可立即开工）** —— 只发布我们自己撰写的概念讲解，不复制原文表达。所有课程均安全。
   **这是 6.824 现行唯一路线。**
2. ~~**6.824 逐字稿翻译路线（已解锁）** —— CC BY 3.0 US 允许翻译与商用，履行署名义务即可。~~
   **【已作废·2026-09-28 二次核实】逐字稿路线未解锁。** 徽章只在主页，讲义 `notes/l01.txt` 无任何声明。
   代码侧已落地：`validate.py` 对 `output_mode = "transcript"` **退出码 1 拒绝**，
   `build_site.py` **不注入**双语原文对照块。**若将来要重启此路线，必须先取得讲义自身的许可依据。**
3. **授权路线（仅 15-445 / CS 144 需要）** —— 这两者无开放许可，须书面申请。**CS 61A 不走这条路**：它已明确声明版权，我们直接不做该课程。
   （6.824 的讲义若也要走逐字稿，同样属于需要先取得依据的情形。）

## 待抓取清单（尚未核实的部分）

- [ ] `mit-pdos/6.5840-golabs-*` 发行包内是否另有 `LICENSE` —— `g.csail.mit.edu` 不可达，GitHub 上无对应仓库
- [ ] 6.824 讲座**视频**的版权归属细节 —— MIT 页面仅嵌 YouTube，视频本体权利声明无从取得
- [x] ~~6.824 / 6.S081 主页徽章**是否覆盖全部子页面**（目前只有主页有标注，属推断而非原文）~~
      → **6.824 部分已解答（2026-09-28）：不覆盖，或者说无法确立覆盖。**
      证据：讲义 `notes/l01.txt` 无许可标注、无版权声明、无 CC 链接（0/0/0）⇒ **讲义 `未确认`**。
      → **6.1810 部分仍未核实**：其 `general.html` 有徽章，但**其讲义文件未单独取证**，覆盖范围同样未确立。
- [ ] 6.824 **主页徽章在许可文本上是否指名覆盖讲义**（徽章只是链到 CC 的通用许可文本，未列覆盖文件）
- [ ] CS 144 是否有其他书面授权渠道（当前只有 README 的一句话自订条款）

## 记录格式（后续新课程沿用）

| 课程 | 材料类型 | 许可条款 | 来源 URL | 访问日期 | 允许商用 | 允许衍生 | 有 SA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MIT 6.5840/6.824 | **主页** | CC BY 3.0 US（徽章仅此一处） | <https://pdos.csail.mit.edu/6.824/> | 2026-09-28 | ✅（就主页而言） | ✅（就主页而言） | ❌ |
| MIT 6.5840/6.824 | **讲义 `notes/l01.txt`** | **无任何声明 → `未确认`（默认保留所有权利）** | <https://pdos.csail.mit.edu/6.824/notes/l01.txt> | 2026-09-28 | ⚠️ 未确认 | ⚠️ 未确认 | ⚠️ 未确认 |
| MIT 6.5840/6.824 | 幻灯片 | ⚠️ 未单独取证（与讲义同处理 = `未确认`） | — | 2026-09-28 | ⚠️ 未确认 | ⚠️ 未确认 | ⚠️ 未确认 |
| MIT 6.5840/6.824 | Lab 代码 | 课程条款禁止公开 | <https://pdos.csail.mit.edu/6.824/labs/collab.html> | 2026-09-28 | — | — | — |
| MIT 6.5840/6.824 | golabs 发行包 | ⚠️ 未核实 | `git://g.csail.mit.edu/6.5840-golabs-2026` | 2026-09-28 | ⚠️ | ⚠️ | ⚠️ |
| MIT 6.5840/6.824 | 视频（2020-） | YouTube 平台条款 | <http://nil.csail.mit.edu/6.824/2020/video/1.html> | 2026-09-28 | ⚠️ | ⚠️ | ⚠️ |
| MIT 6.1810/6.S081 | 主页 / 讲座页 | CC BY 3.0 US | <https://pdos.csail.mit.edu/6.1810/> | 2026-09-28 | ✅（就主页而言） | ✅（就主页而言） | ❌ |
| MIT 6.1810/6.S081 | 讲义文件 | ⚠️ 未单独取证 → `未确认`（沿用 6.824 的教训） | — | 2026-09-28 | ⚠️ 未确认 | ⚠️ 未确认 | ⚠️ 未确认 |
| MIT xv6 / xv6 book | 源码 / 教材 | MIT License | <https://raw.githubusercontent.com/mit-pdos/xv6-riscv/riscv/LICENSE> | 2026-09-28 | ✅ | ✅ | ❌ |
| MIT OCW | 课程材料 | CC BY-NC-SA 4.0 | <https://ocw.mit.edu/terms/> | 2026-09-28 | ❌ | ✅ | ✅ |
| Composing Programs 3ed | 教材 | CC BY-NC-SA 4.0 | <https://composingprograms.com/3ed/> | 2026-09-28 | ❌ | ✅ | ✅ |
| CS 61A | 课件/作业/视频 | **明确声明版权 → 保留所有权利**（`Copyright ©2026, Regents of the University of California`） | <https://cs61a.org/fa26/> | 2026-09-28 | ❌ | ❌ | — |
| CMU 15-445 | 课件 | 未声明 → 保留所有权利 | <https://15445.courses.cs.cmu.edu/> | 2026-09-28 | ❌ | ❌ | — |
| Stanford CS 144 | 站点 | 未声明 | <https://cs144.github.io/> | 2026-09-28 | ❌ | ❌ | — |
| Stanford CS 144 | 实验代码 | 自订：公开可读但禁发解答 | <https://raw.githubusercontent.com/CS144/imp/master/README.md> | 2026-09-28 | ⚠️ 未授予 | ⚠️ 未授予 | — |

## 已知的两个陷阱（务必记住）

1. **「没有声明许可」≠「可以自由使用」，而「主页有 CC 徽章」≠「整站都能随便用」。
   —— 后半句是二次核实（2026-09-28）补上的。**
   6.824 讲义与 15-445 是**未声明**类（`unknown`：只做原创讲解）；CS 61A 是**明确声明版权**类（`forbidden`：不做）。两者法律默认状态相同，但权利人是否表态决定我们的行为 ——
   但 6.824 **主页**确实有 CC BY 3.0 US 徽章（这一点上一轮没错，**不是**「无许可」）。
   **新增的关键限定**：该徽章**全站只出现在主页**，讲义 `notes/l01.txt` 无任何声明
   ⇒ **徽章管不到讲义**，讲义授权 `未确认`。
   判断时既不能只看文字（会漏掉徽章），也不能只看主页（会漏掉子页面的课程条款），
   **更不能只看课程入口页 —— 必须核到我们实际要用的那份文件。**
2. **同一个项目里，不同材料类型的授权经常不同。** CS 61A 课程站是保留所有权利，但它的教材
   Composing Programs 是 CC BY-NC-SA 4.0；6.824 主页是 CC BY 3.0 US，讲义无任何声明，Lab 代码禁止公开。
   这也是 `course.toml` 里要按 `[license.materials]` 分材料类型逐项核实的原因。

### 补充陷阱（第一轮新增）

3. **`rel="license"` 徽章是纯图片链接，没有可见文字。** 6.824 / 6.1810 的授权**全部信息只存在于 `href` 里**。
   用 `grep -i license` 扫可见文本会得到「命中 0」的假阴性 —— 上一版就是这样误判的。
   **但找到徽章只解决了一半问题**：还要问「它覆盖哪些文件」。见第 7 条。
4. **`mit-pdos` 组织的仓库许可不统一。** 同组织下并存 MIT License（`xv6-riscv`、`xv6-book`、`xv6-public`）、
   CC BY-NC-ND 4.0（`6.1600-notes`，含 **NoDerivatives**）、以及无 LICENSE（`xv6-riscv-book`）。
   **不能由「mit-pdos 的 xv6 是 MIT」推出「6.824 lab 也是 MIT」。**
5. **GitHub 404 具有二义性。** `raw.githubusercontent.com` 对「仓库不存在」和「文件不存在」都返回 404。
   本轮通过**逐个仓库页**（`github.com/mit-pdos/6.824-golabs-2024` → 404）与
   **组织仓库列表三页全量枚举**交叉确认：mit-pdos 下确实没有 6.824 仓库。
6. **授权可能写在 `README.md` 而不是 `LICENSE`。** CS 144 就是这种情况 —— 只试 `LICENSE` 会漏掉。

### 二次核实新增陷阱（2026-09-28）

7. **「找到了许可」不等于「许可覆盖我们实际要用的那份文件」。**
   上一轮找到 6.824 主页徽章后，直接推及「讲座笔记 / 幻灯片可翻译、可转载」——
   但**核实清单里从来没有 `notes/*.txt`**。二次核实补上 `notes/l01.txt`：
   `rel="license"` **0**、CC 链接 **0**、版权声明 **0**。
   **徽章覆盖讲义这件事，自始至终只是推断，现在被原文否定。**
   **规则**：核实范围必须包含**我们实际依据的文件**，而不是只核课程入口页；
   拿不到该文件的许可依据时，按 `未确认`（默认保留所有权利）处理 —— 即**不产出逐字稿与双语原文对照**。

### 第三轮新增陷阱（2026-09-28，CS168 复核时发现）

| # | 坑 | 实例 |
| --- | --- | --- |
| **十二** | **404 页会被当成内容页抓下来，而且多个不同 URL 返回的字节数完全相同** | CS168 取证的章节 URL 是猜的（`/introduction.html`、`/ip.html`、`/routing.html`），三页各返回 **18,034 B** —— 与一个**故意编造**的 URL 返回**完全相同的页面**。在 404 上统计「许可声明 0 处」毫无意义。**判据：多个不同 URL 的字节数完全一致 ⇒ 先读 `<title>` 与正文，不要统计。** |
| **十三** | **课程站可能只是跳转壳，真站在「当学期」子域** | `cs168.io` 返回 **285 B**，`<title>Redirecting to https://fa26.cs168.io</title>`；真站在 `fa26.cs168.io`。**取证必须跟到跳转终点**，否则又是一次 404 统计（`cs168.io/schedule.html` 实测 404）。 |

> 这两条合起来说明一件事：**「抓到了页面」不等于「抓到了那个页面」。**
> 现有的「000 不代表 404」只覆盖了**抓取失败**；这两条覆盖的是**抓取成功但抓错了东西** ——
> 更隐蔽，因为它不会报错，只会安静地给出一堆「0 处声明」。

### 第四轮新增陷阱（2026-09-28）：「抓到了 ≠ 抓对了」的镜像

| # | 坑 | 实例 |
| --- | --- | --- |
| **十四** | **检索不到 ≠ 不存在。PDF 的文字层会把单词拆开**（字距/连字伪影），于是完整词组的检索返回 **0 命中**，而内容其实就在那一页。**破法：去掉全部空白后重搜，或改用词的截断形式。** | CS168 幻灯片 s38 的原始抽取是 `Yet  change must  be backward compat i bl e, i ncrement al , and "in place"` —— 所以 `backward compatible` 与 `incremental` 都搜不到，而 `backward compat`、`in place`、以及去空白后的 `backwardcompatible` **都命中 s38**。Lead 亲眼复核确认，**并推翻了自己「0 命中 ⇒ 无出处」的结论**。 |

> 坑十二、十三讲的是「**抓到了页面 ≠ 抓到了那个页面**」—— 抓取成功但抓错了对象；
> 坑十四讲的是反过来的事：**检索确实执行了，但工具本身把证据打散了**。
> 前者靠读 `<title>`、比字节数破；后者只能靠**换第二把尺子**（去空白重搜、词形截断）破。
>
> **★ 这一条对授权核实尤其要紧。** licence 检查大量依赖关键词检索
> （`creativecommons.org/licenses/`、`Copyright`、`all rights reserved`、`rel="license"`…），
> 而我们取证的对象里有不少是 **PDF 讲义**（ETH DDCA 讲义、MIT OCW 讲稿、CS168 幻灯片）。
> **一条许可声明若恰好落在断字里，就会被判成「0 声明」——那是最严重的一类假阴性**，
> 因为它会把一门 A 级课程误判成 B/C 级，或者反过来把「保留所有权利」漏掉。
>
> **因此：凡是对 PDF 下「未声明 / 0 命中」的结论，必须再用去空白与词形截断各搜一遍。**
> 对 HTML 页面无此问题（没有 PDF 文字层），但**HTML 里的注释与图标库许可仍会造成假阳性**（见坑九）。


### 陷阱十五 · PDF 文本抽取会**静默丢掉 Θ**，于是「源里有没有 Θ」永远数成 0

**来源**：MIT 6.006 第 1 讲第 2 轮复核者发现（2026-09-28）。

**现象**：这门课全部现有抽取产物（`.faithful.txt` / `.text.txt` / `.clean.txt` / `.flow.txt`）
**都把 Θ 丢掉了** —— 输出里 `Θ(1)`、`Θ(log n)` 显示成 `(1)`、`(log n)`。

**根因**：Θ 用的是 OML 字体（`cmmi`/`cmsy` 一类数学字体），**字符落在字体的私有槽位里**。
复核者把讲义页的内容流按原始字节枚举，发现：

```
0x00 = −      0x02 = Θ      0x03 = (其他)      0x0f = •      0x15 = ≥
```

**`0x02` 就是 Θ**，它**不在** Unicode 映射里。多数抽取器只认识拉丁区间，
遇到数学字体槽位就**跳过或留空**，于是 Θ 变成一个不可见字符或直接消失。

**为什么这比「抽取失败」更危险**：
抽取失败会让输出变短、报错、看得出不对。**静默丢字符不会** ——
文本长度、行数、段落结构全都正常，**只有那一个符号不见了**。
于是「源里有没有 Θ」这个问题会被稳定地回答成「没有」。

**实测影响**：在本例中，如果核对着复用仓库里的任何一份产物去数 Θ，
会得到 **Θ = 0 次**；而正确值是 **14 次**（讲义 6 页里 9 + 5）。
**一个「源里没有 Θ」的结论会被这份产物稳定地支持 —— 而它是错的。**

**因此定的规则**：

> **凡是要断言「源里有没有某个符号 / 某个词出现几次」，必须说明是用什么方法数的；
> 用通用 PDF 抽取器数数学符号，结论一律不采信。**
>
> 正确做法二选一：
> 1. **在内容流里数原始字节**（像本例的复核者那样，直接找 `0x02`）；
> 2. **栅格化后看图**（把那一页渲染成图片，用眼睛确认符号在不在）。
>
> 并且：**「数不到」必须区分是「源里没有」还是「我的工具看不见」。**
> 这两件事在输出上完全一样，而结论相反。

**与陷阱十四的关系**：
- **陷阱十四**（PDF 文本层断词，`backward compat i bl e`）会让**多词短语**搜不到；
- **陷阱十五**（数学字体槽位）会让**单个符号**搜不到。
两者共同的教训是：**在 PDF 上做「搜不到 ⇒ 不存在」的推断之前，
先证明你的抽取管道能把该类型的字符原样送出来。**
