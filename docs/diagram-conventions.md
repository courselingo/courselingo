# 配图规范 · Diagram Conventions

> **状态：v1（冻结）**。本文是配图的**视觉与技术要求**，与 [`pipeline-spec.md`](./pipeline-spec.md) §1/§7、[`SOP.md`](./SOP.md) §14-9 一致。
> 消费方：`skills/course-diagram/SKILL.md`、人工复核、将来的 SVG 校验脚本。**改动需同步这三处**。
>
> 分工：本文管「长什么样、怎么算」，`SKILL.md` 管「什么时候画、按什么顺序做」。

---

## 1. 位置、命名与引用

| 项 | 规则 |
| --- | --- |
| 位置 | `content/<NN>-<slug>/figures/`（`build.py` 整目录复制到 `site/<slug>/figures/`） |
| 文件名 | `<slug>-<n>.svg`，`n` 从 1 递增，本讲内唯一（例：`raft-leader-election-1.svg`） |
| 格式 | 纯 SVG 文件（不内联、不 base64、不用 Mermaid / PlantUML / ASCII art） |
| 正文引用 | `![一句中文结论](figures/<slug>-<n>.svg)`，**alt 必须写**；用相对路径 |
| 自绘 | 图必须是原创：不得复制或改写原课程的幻灯片、图表、示意图（授权风险最高的一类行为，见 `content-policy.md`） |

`build.py` 的处理方式是 `![alt](src)` → `<img src="…" alt="…" loading="lazy">`，并复制 `figures/` 目录。这个事实决定了后面三条硬约束：

1. **SVG 必须自包含** —— 页面 CSS 不会进入 SVG，外部字体/图片/脚本在离线或严格环境下会挂。
2. **不能内联** —— 内联会绕过构建契约，且 id 会互相覆盖。
3. **无障碍的真正载体是 alt** —— `<img>` 引用时，SVG 内部的 `aria-labelledby` 不参与页面无障碍树。

---

## 2. 画布与网格

| 用途 | `viewBox` 宽 | 说明 |
| --- | --- | --- |
| 紧凑图（2–3 个盒、单列） | 480 | 少量元素时不要把画布拉到 760 |
| **标准图（默认）** | 640 | 大多数结构图、状态图、环境图 |
| 宽图 | 760 | 时序图、分层图、并排对比 |
| 跨栏大图 | 960 | 仅少数（元素确实多）；再宽在小屏上会把 12px 中文压到读不清 |

- `width` / `height` 与 `viewBox` 的数值**相同**（`viewBox="0 0 640 256" width="640" height="256"`）。给出固有尺寸，浏览器才不会在 `img{max-width:100%}` 下把它放大到模糊。
- 高度按内容算：`viewBox height = 最低元素底边 + 22`，不要为了「留白好看」拉高。
- **边距**：四周 20–25px（统一用 22）；左右边距之差 ≤5px，上下也是如此。内容整体偏心时，用一次 `<g transform="translate(dx, 0)">` 修正，并同步图内标题的 `x`。
- **网格**：盒的 `x / y / width / height / rx` 取 **4 的倍数**（这是让图「不像机器随便生成的」的关键）；文字基线由 §7 的公式算出，不强行对齐网格。

---

## 3. 颜色 token

品牌色来自 [`brand.md`](./brand.md)：主色 `#2563EB`、强调色 `#F59E0B`、正文色 `#1F2937`。下表把它们与配图需要的语义角色绑死；**只从这张表取色**。

| token | 值 | 用途 |
| --- | --- | --- |
| 画布 | `#ffffff` | 图底矩形、普通盒填充 |
| 分组底 | `#f8fafc` | 虚线分组框填充 |
| 主色 | `#2563eb` | 默认盒描边、主路径箭头 |
| 主色填充 / 文字 | `#dbeafe` / `#1e40af` | 需要着色的主色盒 |
| 强调色 | `#f59e0b` | **唯一焦点**（1 个，最多 2 个） |
| 强调填充 / 文字 | `#fef3c7` / `#b45309` | 焦点盒（例：正在竞选的候选人） |
| 正文 | `#1f2937` | 图内标题、盒名 |
| 次要 | `#64748b` | 副标签、连接线、箭头、分组框标题 |
| 弱化 | `#94a3b8` | 生命线、虚线、禁用态、分组框描边 |
| 成功 | `#22c55e` / `#d1fae5` / `#166534` | 已确认、多数派、写入成功 |
| 危险 | `#ef4444` | 真正的错误：危险操作、数据损坏、协议违规 |
| 宕机 / 未参与 | `#9ca3af`（配虚线） | 灰色而不是红色 —— 它没有出错，只是没参与 |
| 失效填充 | `#f3f4f6` | 宕机盒的填充 |

**纪律**

- 一张图**只用一种强调色相**；焦点 1–2 个。第三个焦点出现时，说明这张图想讲两件事。
- 不用渐变、阴影、3D、发光。
- **颜色不能是唯一区分手段**：宕机态同时用灰 + 虚线；成功态同时用实线 + 文字「已确认」。
- 文字对比度：正文色/主色文字在 `#ffffff` 与 `#dbeafe`/`#fef3c7` 上都远高于 WCAG AA（4.5:1），不需要额外检查；**不要把 `#f59e0b` 当作文字色**（它在白底上是 2.2:1，只能做描边/色块）。

---

## 4. 描边、圆角与线型

| 用途 | `stroke-width` | 其它 |
| --- | --- | --- |
| 盒描边 | 1.5 | `rx="8"` |
| 连接线 / 箭头 | 1.5 | `fill="none"`（**必须写**，否则描边路径围出的区域会被涂黑） |
| 焦点盒描边 | 2 | 与强调色搭配 |
| 生命线 / 分隔线 | 1 | `dasharray="4 4"`，`#94a3b8` |
| 分组框 | 1.5 | `dasharray="6 4"`，`rx="10"`，`fill="#f8fafc"` |
| 失效盒 | 1.5 | `dasharray="5 4"`，描边 `#9ca3af` |

同一张图里，同类元素的 `stroke-width`、`rx`、`dasharray` 必须完全一致 —— 不一致会立刻显得脏。

---

## 5. 箭头

用**带缺口**的箭头（比实心三角读起来更清楚）。每个颜色定义一个 marker，整块复制，不要现编：

```xml
<defs>
  <!-- 默认（次要色）。markerUnits="userSpaceOnUse" 必须写 -->
  <marker id="arrow" markerWidth="8" markerHeight="8" refX="2" refY="4"
          orient="auto" markerUnits="userSpaceOnUse">
    <path d="M0,0 L8,4 L0,8 L2,4 z" fill="#64748b"/>
  </marker>
  <!-- 主路径（主色） -->
  <marker id="arrow-primary" markerWidth="8" markerHeight="8" refX="2" refY="4"
          orient="auto" markerUnits="userSpaceOnUse">
    <path d="M0,0 L8,4 L0,8 L2,4 z" fill="#2563eb"/>
  </marker>
  <!-- 焦点（强调色） -->
  <marker id="arrow-accent" markerWidth="8" markerHeight="8" refX="2" refY="4"
          orient="auto" markerUnits="userSpaceOnUse">
    <path d="M0,0 L8,4 L0,8 L2,4 z" fill="#f59e0b"/>
  </marker>
  <!-- 危险路径 -->
  <marker id="arrow-danger" markerWidth="8" markerHeight="8" refX="2" refY="4"
          orient="auto" markerUnits="userSpaceOnUse">
    <path d="M0,0 L8,4 L0,8 L2,4 z" fill="#ef4444"/>
  </marker>
</defs>
```

| 规则 | 值 |
| --- | --- |
| 离开源盒 | 源盒边缘 + 5px |
| 止于目标盒 | 目标盒边缘 − 11px（5px 净空 + 尖端再伸 6px） |
| 可见线段 | ≥6px；盒间距 28 时两盒之间正好 12px |
| `refX="2"` | 让线端落在箭头缺口中心，接缝看起来连续 |
| 粗线（`stroke-width` > 1.5） | 换成 12×12 的 marker（`refX="3"`），终点改为边缘 − 14px |

方向控制（曲线箭头指歪的唯一原因就是没有约束第二个控制点）：箭头方向 = 路径**最后一段**的方向。想让箭头朝下，就让第二个控制点与终点 `x` 相同、`y` 更小；朝右就让 `y` 相同、`x` 更小。四个方向依次类推。

线型：**共线**用直线 `L`；**任何转弯或绕行**用 `C`/`Q` 曲线，**不用直角折线**。

---

## 6. 字体与字号

```xml
<style>
  text { font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', system-ui, sans-serif; }
</style>
```

- 顺序是 macOS（PingFang SC）→ Windows（Microsoft YaHei）→ Linux（Noto Sans CJK SC）→ 系统默认。
- **`Noto Sans CJK SC` 不能删**：删了之后 Linux 上的服务端渲染会因为没有 CJK 覆盖而输出豆腐块（□□□）。
- 只允许这一条 `<style>` 规则；`fill` / `stroke` / `font-size` 一律写成元素上的**呈现属性**（见 §14 的实测原因）。
- 代码标识符（`RequestVote`、`:8080`）沿用同一条字体栈即可 —— 这些字体都带拉丁字形，不需要第二套字体。
- 不用外链字体（Google Fonts 等）：本项目要求离线可跑、零依赖。

| 元素 | 字号 | 字重 | 颜色 |
| --- | --- | --- | --- |
| 图内标题 | 16 | 600 | `#1f2937` |
| 盒名（中文 + 英文） | 15 | 600 | `#1f2937`（焦点盒用 `#b45309`） |
| 副标签 / 说明 / 连接线标签 | 12 | 400 | `#64748b` |
| 极小标注（纯英文或数字） | 10–11 | 400 | `#94a3b8` |

- **中文字号下限 12px**。汉字笔画密度高于拉丁字母，10px 的汉字在 1 倍屏上已经糊成一片 —— 放不下就缩短文字或换行，**不要缩字号**。
- 10–11px 只给纯英文/数字（如 `:8080`）。

**中文宽度估算**（放置文字前先算，不要画完再看）：

| 字号 | 汉字宽 | 其它字符宽 |
| --- | --- | --- |
| 12 | 12px | ≈7px |
| 15 | 15px | ≈9px |
| 16 | 16px | ≈9.6px |

```
标签宽 ≈ 汉字数 × 字号 + 其它字符数 × 0.6 × 字号
盒宽   ≥ 最长标签宽 + 32        （左右各 16px 内边距）
一行   ≤ 12 个汉字 或 ≤ 24 个半角字符
```

---

## 7. 文字定位

- **单行**：`baseline y = 盒 y + 盒高/2 + 字号 × 0.35`
- **多行**：按**整块**居中，而不是首行居中：

```
块中心 = 盒 y + 盒高/2 + 字号 × 0.35
首行   = 块中心 − (行数 − 1) × 行距 / 2       行距 = 字号 × 1.5
```

以「15px 盒名 + 12px 副标签」、盒 `y=68`、高 `68` 为例：块中心 = `68 + 34 + 5.25 ≈ 107`，行距 22 → 两行基线为 `96` 与 `118`。

- 水平居中一律 `text-anchor="middle"`；左对齐标注用 `text-anchor="start"`。
- **连接线标签**：放在线的侧面（`x = 线 x + 10`，左对齐），或放在两盒水平中点上方/下方（≥10px 净空）。**不要放在盒与盒之间那条 28px 的缝里** —— 中文标签放不下，会被两侧盒压住。
- **曲线标签**：距曲线最近点 ≥15px。向下弯的曲线，标签放**上面**；向上弯的放**下面**。
- **虚线分组框标题**：框左上角 `(x + 10, y + 14)`，12px，`#64748b`。分组框的垂直位置要按「标题 + 内容」的总高算，否则内容会被压到标题带里。

---

## 8. 盒、间距与绘制顺序

- 盒高公式见 §7；单行 = 字号 × 3（12px → 36，15px → 45），两行 = 字号 × 3 + 行距（15 + 12 的两行 → 68）。
- 同行的盒宽差 ≤60px；同列的盒共享中心线。
- 相邻盒间距 **28px**（25–30）。<25px 时箭头会退化成点（5 + 11 + 可见线段 ≥6 挤不出空间）；>30px 整张图会显得松垮。不相关的盒之间可以更宽，但同一张图里不要两种间距标准。
- 收尾时看一眼密度：内容包围盒 + 22px 就是画布，如果画布里有大片空白，先缩间距、再缩画布。

**绘制顺序**（SVG 没有 z-index，后画的盖住先画的）：

1. 画布底矩形
2. 虚线分组框 / 泳道等底层容器
3. 普通连接线与箭头
4. 盒与其上的文字
5. **跨层回环线**（跨越多个盒的迭代回路）—— 必须画在盒之后，否则会被盒盖住

---

## 9. 图型速查

CS 概念 → 图型 → 关键手法的完整对照表在 [`skills/course-diagram/SKILL.md`](../skills/course-diagram/SKILL.md) §2（含环境图细则）。这里只记图型层面的统一要求：

| 图型 | 默认画布宽 | 统一要求 |
| --- | --- | --- |
| 时序图 | 760 | 生命线 `dasharray="4 4"`；参与者盒同高；消息按时间自上而下；自调用曲线离开生命线再折回 |
| 状态图 | 640 | 盒 = 状态；迁移标签写触发条件；失败/回退用虚线 |
| 结构图 | 760 | 分组框表示进程/机器边界；箭头标协议与端口 |
| 数据流图 | 760 | 左→右主线；步骤标 ①②③ |
| 时间轴 | 760 | 水平轴 = 时间；分段标任期；区间用色块 |
| 集合/多数派 | 480 | 节点成簇；圈出多数派；标注 `2 / 3` |
| 对比图 | 760 | 左右同尺寸同结构，只把差异用强调色标出 |
| 地址空间图 | 480 | 纵向地址带；每段一个盒；左端写地址区间 |
| 环境图（61A） | 640 | frame 盒 + 变量/值两列 + 指针曲线 + `parent` 虚线；见 SKILL.md §2 |
| 层级 / DAG | 640 | 同层同 y；连线用 `C`/`Q` 曲线 |

---

## 10. 怎么保证跨讲一致

一致性不是靠「记得」，而是靠复用同一份东西：

1. **只从 §3 的 token 表取色**，任何图都不许临时调色。
2. **`<defs>` 整块复制**（§5 的 marker 定义），不要每张图现编箭头形状。
3. **同类型图用同一画布宽**（时序/结构/数据流 760，状态/环境/层级 640，集合/地址空间 480）。
4. **字号只用 §6 那一套**（16 / 15 / 12 / 10–11），同类盒的 `rx`、`stroke-width`、行距不随图变化。
5. **命名与编号**：`<slug>-<n>.svg`，`n` 从 1 开始，本讲内唯一。
6. **新增图型先登记**：在 §9 与 `SKILL.md` §2 里加一行，再画第二张。否则会出现「第 2 讲时序图是这样、第 5 讲又是另一样」。
7. CI 目前**不校验 SVG**（`pipeline-spec.md` §6 没有这一项）→ 一致性靠本文件 + `SKILL.md` 的自检清单，别指望自动拦截。

---

## 11. 无障碍

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 256" width="640" height="256"
     role="img" aria-labelledby="raft-roles-title raft-roles-desc">
  <title id="raft-roles-title">Raft 集群中的三种角色</title>
  <desc id="raft-roles-desc">领导者向跟随者与候选人发送心跳与日志复制；候选人因选举超时发起新一轮选举。</desc>
  <!-- 节选：图形本体见 §13 -->
```

- `<title>` / `<desc>` 是根元素的**前两个子元素**，`aria-labelledby` 把两者都接上，根元素加 `role="img"`。
- **id 带 slug 前缀**（`<slug>-title` / `<slug>-desc`）。虽然 `build.py` 用 `<img>` 引用（不内联），但一旦有人把图内联进页面，`figTitle` 这种通用 id 会互相覆盖。
- 本项目以 `<img>` 引用，**真正的无障碍载体是 Markdown 的 alt**：写一句中文，说清「图里有什么 + 结论是什么」，≤60 字。例：
  - ✅ `领导者向跟随者与候选人发送心跳；候选人因选举超时发起新一轮选举。`
  - ❌ `示意图` / `如图所示` / `图 1`
- 两者都写：`<desc>` 服务于直接打开、Figma/Slides 导入、以及将来可能的内联；alt 服务于页面。

---

## 12. 暗色模式

- **每张图的第一个绘制元素是一块画布矩形**：`<rect x="0" y="0" width="640" height="256" fill="#ffffff"/>`。于是无论页面是明色还是暗色，图都读作一张浅色卡片，文字始终可读。
- **不做双主题**。理由：图以 `<img>` 引用，父页配色不会进入 SVG；跟着整站切主题需要 SVG 内部的媒体查询，会把校验工具的模型弄失准（它按呈现属性读取颜色）。站点页面的明暗色是 `build.py` 的事，配图保持浅色。
- 这也是校验工具 `light-bg-fallback` 检查的机器检查点：它要求「每个标签下面都有东西盖住画布」，纯粹为了在深色页面上不出现「深底深字」。
- 如果将来确实要做双主题：用内联 `<style>` + `@media (prefers-color-scheme: dark)` 定义 CSS 变量，并**先改本节与 §14**，接受调色板/字体检查在这类图上失准。不要偷偷加。

---

## 13. 示例：Raft 三节点（完整、可直接用）

坐标账（先算后画）：画布 640 宽 → 内容 `22 … 618`（左右各 22px）→ 领导者通栏盒 `x=22, w=596`；下级两个盒 `w=284`，间距 28（`22…306` / `334…618`）；垂直：标题基线 34 → 领导者 `y=68, h=68`（底 136）→ 间距 28 → 下级 `y=164, h=68`（底 232）→ 下边距 22 得 254，取整到 4 的倍数 256（下边距实际 24，仍在 20–25 内）→ `viewBox` 高 256。盒内两行按「整块居中」：块中心 = `68 + 34 + 5.25 ≈ 107` → 基线 96 / 118。

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 256" width="640" height="256"
     role="img" aria-labelledby="raft-roles-title raft-roles-desc">
  <title id="raft-roles-title">Raft 集群中的三种角色</title>
  <desc id="raft-roles-desc">领导者向跟随者与候选人发送心跳与日志复制；候选人因选举超时发起新一轮选举。</desc>

  <defs>
    <style>
      text { font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', system-ui, sans-serif; }
    </style>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="2" refY="4"
            orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L8,4 L0,8 L2,4 z" fill="#64748b"/>
    </marker>
  </defs>

  <!-- 画布：固定浅色，深色页面上同样可读 -->
  <rect x="0" y="0" width="640" height="256" fill="#ffffff"/>

  <text x="320" y="34" font-size="16" font-weight="600" fill="#1f2937" text-anchor="middle">Raft 集群中的三种角色</text>

  <!-- 领导者：x=22, y=68, w=596, h=68（15px 一行 + 12px 一行，行距 22） -->
  <rect x="22" y="68" width="596" height="68" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
  <text x="320" y="96" font-size="15" font-weight="600" fill="#1f2937" text-anchor="middle">领导者 (Leader)</text>
  <text x="320" y="118" font-size="12" fill="#64748b" text-anchor="middle">任期 3 · 负责心跳与日志复制</text>

  <!-- 跟随者 -->
  <rect x="22" y="164" width="284" height="68" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
  <text x="164" y="192" font-size="15" font-weight="600" fill="#1f2937" text-anchor="middle">跟随者 (Follower)</text>
  <text x="164" y="214" font-size="12" fill="#64748b" text-anchor="middle">等待心跳 · 被动接收日志</text>

  <!-- 候选人：全场唯一焦点，用强调色 -->
  <rect x="334" y="164" width="284" height="68" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="476" y="192" font-size="15" font-weight="600" fill="#b45309" text-anchor="middle">候选人 (Candidate)</text>
  <text x="476" y="214" font-size="12" fill="#b45309" text-anchor="middle">选举超时 · 正在拉票</text>

  <!-- 心跳：离开源盒 5px，止于目标盒前 11px（箭头尖端再伸 6px） -->
  <path d="M164,141 L 164,153" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)"/>
  <path d="M476,141 L 476,153" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="174" y="147" font-size="12" fill="#64748b">心跳 + 日志复制</text>
  <text x="486" y="147" font-size="12" fill="#64748b">心跳 (任期 3)</text>
</svg>
```

正文里的引用（alt 写结论）：

```markdown
Raft 用「任期 + 投票」把三个角色串起来：

![领导者向跟随者与候选人发送心跳；候选人因选举超时发起新一轮选举。](figures/raft-leader-election-1.svg)
```

> **图内标题**：因为图里有不在盒内的文字（连接线标签），校验工具会把「字号最大的游离文字」当成标题，并要求它居中于**内容中心**。所以：只要图里有连接线标签或游离说明，就必须有一行 16px 且居中于内容中心的图内标题 —— 否则会收到 `title-not-centered` 告警。上例的标题 `x=320` 正好是内容中心 `(22+618)/2`。

---

## 14. 机器校验

```powershell
# 1) 必须能解析（零依赖，Python 标准库）
python -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(r'content/01-xxx/figures/xxx-1.svg')"

# 2) 可选：严格房屋风格检查（bybit svg-diagram 的 svg-lint，本机已装）
node "$env:USERPROFILE\.agents\skills\svg-diagram\tools\svg-lint\bin\svg-lint.mjs" content/01-xxx/figures/xxx-1.svg
```

**实测结果（两处，用来校准预期）**

| 文件 | 结果 |
| --- | --- |
| 既有 `template/content/01-what-is-a-distributed-system/figures/write-path.svg` | `5 error(s), 47 warning(s)` —— 用 CSS class 承载 `fill`/`font-size`（工具只建模呈现属性）、marker 缺 `markerUnits`/`orient`、`<style>` 里是 `.lbl` 而不是 `text` 规则、viewBox 边距 30/61/30/32、块间距 50/170 与 16 |
| 本文 §13 的示例 | `0 errors, 5 warnings`，5 条**全部**是 `palette-conformance`，只涉及 `#2563eb`（盒描边 ×2）与 `#1f2937`（正文文字 ×3） |

`svg-lint` 的 12 项检查：XML 转义、viewBox 裁剪、字体栈、盒高、基线偏移、块间距、箭头 marker、文字溢出、元素重叠、浅底可读、调色板、连接线几何。判据是 **`0 errors, 0 warnings`；warning 也算失败**。

因此：

- **唯一可接受的告警**是「品牌 token 未登记」的 `palette-conformance`，且必须在复核时说明条数。其它类别一律修掉。
- 修法不是改颜色，而是把 linter **连同 `LICENSE`（MIT, © 2026 bybit-exchange）** vendor 进仓库（建议 `tools/svg-lint/`），在 `lib/palette.mjs` 里登记 `#2563eb` 与 `#1f2937`。**已实测**：登记后 §13 的示例变为 `0 errors, 0 warnings`。
- 本机 linter 副本位于 `%USERPROFILE%\.agents\skills\svg-diagram\`（另有 `.claude` / `.iflow` / `.lingma` / `.openclaw` / `.qoder-cn` / `.trae-cn` / `.zcode` / `hermes` 各一份）。**已实测**它与上游 `main` 逐行一致（仅换行符 LF→CRLF 之差），所以现在直接引用本机副本即可；vendor 时应固定到具体 commit。

---

## 15. 与外部技能的关系、致谢与授权

本规范的技术骨架来自两个 MIT 许可的 Agent Skill，**取规则、不取产物**：

| 来源 | 取什么 | 为什么不做流水线 |
| --- | --- | --- |
| [`bybit-exchange/svg-diagram`](https://github.com/bybit-exchange/svg-diagram)（MIT, © 2026 bybit-exchange） | 房屋风格的全部算术：20–25px 边距、盒高 `字号×3`、基线 `字号×0.35`、块间距 25–30、箭头 5/11 与缺口 marker、CJK 字体栈必须含 `Noto Sans CJK SC`、汉字宽度表；以及 `svg-lint` 的 12 项检查 | 它本身就是「手绘 SVG + linter」，与本项目契约同构，因此**采纳为标准** |
| [`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design)（MIT, © 2025 Cathryn Lavery） | 编辑式取向：4px 网格、1–2 个焦点、无阴影、`role="img"` + `title`/`desc` 的无障碍契约、图型选择词汇表、汉字 12px 下限 | 默认产物是**自包含 HTML**（内嵌 SVG + Google Fonts 外链），SVG 是导出步骤；其字体链里简中标签没有 `Noto Sans SC` 这一档（靠系统本地字体兜底）；外链字体与本项目「零依赖 + 离线可跑」冲突 |

- 两者都是 **MIT**：vendor 任何代码或文本（含 `svg-lint`）都必须保留版权声明与许可证全文。注意本仓库根目录**目前没有 LICENSE**（授权待定，见 `README.md`「授权」）—— vendor 之前先把本仓库的许可证定下来，别把外部 MIT 代码放进一个没有许可证的仓库。
- 两个仓库里的示例 SVG 虽然也是 MIT（可再分发，需保留声明），但画的是**它们自己的项目**：直接搬进我们的讲座既不合事实也不合规范。**图必须自绘**。
- `cathrynlavery/diagram-design` 的简中字体说明原文（`references/style-guide.md`）：*"Simplified Chinese takes the same three rules with the Simplified stack (`'Noto Sans SC'`, `'PingFang SC'`, `'Microsoft YaHei'`). That face does not ship in the link, so Simplified labels still resolve through whatever the viewer has locally."*

---

## 16. 变更记录

| 版本 | 变更 |
| --- | --- |
| v1 | 首次冻结：画布/网格、token 表、描边、箭头、字体栈、文字定位、间距与绘制顺序、图型速查、跨讲一致性、无障碍、暗色模式、示例、校验方式与外部技能授权说明 |


---

## 斜线段不是终点：**C/Q 曲线就是它的修法**（2026-09-29 补）

**发生过一次误判。**作者报：
> 「房规禁止斜线段 ⇒ **经典时序图在本规范下画不出来**」
> （于是它改了标题、把连接线画成阶梯，并把原因写进正文给读者。）

**⇒ 而修法一直写在本项目自己的 linter 里。**`tools/svg-lint/lib/checks/connector-geometry.mjs`：
```js
// :307  A straight segment is only allowed along an axis;
//       a diagonal one has to become a C / Q curve.
// :314  code: 'diagonal-straight-line'
// :316  repair: { attribute: 'd', actual: `L ...`,
//                expected: 'an axis-aligned L, or a C/Q curve' }
```
**⇒ 也就是说：那条规矩**不是**「不能连接不同行不同列的两个东西」，
而是「**连接它们的那条线不能是直线**」—— 用曲线就行。**

### 怎么画一条「斜的连接」：用 cp2 控制箭头方向

**曲线的终点切线决定了 `orient="auto"` 画出来的箭头朝哪。**
**⇒ 而终点切线由**第二个控制点 cp2 → 终点**这一段的向量决定。**
**⇒ 所以把 cp2 的那个坐标分量对齐到终点，箭头就正：**

| 想要的方向 | cp2 的约束 | 写法 |
| --- | --- | --- |
| ↓ 下 | `cp2.x = end.x`，`cp2.y < end.y` | `C ...,... ex,ey-20 ex,ey` |
| → 右 | `cp2.y = end.y`，`cp2.x < end.x` | `C ...,... ex-20,ey ex,ey` |
| ← 左 | `cp2.y = end.y`，`cp2.x > end.x` | `C ...,... ex+20,ey ex,ey` |
| ↑ 上 | `cp2.x = end.x`，`cp2.y > end.y` | `C ...,... ex,ey+20 ex,ey` |

**★★ 而本项目 linter 检查的正是这件事**（`connector-geometry.mjs:436` 与 `:454`）：
```js
if (!diagonal && Math.abs(cp2.y - end.y) > TANGENT_TOLERANCE) { ... }
if (!diagonal && Math.abs(cp2.x - end.x) > TANGENT_TOLERANCE) { ... }
```
**⇒ 所以「箭头是歪的」与「线段是斜的」在本项目里是同一条判据的两个方向：
前者要 `cp2` 对齐终点，后者要直线只走轴。**

### ⇒ 因此

> **时序图是可以画的**：message 那条线用「起于竖直、终于水平」的 C 曲线，
> **它既是曲线（不违反斜线段）又让箭头朝对方向（cp2 对齐终点）。**
> **★ 而若某张图在旧写法下被判「画不出来」，先读一遍 linter 给出的 `repair` ——
>   修法通常就在那条报错里。**

**★★ 一条更一般的：**
> **报错信息里的 `repair` 字段是**规范作者留给写的人的唯一入口**。
> ⇒ 而它只有在**派单把那条报错连同 repair 一起转述**时才会到达写的人手里。
> ⇒ **我此前的配图派单只转述了「不许斜线段」，没转述 `or a C/Q curve`** —— 那是我的漏。**
