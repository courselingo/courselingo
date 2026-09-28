# Agent Skills · 技能包

这 6 个技能把 [SOP](../docs/SOP.md) 从「文档」变成「Agent 能直接执行的动作」。

它们不是给别人看的说明书 —— 而是给 Agent 加载的操作指令：什么时候用哪个技能、按什么顺序做、哪些事绝对不能做。

## 六个技能

| 技能 | 什么时候用 |
| --- | --- |
| `course-init` | 新建一门课：元数据、**授权核实**、术语表起步 |
| `course-paper` | 处理**单篇经典论文**：登记进 `papers.toml`、**逐篇核实授权**、决定导读还是全文翻译、写导读 |
| `course-translate` | 产出一讲的讲解（术语表前置，不是逐句翻译） |
| `course-explain` | 让讲解真正讲懂：概念前置、推导可见、代码有注释 |
| `course-diagram` | 给概念配图（手绘 SVG，中文标签，统一风格） |
| `course-validate-publish` | 跑校验、解读错误、修完再发布 |

典型串联方式（讲座轨道 + 论文轨道；论文轨道的深度与配图标准复用 `course-explain` / `course-diagram`）：

```
course-init ──┬──► course-translate ──► course-explain ──► course-diagram ──► course-validate-publish
              │              ▲_____________________________________|
              │                   校验失败就回到产出环节
              └──► course-paper ──────────────────────────────────────► course-validate-publish
                     （论文轨道：登记 → 逐篇授权核实 → 导读 / 全文翻译）
```

## 安装

技能的标准布局是 `<技能目录>/<技能名>/SKILL.md`。把本目录下的六个文件夹整体复制过去即可。

### DeepSeek Harness（本机）

用户级（所有项目可用）：

```powershell
Copy-Item -Recurse -Force "D:\Vibe_Workspace\courselingo\courselingo\skills\*" "$env:USERPROFILE\.dsh\skills\"
```

装完后目录应形如：

```
C:\Users\keriko\.dsh\skills\
  course-init\SKILL.md
  course-paper\SKILL.md
  course-translate\SKILL.md
  course-explain\SKILL.md
  course-diagram\SKILL.md
  course-validate-publish\SKILL.md
```

### Claude Code

项目级：复制到仓库根的 `.claude/skills/`；用户级：复制到 `~/.claude/skills/`。

### 验证是否装好

重启会话后，技能会出现在 Agent 的技能清单里。也可以直观检查文件是否就位：

```powershell
Get-ChildItem "$env:USERPROFILE\.dsh\skills" -Recurse -Filter SKILL.md |
  ForEach-Object { $_.Directory.Name }
```

应当列出 6 个技能名。

## 与仓库的关系

这些技能会在执行时读取仓库里的规范文件：

- [`docs/pipeline-spec.md`](../docs/pipeline-spec.md) —— 文件格式与校验规则的唯一真相（**§10 论文**：`papers.toml`、论文页、两档闸门）
- [`docs/content-policy.md`](../docs/content-policy.md) —— 授权与内容边界
- [`docs/paper-licensing.md`](../docs/paper-licensing.md) —— **逐篇论文授权的权威来源**（`course-paper` 逐步都会读它）
- [`docs/SOP.md`](../docs/SOP.md) —— 端到端流程（讲座轨道 + 论文轨道）
- [`docs/diagram-conventions.md`](../docs/diagram-conventions.md) —— 配图规范

所以技能最好配合 **一份课程仓库** 使用：在一门课的仓库目录里启动 Agent，它才能直接读写 `course.toml` / `glossary.toml` / `papers.toml` / `content/`。

## 设计原则

- **技能里写的是「怎么判断」，不是「怎么点击」。** 例如 `course-translate` 会讲清楚为什么术语表必须先冻结、`course-paper` 会讲清楚为什么「能免费下载」不等于「允许翻译」—— 不理解原因，Agent 遇到边界情况就会走样。
- **底线写死在技能里。** 授权闸门、不转载原文、术语一致、**论文逐篇授权**（`verified` 与 `allows_translation` 缺一不可），这四条在相关技能里都有明确的「禁止」段落。
- **默认答案是保守的那一个。** 论文默认写 `guide`（我们自己的导读，不设闸门），只在证据齐全时才开 `translation`；「不确定」永远导向更安全的那档。
- **技能与脚本分工。** 技能负责判断与写作，`scripts/validate.py` 与 `scripts/build.py` 负责机械校验 —— 能自动查的绝不靠 Agent 自觉。
