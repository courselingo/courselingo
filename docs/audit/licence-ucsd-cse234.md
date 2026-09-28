# 授权核实：UCSD CSE 234 (ML Systems / LLM Systems, Winter 2025)

> 核实日期 **2026-09-28**。方法：GitHub 直连（`raw.githubusercontent.com` / `gh api`），渲染页经 `-x socks5h://127.0.0.1:7892`。
> 状态：**逐页 + 逐材料核实完成**（含讲义与 scribe notes 的 PDF 内部扫描）。
> 结论：**B 级（仅原创讲解）** —— 这是**对既有路线图结论的一次下修**，理由见 §0 与 §3。

## 0. 一句话结论（与既有结论相反，必须先看这条）

路线图把 CSE 234 记为「**MIT License（全场最宽松：无 NC、无 SA、可商用）**」，
但仓库根 `LICENSE` 的**授权人与授权对象都不是这门课的内容**：

```text
MIT License

Copyright (c) 2024 DSC 204A          ← 另一门 UCSD 课（DSC 204A）

The website is adapted from UC Berkeley Data Science 8.   ← 自述：这是「网站」模板

Permission is hereby granted, ... to deal in the Software without restriction ... (the "Software")
...
Copyright (c) 2024 Data Science 8    ← 第二个 MIT 块：上游模板（Berkeley Data 8）的许可
```

⇒ 这份 MIT 是**网站模板的软件许可**，**不是**课程内容（讲义 PDF / scribe notes）的许可。
课程内容**没有任何许可声明** ⇒ 按本项目规则「无声明 = 保留所有权利」⇒ **`unknown` ⇒ 只能原创讲解**。
**CSE 234 不能顶替 MLSys 的 A 级翻译位。**

## 1. 逐材料判定表

| 材料 | URL | 逐字证据 | 判定 | 我们能发布什么 |
| --- | --- | --- | --- | --- |
| **仓库根 LICENSE**（唯一许可文件） | <https://raw.githubusercontent.com/hao-ai-lab/cse234-w25/main/LICENSE>（2,182 B，200） | `MIT License` / `Copyright (c) 2024 DSC 204A` / `The website is adapted from UC Berkeley Data Science 8.` / 第二块 `Copyright (c) 2024 Data Science 8`；权利文本对象是 `the "Software"` | **allowed（仅限网站代码/模板）** | 可使用网站代码；**不构成**课程内容授权 |
| GitHub 的机器判定 | `gh api repos/hao-ai-lab/cse234-w25` | `"license": {"spdx_id": "NOASSERTION", "name": "Other"}` | — | ⚠️ **GitHub 自己也没把它识别为 MIT**（双块 + 夹注文本导致） |
| 站点首页（渲染） | <https://hao-ai-lab.github.io/cse234-w25/>（200，24,976 B） | 许可/版权关键词 **0 命中** | unknown | 只做原创讲解 |
| 站点 syllabus（渲染） | `…/syllabus/`（200，24,312 B） | **0 命中** | unknown | 同上 |
| 站点 schedule（渲染） | `…/schedule/`（200，9,825 B） | **0 命中** | unknown | 同上 |
| 站点页面源码 | `index.md` / `syllabus.md` / `assignments.md` / `faq.md` / `resources.md` / `schedule.md` / `README.md` / `_config.yml` / `_includes/nav_footer_custom.html` | 许可/版权措辞 **0 命中**（`MIT` 的命中全是 `submit`、`MIT Press` 之类的假阳性） | unknown | 同上 |
| **讲义 slides**（`assets/slides/*.pdf`，20 份） | 例 `…/main/assets/slides/jan7.pdf`（6,972,902 B） | 抽样 4 份做内部扫描：只有**内嵌字体**声明（`Copyright (c) 1997, 2009 American Mathematical Society … CMBX12`、`© 2017 Microsoft Corporation. All rights reserved.`、`© The Monotype Corporation plc`）；**无课程许可、无版权行** | **unknown** | 只做原创讲解；不译、不做双语对照 |
| **scribe notes**（`assets/scribe_notes/*.pdf`，19 份） | 例 `…/main/assets/scribe_notes/jan9_scribe.pdf`（2,036,053 B） | 抽样 2 份：同样只有 AMS/Computer Modern 字体声明 | **unknown** | 同上（且为**学生**作品，见 §3.3） |
| 讲义内的**第三方素材** | `assets/slides/mar13.pdf` | 逐字命中：`Animation credit: Francisco Massa` | **排除** | 不复制该素材 |
| **PA（编程作业）仓库** | <https://github.com/hao-ai-lab/cse234-w25-PA>（`README.md` 仅 15 B） | `…/cse234-w25-PA/main/LICENSE` → **真 404**（响应体 14 B `404: Not Found`） | **unknown** | 不转载题面、不翻译（叠加 §3.4 的明文禁令） |
| 阅读材料（`_modules/week-*.md` 列出的论文） | 例 week-01 | 论文本身是第三方作品 | **另有权利层** | 走 `paper-licensing.md`：只写原创导读 |

## 2. 取证计数（可复核）

| 对象 | 计数方式 | 结果 |
| --- | --- | --- |
| `cse234-w25` 仓库根许可类文件 | `gh api …/git/trees/main?recursive=1` + 逐名探测 | 只有 `LICENSE` 一个 |
| 页面声明 | 对渲染 HTML + 源 Markdown 匹配 `rel="license"|creativecommons|licen[cs]e|copyright|all rights reserved|©` | **0 命中** |
| 讲义/笔记内部声明 | `pdftext.py` 抽文本 + `ctx.py` 匹配 | 命中**全部**是内嵌字体/证书（坑九的 PDF 版） |
| 独立 LICENSE 的仓库 | `cse234-w25-PA` | **404** |

## 3. 为什么判定是 `unknown`（而不是 allowed）

### 3.1 授权人不对

MIT 文本的授权只能由**权利人**作出。文件里写的权利人是 **`DSC 204A`** 与 **`Data Science 8`** ——
既不是 CSE 234 的授课教师（Hao Zhang 等），也不是 CSE 234 的学生 scribe。
仓库里还留有跨课程复用的痕迹（`assignments.md` 中被注释掉的 `hao-ai-lab/dsc291-PA` 链接；
同组织下另有 `dsc204a-w24` / `dsc204a-f25` / `dsc291-*`）⇒
**这份 LICENSE 是「一门课的网站模板」被复制到另一门课时一起带过来的文件**。

### 3.2 授权对象不对

MIT 授予的是 `the "Software" and associated documentation files`。
`assets/slides/*.pdf`、`assets/scribe_notes/*.pdf` 是**课程内容**（讲义与笔记），
不是该网站的软件或它的文档。文件里那句 `The website is adapted from …` 也把对象指向**网站**。
「仓库根有 LICENSE ⇒ 仓库里的一切都随之授权」是一个**常见但未经条款支持的推断**。

### 3.3 最有利于「allowed」的反证也被逐字读过了（诚实记录）

`syllabus.md` 里 scribe notes 的提交方式**确实是往这个仓库发 PR**：

> "The instructors will then audit your notes, and post them to the [class home page](#) for everyone's benefit."
> "Submission: Submit a pull request to [course website repo](https://github.com/hao-ai-lab/cse234-w25) for review"

这确实说明笔记是**有意并入该仓库**的。但：
① 并入仓库 ≠ 由 `DSC 204A` 授予许可（授权人仍然不对）；
② 学生作品的权利默认在学生手里（除非另有约定，而站点**没有**任何贡献者许可条款 / CLA / DCO）。
⇒ 这一条**不足以**把判定抬到 `allowed`，但它记录在此，供将来进一步取证时作为起点。

### 3.4 作业层面有**明文禁令**（比 ETH 更硬）

`assignments.md` 逐字：

> "**Remember do not use a public repo for your solution!**"
> "But **do not share any code and do not post any of your solution code for discussion.**"
> "**Do not go searching for any code posted online by other students or prior editions.**"

⇒ 作业解答**永久排除**（本项目红线 + 课程明文禁令，双重依据）。

## 4. 我们能发布什么

| 动作 | 判定 | 依据 |
| --- | --- | --- |
| **原创中文讲解**（讲同一批概念：注意机制、Triton kernel、并行训练、MoE、投机解码…） | ✅ **可做** | 思想与概念不受著作权保护；`unknown` 下这正是唯一安全路线 |
| 翻译讲义 slides / scribe notes | ⛔ **不产出** | 内容授权 `unknown`（§3.1–3.2） |
| 双语原文对照排版 | ⛔ **不注入** | 与逐字稿同一道闸门（`content-policy.md`：`[license.materials]` 全 false） |
| 转载讲义/笔记 PDF | ⛔ 不做 | 同上 |
| 翻译 PA 题面 / 解答 | ⛔ 不做 | 红线 + §3.4 明文禁令 |
| 引用站点排期/大纲的事实信息（讲哪一讲、读哪篇论文） | ✅ 可做 | 事实信息不受保护；须标注来源链接 |
| 商用 | ⚠️ **就原创讲解而言不受限** | 原创讲解不复制对方表达；但**不能**据此声称「CSE 234 材料可商用」 |

## 5. 什么证据能把它升回 A 级（给下一步的明确清单）

1. **由 CSE 234 教师/UCSD 作出的内容许可**：站点或仓库里出现由 `Hao Zhang / CSE 234 / UC Regents`
   作出的、明确覆盖**课程内容（slides / notes）**的许可声明（CC 或自定义均可）。
2. **把仓库 LICENSE 的版权行改成 CSE 234**，并加一句明确覆盖网站内容与讲义（现状是 `DSC 204A` + 只谈 `Software`）。
3. **贡献者条款**：scribe notes 的模板/大纲里出现「以 CC BY-NC 4.0 / 任意协议贡献」的授权条款（可解决 §3.3 的学生作品问题）。
4. **书面许可**：直接联系课程教师取得可归档的书面授权（`evidence_url` 指向该凭证）。

> 上述任一成立后再把 `license.verified` / `allows_translation` 置真；
> **在那之前，CSE 234 的 `output_mode` 只能是 `explanation`。**

## 6. 仍存疑 / 未闭环

| # | 未闭环项 | 缺什么 |
| --- | --- | --- |
| 1 | 渲染版 `/assignments/` 页面的 HTML | 该页代理抓取多次返回 `000`（**不是 404**）；已用**源 Markdown**（`assignments.md`，GitHub 200）替代取证，结论不受影响 |
| 2 | `assets/slides/` 与 `assets/scribe_notes/` 是否**全部**无内部声明 | 本轮抽样 4 份 slides + 2 份笔记；其余可由同一脚本批量复跑（§7） |
| 3 | scribe notes 的 Overleaf 模板是否含授权条款 | 模板在 Overleaf（`overleaf.com/read/tfpkfgxxpgyd`），本轮未取回 |
| 4 | 同组织其他学期实例（`dsc204a-w24` / `dsc204a-f25`）的 LICENSE 是否同样错位 | 本轮只核 `cse234-w25`；同组织另有 3 个 `NOASSERTION` 仓库，若要复用需各自核 |

## 7. 复现方式

```powershell
# LICENSE（直连）
& "C:\Windows\System32\curl.exe" -s -L -o LICENSE https://raw.githubusercontent.com/hao-ai-lab/cse234-w25/main/LICENSE
# 仓库清单 + GitHub 的许可判定
gh api "repos/hao-ai-lab/cse234-w25/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/hao-ai-lab/cse234-w25 --jq .license
# PA 仓库有没有 LICENSE（真 404 的响应体是 "404: Not Found"）
& "C:\Windows\System32\curl.exe" -s -L https://raw.githubusercontent.com/hao-ai-lab/cse234-w25-PA/main/LICENSE
# 讲义内部声明扫描
python _sources\_audit\pdftext.py <deck>.pdf ; python _sources\_audit\ctx.py <deck>.pdf.text.txt
```

**落盘证据**：`_sources/ucsd-cse234/evidence/`（LICENSE、仓库树、页面源码与渲染 HTML、讲义与笔记 PDF、PA 仓库探针）
与 `_sources/ucsd-cse234/text-clean/`（讲义可读文本）。

## 8. 需要路线图同步修正的两处（不在本文件写入范围内）

| 文件 | 现表述 | 应改为 |
| --- | --- | --- |
| `docs/course-selection.md` §2 表 + §4.1 | CSE 234「**MIT License**（无 NC、无 SA、可商用）」⇒ **A 级** | 内容授权 **`unknown`** ⇒ **B 级（仅原创讲解）**；"MIT" 仅覆盖网站代码/模板，且授权人写作 `DSC 204A` |
| `docs/course-selection.md` §4.1「第一顺位备选」 | 因 MLSys 的 NC 约束可立刻顶上 | **不可顶上** —— 它的内容授权比 MLSys 更弱（MLSys 至少是明文的 CC BY-NC 4.0） |
