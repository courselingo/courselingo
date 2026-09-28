# ROADMAP · 路线图

> 原则：先把规矩定好，再动手翻译。宁可 Phase 0 慢一周，也不要返工一万行。

## Phase 0 · 基础设施 ← **当前阶段**

目标：让项目「可开工、可协作、不侵权」。

**组织与门面**

- [x] 建立 GitHub 组织 `courselingo`（display name 待设置）
- [x] 组织主页与社区规范（[`.github` 仓库](https://github.com/courselingo/.github)）
- [x] 平台主仓库与本路线图（[courselingo](https://github.com/courselingo/courselingo)）

**流水线（零依赖，已跑通并测试）**

- [x] 冻结**接口契约** —— [pipeline-spec.md](./docs/pipeline-spec.md)
- [x] **课程模板** `template/`：course.toml + glossary.toml + content/ + scripts/
- [x] `validate.py` —— 授权闸门、术语一致性、格式、原文转载探测（5 类检查）
- [x] `build.py` —— Markdown → 静态站（零第三方依赖，仅 Python 标准库）
- [x] `new_course.py` / `new_lecture.py` —— 脚手架
- [x] **授权闸门按材料类型逐项核实**（笔记 ≠ 视频，各类许可常不同）
- [x] 5 个 **Agent Skills** + [操作手册 SOP](./docs/SOP.md)
- [x] **发布流水线**：GitHub Pages + 三个工作流（校验 / 部署 / 链接巡检）
      —— 决策记录见 [publishing.md](./docs/publishing.md)
- [x] **配图规范** [diagram-conventions.md](./docs/diagram-conventions.md) + 合规示例图
- [ ] 把 `svg-diagram` 的房规 linter 纳入 CI（需先确定 LICENSE 与是否 vendor）

**授权（曾经阻塞，现已核实完毕 —— 结论不乐观，但明确）**

- [x] **逐课程核实授权状态** —— 见 [course-catalog.md](./docs/course-catalog.md)
      与 [licensing-research-log.md](./docs/licensing-research-log.md)。
      方法：`curl -x socks5h://127.0.0.1:7892`（**端口 7892 是 SOCKS5 不是 HTTP**，写成 http 会静默失败）。
      🔴 **结论：6.824 与 CS 61A 均未声明开放许可（= 保留所有权利）**，
      因此 `transcript` 模式在这两门课上**不可用**；只有「我们自己写的讲解」可做。
      MIT OCW 是 CC BY-NC-SA 4.0（禁商用 + ShareAlike 传染）。
- [ ] 确定代码与内容的**授权协议**
- [ ] 若要走逐字稿路线：给 6.824 / CS 61A 讲师或版权方写信申请书面授权
- [ ] 核实 MIT OCW 上是否有 6.824 对应课程（决定能否用 CC 许可替代「无许可」）

**待办**

- [ ] 建立**质量评估**基线（术语一致率、抽样人工复核）
- [ ] 选定模型与调用方式、成本估算
- [ ] 把 Agent Skills 安装到本机技能目录（见 [skills/README.md](./skills/README.md)）

**出口条件**：任一课程的一条讲座可以被完整产出并通过人工复核，且全程有授权依据。

## Phase 1 · 单课 MVP

目标：跑通一门课的一小段，验证质量而非规模。

- 选 **MIT 6.5840 / 6.824** 作为首门课程（分布式系统，概念密度高，最能验证讲解能力）
- 范围：Lecture 1–3，约 3 篇讲解
- 建立该课程术语表（首版约 60–100 条）
- 产出：分段翻译 + 概念讲解 + 代码注释 + 中英对照
- 落地渲染：可访问的静态站点或 Markdown 集

**验收**：读者能不看英文原文读懂该讲，且术语零冲突。

## Phase 2 · 质量与流程固化

- 自动化校验：术语一致性、漏译、格式
- 回译抽检与 LLM 评审流水线
- 人工复核流程（谁审、审什么、如何驳回）
- CI：提交即校验，术语表变更需两人确认
- 成本与速度基线（每篇讲座的 token 与耗时）

## Phase 3 · 规模化

- 引入 **CS 61A**，验证非系统类课程（这门课偏编程与抽象，讲解方式不同）
- 课程数量扩展至 5+
- 多语言支持（架构预留，不急于实现）
- 全文检索与「提问式学习」

## Phase 4 · 社区

- 开放校对贡献通道
- 发布课程质量榜单 / 术语表公开索引
- 与原作者沟通，争取正式授权或合作

## 待决事项（需要决策）

| # | 事项 | 说明 |
| --- | --- | --- |
| 1 | 代码授权协议 | 倾向 MIT 或 Apache-2.0 |
| 2 | 翻译产物授权协议 | 必须与各原课程许可兼容，可能需要逐课程区分 |
| 3 | 主仓库命名 | 当前 `courselingo/courselingo`；备选 `courselingo/platform` |
| 4 | 站点形态 | 静态站（Next.js / Astro）还是纯 Markdown + GitHub Pages |
| 5 | 模型与预算 | 用哪个模型做翻译、哪个做讲解；是否需要自建术语约束层 |
| 6 | 是否接受外部内容投稿 | 涉及授权连带责任 |
