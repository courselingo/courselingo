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
template/           ★ 课程仓库模板：复制即成一门新课
  course.toml         课程元数据 + 授权闸门
  glossary.toml       术语表（核心资产）
  content/            讲座：front matter + Markdown + SVG 配图
  scripts/            new_lecture.py / validate.py / build.py（零依赖）
  .github/workflows/  校验 + 部署到 GitHub Pages
skills/             ★ Agent Skills：把 SOP 变成可执行的技能
  course-init/          课程立项
  course-translate/     术语表前置的讲座产出
  course-explain/       讲懂而不只是译完
  course-diagram/       概念配图
  course-validate-publish/  校验与发布
scripts/
  new_course.py       从 template/ 生成一个新的课程仓库
docs/
  SOP.md              端到端操作手册（Agent 与人都照着做）
  pipeline-spec.md    ★ 接口契约：文件格式、校验规则、构建契约
  architecture.md     流水线设计（含授权闸门）
  content-policy.md   授权、署名与内容边界（必读）
  course-catalog.md   目标课程清单与授权状态
  licensing-research-log.md  授权核实记录与证据
  publishing.md       发布方案决策
  diagram-conventions.md     配图规范
  brand.md            命名、口号与语气规范
ROADMAP.md            阶段计划
```

## 快速开始

零依赖，只需要 **Python 3.11+**（标准库 `tomllib`）。没有 `npm install`，没有 `pip install`。

```bash
# 1. 从模板生成一门新课
python scripts/new_course.py --id mit-6.5840 --out ../courses/mit-6.5840 \
    --title "Distributed Systems" --title-zh "分布式系统" \
    --institution MIT --course-number "6.5840 / 6.824" \
    --homepage "https://pdos.csail.mit.edu/6.824/"

# 2. 在课程仓库里新增一讲、校验、构建
cd ../courses/mit-6.5840
python scripts/new_lecture.py --title "Raft 领导者选举" --slug raft-leader-election \
    --source-url "https://pdos.csail.mit.edu/6.824/" --source-title "Raft (2)"
python scripts/validate.py
python scripts/build.py --out site
```

想先看看效果，可以不生成新课，直接构建模板自带的演示课程：

```bash
python template/scripts/build.py --root template --out template/site
# 打开 template/site/index.html
```


## 两条不可让步的底线

1. **授权** —— 只发布我们自己的翻译与讲解，不转载原始课件、视频与作业答案。逐课程核对许可，见 [content-policy.md](./docs/content-policy.md)。
2. **术语一致** —— 同一概念全篇同译。术语表先行，翻译跟随。

这两条不是写在文档里的口号，而是**代码层面的强制**：`validate.py` 会在授权未核实时拒绝任何逐字稿翻译，并拦下疑似整段转载的英文原文。

## 快速开始

本仓库目前以文档为主，暂无需要构建的代码。开始贡献前请阅读：

- [贡献指南](https://github.com/courselingo/.github/blob/main/CONTRIBUTING.md)
- [内容策略](./docs/content-policy.md)
- [架构设计](./docs/architecture.md)

## 授权

代码与文档的授权协议**尚待确定**（见 [ROADMAP.md](./ROADMAP.md) 的待决事项）。

注意：翻译产物可能属于原课程的衍生作品，其授权须与原始课程许可兼容 —— 这也是为什么我们坚持「不转载原文」的设计。
