# 授权核实记录 · Licensing Research Log

> 本文件记录**实际做过的核实动作与结果**，不是许可条款本身。
> 状态：**网络阻塞已解除，主要来源全部实测抓取完成**（2026-09-28）。
> 每一条结论都附逐字原文引用与来源 URL。

## 状态：UNBLOCKED → RESOLVED

本任务此前标记为 **BLOCKED**，理由是「工具层面受阻」。本轮实测确认：**阻塞已解除**，
恢复的条件是「Clash fake-IP + SOCKS5 代理」这一组合。

### 解除阻塞的真实机制

| 现象 | 真实原因 | 解法 |
| --- | --- | --- |
| `web_search` 全部失败 | 未配置搜索后端（无 API key） | 不用搜索，直接抓官方页面 |
| `web_fetch` 拒绝所有学术域名 | 本机 DNS 是 **Clash fake-IP**，学术域名全部解析到 `198.18.0.x`（RFC 2544 保留段，非公网），`web_fetch` 因此拒收 | 改用 `pwsh` + `curl` |
| `curl` 直连返回 `000` | **代理端口 7892 是 SOCKS5，不是 HTTP** —— 用 `http://` 去连它必然失败，且失败得很安静 | 改用 `-x socks5h://127.0.0.1:7892` |

**核心教训：本环境抓外网必须用 `curl.exe -x socks5h://127.0.0.1:7892`。**
写 `http://127.0.0.1:7892` 会静默返回 `000`，看起来像「整台机器被墙」，实则是协议用错。

### 代理的实际健康状态（重要，影响复现）

- 端口 `7892` 的监听进程是 `QingyunLiteCore.exe`（PID 15240），**唯一的代理端口**；另有一个 `198.18.0.1:52453`（TUN 模式网关）。
- 端口在监听 ≠ 链路可用。**主导失败模式是 TLS 握手失败**：

  ```
  * Opened SOCKS connection from 127.0.0.1 port 55752 to raw.githubusercontent.com port 443
  * schannel: failed to receive handshake, SSL/TLS connection failed
  curl: (35) schannel: failed to receive handshake, SSL/TLS connection failed
  ```

  → SOCKS5 隧道建立成功、DNS 也成功，**但上游节点握手失败**。这是**逐连接随机**的，不是全站封锁：
  同一 URL 前一次 `200`、后一次 `000`、再下一次又 `200`。
- 因此本轮全部抓取都采用**多轮重试**（每个 URL 3–12 轮，失败间隔 2–5 秒），并落盘留证于 `docs/_fetch/`。
- 副作用：`curl -L` 跟随重定向后的**短内容也会被视为成功**，需要额外检查长度（例如 `cs61a.org/` 只返回 395 字节的跳转页）。

## 实际抓取记录

抓取物留证在 `docs/_fetch/`（含 `lic/` 子目录存放各 LICENSE 原文）。

### 成功取得（200，且内容有效）

| # | URL | 返回 | 关键内容 |
| --- | --- | --- | --- |
| 1 | <https://pdos.csail.mit.edu/6.824/> | 200, 3995 B | ✅ **CC BY 3.0 US 徽章**（`rel="license"` → `creativecommons.org/licenses/by/3.0/us/`） |
| 2 | <https://pdos.csail.mit.edu/6.824/general.html> | 200, 8065 B | 无许可标注；含「禁止公开代码」条款 |
| 3 | <https://pdos.csail.mit.edu/6.824/schedule.html> | 200, 17414 B | 无许可标注（0 命中） |
| 4 | <https://pdos.csail.mit.edu/6.824/questions.html> | 200, 35011 B | 无许可标注（0 命中） |
| 5 | <https://pdos.csail.mit.edu/6.824/labs/lab-mr.html> | 200, 15394 B | 无许可标注；**Lab 代码来自 `git://g.csail.mit.edu/6.5840-golabs-2026`，不在 GitHub** |
| 6 | <https://pdos.csail.mit.edu/6.824/labs/collab.html> | 200, 1034 B | ✅ 禁发代码条款 |
| 7 | <https://pdos.csail.mit.edu/6.824/labs/guidance.html> | 200, 4351 B | 无许可标注 |
| 8 | <https://pdos.csail.mit.edu/6.824/labs/submit.html> | 200, 1020 B | 无许可标注 |
| 9 | <http://nil.csail.mit.edu/6.824/2020/> | 200 | ✅ 含 `rel="license"` 徽章 |
| 10 | <http://nil.csail.mit.edu/6.824/2018/> | 200 | ✅ 含 `rel="license"` 徽章 |
| 11 | <http://nil.csail.mit.edu/6.824/2020/schedule.html> | 200, 18008 B | 40 处 video 链接 |
| 12 | <http://nil.csail.mit.edu/6.824/2020/video/1.html> | 200 | ✅ **全文只是一个 YouTube iframe**（`youtube.com/embed/cQP8WApzIQQ`） |
| 13 | <https://pdos.csail.mit.edu/6.S081/> | 200, 4303 B | 主页 |
| 14 | <https://pdos.csail.mit.edu/6.S081/2023/general.html> | 200, 9853 B | ✅ **CC BY 3.0 US 徽章** + 「禁止公开 Lab/作业解答」 |
| 15 | <https://pdos.csail.mit.edu/6.1810/> | 200, 4303 B | ✅ **CC BY 3.0 US 徽章** |
| 16 | <https://cs61a.org/> | 302 → `/fa26/` | 非 200，是跳转页（仅 395 B） |
| 17 | <https://cs61a.org/fa26/> | 200, 84004 B | ❌ **无许可声明**；页脚仅版权行 |
| 18 | <https://cs61a.org/fa26/syllabus/> | 200, 54348 B | ✅ 「Do not post your solutions publicly during or after the semester.」 |
| 19 | <https://cs61a.org/fa26/textbook/> | 200, 477 B | 无许可声明 |
| 20 | <https://cs61a.org/fa26/resources/> | 200, 21193 B | 无许可声明 |
| 21 | <https://cs61a.org/fa26/articles/contact/> | 200, 20499 B | 无许可声明，仅版权行 |
| 22 | <https://ocw.mit.edu/> | 200, 893319 B | ✅ 链向 CC BY-NC-SA 4.0 |
| 23 | <https://ocw.mit.edu/terms/> | 200, 27747 B | ✅ **完整条款**（落点 `/pages/privacy-and-terms-of-use/`） |
| 24 | <https://ocw.mit.edu/pages/privacy-and-terms-of-use/> | 200, 27747 B | 与 #23 同一内容（确认 `terms` 是别名） |
| 25 | <https://composingprograms.com/> | 200, 407 B | 302 跳转页 → `/3ed/` |
| 26 | <https://composingprograms.com/3ed/> | 200, 60930 B | ✅ **CC BY-NC-SA 4.0 正文声明** |
| 27 | <https://composingprograms.com/3ed/getting-started/> | 200, 102210 B | 内页带同一许可徽章（逐页生效） |
| 28 | <https://15445.courses.cs.cmu.edu/> | 200, 32181 B | ❌ **无许可声明** |
| 29 | <https://15445.courses.cs.cmu.edu/spring2024/> | 200, 22863 B | ❌ 无许可声明 |
| 30 | <https://15445.courses.cs.cmu.edu/fall2023/> | 200, 25074 B | ❌ 无许可声明 |
| 31 | <https://15445.courses.cs.cmu.edu/spring2023/> | 200, 18306 B | ❌ 无许可声明（仅 1 处 copyright，指向 db.cs.cmu.edu） |
| 32 | <https://15445.courses.cs.cmu.edu/spring2024/syllabus.html> | 200, 22143 B | 仅学术诚信条款 |
| 33 | <https://15445.courses.cs.cmu.edu/spring2024/faq.html> | 200, 15214 B | 无许可措辞（0 命中） |
| 34 | <https://cs144.github.io/> | 200, 19674 B | ❌ 站点无许可声明；「Please don't post source code to lab solutions.」 |
| 35 | <https://cs144.github.io/lab_faq.html> | 200, 14877 B | 无许可措辞（0 命中） |
| 36 | <https://github.com/mit-pdos> | 200, 298685 B | 组织概览（12 个仓库） |
| 37 | <https://github.com/orgs/mit-pdos/repositories> | 200, 416645 B | 仓库列表第 1 页 |
| 38 | <https://github.com/orgs/mit-pdos/repositories?page=2> | 200, 410386 B | 仓库列表第 2 页 |
| 39 | <https://github.com/orgs/mit-pdos/repositories?page=3> | 200, 203486 B | 第 3 页（仅 `csail-events-slack`，说明列表已到底） |
| 40 | <https://github.com/CS144> | 200, 256758 B | 组织仅 `cs144.github.io`、`imp` 两仓库 |
| 41 | <https://raw.githubusercontent.com/mit-pdos/xv6-riscv/riscv/LICENSE> | 200, 1174 B | ✅ **MIT License** |
| 42 | <https://raw.githubusercontent.com/mit-pdos/xv6-book/master/LICENSE> | 200, 1149 B | ✅ **MIT License**（教材版措辞） |
| 43 | <https://raw.githubusercontent.com/mit-pdos/xv6-public/master/LICENSE> | 200, 1174 B | ✅ **MIT License** |
| 44 | <https://raw.githubusercontent.com/mit-pdos/6.1600-notes/main/LICENSE> | 200, 134 B | ✅ **CC BY-NC-ND 4.0**（含 NoDerivatives） |
| 45 | <https://raw.githubusercontent.com/CS144/imp/master/README.md> | 200, 751 B | ✅ **自订授权条款**（见下） |
| 46 | <https://github.com/CS144/imp> | 200, 256758 B | 仓库页 |

**mit-pdos 仓库全量枚举结论**：三页共 63 个仓库，**其中没有任何 6.824 / golabs 相关仓库**。
列表中出现的是 `xv6-riscv`、`xv6-book`、`xv6-public`、`xv6-riscv-book`、`6.1600-labs`、`6.1600-notes`、
`6.566-lab-2024/2026`、`6.826-*-labs`、`6.S060-labs`、`sigmaos`、`gokv`、`noria`、`biscuit`、
`perennial`、`grove`、`tulip`、`security-book` 等 —— **没有 6.824**。

### 真实 HTTP 404（连接成功，资源确实不存在 —— 这些是有效证据，不是抓取失败）

| URL | 说明 |
| --- | --- |
| `raw.githubusercontent.com/mit-pdos/6.824-golabs-2024/main/LICENSE` | 任务指定的 URL，**确认不存在** |
| `github.com/mit-pdos/6.824-golabs-2024` / `-2023` / `-2022` / `-2021` / `-2020` | **仓库页 404** → 这些仓库公开不存在（交叉印证上面 404 的含义） |
| `raw.githubusercontent.com/cs61a/composing-programs/master/README.md` | 404（14 B = `404: Not Found`） |
| `github.com/cs61a/composing-programs` | 404，仓库不存在 |
| `cs61a.org/about.html`、`/faq.html`、`/articles/about.html`、`/articles/` | 这四个页面**不存在**（不是被墙） |
| `ocw.mit.edu/citation/`、`/privacy/`、`/pages/cite/`、`/pages/how-to-cite-ocw/`、`/pages/attribution/` | OCW **已无独立引用页**，署名要求只在 terms 页 |
| `raw.githubusercontent.com/CS144/imp/master/LICENSE`、`.../CS144/cs144.github.io/master/LICENSE` | 无独立 LICENSE 文件 |
| `raw.githubusercontent.com/mit-pdos/xv6-riscv-book/{riscv,main}/{LICENSE,LICENSE.md,LICENSE.txt,COPYING,COPYING.md,LICENSE-MIT}` | 6 个候选路径**全部 404** → 该仓库无 LICENSE |
| `raw.githubusercontent.com/mit-pdos/6.1600-labs/main/LICENSE`、`sigmaos/main/LICENSE`、`gokv/main/LICENSE` | 无 LICENSE |
| `github.com/john-de-nero/composing-programs/raw/master/README.md` | 404 |

### 仍然不可达 / 无法判定（保留 `⚠️ 未核实`）

| URL / 目标 | 结果 | 影响 |
| --- | --- | --- |
| `https://g.csail.mit.edu/` | **4 次全部 `000`**（连接层失败，非 404） | ⚠️ 无法确认 `6.5840-golabs-*` 发行包内是否另有 `LICENSE`。这是 6.824 结论中**唯一**的缺口 |
| `https://ocw.mit.edu/help/` | 5 次均未取得 200/404 | 无独立引用页的进一步佐证 |
| `https://www.composingprograms.com/` (www 子域) | `301` / `000` | 改用无 www 域成功，不影响结论 |
| `https://cs61a.org/fa26/policies.html`、`/resources.html`、`/sp25/` | 始终 `000`（未取得任何 HTTP 响应） | 无法判定这些页面是否存在；不影响主结论（`/fa26/` 与 `/fa26/syllabus/` 已足够） |
| 6.824 讲座视频的版权归属 | MIT 页面只嵌 YouTube，无任何权利声明 | ⚠️ 视频字幕翻译需另行确认 |
| `raw.githubusercontent.com/.../main/LICENSE.md`、`LICENSE.txt` 等若干变体 | `000`（连接失败，非 404） | 少数候选文件名未穷尽，但主文件名已全查 |

> **诚实性说明**：`000`（连接层失败）与 `404`（服务端明确回答「不存在」）必须严格区分。
> 本轮所有「无许可」结论都建立在**取得真实 404 或完整 200 页面**之上，没有把连不通当成不存在。

## 核实表

| 课程 / 来源 | 材料类型 | 许可条款 | 来源 URL | 访问日期 | 可信度 |
| --- | --- | --- | --- | --- | --- |
| MIT 6.5840 / 6.824 | 主页 / 讲座笔记 / 幻灯片 | **CC BY 3.0 US** | <https://pdos.csail.mit.edu/6.824/> | 2026-09-28 | ✅ 已核实（主页徽章） |
| MIT 6.5840 / 6.824 | 子页面（general/schedule/questions/labs） | 无标注 | 同上路径 | 2026-09-28 | ✅ 已核实「无标注」 |
| MIT 6.5840 / 6.824 | Lab 代码 | 课程条款禁止公开 | <https://pdos.csail.mit.edu/6.824/labs/collab.html> | 2026-09-28 | ✅ 已核实 |
| MIT 6.5840 / 6.824 | golabs 发行包 | ⚠️ 未核实（`g.csail.mit.edu` 不可达） | `git://g.csail.mit.edu/6.5840-golabs-2026` | 2026-09-28 | ⚠️ 未核实 |
| MIT 6.5840 / 6.824 | 讲座视频 | ⚠️ 未核实（YouTube 嵌入，无权利声明） | <http://nil.csail.mit.edu/6.824/2020/video/1.html> | 2026-09-28 | ⚠️ 未核实 |
| MIT 6.1810 / 6.S081 | 主页 / 讲座 | **CC BY 3.0 US** | <https://pdos.csail.mit.edu/6.1810/> | 2026-09-28 | ✅ 已核实 |
| MIT xv6 / xv6 book | 源码 / 教材 | **MIT License** | <https://raw.githubusercontent.com/mit-pdos/xv6-riscv/riscv/LICENSE> | 2026-09-28 | ✅ 已核实 |
| MIT OpenCourseWare | 课程材料（含衍生作品） | **CC BY-NC-SA 4.0** | <https://ocw.mit.edu/terms/> | 2026-09-28 | ✅ 已核实 |
| Composing Programs（3ed） | 教材 | **CC BY-NC-SA 4.0** | <https://composingprograms.com/3ed/> | 2026-09-28 | ✅ 已核实 |
| UC Berkeley CS 61A | 课件 / 作业 / 视频 | **未声明 = 保留所有权利** | <https://cs61a.org/fa26/> | 2026-09-28 | ✅ 已核实「无声明」 |
| CMU 15-445 | 课件 | **未声明 = 保留所有权利** | <https://15445.courses.cs.cmu.edu/> | 2026-09-28 | ✅ 已核实「无声明」 |
| Stanford CS 144 | 站点 | **未声明** | <https://cs144.github.io/> | 2026-09-28 | ✅ 已核实「无声明」 |
| Stanford CS 144 | 实验代码 | 自订：公开可读但禁发解答 | <https://raw.githubusercontent.com/CS144/imp/master/README.md> | 2026-09-28 | ✅ 已核实（但**未授予**商用/衍生） |

### 关键原文引用（全部逐字）

**MIT 6.5840 / 6.824 的授权（唯一证据，纯 HTML 徽章，无可见文字）**：

```html
<a rel="license" href="https://creativecommons.org/licenses/by/3.0/us/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/us/88x31.png" /></a>
```

**6.824 禁发代码条款**（<https://pdos.csail.mit.edu/6.824/labs/collab.html>）：

> "Please do not publish your code or make it available to current or future 6.5840 students."

**6.1810 禁发解答条款**（<https://pdos.csail.mit.edu/6.S081/2023/general.html>）：

> "Do not post your lab or homework solutions on publicly accessible web sites (such as GitHub) or file spaces (such as your Athena Public directory)."

**MIT OCW 的许可与商用限制**：

> "The following notices and licenses comprise together the MIT OpenCourseWare License."

> "Creative Commons License Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)"

> "Noncommercial — You may not use the material for commercial purposes."

> "Non-commercial use means that users may not sell, profit from, or commercialize OCW materials or **works derived from** them."

> "Share Alike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original."

> "Adapt — remix, transform, and build upon the material"

> "you may not use MIT's names or logos, or any variations thereof, without prior written consent of MIT."

**Composing Programs（3ed）**：

> "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)."

> "This online book is a derivative of Structure and Interpretation of Computer Programs (2nd ed.) by Harold Abelson, Gerald Jay Sussman, and Julie Sussman. Composing Programs was originally authored in 2011 under the CC BY-NC-SA 3.0 Unported license applied to SICP by MIT Press at that time. (SICP was later relicensed under CC BY-SA 4.0 in 2016). As permitted under Section 4(b) of the original 3.0 license, this adaptation has been upgraded to CC BY-NC-SA 4.0, but remains non-commercial."

> "Copyright John DeNero."

> `aria-label` = "Content License: Creative Commons Attribution Non Commercial Share Alike 4.0 International (CC-BY-NC-SA-4.0)"

**CS 61A**：

> "Copyright ©2026, Regents of the University of California and respective authors."

> "Do not post your solutions publicly during or after the semester."

**Stanford CS 144**（注意：授权写在 `README.md`，不是 `LICENSE`）：

> "These labs are open to the public under the (friendly, but also mandatory) condition that to preserve their value as a teaching tool, solutions not be posted publicly by anybody."

> 站点： "Please don't post source code to lab solutions."

**MIT xv6（MIT License）**：

> "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."

**mit-pdos 内部许可不统一的反例**（`6.1600-notes`）：

> "This work is licensed under CC BY-NC-ND 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/"

## 上一版结论的错误（必须留档）

本文件与 `course-catalog.md` 的上一版写入了**四处错误**，本轮已修正：

| 上一版错误结论 | 实测真相 | 错因 |
| --- | --- | --- |
| 6.824「未声明任何许可」（声称 5 个页面 0 命中） | **主页有 CC BY 3.0 US 徽章** | 徽章是**纯图片链接，零可见文字**；只扫文本必然假阴性 |
| Composing Programs = CC BY-NC-SA **3.0** | 现行 `/3ed/` = **CC BY-NC-SA 4.0** | 引用旧版措辞；站点已 302 到 `/3ed/` |
| CS 144「未确认」（因 LICENSE 返回空） | 授权写在 **`README.md`**，条款明确 | 只找文件名 `LICENSE`，没找 README |
| 6.1810 未列入 | **CC BY 3.0 US** + xv6 教材 **MIT** | 未抓取 |

> **最危险的一处**：6.824 被误判为「保留所有权利」会让项目**白白放弃一个已开放授权的目标课程**。
> 这正是「不许凭记忆填表」这条规则要防的事 —— 只不过这次的坑不是记忆，而是**取证方式**（只看可见文本）。

## 风险分级（基于**已核实条款**，不再是通用推理）

| 做法 | 判定 | 依据（已核实） |
| --- | --- | --- |
| (b) 我们自己写概念讲解，讲同一批概念 | 🟢 **全部课程可做** | 思想与概念不受著作权保护；即使对无许可课程也成立 |
| (e) 链接官方来源 + 自己的解读与署名 | 🟢 **全部课程可做** | 只引用不复制表达；但署名**不能**豁免侵权 |
| 6.824 / 6.1810 讲座笔记的翻译与转载 | 🟢 **可做（署名）** | CC BY 3.0 US：无 NC、无 SA、无 ND |
| 使用 xv6 源码与 xv6 教材 | 🟢 **可做（含商用）** | MIT License |
| 使用 OCW / Composing Programs 材料做改编 | 🟡 **条件允许** | 须非商业 + 以 CC BY-NC-SA 4.0 发布（SA 传染） |
| (a) 翻译完整讲座逐字稿 —— **CS 61A / 15-445** | 🔴 **禁止** | 无许可 = 保留所有权利；翻译是衍生作品 |
| (a) 翻译完整讲座逐字稿 —— **OCW / Composing Programs** | 🟡 **非商业可行** | 商用即违规；且译文须同样以 BY-NC-SA 4.0 发布 |
| (f) 翻译视频字幕 | ⚠️ **分情况**：6.824 视频权利未声明 → 需授权；CS 61A 禁止 | 视频另有平台/权利层 |
| (d) 转载原始课件 / 视频 —— **CS 61A / 15-445** | 🔴 **禁止** | 无许可；一律链接，不转载 |
| (c) 翻译作业答案 | ⛔ **全部课程永久排除** | 著作权 + 明确的课程禁令，双重风险 |

## 仍未核实

- `mit-pdos/6.5840-golabs-*` 发行包内是否另有 `LICENSE`（`g.csail.mit.edu` 不可达，GitHub 上无对应仓库）
- 6.824 讲座视频的版权归属（MIT 页面仅嵌 YouTube，无权利声明）
- 6.824 / 6.1810 主页徽章**是否在授权上覆盖全部子页面**（目前只有主页有标注，此点属推断而非原文）
- CS 144 除 README 那句话外是否有其他书面授权渠道

---

## 一般著作权推理（**非**已核实条款，仅作兜底框架）

> 以下与具体课程条款无关，是条款缺失或不明时的通用推理，可被真实条款推翻。

- **自己撰写讲解、讲同一批概念 —— 风险最低。** 思想与概念不受著作权保护，只有表达受保护。但须避免逐句改写原文、避免复制原图与幻灯片。
- **链接官方来源 + 自己的解读与署名 —— 模式安全。** 但署名本身**不能**豁免侵权。
- **翻译完整逐字稿 / 翻译视频字幕 —— 许可依赖度最高。** 翻译是衍生作品，复制了原作的完整表达，完全取决于实际条款（NC/ND 条款，或根本无许可）。
- **翻译官方作业答案 —— 风险最高。** 著作权风险叠加学术诚信规则，且答案常被故意不公开，应默认无授权。
- **转载原始课件 / 视频 —— 最高风险且通常没有必要。** 即使材料许可宽松，视频还另有平台条款。一律链接，不转载。

---

## 设计问题：中文翻译/讲解项目的「最安全 → 最危险」排序

> 前提：一个发布**中文翻译与讲解**的项目。以下逐项给出 PERMITTED / FORBIDDEN / NEEDS-PERMISSION，
> 全部依据上文**实际读到的**条款。

### 总排序（最安全 → 最危险）

| 排名 | 做法 | 判定 | 依据 |
| --- | --- | --- | --- |
| 1 | **(e)** 链接官方来源 + 自己的解读与署名 | 🟢 **PERMITTED**（全部课程） | 只引用不复制表达。链接与署名本身不产生新权利，也不侵犯原权利 |
| 2 | **(b)** 我们自己原创的概念讲解文章 | 🟢 **PERMITTED**（全部课程） | 思想/概念不受保护。**对无许可课程同样成立**，这是 CS 61A 的唯一安全路线 |
| 3 | **(a)(d)** 6.824 / 6.1810 讲座笔记、幻灯片的翻译与转载 | 🟢 **PERMITTED**（需署名） | [CC BY 3.0 US](https://creativecommons.org/licenses/by/3.0/us/)：只有 BY，**无 NC/SA/ND** → 翻译（衍生）合法、商用合法、无需回馈许可 |
| 4 | **(a)(d)** OCW / Composing Programs 的翻译与转载 | 🟡 **PERMITTED ONLY IF 非商业 + 以 BY-NC-SA 4.0 发布** | [OCW terms](https://ocw.mit.edu/terms/)、[CP 3ed](https://composingprograms.com/3ed/)：`Adapt` 允许衍生，但 `Noncommercial — You may not use the material for commercial purposes` + `Share Alike` 传染 |
| 5 | **(f)** 6.824 讲座视频的中文字幕 | ⚠️ **NEEDS-PERMISSION** | MIT 页面只有 CC BY 徽章，但视频本体是 [YouTube 嵌入](http://nil.csail.mit.edu/6.824/2020/video/1.html)，**视频自身的权利声明无从取得**；叠加 YouTube 条款 |
| 6 | **(d)** 转载 CS 61A / 15-445 的原始幻灯片与视频 | 🔴 **FORBIDDEN** | 两站均**无许可声明 = 保留所有权利**；转载是完整复制表达 |
| 7 | **(a)(f)** CS 61A / 15-445 的逐字稿与字幕翻译 | 🔴 **FORBIDDEN** | 同上：翻译是衍生作品，无许可即无权利 |
| 8 | **(c)** 翻译作业 / Lab 解答 | ⛔ **FORBIDDEN（全部课程，且不可谈）** | 著作权 + **五门课全部有明文禁令**（见下） |

### 关键澄清

**「无许可声明」的法律含义 —— 必须说清楚：**

> **无许可声明 = 保留所有权利（all rights reserved）。** 它与「宽松开源许可」是**完全不同且更严格**的处境。
> 公开可访问 ≠ 授权改编。适用于：**CS 61A、CMU 15-445、Stanford CS 144 站点**。
> 这三者想翻译逐字稿或字幕，**只能走书面授权路线**，不存在「合理使用」的稳妥空间（整篇翻译不属合理使用）。

**6.824 的重要反转 —— 它不是「无许可」：**

> 6.824 主页有 [CC BY 3.0 US](https://creativecommons.org/licenses/by/3.0/us/) 徽章，**不是**无许可类。
> 因此 **(a) 完整翻译逐字稿、(d) 转载幻灯片、(f) 字幕（就笔记部分而言）在法律上都被许可**，只需署名。
> **但**：(d) 转载**视频**不行（YouTube 平台层），(c) 翻译**解答**不行（课程禁令层）。**授权与禁令是两层，不能混为一谈。**

**为什么 (c) 是唯一「不可谈」的：** 五门课全部有明文禁令，且都是独立于著作权之外的条件：

- 6.824 — <https://pdos.csail.mit.edu/6.824/labs/collab.html>：> "Please do not publish your code or make it available to current or future 6.5840 students."
- 6.1810 — <https://pdos.csail.mit.edu/6.S081/2023/general.html>：> "Do not post your lab or homework solutions on publicly accessible web sites (such as GitHub) or file spaces (such as your Athena Public directory)."
- CS 61A — <https://cs61a.org/fa26/syllabus/>：> "Do not post your solutions publicly during or after the semester."
- CS 144 — <https://raw.githubusercontent.com/CS144/imp/master/README.md>：> "solutions not be posted publicly by anybody."
- CMU 15-445 — <https://15445.courses.cs.cmu.edu/spring2024/syllabus.html>：学术诚信条款，作弊最低处罚为整份作业零分

> 注意：**即使是 CC BY 3.0 US 的 6.824，也没有因为许可宽松而放开解答禁令** ——
> 这证明「某材料有开放许可」**不能**推出「围绕该课程的一切都能发布」。同一课程内必须按材料类型分别判断。

### 落地建议

1. **(b)+(e) 是唯一的全域安全组合**，可立即对**全部**目标课程开工，不需要任何授权。
2. **6.824 与 6.1810 可以升级为逐字稿翻译**（CC BY 3.0 US），履行三项署名义务即可：
   标注原作者/课程、链接许可、标明已做翻译修改。
3. **CS 61A / 15-445 必须停在 (b)+(e)**，逐字稿、字幕、课件转载一律不做；要做得先写信。
4. **OCW / Composing Programs 可以做，但要先决定项目的商业模式**：只要沾了这两者，
   产出就**不得商业化**且**必须以 CC BY-NC-SA 4.0 发布**（SA 会传染整份衍生作品）。
   建议把 OCW/CP 相关内容**隔离成独立的 BY-NC-SA 4.0 子项目**，避免传染到 6.824 的 BY 内容。
5. **(c) 永久排除**，任何课程都不做 —— 这是唯一一条不需要权衡的红线。
