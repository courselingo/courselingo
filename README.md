<div align="center">

# CourseLingo · 译课 AI

**AI-powered translation & explanation for classic CS courses.**

让经典 CS 课程，跨语言也能学懂。

</div>

---

## 关于本仓库

这是 CourseLingo 的**平台主仓库**：承载架构决策、术语规范、翻译与讲解流水线。

课程内容本身将存放在独立的课程仓库中（随首批课程启动后创建），做到**内容与工具分离** —— 工具可复用，内容可独立授权与下线。

> **当前状态：Phase 0 · 基础设施**
> 正在搭骨架、定规范。**课程翻译尚未开始。** 进度见 [ROADMAP.md](./ROADMAP.md)。
>
> 🚧 **头号阻塞项：课程授权未核实。** 本机网络无法访问课程官方页面，因此
> [课程目录](./docs/course-catalog.md)中所有授权状态均为「未核实」——
> 我们**没有**用记忆填补这些空白。在核实完成前，不产出逐字稿翻译与字幕。

## 目录结构

```
docs/
  architecture.md          翻译与讲解流水线的设计（含授权闸门）
  content-policy.md        授权、署名与内容边界（必读）
  course-catalog.md        目标课程清单与授权状态
  licensing-research-log.md 授权核实记录：当前受阻及其证据
  brand.md                 命名、口号与语气规范
ROADMAP.md                 阶段计划
```

`glossary/`（分课程术语表）与 `pipeline/`（流水线代码）将在 Phase 1 落地。

## 两条不可让步的底线

1. **授权** —— 只发布我们自己的翻译与讲解，不转载原始课件、视频与作业答案。逐课程核对许可，见 [content-policy.md](./docs/content-policy.md)。
2. **术语一致** —— 同一概念全篇同译。术语表先行，翻译跟随。

## 快速开始

本仓库目前以文档为主，暂无需要构建的代码。开始贡献前请阅读：

- [贡献指南](https://github.com/courselingo/.github/blob/main/CONTRIBUTING.md)
- [内容策略](./docs/content-policy.md)
- [架构设计](./docs/architecture.md)

## 授权

代码与文档的授权协议**尚待确定**（见 [ROADMAP.md](./ROADMAP.md) 的待决事项）。

注意：翻译产物可能属于原课程的衍生作品，其授权须与原始课程许可兼容 —— 这也是为什么我们坚持「不转载原文」的设计。
