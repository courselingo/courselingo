# 授权核实记录 · Licensing Research Log

> 本文件记录**实际做过的核实动作与结果**。结论：**已于 2026-09-28 完成主要核实。**
> 每一条都有原文引用，**没有一条来自记忆或推测**。

## 状态：RESOLVED（此前因网络受阻，现已解除）

### 此前为什么受阻，后来怎么解决的

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| `web_search` 全部失败 | 未配置搜索后端 | 不用搜索，直接抓官方页面 |
| `web_fetch` 拒绝学术域名 | 本机 DNS 是 Clash fake-IP，所有域名解析到 `198.18.0.x`（非公网段），`web_fetch` 因而拒收 | 改用 `pwsh` + `curl` |
| `curl` 直连也返回 000 | 代理端口 **7892 是 SOCKS5，不是 HTTP**；用 `http://` 连它必然失败 | 改用 `-x socks5h://127.0.0.1:7892` |

**关键教训**：这个环境下要抓外网，必须用 `curl -x socks5h://127.0.0.1:7892`。
写成 `http://127.0.0.1:7892` 会静默失败（返回 000），看起来像「网络被墙」。

## 实际抓取记录

抓取物留证在 `docs/_fetch/`（已在 `.gitignore` 中排除，不入库）。主要目标与结果：

| 目标 | URL | 结果 |
| --- | --- | --- |
| MIT OCW 条款 | `https://ocw.mit.edu/terms/` | ✅ 200，取得完整许可与 MIT 对「非商业」的解释 |
| MIT 6.824 主页 / general / schedule / questions / Lab1 | `https://pdos.csail.mit.edu/6.824/...` | ✅ 200，**5 个页面均无任何 license / copyright 字样** |
| CS 61A 首页 / syllabus / resources / fa26 | `https://cs61a.org/...` | ✅ 200，页脚为 Regents of the University of California 版权声明 |
| Composing Programs 章节页 | `https://www.composingprograms.com/...` | ✅ 200，正文写明 CC BY-NC-SA 3.0 |
| CMU 15-445 主页 / syllabus / faq / 历年 | `https://15445.courses.cs.cmu.edu/...` | ✅ 200，**6 个页面均无许可声明** |
| Stanford CS 144 主页 / Lab FAQ / 各 LICENSE | `https://cs144.github.io/...` | ⚠️ 部分 200 但**无许可声明**；若干 LICENSE 抓取返回空（14 字节） |

## 核实表

| 课程 / 来源 | 材料类型 | 许可条款 | 来源 URL | 可信度 |
| --- | --- | --- | --- | --- |
| MIT OpenCourseWare | 课程材料（含衍生作品） | **CC BY-NC-SA 4.0** | <https://ocw.mit.edu/terms/> | ✅ 已核实 |
| Composing Programs | 教材 | **CC BY-NC-SA 3.0** | <https://www.composingprograms.com/> | ✅ 已核实 |
| MIT 6.5840 / 6.824 | 课件 / 作业 / 视频 | **未声明（= 保留所有权利）** | <https://pdos.csail.mit.edu/6.824/> | ✅ 已核实「无声明」 |
| UC Berkeley CS 61A | 课件 / 作业 / 视频 | **保留所有权利**（© Regents of UC） | <https://cs61a.org/> | ✅ 已核实 |
| CMU 15-445 | 课件 | **未声明** | <https://15445.courses.cs.cmu.edu/> | ✅ 已核实「无声明」 |
| Stanford CS 144 | 课件 / Lab | **未确认** | <https://cs144.github.io/> | ⚠️ 未核实 |

### 关键原文引用

**MIT OCW 的商用限制**（这是最关键的一条）：

> “Noncommercial — You may not use the material for commercial purposes.”

> “Non-commercial use means that users may not sell, profit from, or commercialize OCW materials or **works derived from** them.”

**MIT OCW 的 ShareAlike 传染**：

> “Share Alike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.”

**CS 61A**：

> “Copyright ©2026, Regents of the University of California and respective authors.”

**Composing Programs**：

> “These notes are published under the Creative Commons attribution non-commercial share-alike license version 3.”

## 风险分级（基于**已核实条款**，不再是通用推理）

| 做法 | 判定 | 依据 |
| --- | --- | --- |
| (b) 我们自己写概念讲解，讲同一批概念 | 🟢 **可以做** | 思想与概念不受著作权保护（6.824 / CS 61A 无许可也成立） |
| (e) 链接官方来源 + 自己的解读与署名 | 🟢 **可以做** | 署名不豁免侵权，但「只引用 + 自己写」不构成复制表达 |
| (a) 翻译完整讲座逐字稿 | 🔴 **对 6.824 / CS 61A / 15-445 禁止** | 无许可 = 保留所有权利；翻译是衍生作品 |
| (f) 翻译视频字幕 | 🔴 **同上，且更复杂** | 视频另有平台条款 |
| (c) 翻译作业答案 | ⛔ **永久排除** | 著作权 + 学术诚信，双重风险 |
| (d) 转载原始课件 / 视频 | 🔴 **禁止** | 6.824 / CS 61A 无许可；一律链接，不转载 |
| 使用 OCW 材料做改编 | 🟡 **条件允许** | 须非商业 + 以 CC BY-NC-SA 4.0 发布（传染） |

## 仍未核实

- Stanford CS 144 的许可（LICENSE 文件多次抓取返回空）
- 6.824 如果走 MIT OCW 版本，OCW 上是否有对应课程（决定能否用 CC 许可替代「无许可」）
- 6.824 讲座视频的平台条款（与课件授权是两回事）
- Composing Programs 完整页脚声明（当前证据来自教材章节正文）

## 一句话总结

**两门首选课程（6.824、CS 61A）都没有开放许可，逐字稿翻译在拿到书面授权之前不能做。**
但「我们自己写的概念讲解」在任何一门课上都可以做 —— 这正是本项目把默认产出定为
`explanation` 而不是 `transcript` 的原因。授权闸门现在有了真实的牙齿，不再只是预防性设计。
