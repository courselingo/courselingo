# 课程目录 · Course Catalog

> 授权状态已在 2026-09-28 经**实际抓取**核实。每条都附原文引用与来源 URL。
> 方法：本机 DNS 为 Clash fake-IP，`web_fetch` 会拒绝非公网地址，因此统一用
> `curl -x socks5h://127.0.0.1:7892` 抓取。抓取到的原始页面留证在 `docs/_fetch/`（不入库）。

## ⚠️ 先说结论：两门首选课程都没有开放许可

| 课程 | 授权状态 | 对我们的含义 |
| --- | --- | --- |
| **MIT 6.5840 / 6.824** | 🔴 **未声明任何许可** | 未声明 = 保留所有权利。**逐字稿翻译不可做**，需先取得书面授权 |
| **UC Berkeley CS 61A** | 🔴 **保留所有权利** | 同上 |
| MIT OpenCourseWare | 🟡 **CC BY-NC-SA 4.0** | 可改编，但**禁止商用**且 **ShareAlike 传染** |
| Composing Programs（教材） | 🟡 **CC BY-NC-SA 3.0** | 可改编，同样禁止商用 + 相同方式共享 |
| CMU 15-445 | 🔴 未声明许可 | 同 6.824 |
| Stanford CS 144 | ⚠️ 未确认 | 抓到的页面无许可声明，但部分 LICENSE 文件抓取失败 |

**这件事直接印证了项目的「讲解优先」架构不是保守，而是必需。**

---

## 目标课程

### MIT 6.5840 / 6.824 · 分布式系统

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://pdos.csail.mit.edu/6.824/> |
| 许可 | **未声明**（红线） |
| 核实范围 | 主页、`/general.html`、`/schedule.html`、`/questions.html`、Lab 1 页面 |
| 结果 | 以上页面**均未出现** "license" / "copyright" 字样（逐页扫查，命中 0） |

**判读**：没有声明许可**不等于**可以自由使用 —— 法律上它是「保留所有权利」。
这与「宽松开源许可」是完全相反的两件事。因此：

- ⛔ 翻译讲座逐字稿 / 字幕：**不可做**
- ⛔ 转载课件 PDF：**不可做**
- ⛔ 翻译 Lab 题面与答案：**不可做**（且叠加学术诚信问题）
- ✅ 我们自己撰写概念讲解、术语表、原创配图：**可以做**（思想与概念不受著作权保护）

### UC Berkeley CS 61A · 计算机程序的构造与解释

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://cs61a.org/> |
| 许可 | **保留所有权利** |
| 原文引用 | “Copyright ©2026, Regents of the University of California and respective authors.” |
| 出现位置 | `cs61a.org/` 首页、`/syllabus`、`/resources` 页脚 |

**判读**：版权归加州大学校董会。没有授予改编或再发布的权利。结论同 6.824。

### MIT OpenCourseWare

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://ocw.mit.edu/> · 条款 <https://ocw.mit.edu/terms/> |
| 许可 | **CC BY-NC-SA 4.0** |
| 原文引用 | “Creative Commons License Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)” |
| 商用 | “Noncommercial — You may not use the material for commercial purposes.” |
| MIT 的解释 | “Non-commercial use means that users may not sell, profit from, or commercialize OCW materials or **works derived from** them.” |
| 相同方式共享 | “Share Alike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.” |

**判读**：这是唯一明确允许改编的目标来源，但代价是两条**传染性**约束：

1. **禁止商用** —— 一旦用了 OCW 材料（含其衍生作品），整个产出不得商业化。
2. **ShareAlike 传染** —— 我们的翻译/讲解必须以 CC BY-NC-SA 4.0 发布。

注意 **OCW 与校内课程站是两套授权**：`ocw.mit.edu` 上的课程版本带 CC 许可，
而 `pdos.csail.mit.edu/6.824/` 的课程站没有。要翻译 6.824，走 OCW 版本才可能有据。

### Composing Programs（CS 61A 教材）

| 项 | 内容 |
| --- | --- |
| 入口 | <https://www.composingprograms.com/> |
| 许可 | **CC BY-NC-SA 3.0** |
| 原文引用 | “These notes are published under the Creative Commons attribution non-commercial share-alike license version 3.” |

**判读**：教材本身允许改编，但同样禁止商用 + 相同方式共享。
**注意它与 CS 61A 课程站是两套授权** —— 教材开放 ≠ 课程幻灯片/作业开放。

### CMU 15-445 · 数据库系统

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://15445.courses.cs.cmu.edu/> |
| 许可 | **未声明**（6 个页面全部命中 0） |

### Stanford CS 144 · 计算机网络

| 项 | 内容 |
| --- | --- |
| 官方入口 | <https://cs144.github.io/> |
| 许可 | ⚠️ **未确认** |

抓取的主页、Lab FAQ 与若干 `LICENSE` / `README` 文件**均未找到许可声明**；
但部分 LICENSE 文件抓取返回了空内容（14 字节），**因此不能断定「无许可」**。
结论标记为待核实。

---

## 对 Phase 1 的直接影响

原计划是「先做 6.824」。按核实结果，必须调整：

| 做法 | 6.824 | CS 61A |
| --- | --- | --- |
| 原创概念讲解（我们自己写） | ✅ 可做 | ✅ 可做 |
| 术语表、学习路径 | ✅ 可做 | ✅ 可做 |
| 原创配图 | ✅ 可做 | ✅ 可做 |
| 逐字稿翻译 | ⛔ 需书面授权 | ⛔ 需书面授权 |
| 视频字幕翻译 | ⛔ 需书面授权 | ⛔ 需书面授权 |
| 作业答案翻译 | ⛔ 永久排除 | ⛔ 永久排除 |

**两条可行路线：**

1. **讲解路线（默认，可立即开工）** —— 只发布我们自己撰写的概念讲解，不复制原文表达。
   引用原文观点可以，但不得整段改写、不得复制图表。
2. **授权路线（要主动争取）** —— 给课程讲师或相应版权办公室写信申请翻译授权。
   MIT OCW 有专门的帮助渠道；这条路一旦走通，逐字稿翻译才谈得上。

## 待抓取清单（尚未核实的部分）

- [ ] CS 144 的 `LICENSE` 文件（多次抓取返回空，需换 URL 或换方式重试）
- [ ] `composingprograms.com` 页脚的完整许可声明（当前证据来自教材章节页正文）
- [ ] 6.824 讲座**视频**的平台条款（即使课件授权谈成，视频另有条款）
- [ ] MIT OCW 上是否存在 6.824/6.5840 的对应版本（决定了能否走 OCW 授权路线）

## 记录格式（后续新课程沿用）

| 课程 | 材料类型 | 许可条款 | 来源 URL | 访问日期 | 允许商用 | 允许衍生 | 有 SA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MIT OCW | 课程材料 | CC BY-NC-SA 4.0 | <https://ocw.mit.edu/terms/> | 2026-09-28 | ❌ | ✅ | ✅ |
| Composing Programs | 教材 | CC BY-NC-SA 3.0 | <https://www.composingprograms.com/> | 2026-09-28 | ❌ | ✅ | ✅ |
| MIT 6.5840/6.824 | 课件/作业/视频 | 未声明 | <https://pdos.csail.mit.edu/6.824/> | 2026-09-28 | ❌ | ❌ | — |
| CS 61A | 课件/作业/视频 | 保留所有权利 | <https://cs61a.org/> | 2026-09-28 | ❌ | ❌ | — |
| CMU 15-445 | 课件 | 未声明 | <https://15445.courses.cs.cmu.edu/> | 2026-09-28 | ❌ | ❌ | — |

## 已知的两个陷阱（务必记住）

1. **「没有声明许可」≠「可以自由使用」。** 6.824、15-445 属于这一类。法律状态是保留所有权利。
2. **同一个项目里，不同材料类型的授权经常不同。** CS 61A 课程站是保留所有权利，但它的教材
   Composing Programs 是 CC BY-NC-SA 3.0。这也是 `course.toml` 里要按
   `[license.materials]` 分材料类型逐项核实的原因。
