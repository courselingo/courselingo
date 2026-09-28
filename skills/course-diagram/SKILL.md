---
name: course-diagram
description: Produce a hand-placed, CJK-labelled SVG concept diagram for one CourseLingo lecture — pick the diagram type that fits the CS concept (Raft leader election, RPC, replication, memory layout, 61A environment diagrams), follow the house style and brand tokens, add accessible title/desc plus Chinese alt text, and save it to content/<NN>-<slug>/figures/. Use when a section's difficulty is sequence, state, structure, or comparison rather than wording, or when reworking an existing figure.
---

# course-diagram · 概念配图

把「关系 / 时序 / 状态 / 结构 / 对比」画成一张**中文标注、手工排布、风格统一**的 SVG。

具体到不能再具体的规则（颜色值、字号、公式、示例 SVG）在 [`docs/diagram-conventions.md`](../../docs/diagram-conventions.md) —— 那是唯一真相，本文件只讲**怎么判断、按什么顺序做、哪些不能做**。两者冲突时以 `diagram-conventions.md` 为准。

## 前置阅读

| 文件 | 取什么 |
| --- | --- |
| `docs/diagram-conventions.md` | 画布 / 网格 / 颜色 token / 字体栈 / 箭头 / 暗色 / 示例 |
| `docs/pipeline-spec.md` §1 | `content/<NN>-<slug>/figures/*.svg` 的位置约定 |
| `docs/SOP.md` §14-9 | 产出契约：命名 `<slug>-<n>.svg`、alt 文本必写、不内联 |
| `glossary.toml` | 图里出现的术语必须与它一致 |
| 本讲 `index.md` | 哪一节要图、那一节要表达什么关系 |
| `docs/brand.md` | 语气与用词（图里也一样：不做营销腔） |

---

## 一、先判断：这张图该不该画

**判据**：这一节的难点是「**关系 / 时序 / 结构 / 对比**」，还是「文字本身」？

| 该画 | 不该画 |
| --- | --- |
| 消息顺序与时序（RPC 往返、心跳、AppendEntries、超时重传） | 术语的并列定义 |
| 角色 / 状态迁移（跟随者 → 候选人 → 领导者） | 单行公式或一步就能推完的变形 |
| 多方并发与交错（两个候选人同时拉票、日志分歧后回滚） | 一段直白代码（代码块更好，注释用 `course-explain` 的写法） |
| 系统结构 / 分层（客户端 → 协调者 → 副本组；RPC 栈） | 清单、枚举、参数表（用表格/markdown 列表） |
| 数据流与复制路径（写入路径、日志应用顺序） | 结论性总结 |
| 内存 / 地址空间布局、栈帧 | 只为「显得有图」而配的装饰 |
| 环境图（CS 61A：frame、闭包、递归求值） | 一张图想同时讲三件事 |
| 两种方案对比（主从复制 vs 分片） | —— |

其它纪律：

- **一讲 2–4 张**，一张图只讲**一个**结论。
- 自问一遍：读者看这张图，比读一段文字**多**得到什么？答不出来就别画。
- 如果一张图需要三行以上图注才能解释，说明它塞了两件事 —— 拆成两张，或者改写正文。

## 二、选图型（CS 概念对照表）

| 要表达 | 图型 | 关键手法 |
| --- | --- | --- |
| 消息时序 | 时序图 | 竖向生命线（`#94a3b8`，`dasharray="4 4"`）+ 顶部参与者盒；消息箭头带标签；自调用从生命线离开再折回（第二个控制点与终点同 y，箭头才指得正） |
| 角色 / 状态迁移 | 状态图 | 盒 = 状态，曲线箭头 = 迁移，标签写**触发条件**（`选举超时`、`收到更高任期`）；失败转移用虚线 |
| 系统结构 / 分层 | 结构图 | 分行的盒 + 虚线分组框表示进程/机器边界；箭头标协议与端口（`:8080 gRPC`） |
| 数据流 / 复制路径 | 数据流图 | 左→右主线，步骤标 ①②③；同一条结论只画一遍 |
| 时间 / 任期 | 时间轴 | 水平轴 = 时间；分段标 `任期 1 / 2 / 3`；超时区间用色块或斜线 |
| 多数派 / 集合关系 | 集合图 | 节点摆成簇，圈出多数派，标 `2 / 3` |
| 两种方案对比 | 双栏并置 | 左右同尺寸同结构，**只把差异**用强调色标出来 |
| 内存 / 地址空间 | 地址空间图 | 纵向地址带；每段一个盒，左端写地址区间；堆与栈用不同填充 |
| 环境图（CS 61A） | 环境图 | frame 盒 + 变量/值两列 + 指针曲线 + `parent` 虚线（细则见下） |
| 依赖 / 目录 / 日志 DAG | 层级图 | 同层同 y；同层盒宽差 ≤60px；连线用 `C`/`Q` 曲线，不用直角折线 |

**环境图细则（61A 专用）**

- 一个环境 = 一个 frame：外框 `rx="8"`，顶部标题带写函数名（`global` / `f` / `λ`）与参数。
- frame 内两列：左列变量名（`text-anchor="start"`，`x = frameX + 12`），右列值框（起点 `x = frameX + 96`），两列不要互相压。
- 值框：数字/字符串直接写；列表每个元素一段，尾部留一个空槽表示「后面没有了」。
- 指针：从变量名右侧出发的曲线 + 箭头，指向值框左边缘；**不要用直线穿过别的值框**。
- `parent` 指针：虚线 `6 4`，从 frame 底部出发指向父 frame。
- 求值顺序：①②③ 圆圈序号放在被求值表达式的上方。
- 递归：同一函数的多个 frame 按调用顺序纵向排列，最近的在上。

## 三、动手流程（八步，照做）

1. 读 `docs/diagram-conventions.md`，确认这次要用的画布宽、颜色 token、字号。
2. **先用一句中文写下这张图的结论**。这句话同时是 `<desc>` 和 alt 文本的底稿（两者可以不同，但不能互相矛盾）。
3. 列元素清单：节点（中文名 + 英文名）、边（含标签）、标注（≤2 条）。**删掉不改变结论的元素** —— 删减是收益最高的操作。
4. **先算坐标，再写 XML**：
   - 画布宽取 `480 / 640 / 760 / 960` 之一（时序与结构图 760，一般图 640，环境图 640）；
   - 盒高 = 字号 × 3（两行 = 字号 × 3 + 行距）；
   - 行距 = 字号 × 1.5；
   - 相邻盒间距 = 28（允许 25–30）；
   - 箭头：离开源盒 5px，止于目标盒前 11px；
   - `viewBox` = 内容包围盒 + 四周 22px。
   把这张坐标表写在草稿里，别一边写 XML 一边猜数字。
5. 写 SVG：`fill` / `stroke` / `font-size` 直接写成**呈现属性**（presentation attributes）；`<style>` 里**只放一条** `text { font-family: … }` 规则。
6. 自检：过一遍 §六 清单，再跑 §七 的两条命令。
7. 存盘：`content/<NN>-<slug>/figures/<slug>-<n>.svg`（`n` 从 1 开始递增，本讲内唯一）。
8. 在正文对应小节引用：`![中文说明](figures/<slug>-<n>.svg)`，**alt 必须写**，而且写「结论」，不写「示意图」。

## 四、房屋风格硬规则（速查）

| 项 | 值 |
| --- | --- |
| 画布宽 | 480 / 640 / 760 / 960（`width`/`height` 与 `viewBox` 数值相同） |
| 边距 | 四周 20–25px（用 22）；左右差 ≤5px |
| 网格 | 盒的 `x/y/width/height/rx` 取 4 的倍数；文字基线由公式算出，不强行对齐网格 |
| 盒高 | 单行 = 字号 × 3；两行 = 字号 × 3 + 1.5 × 字号 |
| 行距 | 字号 × 1.5（15px → 22） |
| 盒间距 | 28（25–30）；<25 箭头会退化成点，>30 显松 |
| 箭头 | 起 5 / 止 11；可见线段 ≥6px |
| 描边 | 盒 1.5、连接线 1.5、焦点盒 2、生命线 1、圆角 `rx="8"` |
| 字号 | 图内标题 16、盒名 15（600）、副标签/线标签 12、极小标注 10–11 |
| 中文字号下限 | **12px**（汉字比拉丁字更容易糊，不要再小） |
| 字体栈 | `'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', system-ui, sans-serif`，必须原样、必须含 `Noto Sans CJK SC` |
| 字号 12px 时的文字宽 | 汉字 12px/字，其它字符 ≈7px/字 |

**颜色 token**（完整表与用途见 `docs/diagram-conventions.md` §3）：

| token | 值 | 用途 |
| --- | --- | --- |
| 主色 | `#2563eb` | 默认盒描边、主路径箭头 |
| 主色填充 / 文字 | `#dbeafe` / `#1e40af` | 需要着色时的一对 |
| 强调色 | `#f59e0b` | **唯一焦点**（1 个，最多 2 个） |
| 强调填充 / 文字 | `#fef3c7` / `#b45309` | 焦点盒 |
| 正文 | `#1f2937` | 盒名、图内标题 |
| 次要 | `#64748b` | 副标签、连接线、箭头 |
| 弱化 | `#94a3b8` | 生命线、虚线、禁用态 |
| 成功 | `#22c55e` / `#d1fae5` / `#166534` | 已确认、多数派 |
| 危险 | `#ef4444` | 真正的错误路径（危险操作、数据损坏） |
| 宕机 / 未参与 | `#9ca3af` + 虚线 | 灰色而不是红色：它没有出错，只是没参与 |
| 画布 / 分组底 | `#ffffff` / `#f8fafc` | 背景矩形、虚线分组框 |

颜色纪律：**一张图只用一种强调色相**，焦点 1–2 个；不要渐变、阴影、3D；不要用颜色作为唯一区分手段。

字体栈一定要这么写（`<style>` 里唯一允许的规则）：

```xml
<style>
  text { font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', system-ui, sans-serif; }
</style>
```

## 五、中文标签怎么写

1. **术语与 `glossary.toml` 完全一致**：术语表里 `replication = 副本`，图里就写「副本」，不要写「复制」「拷贝」。图上的术语漂移和正文里的算同一类错误。
2. 首次出现可以写「中文 (English)」（`领导者 (Leader)`），同一张图内不重复。
3. **代码标识符、协议名、端口、类型名保持英文**：`RequestVote`、`AppendEntries`、`:8080`、`int` —— 翻译它们只会让读者和原文对不上。
4. 一行 ≤ 12 个汉字或 ≤ 24 个半角字符；超了就换行、缩短，或者把细节放回正文。
5. **不要在图里写完整句子**。标注用「名词短语 + 箭头」（`选举超时`、`2 / 3 已确认`），连接线标签用 2–6 个字（`心跳`、`追加日志`）。
6. 数字与单位用半角；中英文之间留一个空格（与正文一致）。
7. 不用感叹号、不用「全网最全 / 封神」这类词（`docs/brand.md`）。

## 六、交付前自检清单（每条都要能指到具体坐标或元素）

- [ ] 一张图只讲一个结论，删掉了不改变结论的元素
- [ ] 所有元素都在 `viewBox` 内（底部 = 最低元素 + 22px，别让最后一个标注被裁掉）
- [ ] 文字不压盒、不压线（离直线 ≥10px、离曲线 ≥15px）
- [ ] 箭头两端 5 / 11，可见线段 ≥6px
- [ ] 每个 `<marker>` 都声明了 `markerUnits="userSpaceOnUse"` 与 `orient="auto"`
- [ ] 盒高 ≥ 字号 × 3；多行文本按**整块**居中（不是首行居中）
- [ ] 左右边距差 ≤5px；上下边距在 20–25px
- [ ] `<style>` 里有 `text { font-family: … }`，且含 `Noto Sans CJK SC`
- [ ] 强调色只出现在 1–2 个焦点元素上
- [ ] 根元素有 `role="img"` + `aria-labelledby`，`<title>` / `<desc>` 是前两个子元素，id 带 slug 前缀
- [ ] 图里有盒外文字（连接线标签、游离说明）时，**必须有一行 16px、居中于内容中心的图内标题**（校验工具会把「字号最大的游离文字」当标题，否则报 `title-not-centered`）
- [ ] 图里术语与 `glossary.toml` 一致
- [ ] 正文用相对路径引用，alt 是一句中文结论
- [ ] **图是自己画的**：不得复制或改写原课程的幻灯片、图表、示意图（授权风险最高的一类行为）

## 七、校验（两条命令）

```powershell
# 1) 必须能解析（零依赖，Python 标准库）
python -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(r'content/01-xxx/figures/xxx-1.svg')"

# 2) 可选：严格房屋风格检查（bybit svg-diagram 的 svg-lint，本机已装）
node "$env:USERPROFILE\.agents\skills\svg-diagram\tools\svg-lint\bin\svg-lint.mjs" content/01-xxx/figures/xxx-1.svg
```

- XML 解析失败 = 图在页面上直接不显示，属于**必须修**。
- `svg-lint` 的 12 项检查覆盖转义、viewBox 裁剪、字体栈、盒高、基线、块间距、箭头 marker、文字溢出、重叠、浅底可读、调色板、连接线几何。判据是 `0 errors, 0 warnings`。
- **目前唯一可接受的告警**是 `palette-conformance`，且只针对两个品牌 token：`#2563eb`、`#1f2937`（它们不在上游的调色板里）。修法不是改颜色，而是把 linter 连同 `LICENSE`（MIT, © 2026 bybit-exchange）vendor 进仓库、在 `lib/palette.mjs` 里登记这两个值 —— 实测这样改完，规范里的示例图是 `0 errors, 0 warnings`。
- 出现其它类别的告警一律修掉，别用「风格偏好」解释。
- CI 目前**不校验 SVG**（`pipeline-spec.md` §6 未定义 SVG 检查项）—— 所以这一步靠你自己跑，别指望自动拦住。

## 八、不要做

- ❌ Mermaid / PlantUML / Graphviz / ASCII art / 自动布局引擎（项目明确不要 Mermaid 味儿的 slop）
- ❌ 把 SVG 内联进 Markdown（`build.py` 按图片处理，内联会破坏构建契约）
- ❌ 外链字体、CDN、JavaScript、`<foreignObject>`、动画、`<image href>`
- ❌ 复制或重绘原课程的幻灯片与图表
- ❌ 渐变、阴影、3D、超过两处的强调色、装饰性图标
- ❌ 一张图超过 12 个盒（超了就拆）
- ❌ 改了正文却忘了改图（图与正文结论不一致比没有图更糟）
- ❌ 用 CSS class 承载 `fill` / `font-size`（linter 只建模呈现属性，class 会让几何与配色检查集体失准）
