# 配图作业规范 · Figure Spec（可机检）

> 这是**作业规范**，不是设计随想。设计理由见 [diagram-conventions.md](./diagram-conventions.md)。
>
> **先看 [figure-audit.md](./figure-audit.md) 决定「这里该不该有图」，**
> 再回来看本文件决定「怎么画」。顺序反了就会出现「图都合规，但该画的地方空着」。
> 每条规则都由房规 linter 实际校验过，**照做就能 0 error 0 warning**。

## 0. 一句话

手绘 SVG、单一浅色底、中文标签居中、只用房规调色板、线走曲线不走直角。
**不要用 Mermaid，不要用 CSS class 上色。**

## 1. 交付前必须跑的命令

**PowerShell 不会替原生命令展开通配符** —— 直接写 `...\figures\*.svg` 会让 CLI
拿到字面量 `*.svg` 并以 ENOENT 退出（退出码 2）。必须显式展开：

```powershell
# ✅ 推荐：交给封装脚本，它自己枚举文件
python scripts/check_figures.py --root . --strict

# ✅ 手动跑 linter：用 Get-ChildItem 展开
$node = "C:\Users\keriko\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe"
& $node tools\svg-lint\bin\svg-lint.mjs (Get-ChildItem content\<页面目录>\figures\*.svg).FullName

# ❌ 错：字面量通配符，退出码 2
& $node tools\svg-lint\bin\svg-lint.mjs content\<页面目录>\figures\*.svg
```

- 退出码 `1` = 有 error。**必须修到 `0 error(s), 0 warning(s)`。**
- 只想看 error：加 `--quiet`。
- node 不在 PATH 时用 `COURSELINGO_NODE` 指过去。
- 肉眼复核可以把单张 SVG 交给浏览器光栅化（Windows 上 `msedge.exe` / `chrome.exe`
  加 `--headless=new --screenshot=out.png --window-size=W,H`），再量一次真实墨迹边距。

## 2. 调色板（**只能用这些**）

写别的十六进制色值 → `palette-conformance` 直接报 warning。

| 用途 | fill | stroke | text |
| --- | --- | --- | --- |
| input | `#dbeafe` | `#3b82f6` | `#1e40af` |
| processing | `#fef3c7` | `#f59e0b` | `#b45309` |
| output | `#d1fae5` | `#22c55e` | `#166534` |
| analysis | `#f3e8ff` | `#a855f7` | `#6b21a8` |
| warning | `#fce7f3` | `#ec4899` | `#9d174d` |

文本色：`#1e293b`（主）/ `#64748b`（次）/ `#94a3b8`（弱）。
箭头：`#64748b`、`#3b82f6`、`#f59e0b`、`#22c55e`、`#a855f7`、`#ef4444`。
分组框：fill `#f8fafc`、stroke `#94a3b8`、`stroke-dasharray="6,4"`。
画布：`#ffffff`。

**CourseLingo 已额外登记的 4 个品牌色**（本项目补丁）：`#2563eb`、`#1f2937`、`#1d4ed8`、`#eff6ff`。
除这 4 个之外，仍只能用上表。

## 3. 骨架（照抄，改内容即可）

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 260" width="760" height="260"
     role="img" aria-labelledby="fig-x-title fig-x-desc">
  <title id="fig-x-title">图的中文标题</title>
  <desc id="fig-x-desc">一句话说清图里有什么、结论是什么。</desc>

  <defs>
    <style>
      text { font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', system-ui, sans-serif; }
    </style>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="2" refY="4"
            orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L8,4 L0,8 L2,4 z" fill="#64748b"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="760" height="260" fill="#ffffff"/>

  <text x="380" y="34" font-size="16" font-weight="600" fill="#1f2937" text-anchor="middle">图的中文标题</text>
  <!-- 方块与连线 -->
</svg>
```

### 硬性细节（漏一条就报错）

1. **必须有 `<style>` 且里面有一条 `text { font-family: ... }` 规则**，字体栈照抄上面。
   —— 只写 class 选择器（如 `.lbl`）不算，会报 `missing-font-stack`。
2. **marker 必须同时写 `markerUnits="userSpaceOnUse"` 和 `orient="auto"`**，`markerWidth` 只能是 **8 / 12 / 16**。
3. **第一个绘制元素是画布矩形** `fill="#ffffff"`，覆盖整个 viewBox。
4. **`<title>` / `<desc>` 是根元素前两个子元素**，`aria-labelledby` 把两者都接上。
5. **方块内的文字必须 `text-anchor="middle"`**（水平居中于方块中心）。
   —— 左对齐/右对齐的方块标签会报 `label-not-centered`。
6. **上色一律用呈现属性**（`fill=` / `stroke=` 写在元素上），**不要用 CSS class 上色**。
7. **不要写直角折线，也不要写斜的直线段** —— 转角用 `C`/`Q` 曲线；直线只在两端同轴时用。

## 4. 几何规则（数值是硬性的）

| 项 | 要求 |
| --- | --- |
| viewBox 边距 | **20–25px**，左右相差 ≤5px |
| 方块之间的间距 | **25–30px**（低于 25 箭头会退化成点） |
| 方块高度 | `font-size × 3 + (行数 − 1) × (font-size × 1.5)` |
| 行距 | `font-size × 1.5`（12px 字 → 18px；15px 字 → 22.5px） |
| 同一行内方块宽度 | 相差 **≤60px** |
| 箭头起点/箭尖留白 | 距源/目标方块各 **5px** |
| 绕行路径 | 距无关方块 ≥20px |

### 两行方块的算例（最常用）

方块 `y=68, h=68`，第一行 15px、第二行 12px：

```
基线1 = y + 28 = 96      （15px 字）
基线2 = y + 50 = 118     （12px 字）
```

## 5. 页面里怎么引用

```markdown
![一句话说清「图里有什么 + 结论是什么」的中文 alt](figures/xxx.svg)
```

- 图放在**本页目录**的 `figures/` 下，与 `index.md` 同级。
- 文件名：`<slug>-<n>.svg`，`n` 从 1 开始。
- **alt 不是「示意图」** —— 要能替代图片传达信息，≤60 字。
- 图前面写一句引出、图后面写一句解读，不要让图孤零零挂着。

## 6. 常见报错对照

| 报错 | 改法 |
| --- | --- |
| `missing-font-stack` | `<style>` 里加 `text { font-family: ... }` |
| `marker-units-missing` / `marker-orient-missing` | marker 补 `markerUnits="userSpaceOnUse"` / `orient="auto"` |
| `label-not-centered` | 方块内文字加 `text-anchor="middle"` |
| `box-too-short` | 方块高度按 §4 公式算 |
| `row-box-size-mismatch` | 同行方块宽度差压到 ≤60px |
| `margin-too-large` / `horizontal-margin-asymmetric` | 收紧 viewBox，左右留白对齐 |
| `diagonal-straight-line` | 斜线改成 `C`/`Q` 曲线 |
| `off-palette-color` | 换成 §2 里的色值 |
| `spacing-too-small` | 方块间距加到 ≥25px |
| `arrow-start-clearance` / `arrow-tip-clearance` | 线端离方块 5px |


## 7. ★ 版面必须与内容匹配（不要什么都画成网格）

**实测教训**：第一轮批量补图后，**145 张里有 62 张（43%）用了完全相同的版面** ——
同样是六个 220×50 的方块摆成 3×2 网格，只有文字不同。几何全过、房规全过、密度也达标，
但读者连着看到同一个形状几十次，**视觉通道就失效了**：
图变成了「把文字装进框里」，而不是在讲关系。

问题不在于「网格不好」，而在于**网格被用来装一切**。
下面这些内容塞进网格就是错的：

| 内容在讲 | 网格为什么错 | 该用的版面 |
| --- | --- | --- |
| **脑裂：断成两半** | 网格看不出「两半」 | 左右两组 + 中间断开的链路 |
| **阶段一的两条分支** | 网格没有分叉 | 一进二出的分叉（`C`/`Q` 曲线） |
| **日志匹配 / 前缀检查** | 网格看不出「对齐」 | 两条平行日志条，逐格对齐 |
| **任期作为逻辑时钟** | 网格没有时间 | 横向时间轴 + 刻度 |
| **三个时间尺度** | 同上 | 三条并列的时间轴（长度可比） |
| **只监视前一个（链）** | 网格没有顺序 | 横向链式箭头 |
| **版本号 / 编号递增** | 网格没有递增感 | 时间轴或递增刻度 |
| **延迟下界** | 网格看不出长度 | 水平条形 + 刻度 |
| **角色转换** | 网格没有环 | 环形箭头（双向） |
| **层次 / 包含关系** | 网格没有层级 | 树或嵌套框 |
| **吞吐 vs 延迟（取舍）** | 网格没有对立 | 左右双列 + 中间的取舍箭头 |

### 版面词汇表（先选版面，再填内容）

| 版面 | 用在 | 视觉特征 |
| --- | --- | --- |
| **链** | 流程、时序、管道 | 一排方块 + 同轴箭头 |
| **分叉** | 条件分支 | 一进多出，`Q` 曲线 |
| **环** | 状态机、角色转换 | 方块围成圈 + 弧线箭头 |
| **时间轴** | 任期、编号、延迟 | 一条横线 + 刻度 + 上方事件 |
| **双列对照** | 取舍、对比、正反例 | 两列 + 中间分隔或对比标记 |
| **分组（泳道）** | 归属、分区、断成两半 | 虚线框包住若干方块 |
| **树 / 嵌套** | 层次、包含、分工 | 上下层或框套框 |
| **平行对齐** | 日志、副本、逐步比对 | 两条以上等宽横条逐格对齐 |
| **网格** | **真正的清单 / 参数表**（只在此时用） | 等大方块阵列 |

### 怎么自查

```bash
# 语料级：同一版面指纹是否被过多图复用（>15% 警告，>25% 报错）
python scripts/audit_content.py --root .
```

`audit_content.py` 会输出类似：
```
[版面复用] 62/145 张图（43%）的版面完全一致……只有文字不同。
```

**看到这个警告，不要去改指纹，要去改版面** —— 逐张问：
「这张图讲的是关系还是清单？」关系就用上面对应的版面，只有真清单才用网格。
