# 授权核实 · 第二人独立复核（Lead 签字）· CMU 15-442 / 15-642

- **复核人**：CourseLingo Lead（独立于作者 `mlsys-author`）
- **复核日期**：2026-09-29
- **复核对象**：`courselingo/docs/audit/licence-mlsys-15442.md`（作者记录）
- **复核方法**：`curl.exe` 直连 `raw.githubusercontent.com` 取**仓库根 `LICENSE` 原文**，逐字数关键条款。
  作者记录称「课程站页面 0 命中，唯一有效声明是仓库根 `LICENSE`」⇒ 我直接复核那个唯一依据。
- **结论**：✅ **与作者记录一致，复核通过。可翻译（transcript）。**

## 1. 逐字复核

| 复核项 | 作者记录 | 我实测 | 一致 |
| --- | --- | --- | --- |
| `LICENSE` 字节数 | 19,342 B | **19,342 B** | ✅ |
| 许可名称 | CC BY-NC 4.0 | **`Attribution-NonCommercial 4.0 International`** | ✅ |
| `ShareAlike` 命中 | 0 | **0** | ✅ |
| `NoDerivatives` 命中 | 0 | **0** | ✅ |

**取回 URL**：`https://raw.githubusercontent.com/mlsyscourse/mlsyscourse.github.io/main/LICENSE`

## 2. 条款含义与义务

| 要素 | 含义 | 对我们的约束 |
| --- | --- | --- |
| **BY** | 必须署名 | 每页给出课程名、讲师、讲次与原文链接 |
| **NC** | 非商用 | 产出不得进入商业场景 |
| **无 SA** | **不必**同协议发布 | 与 CS168（BY-SA）/ 6.006（BY-NC-SA）不同 —— 本仓产出**不传染** |
| **无 ND** | 翻译（衍生）被允许 | ⇒ **可出译文** |

**⇒ 本仓库的产出协议可以自定**（不必与上游同协议），这是四门里除 6.5840 外最宽松的一门。

## 3. 仍受排除（不因本次复核而放开）

- **`slides/` 里混放的三份第三方客座/业界演讲**（ByteDance Seed / Tim Dettmers / Zihao Ye, UW & NVIDIA）
  —— `LICENSE` 里有 `Except where otherwise noted` 一类例外语，**第三方材料逐件排除**；
- **作业仓库**：3 个 `LICENSE` 探针是 **14 B 的 `404: Not Found`** ⇒ **没有许可** ⇒ 题面/解答一律不用；
  （`assignment-tirx-gemm` 是 Apache-2.0，但**仍属作业材料，按学术诚信一并排除**）
- **不在 `_data/lectures.yml` 排期里的 PDF** ⇒ 视为第三方遗留文件，不译。

## 4. 本次复核没有覆盖的东西（诚实记录）

- 本文件只复核了**仓库根 `LICENSE`**（作者指定的唯一依据）。
  **页面级**（`index.md` / `schedule.md` / `materials.md`）的「0 命中」我**没有重抓**——
  作者记录它们本就无声明，而 `LICENSE` 是更保守也更明确的那一侧 ⇒ 不影响结论。
- 逐份自制讲义 PDF 的**内部**声明未逐件打开（作者已抽样；本次不复核）。
