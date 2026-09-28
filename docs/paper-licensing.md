# 论文授权 · Paper Licensing

> 核实日期 **2026-09-28**。方法：`curl -x socks5h://127.0.0.1:7892` 抓**原始 HTML**，逐条留证于 `docs/_fetch/`。
> 每条都有原文引用；**无法确认的一律标 `⚠️ 未确认`，不推测**。

## 0. 最重要的一句话

**课程采用 CC BY，不等于它推荐的论文也是 CC BY。**

MIT 6.824 课程站是 **CC BY 3.0 US**（已核实，见 [course-catalog.md](./course-catalog.md)），
但那个许可覆盖的是**课程自己的材料** —— 讲义、作业、课程网页。
它**管不到**课程阅读列表里的第三方论文。

MapReduce（USENIX）、GFS（ACM）、Raft（USENIX）、Paxos（ACM）各自是**独立的作品、独立的版权**。
「6.824 是 CC BY」这句话**不能**用来论证「所以 MapReduce 也能翻」。

这是本项目最容易犯、后果最严重的一个推理错误。

---

## 1. 逐篇判定

| 论文 | 出版社 | 免费可读 | **全文翻译** | 商用 | 依据 |
| --- | --- | --- | --- | --- | --- |
| MapReduce (OSDI 2004) | USENIX | ✅ | ⚠️ **未确认** | ⚠️ 未确认 | 论文页 200，但未找到复用/翻译授权 |
| The Google File System (SOSP 2003) | ACM | 🔒 付费 | ⛔ **需 ACM 授权** | ⛔ | ACM 标准声明（见 §2） |
| Raft (USENIX ATC 2014) | USENIX | ✅ Open Access | ⚠️ **未确认** | ⚠️ 未确认 | 页面标 "Open Access"，但无许可条款 |
| Paxos Made Simple (2001) | ACM | 🔒 | ⛔ **需 ACM 授权** | ⛔ | 页面含 ACM 完整声明（见 §2），原文引用 |
| Paxos Made Live (PODC 2007) | ACM | 🔒 | ⛔ **需 ACM 授权** | ⛔ | 同 ACM 政策 |
| Spanner (OSDI 2012) | USENIX | ✅ | ⚠️ **未确认** | ⚠️ 未确认 | 同 USENIX 类 |
| ZooKeeper (ATC 2010) | USENIX | ✅ | ⚠️ **未确认** | ⚠️ 未确认 | 同 USENIX 类 |
| Dynamo (SOSP 2007) | ACM | 🔒 | ⛔ **需 ACM 授权** | ⛔ | 同 ACM 政策 |
| Chord (SIGCOMM 2001) | ACM | 🔒 | ⛔ **需 ACM 授权** | ⛔ | 同 ACM 政策 |
| Chain Replication (OSDI 2004) | USENIX | ✅ | ⚠️ **未确认** | ⚠️ 未确认 | 同 USENIX 类 |

**一行结论**：目前**没有一篇论文**拿到了「允许翻译」的明确条款。
ACM 的一律需要走授权流程；USENIX 的能免费读，但**免费读 ≠ 允许翻译**。

---

## 2. 出版社政策

### ACM —— 已取得原文，结论明确

ACM 论文第一页的标准声明（取自 *Paxos Made Simple* 的官方发布页，逐字引用）：

> “Copyright © 2001 by the Association for Computing Machinery, Inc. **Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage** and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. **To copy otherwise, to republish, to post on servers, or to redistribute to lists, requires prior specific permission and/or a fee.** Request permissions from Publications Dept, ACM Inc., fax +1 (212) 869-0481, or **permissions@acm.org**. The definitive version of this paper can be found at ACM's Digital Library”

来源：<https://www.microsoft.com/en-us/research/publication/paxos-made-simple/>（访问 2026-09-28）

**解读**：

- ✅ 个人 / 课堂教学用途的复制**免费且被允许** —— 但**不得**用于营利或商业优势。
- ⛔ **再发布（republish）与再分发（redistribute）需要事先获得专门许可**，可能收费。
- **翻译是「复制 + 改编」，落在 ⛔ 那一类。** 所以要翻译 ACM 论文，必须走授权流程。

**授权路径**：`permissions@acm.org`，或 ACM 的 RightsLink / 授权申请入口。

**取证限制**：`dl.acm.org` 与 `acm.org` 对非浏览器客户端返回 **403**，
本次**无法**直接读取 ACM 的政策页面。上面的结论来自 ACM **印在论文上的许可声明** ——
这是 ACM 自己的条款原文，可信。但若要引用 ACM 政策页原文，需在浏览器里看。

### USENIX —— 能免费读，但复用条款**未找到**

已确认：

- USENIX 会议论文页面可公开访问，部分标注 **"Open Access"**（如 Raft 页）。
- 论文页面上**未出现**任何 Creative Commons 链接或 `rel="license"` 属性（已按原始 HTML 搜过）。
- `usenix.org/policies` 抓取成功（200），但那是**会议政策目录页**，全文 1598 字符里
  `copyright` 与 `open access` 各出现 **0 次** —— 没有复用/翻译条款。
- `usenix.org/copyright`、`/publications/editorial-policies`、`/publications/open-access`、
  `/faq/copyright` 均 **404**。

**结论：⚠️ 未确认。** USENIX 允许免费阅读是明确的，但**是否允许翻译并再发布，没有找到依据**。
要得到确定答案，需要：找到 USENIX 的版权/许可政策页，或直接联系 USENIX。

> 不要因为「USENIX 是开放获取」就推论「可以翻译」。开放获取讲的是**阅读**，不是**改编**。

### IEEE

本次未涉及（6.824 阅读列表里没有 IEEE 论文）。若将来遇到，同样需单独核实。

---

## 3. 推荐默认策略

按风险从低到高：

| 做法 | 判定 | 说明 |
| --- | --- | --- |
| **(a) 我们自己写的导读** | 🟢 **默认做法，所有课程都可以做** | 讲清论文要解决什么问题、怎么解、代价是什么。**不复制原文表达**，不整段改写，不复制图表 |
| **(d) 引用短句做评论** | 🟢 可以做 | 引用要**短**、要标注出处、要服务于评论。不要用引用来拼凑出一篇译文 |
| **(b) 全文翻译** | 🔴 **逐篇授权后才可做** | 翻译 = 复制全部表达的衍生作品。当前**没有任何一篇**获得此授权 |
| **(c) 转载原始 PDF** | 🔴 一律不做 | 没有必要 —— 链接官方来源即可 |

### 落地规则

1. **默认写导读。** 这是法律上最安全、产品上也最有价值的形态 ——
   读者要的不是「英文论文的中文版」，而是「有人把这篇论文讲明白」。
2. **要翻译就先拿授权，再登记。** 拿到书面授权后，把
   `papers.toml` 里该篇的 `license.verified = true`、`allows_translation = true`、
   `evidence_url` 指向授权凭证、`checked_at` 填日期。**然后**才能写 `output_mode = "translation"`。
3. **只核实了还不够。** `verified = true` 只表示「我们查过了」；
   `allows_translation = true` 才表示「查出来的结果是允许翻译」。
   两个字段分开正是为了让「查过了，结论是不行」也能被如实记录。
4. **绝不用课程授权替代论文授权。** 见 §0。

---

## 4. 「怎么核实一篇论文的许可」检查清单

给后续贡献者与 Agent 用。**这个项目在这上面栽过跟头，所以每一条都有来由。**

- [ ] **抓原始 HTML，不要先过滤标签再搜文本。**
      许可经常只存在于 `rel="license"` 属性、`href` 或图片徽章的 `alt` 里。
      本项目曾因过滤标签后搜索，把 MIT 6.824 误判为「无许可」，**结论完全相反**。
- [ ] **确认「免费可读」和「允许翻译」是两件事。**
      作者把 PDF 挂在自己主页上，**不构成任何授权**。
- [ ] **查出版社政策，而不只是论文页。** ACM 有明确的授权申请流程（`permissions@acm.org`）。
- [ ] **区分会议版与扩展版 / 技术报告版。** 同一篇论文的不同版本可能适用不同条款
      （例如 Raft 的会议版与扩展技术报告）。
- [ ] **记录 `evidence_url` + `checked_at`。** 没有出处的「已核实」等于没核实。
- [ ] **查不到就写「未确认」。** 不要用「大家都这么用」「应该可以」来填空 ——
      这正是文档里 `⚠️ 未确认` 存在的意义。
- [ ] **注意 403 与 000 的区别。** `403` 是对方主动拒绝（如 `dl.acm.org` 挡机器人），
      需要换浏览器；`000` 在本机通常只是 TLS 抖动，**重试 5–12 次**，它从不表示「页面不存在」。

---

## 5. 未确认事项（诚实清单）

- **USENIX 的复用/翻译政策**：未找到政策页；USENIX 类论文的翻译权利**仍属未知**。
- **ACM 政策页原文**：`acm.org` / `dl.acm.org` 返回 403，未能直接读取；
  结论基于 ACM 印在论文上的许可声明。
- **各论文的开放获取状态细节**：仅抽样确认了 MapReduce、Raft、Paxos 三篇的页面，
  其余各篇按出版社归类推断 —— **推断不等于核实**，真要翻译某一篇时必须单独走一遍本文件 §4。
- **6.824 讲座视频的权利**：与论文无关，但也未核实（需单独查视频平台条款）。
