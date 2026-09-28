# 课程目录 · Course Catalog

> 授权状态已在 2026-09-28 经**实际抓取**核实。每条都附逐字原文引用与来源 URL。
> 方法：本机 DNS 为 Clash fake-IP（学术域名解析到 `198.18.0.x`），`web_fetch` 会拒绝非公网地址、
> `web_search` 无 API key，因此统一用 `curl -x socks5h://127.0.0.1:7892` 抓取
> （**必须是 SOCKS5，`socks5h://`**；同端口的 HTTP 代理模式不可用）。抓取到的原始页面留证在 `docs/_fetch/`。

## ⚠️ 本轮修正：上一版结论有四处错误

本文件上一版把 6.824 判为「未声明许可」、把 Composing Programs 判为 CC BY-NC-SA 3.0。**两处都不对**，原因是只扫了可见文字、以及引用了过期版本。修正如下：

| 上一版结论 | 实测真相 | 错因 |
| --- | --- | --- |
| 6.824「未声明任何许可」 | **主页有 CC BY 3.0 US 徽章**（`rel="license"`） | 徽章是**纯图片链接，无任何可见文字**；只扫文字必然漏掉 |
| Composing Programs = CC BY-NC-SA **3.0** | 现行 `/3ed/` = CC BY-NC-SA **4.0** | 引用了旧版教材的措辞；站点现已 302 到 `/3ed/` |
| CS 144「未确认」 | 实验 README 有**明确自订条款** | 只试了 `LICENSE` 文件；授权写在同一仓库的 `README.md` 里 |
| 6.1810 未列 | **CC BY 3.0 US**，配套 xv6 教材 **MIT License** | 未抓取 |

> 教训：**`rel="license"` 徽章的授权信息全在 `href` 里，纯文本抽取会 100% 丢失这条证据。**

## 结论总表

| 课程 | 授权状态 | 对我们的含义 |
| --- | --- | --- |
| **MIT 6.5840 / 6.824** | 🟢 **CC BY 3.0 US** | 只有署名义务：**可商用、可翻译、无 SA**。但 Lab 代码另有禁发条款 |
| **UC Berkeley CS 61A** | 🔴 **未声明许可 = 保留所有权利** | 逐字稿 / 字幕 / 课件转载**一律不可做** |
| MIT 6.1810 / 6.S081 | 🟢 **CC BY 3.0 US**；xv6 教材 **MIT** | 可商用、可翻译、无 SA |
| MIT OpenCourseWare | 🟡 **CC BY-NC-SA 4.0** | 可改编，**禁止商用**且 **SA 传染** |
| Composing Programs（3ed） | 🟡 **CC BY-NC-SA 4.0** | 可改编，**禁止商用** + 相同方式共享 |
| CMU 15-445 | 🔴 **未声明许可 = 保留所有权利** | 同 CS 61A |
| Stanford CS 144 | ⚠️ **混合**：站点无声明；实验 README 自订「公开可读但禁发解答」 | 未授予明确的商用与衍生权 |

**关键判断：6.824 并非「无授权」而是「开放授权」，因此 Phase 1 的 6.824 逐字稿翻译在法律上可行（需署名）。**
但 CS 61A 仍然是红线。

---

## 目标课程

### MIT 6.5840 / 6.824 · 分布式系统

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://pdos.csail.mit.edu/6.824/> |
| 许可 | **CC BY 3.0 US**（Creative Commons Attribution 3.0 United States） |
| 核实范围 | 主页、`/general.html`、`/schedule.html`、`/questions.html`、`/labs/lab-mr.html`、`/labs/collab.html`、2020 与 2018 历史主页 |
| 出现位置 | **仅主页**（含 2018 / 2020 历史主页）；其余页面**均无**标注 |

主页原文 HTML（逐字，这是**唯一**的授权证据）：

```html
<a rel="license" href="https://creativecommons.org/licenses/by/3.0/us/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/us/88x31.png" /></a>
```

**判读**：`by/3.0/us` 是**只有 BY 一项**的许可 —— 无 NC、无 SA、无 ND。

- ✅ 翻译讲座笔记 / 逐字稿：**可做**（署名 + 链接许可 + 标明已修改）
- ✅ 商用：**可做**（无 NC）
- ✅ 译文不必以相同许可发布（无 SA）
- ⛔ **Lab 代码不得公开** —— 这是与 CC 并行的另一层课程条款，来源 <https://pdos.csail.mit.edu/6.824/labs/collab.html>，逐字引用：
  > "Please do not publish your code or make it available to current or future 6.5840 students."
- ⚠️ **视频**：当前 2026 版无视频。2020 及更早是 **YouTube 嵌入**（<http://nil.csail.mit.edu/6.824/2020/video/1.html> 全文即一个 `youtube.com/embed/cQP8WApzIQQ` 的 iframe），**视频本体另受 YouTube 条款约束**。
- ⚠️ **golabs 发行包内是否另有 `LICENSE`：未核实。** Lab 代码走 MIT 自建 git（`git clone git://g.csail.mit.edu/6.5840-golabs-2026`），不在 GitHub；且 `g.csail.mit.edu` 实测**不可达**（4 次 `000`）。

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
  而 `pdos.csail.mit.edu/6.824/` 课程站带的是 CC BY 3.0 US（更宽松）。**走课程站比走 OCW 更自由**（无 NC、无 SA）。
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
| 许可 | **CC BY 3.0 US**（与 6.824 同一徽章、同一 href） |
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

原计划「先做 6.824」。按核实结果，**6.824 可以按逐字稿翻译推进（CC BY 3.0 US）**，但 CS 61A 必须改走讲解路线。

| 做法 | 6.824 | CS 61A | OCW / Composing Programs |
| --- | --- | --- | --- |
| 原创概念讲解（我们自己写） | ✅ 可做 | ✅ 可做 | ✅ 可做 |
| 逐字稿翻译 | ✅ 可做（署名） | ⛔ 不可做 | ✅ 可做（NC + SA） |
| 视频字幕翻译 | ⚠️ 需先确认视频权利 | ⛔ 不可做 | ✅ 可做（NC + SA） |
| 转载课件 PDF | ✅ 可做（署名） | ⛔ 不可做 | ✅ 可做（NC + SA） |
| 术语表、学习路径、原创配图 | ✅ 可做 | ✅ 可做 | ✅ 可做 |
| 作业 / Lab 解答翻译 | ⛔ **永久排除** | ⛔ **永久排除** | ⛔ **永久排除** |

**三条可行路线：**

1. **讲解路线（默认，可立即开工）** —— 只发布我们自己撰写的概念讲解，不复制原文表达。所有课程均安全。
2. **6.824 逐字稿翻译路线（已解锁）** —— CC BY 3.0 US 允许翻译与商用，履行署名义务即可。
3. **授权路线（仅 CS 61A / 15-445 / CS 144 需要）** —— 这三者无开放许可，须书面申请。

## 待抓取清单（尚未核实的部分）

- [ ] `mit-pdos/6.5840-golabs-*` 发行包内是否另有 `LICENSE` —— `g.csail.mit.edu` 不可达，GitHub 上无对应仓库
- [ ] 6.824 讲座**视频**的版权归属细节 —— MIT 页面仅嵌 YouTube，视频本体权利声明无从取得
- [ ] 6.824 / 6.S081 主页徽章**是否覆盖全部子页面**（目前只有主页有标注，属推断而非原文）
- [ ] CS 144 是否有其他书面授权渠道（当前只有 README 的一句话自订条款）

## 记录格式（后续新课程沿用）

| 课程 | 材料类型 | 许可条款 | 来源 URL | 访问日期 | 允许商用 | 允许衍生 | 有 SA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MIT 6.5840/6.824 | 主页 / 讲座笔记 / 幻灯片 | CC BY 3.0 US | <https://pdos.csail.mit.edu/6.824/> | 2026-09-28 | ✅ | ✅ | ❌ |
| MIT 6.5840/6.824 | Lab 代码 | 课程条款禁止公开 | <https://pdos.csail.mit.edu/6.824/labs/collab.html> | 2026-09-28 | — | — | — |
| MIT 6.5840/6.824 | golabs 发行包 | ⚠️ 未核实 | `git://g.csail.mit.edu/6.5840-golabs-2026` | 2026-09-28 | ⚠️ | ⚠️ | ⚠️ |
| MIT 6.5840/6.824 | 视频（2020-） | YouTube 平台条款 | <http://nil.csail.mit.edu/6.824/2020/video/1.html> | 2026-09-28 | ⚠️ | ⚠️ | ⚠️ |
| MIT 6.1810/6.S081 | 主页 / 讲座 | CC BY 3.0 US | <https://pdos.csail.mit.edu/6.1810/> | 2026-09-28 | ✅ | ✅ | ❌ |
| MIT xv6 / xv6 book | 源码 / 教材 | MIT License | <https://raw.githubusercontent.com/mit-pdos/xv6-riscv/riscv/LICENSE> | 2026-09-28 | ✅ | ✅ | ❌ |
| MIT OCW | 课程材料 | CC BY-NC-SA 4.0 | <https://ocw.mit.edu/terms/> | 2026-09-28 | ❌ | ✅ | ✅ |
| Composing Programs 3ed | 教材 | CC BY-NC-SA 4.0 | <https://composingprograms.com/3ed/> | 2026-09-28 | ❌ | ✅ | ✅ |
| CS 61A | 课件/作业/视频 | 未声明 → 保留所有权利 | <https://cs61a.org/fa26/> | 2026-09-28 | ❌ | ❌ | — |
| CMU 15-445 | 课件 | 未声明 → 保留所有权利 | <https://15445.courses.cs.cmu.edu/> | 2026-09-28 | ❌ | ❌ | — |
| Stanford CS 144 | 站点 | 未声明 | <https://cs144.github.io/> | 2026-09-28 | ❌ | ❌ | — |
| Stanford CS 144 | 实验代码 | 自订：公开可读但禁发解答 | <https://raw.githubusercontent.com/CS144/imp/master/README.md> | 2026-09-28 | ⚠️ 未授予 | ⚠️ 未授予 | — |

## 已知的两个陷阱（务必记住）

1. **「没有声明许可」≠「可以自由使用」，而「主页有 CC 徽章」≠「整站都能随便用」。**
   6.824、15-445、CS 61A 都是无声明类，法律状态是保留所有权利；
   但 6.824 主页确实有 CC BY 3.0 US 徽章，属**开放授权** —— 两者不可混为一谈。
   判断时既不能只看文字（会漏掉徽章），也不能只看主页（会漏掉子页面的课程条款）。
2. **同一个项目里，不同材料类型的授权经常不同。** CS 61A 课程站是保留所有权利，但它的教材
   Composing Programs 是 CC BY-NC-SA 4.0；6.824 主页是 CC BY 3.0 US，但 Lab 代码禁止公开。
   这也是 `course.toml` 里要按 `[license.materials]` 分材料类型逐项核实的原因。

### 补充陷阱（本轮新增）

3. **`rel="license"` 徽章是纯图片链接，没有可见文字。** 6.824 / 6.1810 的授权**全部信息只存在于 `href` 里**。
   用 `grep -i license` 扫可见文本会得到「命中 0」的假阴性 —— 上一版就是这样误判的。
4. **`mit-pdos` 组织的仓库许可不统一。** 同组织下并存 MIT License（`xv6-riscv`、`xv6-book`、`xv6-public`）、
   CC BY-NC-ND 4.0（`6.1600-notes`，含 **NoDerivatives**）、以及无 LICENSE（`xv6-riscv-book`）。
   **不能由「mit-pdos 的 xv6 是 MIT」推出「6.824 lab 也是 MIT」。**
5. **GitHub 404 具有二义性。** `raw.githubusercontent.com` 对「仓库不存在」和「文件不存在」都返回 404。
   本轮通过**逐个仓库页**（`github.com/mit-pdos/6.824-golabs-2024` → 404）与
   **组织仓库列表三页全量枚举**交叉确认：mit-pdos 下确实没有 6.824 仓库。
6. **授权可能写在 `README.md` 而不是 `LICENSE`。** CS 144 就是这种情况 —— 只试 `LICENSE` 会漏掉。
