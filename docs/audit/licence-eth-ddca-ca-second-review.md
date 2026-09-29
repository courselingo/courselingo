# 授权核实 · 第二人独立复核（Lead 签字）· ETH Zurich DDCA → Computer Architecture

- **复核人**：CourseLingo Lead（独立于作者 `eth-author`）
- **复核日期**：2026-09-29
- **复核对象**：`courselingo/docs/audit/licence-eth-ddca-ca.md`（作者记录）
- **复核方法**：抓**原始 HTML**，对 `rel="license"`、`by-nc-sa`、`All rights reserved` 各数一次，
  并抽出**页脚许可块的逐字原文**与 CC 链接本身。
- **结论**：✅ **与作者记录一致，且「逐页出现」这一关键特征我独立确认。复核通过。**

## 1. 逐页复核（我这次实测）

| # | 页面 | 抓取大小 | `rel="license"` | `by-nc-sa` | All rights reserved | CC 链接 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | DDCA **Spring 2023** `?id=start` | 39,402 B | **2** | **3** | 0 | `…/by-nc-sa/4.0/deed.en` |
| 2 | DDCA **Spring 2023** `?id=lectures` | 17,099 B | **2** | **3** | 0 | `…/by-nc-sa/4.0/deed.en` |
| 3 | CA **Fall 2022** `?id=start` | 32,982 B | **2** | **3** | 0 | `…/by-nc-sa/4.0/deed.en` |

**⇒ 三页三项**逐项相同**。**（作者记录称「每个页面的页脚都带同一份站点级许可块」，这一点得到确认。）

## 2. 逐字证据（页脚原文，三页同款）

```html
<footer id="dokuwiki__footer"><div class="pad">
  <div class="license">Except where otherwise noted, content on this wiki is licensed under the following license:
  <bdi><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en" rel="license">…
```

**★ 与 6.824 形成关键对照**：6.824 的徽章**全站只在主页**（子页面 0 命中 ⇒ 覆盖范围无法确立）；
**ETH 的许可块**逐页出现**在页脚 ⇒ 覆盖范围是「**this wiki**」，这是**站点级**声明。**
**⇒ 这正是本项目把 ETH 判 A、把 6.824 判未确认的那条分界线，我独立复核了它成立。**

**⚠️ 例外条款 `Except where otherwise noted` 真实存在** ⇒ **第三方材料必须逐件排除**（见 §3）。

## 3. 放行范围与义务

**⇒ 可翻译：wiki 文本 + 课程自制 `onur-*` 讲义。**
**⇒ 自本文件起，ETH 仓库的产出可以出译文（transcript）。**

| 要素 | 义务 |
| --- | --- |
| **BY** 署名 | 每页给出课程名、机构、讲次与原文链接 |
| **NC** 非商用 | 不得进入商业场景 |
| **SA** 同协议 | 本仓库产出以 **CC BY-NC-SA 4.0** 发布 |

**仍受排除（逐条，依 `Except where otherwise noted`）**：
第三方客座报告 / 会议论文（`*_micro2021`、`*_micro2022`、`hermes-*`、`pluto_*`、`segram_*` 等）、
`(Paper)` 项、YouTube 视频、**作业材料**；
助教材料（`ataberk-*` / `kanellok-*`）**须逐件**确认无 `otherwise noted` 才可考虑。

## 4. 本次复核没有覆盖的东西（诚实记录）

- 我复核了**三个页面**（两门课各自的 start + DDCA 的 lectures）。**其余页面未逐页重抓**——
  但「逐页页脚」这一结构本身已被三页确认，且作者记录称全站一致。
  **⇒ 若要把某讲改为 transcript，该讲依据的讲义**文件内部**仍应单独扫一次**（作者已作 3 份抽样）。
- **讲义 PDF 的字节数与内部声明**本次未复核。
