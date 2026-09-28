# 配图作业规范 · Figure Spec（可机检）

> 这是**作业规范**，不是设计随想。设计理由见 [diagram-conventions.md](./diagram-conventions.md)。
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
