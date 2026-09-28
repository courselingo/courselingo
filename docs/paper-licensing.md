# 论文授权核实 · Paper Licensing

> 核实日期 **2026-09-28**。方法：`curl.exe -s -L -x socks5h://127.0.0.1:7892` 抓**原始 HTML / PDF**，
> ACM 系域名（Cloudflare 拦截本机出口 IP）改走 reader 代理 `https://r.jina.ai/<原始 URL>`。
> 每条结论都附**逐字原文引用**与 URL；**无法确认的一律标 `⚠️ 未确认`，不推测、不填空**。

## 0. 最重要的一句话

**课程采用 CC BY，不等于它推荐的论文也是 CC BY。**

MIT 6.824 课程站是 **CC BY 3.0 US**（已核实，见 [course-catalog.md](./course-catalog.md)），
但那个许可触碰得到的**最多只是课程自己的材料** —— 讲义、作业、课程网页；
**而且它「覆盖讲义」这一点并未被证实**（徽章只在主页，见下方范围限定）。
无论它覆盖面多大，都**管不到**课程阅读列表里的第三方论文。

> ⚠️ **范围限定（2026-09-28 二次核实补正）**：6.824 的 CC BY 3.0 US 徽章**只出现在课程主页**；
> 我们实际依据的讲义文件 `notes/l01.txt` **无许可标注、无版权声明**（0/0/0）
> ⇒ 连「讲义」这一项都按 **`未确认`** 处理（默认保留所有权利）。
> 详见 [licensing-research-log.md](./licensing-research-log.md) 与 [content-policy.md](./content-policy.md)。
> **结论：6.824 现在只发布原创讲解，不产出逐字稿与双语原文对照。**
> 本文件下面关于论文授权的分析**不受影响**（论文从来就没有课程许可可用），
> 但 §0 这句「课程站是 CC BY」**不得再被用作任何材料的授权依据** —— 包括课程讲义本身。

MapReduce（USENIX）、GFS（ACM）、Raft（USENIX）、Paxos（ACM）各自是**独立的作品、独立的版权**。
「6.824 是 CC BY」这句话**不能**用来论证「所以 MapReduce 也能翻」。

这是本项目最容易犯、后果最严重的一个推理错误。

---

## 1. 结论总表

| 论文 | 出版社 | 版权持有方 | 开放获取？ | **全文翻译允许？** | 商用？ | 依据（URL + 日期） |
| --- | --- | --- | --- | --- | --- | --- |
| MapReduce: Simplified Data Processing on Large Clusters (OSDI 2004) | USENIX | ⚠️ 未确认（论文本身无版权声明；USENIX 无政策页） | ✅ 免费公开 PDF | ⛔ **无授权，须向 USENIX 申请** | ⚠️ 未确认 | 论文页 + PDF 首屏无任何版权/许可字样（2026-09-28） |
| The Google File System (SOSP 2003) | ACM | **© 2003 ACM** | ✅ 2026-01-01 起 ACM 全文库免费（此前付费） | ⛔ **须 ACM 许可** | ⛔ 须付费许可 | 论文第一页 ACM 标准声明（2026-09-28） |
| In Search of an Understandable Consensus Algorithm / Raft (ATC 2014 + 扩展版) | USENIX | ⚠️ 未确认 | ✅ Open Access（页面明示） | ⛔ **无授权，须申请** | ⚠️ 未确认 | 论文页 "Open Access Media" + PDF 封面无许可（2026-09-28） |
| Paxos Made Simple (SIGACT News 2001 / MSR-TR-2001-112) | ACM | **© 2001 ACM** | ✅ 2026 起免费 | ⛔ **须 ACM 许可** | ⛔ 须付费许可 | MSR 官方发布页载 ACM 完整声明（2026-09-28） |
| Paxos Made Live — An Engineering Perspective (PODC 2007) | ACM | ⚠️ 未确认（**任何原文副本均未取到**；按 ACM 政策处理） | ✅ 2026 起免费 | ⛔ **须 ACM 许可** | ⛔ 须付费许可 | 仅出版社级政策；论文自身声明 ⚠️ 未确认 |
| Spanner: Google's Globally-Distributed Database (OSDI 2012) | USENIX | ⚠️ 未确认 | ✅ Open Access（页面明示） | ⛔ **无授权，须申请** | ⚠️ 未确认 | 论文页 "Open Access Media" + PDF 无许可（2026-09-28） |
| ZooKeeper: Wait-free coordination for Internet-scale systems (ATC 2010) | USENIX | ⚠️ 未确认 | ✅ Open Access（页面明示） | ⛔ **无授权，须申请** | ⚠️ 未确认 | 论文页 "Open Access Media" + PDF 无许可（2026-09-28） |
| Dynamo: Amazon's Highly Available Key-value Store (SOSP 2007) | ACM | **© 2007 ACM** | ✅ 2026 起免费 | ⛔ **须 ACM 许可** | ⛔ 须付费许可 | 论文第一页 ACM 标准声明（2026-09-28） |
| Chord: A Scalable Peer-to-peer Lookup Service (SIGCOMM 2001) | ACM | **© 2001 ACM** | ✅ 2026 起免费 | ⛔ **须 ACM 许可** | ⛔ 须付费许可 | 论文第一页 ACM 标准声明（2026-09-28） |
| Chain Replication for Supporting High Throughput and Availability (OSDI 2004) | USENIX | ⚠️ 未确认 | ✅ 免费公开 PDF | ⛔ **无授权，须申请** | ⚠️ 未确认 | 论文页 + PDF 无任何版权/许可字样（2026-09-28） |

**三行结论**

1. **十篇里没有任何一篇拿到了「允许全文翻译」的明确授权。** 一篇都没有。
2. **ACM 五篇**（GFS / Paxos Made Simple / Paxos Made Live / Dynamo / Chord）版权在 ACM 手上，
   论文上印的声明**只授权个人与课堂教学复制**，明示 **republish / redistribute 须事先专门许可**。
3. **USENIX 五篇**（MapReduce / Raft / Spanner / ZooKeeper / Chain Replication）能免费读，
   但**免费读 ≠ 允许翻译**：USENIX **没有发布任何复用/翻译政策**，
   论文 PDF 上**连版权声明都没有**。没有声明**不等于**没有版权（《伯尔尼公约》下版权自动产生）。

> ⚠️ **重要更新（本轮新发现）**：ACM 自 **2026-01-01** 起全面开放获取，
> **整个 ACM 历史存档**在 Basic 版 ACM Digital Library **免费**。
> 因此本文件此前版本把 ACM 五篇标为「🔒 付费」**已过时** —— 它们现在**免费可读**。
> 但 ACM 政策同时明确：**2023-01-01 之前发表的 Works，许可与版权维持原状不变。**
> 即：**从「付费才能读」变成「免费能读」，翻译权一个字都没多给。**

---

## 2. 出版社政策

### 2.1 USENIX —— 开放获取明确，但**复用/翻译政策根本不存在**

#### 已确认的事实

**① 论文页面明示开放获取**（Raft / Spanner / ZooKeeper 三页均有此区块，逐字原文）：

> "USENIX is committed to Open Access to the research presented at our events.
> Papers and proceedings are freely available to everyone once the event begins.
> Any video, audio, and/or slides that are posted after the event are also free and open to everyone.
> Support USENIX and our commitment to Open Access."

来源：<https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro>（2026-09-28）
（MapReduce / Chain Replication 的 OSDI '04 旧页面**没有**这个区块。）

**② 论文 PDF 封面只有「open access 由 USENIX 赞助」，没有任何许可**（Raft ATC '14 逐字原文）：

> "This paper is included in the Proceedings of USENIX ATC '14: 2014 USENIX Annual Technical Conference. June 19–20, 2014 • Philadelphia, PA"
> "978-1-931971-10-2"
> "Open access to the Proceedings of USENIX ATC '14: 2014 USENIX Annual Technical Conference is sponsored by USENIX."

**③ 五篇 USENIX 论文全文抽取后，版权/许可字样命中数为 0。**
对 5 个 PDF 做了全文文本抽取（MapReduce 57,356 字符；Raft 80,324；Spanner 71,020；ZooKeeper 70,575；
Chain Replication 59,622），搜索
`© | copyright | licence | license | permission | creative commons | all rights | reproduc`
**全部 0 命中**。论文上只有作者名、单位、摘要、正文与参考文献。

**④ USENIX 没有版权/复用/翻译政策页。** 已实测：

| URL | 结果 |
| --- | --- |
| `https://www.usenix.org/copyright` | ❌ **404**（`<title>Page not found \| USENIX</title>`，17820 B） |
| `https://www.usenix.org/copyright-policy` | ❌ 404 |
| `https://www.usenix.org/about/copyright` | ❌ 404 |
| `https://www.usenix.org/publications/copyright` | ❌ 404 |
| `https://www.usenix.org/policies/copyright` | ❌ 404 |
| `https://www.usenix.org/publications/openaccess` | ❌ 404 |
| `https://www.usenix.org/conferences/policies-resources` | ✅ **200**（真实页，政策目录） |
| `https://www.usenix.org/conferences/submissions-policy` | ✅ 200，`copyright/license/permission` **0 命中** |
| `https://www.usenix.org/conferences/author-resources` | ✅ 200，**0 命中** |
| `https://www.usenix.org/conference/atc14/call-for-papers` | ✅ 200（62,660 B），**0 命中** |
| `https://www.usenix.org/publications/proceedings` | ✅ 200（`<title>Papers \| USENIX</title>`），**0 命中** |
| `https://www.usenix.org/conferences/faq` | ✅ 200，**0 命中** |
| `https://www.usenix.org/search/node?keys=copyright` | ✅ 200，**站内搜索结果全是「讨论版权主题的论文」，没有一条政策页** |

`/conferences/policies-resources` 列出的全部政策条目为：Code of Conduct、Concern Reporting Process、
Accessibility Information、Staying Safe and Healthy、Registration Substitution and Cancellation、
Conference Fees for Students、Conference Grant Programs、Conference Submissions Policy、Authorship Policy、
Author Resources、Conference Network Policy、Conference Photography Policy、Conference Sponsorship Policy、
Name Change Policy、Statement on Environmental Responsibility、Process for Establishing Membership、
Privacy Policy —— **其中没有版权、复用或翻译政策。**

#### USENIX 结论

- ✅ **免费阅读、下载、存档**：明确且无争议（官方页面明示 + 无付费墙）。
- ⛔ **是否允许全文翻译并再发布：`⚠️ 未确认`** —— 不是「禁止」，而是**根本找不到任何依据**。
- **不要**因为「USENIX 是 open access」就推论「可以翻译」。Open Access 讲的是**获取（access）**，
  不是**改编（adaptation）**。USENIX 的 "Open Access Media" 文本里
  只谈 "freely available"（可自由获取），**只字未提** reuse / derivative / translate。
- **法律默认值**：USENIX 论文虽无版权声明，但受《伯尔尼公约》保护，**默认保留全部权利**。
  无声明 ≠ 公共领域。
- **现实路径**：向 USENIX 直接发信申请书面许可（`office@usenix.org`，或
  <https://www.usenix.org/contact>）。**在拿到书面许可前，不得发布全文译本。**

---

### 2.2 ACM —— 政策原文已完整取得，翻译权**明确不在免费范围内**

ACM 的版权政策页现已改名，权威 URL 为：

- <https://www.acm.org/publications/policies/publication-rights-and-licensing-policy>
  （页面标题 **"Publication Rights & Licensing Policy"**，正文首行标注 **"Updated on December 19, 2025"**）
- 旧地址 <https://www.acm.org/publications/policies/copyright-policy> 重定向到上面同一页。

> 取证说明：`acm.org` / `authors.acm.org` / `dl.acm.org` 对非浏览器客户端返回 Cloudflare
> **JS 质询页**（本机出口 IP `103.172.81.231`），**不是 403 也不是 000**。
> 本轮通过 reader 代理 `https://r.jina.ai/<原始 URL>` 成功取得政策页全文（31,571 字符）。以下引用均出自该全文。

#### 关键原文（逐字）

**① 2026-01-01 起全面开放获取 —— 但仅限「可访问」**

> "As from January 1, 2026, all articles published by ACM will be published on an Open Access basis in the ACM Digital Library and the entire archive of ACM published journal, conference, and magazine articles will be freely available on the Basic version of the ACM Digital Library."

**② 2023-01-01 之前的作品：许可与版权「冻结」，只多给阅读权**

> "For all Works published prior to January 1, 2023 ACM will not be changing the licensing or copyright assigned at the time of publication, although they will be made freely available to access and download from the Basic version of the ACM Digital Library for as long as ACM's Open Access model remains sustainable."

**③ 免费到底意味着什么（只列了 read / download / print）**

> "Since all ACM Publications are freely available in the Basic version of the ACM Digital Library, except for ACM Books titles, anyone with an internet connection may **read, download, and print** articles."

→ 注意：**read / download / print**。**没有** translate、adapt、publish derivative。

**④ 2023 年起作者不再转让版权（对本列表 10 篇不适用 —— 它们都在 2023 年之前）**

> "On January 1, 2023, ACM ceased asking authors of accepted manuscripts to transfer copyright of their Work to ACM prior to publication."
> "All authors publishing with ACM on a going forward basis retain copyright of their Works, but will continue to be required to grant ACM (1) a non-exclusive license to publish that Work in the ACM Digital Library, (2) the right to serve as the official Publisher of that Work with associated commercial rights, including the right to license the Work to third parties, such as for training by LLMs, and (3) the right to defend the integrity of that Work against various forms of infringement and misconduct by third parties on behalf of the author."

**⑤ 商业性再发布：一律需要专门许可 + 付 ACM 费用**（本节是判定全文翻译的核心）

> "_Definition of commercial republication: Any use that is not personal or non-profit educational use. Includes reprinting by trade and scholarly publishers, and use in corporate settings and their web sites, both internal and external. No direct profit need be realized from the publication or sale of ACM material._"
>
> "For Works not published under a CC-BY license, commercial use normally requires a license and payment of release fees. For such Works, **all reproductions other than those listed in this document require specific permission and a fee payable to ACM.** This includes republishing in textbooks, commercially-produced course packs sold to students, anthologies, and other edited publications, and posting or other electronic distributions, unless use is done in connection with the STM Permission Guidelines Initiative."

**⑥ 无 CC 许可的作品，多份分发须书面许可 + CCC 交易许可**

> "Works published without a Creative Commons license must obtain written permission from ACM to produce multiple copies of Works for distribution to more than ten peers, co-workers, clients, etc. and will require a transactional license from the CCC and payment of the required per copy fee. Send requests to permissions@acm.org or go to http://www.copyright.com."

**⑦ ACM 是 STM Permissions Guidelines 签署方**

> "ACM is a signatory to the STM Permissions Guidelines, which simplifies the process for third parties (including researchers) to reuse ACM published content in new works under development."

链接：<https://www.stm-assoc.org/intellectual-property/permissions/permissions-guidelines/>

**⑧ 若某作品选了 CC BY-NC-ND，则衍生作品被明确禁止（= 翻译被禁）**

> "CC-BY-NC-ND: Requires attribution but allows limited reuse by prohibiting the use of the material for commercial purposes **and the creation and distribution of derivative works**."

（**翻译就是衍生作品**。所以即使是 CC 许可的作品，只要带 **ND**，翻译同样被禁。
本项目已有前例：`6.1600-notes` 是 **CC BY-NC-ND 4.0**。）

#### ACM 政策里「翻译」这个词出现了几次？—— **0 次**

对当前政策页全文（31,571 字符）做精确计数：

| 关键词 | 命中次数 |
| --- | --- |
| `translat` | **0** |
| `translate` | **0** |
| `translation` | **0** |
| `language` | **0** |
| `reprint` | 1 |
| `derivative` | 2 |
| `adaptation` | 1 |
| `permission` | 73 |

#### ACM 的「翻译授权」机制 —— 实际情况（请勿照抄旧说法）

**必须如实说明：今天在 `acm.org` 上已经找不到一个专门的「申请翻译」表单页。**
本轮实测以下候选地址**全部 404**：

| 候选 URL | 结果 |
| --- | --- |
| `https://www.acm.org/publications/rights-and-permissions` | ❌ **404**（旧版曾存在的入口，现已下线） |
| `https://www.acm.org/publications/policies/rights-and-permissions` | ❌ 404 |
| `https://authors.acm.org/author-resources/rights/permissions` | ❌ 404 |
| `https://www.acm.org/publications/policies/permission-to-translate` | ❌ 404 |
| `https://www.acm.org/publications/policies/translations` | ❌ 404 |

**「翻译」在 ACM 的体系里被归类为一种「一揽子再发布请求（blanket republication request）」** ——
这一点有历史原文为证。2018 年版 ACM Copyright Policy
（存档：`https://web.archive.org/web/2018id_/https://www.acm.org/publications/policies/copyright-policy`，
94,773 字符，`<title>Copyright Policy</title>`）全文里 `translat` 只出现 **1 次**，且是复数 `translations`：

> "...to further disseminate works by acting as a single source for **blanket republication requests, such as aggregated collections or translations**, and the delivery of the material to the requesting party..."

→ 语义很清楚：**ACM 把「翻译」和「汇编集」并列为一种由 ACM 统一对外发放的再发布授权**。
即翻译权由 ACM（或其指定的权利人）掌握，需要**逐件申请**。

#### 因此，ACM 的翻译授权实际路径是（按顺序尝试）

1. **写信给 `permissions@acm.org`** —— 这是 ACM 自己的政策文本与 ACM 旗下刊物
   （Ubiquity 权限页：<https://ubiquity.acm.org/permissions.cfm>）**反复指向的唯一收件地址**。
   Ubiquity 页原文：> "Requests for permission to reprint or use any materials posted by _Ubiquity_ should be directed to permissions@acm.org."
   申请时须写清：作品标题、DOI（见 §3）、**用途（全文中文翻译）**、**发行范围与是否商用**、预计印数/流量。
2. **走 CCC（Copyright Clearance Center）取得交易许可**：<http://www.copyright.com>
   —— ACM 政策明示「transactional license from the CCC and payment of the required per copy fee」。
   **商用（含售卖的译本、教材、课程包）几乎必然要付费。**
3. **STM Permissions Guidelines**（ACM 是签署方）—— 覆盖的是在**新学术作品**中复用**有限篇幅**的
   ACM 内容，**不覆盖**「整篇论文的完整译本」。不要拿它当全文翻译的依据。
4. **查该篇论文的第一页声明，确认权利人到底是谁。** 2001–2007 年的 ACM 会议论文，
   版权通常在 ACM（见 §3 逐字声明）；但少数情况作者保留了版权，此时**权利人可能是作者**，
   需另行联系作者。

> ⚠️ **不要**把「ACM 2026 年开放获取了」当成「可以翻译了」。政策原文亲手堵死了这个推论（见 ② 与 ③）。

#### ACM Open / OpenTOC 对本列表的影响

**对本列表 10 篇中的 5 篇 ACM 论文：无任何正面影响。**

- **ACM Open**（机构/APC 路径的开放获取）与 **OpenTOC**（会议论文集目录免费开放）解决的都是
  **「能不能免费读到」**，即 access。
- 本列表的 ACM 论文全部发表于 **2001–2007**，**早于** ACM 2013-04-01 才开始的 CC 许可选项，
  更早于 2023 年的版权保留改革。
- 政策原文直接判定：> "For all Works published prior to January 1, 2023 ACM will not be changing the licensing or copyright assigned at the time of publication..."
  → 这 5 篇**当年是什么条款，现在还是什么条款**：ACM 版权 + 仅个人/课堂复制 + 再发布须许可。
- 也就是说，**开放获取让它们从「付费才能读」变成「免费能读」，但翻译权一点没变。**

---

### 2.3 IEEE

**本次未涉及。** MIT 6.824 阅读列表里没有 IEEE 论文。
若将来引入 IEEE 论文，**必须单独核实** —— IEEE 的版权政策与 ACM/USENIX 都不同，
且 IEEE 亦有独立的 permissions 流程。**不要**用本文件的结论外推到 IEEE。

---

## 3. 逐篇取证附录

> 状态说明：**200** = 真实页面/真实 PDF（内容有效）；
> **404** = 连接成功且确认资源不存在（`<title>` 为官方 404 页，**是有效证据**）；
> **000** = 连接层 TLS 抖动，**按规则重试 5–12 次后仍失败**才记录，**绝不等于「页面不存在」**。

### 3.1 MapReduce: Simplified Data Processing on Large Clusters (OSDI 2004, USENIX)

| 项目 | 内容 |
| --- | --- |
| 论文页 | <https://www.usenix.org/conference/osdi-04/mapreduce-simplified-data-processing-large-clusters> → **200**，`<title>MapReduce: Simplified Data Processing on Large Clusters \| USENIX</title>` |
| PDF | <http://usenix.org/publications/library/proceedings/osdi04/tech/full_papers/dean/dean.pdf> → **200**（57,356 字符） |
| 开放获取 | ✅ 免费公开下载（无付费墙） |
| 版权声明 | **无。** PDF 全文搜索 `© / copyright / license / permission` **0 命中**。 |

**逐字原文（PDF 开头，即全部前置信息）**：

> "MapReduce: Simplified Data Processing on Large Clusters"
> "Jeffrey Dean and Sanjay Ghemawat"
> "jeff@google.com, sanjay@google.com"
> "Google, Inc."

→ 没有任何版权行、没有许可条款、没有 `sponsorship`/`open access` 封面页（OSDI '04 早于该惯例）。
**版权持有方：`⚠️ 未确认`**（论文未声明；USENIX 未公布政策）。

**判定：全文翻译 ⛔ 无授权，须向 USENIX 申请；商用 `⚠️ 未确认`。**

---

### 3.2 The Google File System (SOSP 2003, ACM)

| 项目 | 内容 |
| --- | --- |
| DOI | `10.1145/945445.945450` |
| 官方页 | `dl.acm.org/doi/10.1145/945445.945450` → ❌ 被 Cloudflare 质询拦截；经 reader 代理仍 **0 字节**（不可达） |
| 采用副本 | <https://static.googleusercontent.com/media/research.google.com/en/us/archive/gfs-sosp2003.pdf> → **200**（90,349 字符） |
| 交叉验证副本 | <https://research.google.com/archive/gfs-sosp2003.pdf>（90,308）、<https://pdos.csail.mit.edu/6.824/papers/gfs.pdf>（90,484）—— **三者声明完全一致** |
| 版权持有方 | **© 2003 ACM** |
| 开放获取 | ✅ ACM 自 2026-01-01 起全文库免费（此前付费） |

**逐字原文（论文第一页 ACM 标准声明）**：

> "Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. SOSP'03, October 19–22, 2003, Bolton Landing, New York, USA. **Copyright 2003 ACM 1-58113-757-5/03/0010 ... $5.00.**"

**判定：全文翻译 ⛔ 须 ACM 许可（翻译 = "copy otherwise" + "republish"）；商用 ⛔ 须付费许可。**

---

### 3.3 In Search of an Understandable Consensus Algorithm (Raft) (ATC 2014, USENIX)

| 项目 | 内容 |
| --- | --- |
| 论文页 | <https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro> → **200**（含 "Open Access Media" 区块） |
| 会议版 PDF | <https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf> → **200**（80,324 字符） |
| **扩展版 PDF** | <https://raft.github.io/raft.pdf> → **200**（92,068 字符），`<title>` 页首为 **"In Search of an Understandable Consensus Algorithm (Extended Version)"** |
| 开放获取 | ✅ 页面明示（见 §2.1 ①） |
| 版权声明 | **无。** 两个版本全文搜索 `© / copyright / license / permission / creative commons` **均 0 命中**。 |

**逐字原文（会议版 PDF 封面页）**：

> "This paper is included in the Proceedings of USENIX ATC '14: 2014 USENIX Annual Technical Conference. June 19–20, 2014 • Philadelphia, PA"
> "978-1-931971-10-2"
> "Open access to the Proceedings of USENIX ATC '14: 2014 USENIX Annual Technical Conference is sponsored by USENIX."

**关于「会议版 vs 扩展版」**：两版本**都没有**任何许可条款，故**不构成**「换一个版本就有授权」的可能。
扩展版与会议版**同样受版权保护**，且版权归属同样 `⚠️ 未确认`。

**判定：全文翻译 ⛔ 无授权，须向 USENIX 申请；商用 `⚠️ 未确认`。**

---

### 3.4 Paxos Made Simple (2001, ACM SIGACT News / MSR-TR-2001-112)

| 项目 | 内容 |
| --- | --- |
| DOI | `10.1145/568425.568398` |
| 官方发布页 | <https://www.microsoft.com/en-us/research/publication/paxos-made-simple/> → **200**（16,515 字符） |
| 作者 PDF | <https://lamport.azurewebsites.net/pubs/paxos-simple.pdf> → **200**（27,064 字符）；**该 PDF 抽取文本中无版权声明**，声明在 MSR 官方发布页上 |
| 版权持有方 | **© 2001 ACM**（注意：**不是** Microsoft —— 尽管技术报告挂在 Microsoft Research） |
| 开放获取 | ✅ ACM 自 2026-01-01 起全文库免费 |

**逐字原文（MSR 官方发布页所载 ACM 声明）**：

> "Copyright © 2001 by the Association for Computing Machinery, Inc. Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. **Abstracting with credit is permitted.** To copy otherwise, to republish, to post on servers, or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from Publications Dept, ACM Inc., fax +1 (212) 869-0481, or permissions@acm.org."

**要点**：`Abstracting with credit is permitted` —— **带署名的「摘要」是明确允许的**，
这为「自己写的导读 + 带署名的摘要」提供了直接依据（见 §4(a)(d)）。
但**全文翻译不在此列**。

**判定：全文翻译 ⛔ 须 ACM 许可；商用 ⛔ 须付费许可。**

---

### 3.5 Paxos Made Live — An Engineering Perspective (PODC 2007, ACM)

| 项目 | 内容 |
| --- | --- |
| DOI | `10.1145/1281100.1281103` |
| 版权持有方 | **`⚠️ 未确认`** —— 未能取得该论文任何原文副本 |
| 开放获取 | ✅ ACM 自 2026-01-01 起全文库免费 |

**⚠️ 无法取得原文 —— 明确记录，不推测。** 本轮尝试的全部副本均失败：

| 尝试的 URL | 结果 |
| --- | --- |
| `https://dl.acm.org/doi/10.1145/1281100.1281103` | ❌ Cloudflare 质询，经 reader 代理仍 **0 字节** |
| `https://dl.acm.org/doi/pdf/10.1145/1281100.1281103` | ❌ 同上 |
| `https://research.google.com/archive/paxos-made-live.pdf` | ❌ **404**（1,618 B，确认真实不存在） |
| `https://static.googleusercontent.com/media/research.google.com/en//archive/paxos-made-live.pdf` | ❌ **000**（7 轮重试仍为连接层失败） |
| `https://www.cs.utexas.edu/users/lorenzo/corsi/cs380d/papers/paxos-made-live.pdf` | ❌ **000**（7 轮重试） |
| `https://people.csail.mit.edu/nickolai/6.824-2015/papers/paxos-made-live.pdf` | ❌ 0 字节 |
| `https://read.seas.harvard.edu/~kohler/class/08w-sys/paxos-live.pdf` | ❌ 0 字节 |
| `https://cs.stanford.edu/~matei/courses/2015/6.S897/papers/paxos_made_live.pdf` | ❌ 跳转至 Berkeley，**access is restricted** |
| `https://web.stanford.edu/class/cs244b/papers/paxos-made-live.pdf` | ❌ 0 字节 |
| `https://www.cs.virginia.edu/~son/cs851/papers/paxos-made-live.pdf` | ❌ 0 字节 |
| `https://research.google/pubs/paxos-made-live-an-engineering-perspective/` | ❌ **404** |

**判定**：论文自身的许可声明 `⚠️ 未确认`。
但它是 **ACM PODC 2007 会议论文（DOI 10.1145/1281100.1281103）**，
**与 GFS / Dynamo / Chord 同属 ACM 2001–2007 时期作品**，适用 ACM 同一政策
（§2.2 ②「2023 年前的 Works 许可与版权维持原状」+ ⑤ 商业再发布须许可）。
**在这个基础上：全文翻译 ⛔ 须 ACM 许可；商用 ⛔ 须付费许可。**
但这个结论是**出版社级**的，**未获论文级声明佐证** —— 真要翻译这一篇时，**必须单独补做一遍 §5 的清单**。

---

### 3.6 Spanner: Google's Globally-Distributed Database (OSDI 2012, USENIX)

| 项目 | 内容 |
| --- | --- |
| 论文页 | <https://www.usenix.org/conference/osdi12/technical-sessions/presentation/corbett> → **200**（含 "Open Access Media"） |
| PDF | <https://www.usenix.org/system/files/conference/osdi12/osdi12-final-16.pdf> → **200**（71,020 字符） |
| 开放获取 | ✅ 页面明示 |
| 版权声明 | **无。** 全文 `© / copyright / license / permission` **0 命中**。 |

**逐字原文（PDF 页眉，即全部法律信息）**：

> "USENIX Association 10th USENIX Symposium on Operating Systems Design and Implementation (OSDI '12) 251"

→ 只有协会名与会议名、页码，**没有版权行、没有许可**。

**判定：全文翻译 ⛔ 无授权，须向 USENIX 申请；商用 `⚠️ 未确认`。**

---

### 3.7 ZooKeeper: Wait-free coordination for Internet-scale systems (ATC 2010, USENIX)

| 项目 | 内容 |
| --- | --- |
| 论文页 | <https://www.usenix.org/conference/usenix-atc-10/zookeeper-wait-free-coordination-internet-scale-systems> → **200**（含 "Open Access Media"） |
| PDF | <https://www.usenix.org/events/atc10/tech/full_papers/Hunt.pdf> → **200**（70,575 字符） |
| 开放获取 | ✅ 页面明示 |
| 版权声明 | **无。** 全文 `© / copyright / license / permission` **0 命中**（唯一片段是参考文献里引用他人论文时出现的 "USENIX Association"）。 |

**逐字原文（PDF 开头）**：

> "ZooKeeper: Wait-free coordination for Internet-scale systems"
> "Patrick Hunt and Mahadev Konar — Yahoo! Grid"
> "Flavio P. Junqueira and Benjamin Reed — Yahoo! Research"

**判定：全文翻译 ⛔ 无授权，须向 USENIX 申请；商用 `⚠️ 未确认`。**

---

### 3.8 Dynamo: Amazon's Highly Available Key-value Store (SOSP 2007, ACM)

| 项目 | 内容 |
| --- | --- |
| DOI | `10.1145/1294261.1294281` |
| 官方 DL 页 | `dl.acm.org/doi/10.1145/1294261.1294281` → ❌ Cloudflare 拦截 + reader 代理 **0 字节**（不可达） |
| 采用副本 | <https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf> → **200**（94,262 字符） |
| 版权持有方 | **© 2007 ACM** |
| 开放获取 | ✅ ACM 自 2026-01-01 起全文库免费 |

**逐字原文（论文第一页 ACM 标准声明）**：

> "Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. SOSP'07, October 14–17, 2007, Stevenson, Washington, USA. **Copyright 2007 ACM 978-1-59593-591-5/07/0010...$5.00.**"

**判定：全文翻译 ⛔ 须 ACM 许可；商用 ⛔ 须付费许可。**

---

### 3.9 Chord: A Scalable Peer-to-peer Lookup Service (SIGCOMM 2001, ACM)

| 项目 | 内容 |
| --- | --- |
| DOI | `10.1145/383059.383071` |
| 采用副本 | <https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf> → **200**（69,846 字符） |
| 版权持有方 | **© 2001 ACM** |
| 开放获取 | ✅ ACM 自 2026-01-01 起全文库免费 |

**逐字原文（论文第一页 ACM 标准声明）**：

> "Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, or republish, to post on servers, or to redistribute to lists, requires prior specific permission and/or a fee. SIGCOMM'01, August 27-31, 2001, San Diego, California, USA. **Copyright 2001 ACM 1-58113-411-8/01/0008 ... $5.00.**"

**判定：全文翻译 ⛔ 须 ACM 许可；商用 ⛔ 须付费许可。**

---

### 3.10 Chain Replication for Supporting High Throughput and Availability (OSDI 2004, USENIX)

| 项目 | 内容 |
| --- | --- |
| 论文页 | <https://www.usenix.org/conference/osdi-04/chain-replication-supporting-high-throughput-and-availability> → **200**（**无** "Open Access Media" 区块，属旧版页面） |
| PDF | <http://usenix.org/publications/library/proceedings/osdi04/tech/full_papers/renesse/renesse.pdf> → **200**（59,622 字符） |
| 开放获取 | ✅ 免费公开下载 |
| 版权声明 | **无。** 全文 `© / copyright / license / permission` **0 命中**。 |

**逐字原文（PDF 开头）**：

> "Chain Replication for Supporting High Throughput and Availability"
> "Robbert van Renesse — rvr@cs.cornell.edu"
> "Fred B. Schneider — fbs@cs.cornell.edu"
> "FAST Search & Transfer ASA Tromsø, Norway and Department of Computer Science Cornell University Ithaca, New York 14853"

**判定：全文翻译 ⛔ 无授权，须向 USENIX 申请；商用 `⚠️ 未确认`。**

---

## 4. 推荐默认策略

### 4.1 四种做法的判定

| 做法 | 判定 | 依据与说明 |
| --- | --- | --- |
| **(a) 我们自己写的导读 / 原创讲解** | 🟢 **默认做法，全部课程都可以做** | **思想、事实、算法、原理不受版权保护，受保护的只是「表达」。** 用我们自己的话讲清：这篇论文要解决什么问题、怎么做、代价是什么、哪里已经过时。**不复制原文表达**，不做逐句改写（逐句改写仍是衍生作品），不复制图表。ACM 声明中 `Abstracting with credit is permitted`（带署名做摘要被明确许可）进一步支持这一形态。仍须**标注出处**（作者、会议、年份、DOI/URL）。 |
| **(b) 论文的全文中文翻译** | 🔴 **逐篇取得书面授权后才可做。当前 10 篇一篇都没有授权** | 全文翻译是**复制了论文全部表达的衍生作品**。ACM 五篇：版权在 ACM，声明明示 `To copy otherwise... or republish... requires prior specific permission and/or a fee`；翻译正落在此类。USENIX 五篇：**没有任何授权条款**，默认保留全部权利。**没有例外，没有「大家都这么翻」的豁免。** |
| **(c) 转载原始 PDF** | 🔴 **一律不做** | 这是**再分发（redistribute）**。ACM 声明要求 `post on servers, or to redistribute to lists, requires prior specific permission`；USENIX 无任何许可。**且没必要** —— 直接链接官方来源即可，读者点一下就能免费拿到（ACM 现在也免费了）。 |
| **(d) 为评论/导读引用短句原文** | 🟢 **可以做（有边界）** | 引用要**短**、要**标注出处**、要**服务于评论**（引用是为了说明观点，不是为了替代原文）。ACM 的 `Abstracting with credit is permitted` 给摘要留了明路；`fair use / fair dealing` 给评论性引用留了空间。**红线**：不要用连续引用拼凑出一篇实质上的译文。 |

### 4.2 落地规则

1. **默认写导读。** 这是法律上最安全、产品上也最有价值的形态 ——
   读者要的不是「英文论文的中文版」，而是「有人把这篇论文讲明白」。
   **(a) 是唯一无需任何外部许可就能立刻开工的形态。**
2. **要翻译就先拿授权，再登记。** 拿到**书面**授权后，把该篇的
   `license.verified = true`、`allows_translation = true`、
   `evidence_url` 指向授权凭证、`checked_at` 填日期。**然后**才能写 `output_mode = "translation"`。
3. **只核实了还不够。** `verified = true` 只表示「我们查过了」；
   `allows_translation = true` 才表示「查出来的结果是允许翻译」。
   两个字段分开，正是为了让「查过了，结论是不行」也能被如实记录。
4. **绝不用课程授权替代论文授权。** 见 §0。
5. **是否商用要单独问。** 即使拿到翻译许可，若本项目有**任何**商业化（付费墙、广告、卖课、
   企业内训、售书），必须**在申请时明说**「commercial use」。
   ACM 政策对商业性再发布是 `payment of release fees`，USENIX 则完全未知。
6. **授权是逐篇的，不是逐出版社就够。** 出版社政策给出**基线**，但论文第一页声明可能不同
   （例如作者保留版权的情形）。**每一篇都要落到自己的声明上。**

### 4.3 拿到翻译许可的现实路径

**ACM 五篇（GFS / Paxos Made Simple / Paxos Made Live / Dynamo / Chord）：**

1. 发信 **`permissions@acm.org`**（ACM 政策与旗下刊物共同指向的唯一地址），
   写明：标题、DOI、**用途 = 全文中文翻译**、发行介质、**是否商用**、印数/流量、是否收费。
2. 或走 **CCC / RightsLink**：<http://www.copyright.com>（ACM 明示的 transactional license 渠道）。
3. 商业用途预期**需要付费**（`payment of release fees` / `per copy fee`）。
4. 若该篇声明显示版权在**作者**手上（而非 ACM），改联系作者。

**USENIX 五篇（MapReduce / Raft / Spanner / ZooKeeper / Chain Replication）：**

1. USENIX **没有公开的授权流程**，只能**直接发信**
   （<https://www.usenix.org/contact>，或 `office@usenix.org`）。
2. 申请里同样写清：标题、会议与年份、**用途 = 全文中文翻译**、**是否商用**。
3. **在收到书面许可之前，默认答案是不行。** 不要因为「找不到禁止条款」就当作得到了许可。

**兜底（推荐）**：如果授权谈不下来（很可能谈不下来，尤其是商业化项目），
**就做 (a) 原创导读**。这既避开了全部版权风险，也不牺牲产品价值。

---

## 5. 「怎么核实一篇论文的许可」检查清单

给后续贡献者与 Agent 用。**这个项目在这上面栽过跟头，所以每一条都有来由。**

- [ ] **抓原始 HTML，不要先过滤标签再搜文本。**
      许可经常只存在于 `rel="license"` 属性、`href` 或图片徽章的 `alt` 里。
      本项目曾因过滤标签后搜索，把 MIT 6.824 误判为「无许可」，结论完全相反。
- [ ] **找到许可之后，还要确认它覆盖哪份文件 —— 尤其是「我们实际要用的那一份」。**
      本项目纠正上一条之后又栽了第二次：由「6.824 主页有 CC BY 徽章」推出「讲义可翻译」，
      但**从未检查 `notes/l01.txt` 本身**；补查后该文件 0 命中 ⇒ 讲义按 `未确认` 处理。
      **只核课程入口页 = 又一次把推断当原文。**
      同理适用于论文：**出版社政策 ≠ 这一篇的声明**（见下一条）。
- [ ] **`000` ≠ 404。** 本机主导失败模式是**逐连接随机的 TLS 握手失败**
      （`schannel: failed to receive handshake`），**同一 URL 可能失败 5 次后成功**。
      **每个 URL 重试 5–12 次**，再下结论。
      本项目曾把一次瞬时 `000` 当成「页面不存在」，导致过错误结论。
- [ ] **确认 404 的方法是看 `<title>`，不是看「抓不到」。**
      例：USENIX 的 404 页是 `<title>Page not found | USENIX</title>`，固定 17820 字节；
      真实页面 `<title>` 各不相同。
- [ ] **确认「免费可读」和「允许翻译」是两件事。**
      作者把 PDF 挂在自己主页、出版社开放获取、会议论文集免费 ——
      **这三种都不构成任何复用授权**。
- [ ] **分清三类状态**：
      ①「作者/出版社挂了个免费 PDF」= 无授权；
      ②「明确的复用许可」= 例如 CC BY / CC BY-SA；
      ③「排除了派生的许可」= 例如 **CC BY-NC-ND**，**ND 直接禁止翻译**。
      三者天差地别，**不要混为一谈**。
- [ ] **查出版社政策，而不只是论文页；也要查论文页，而不只是出版社政策。**
      两者可能不一致（作者保留版权时，权利人就是作者而不是出版社）。
- [ ] **同时看论文 PDF 的第一页页脚。**
      ACM 这类老论文的许可声明**只印在 PDF 首页**，网页上根本没有。
- [ ] **查 `LICENSE` / `terms` / `about` / `copyright` / `permissions` 页面。**
      找不到时要**穷举候选 URL** 并逐个记录状态，而不是写「没有政策」。
- [ ] **区分会议版与扩展版 / 技术报告版。**
      同一篇论文的不同版本可能适用不同条款（例如 Raft 的会议版与扩展技术报告；
      Paxos Made Simple 同时是 SIGACT News 文章与 MSR 技术报告）。
- [ ] **无版权声明 ≠ 公共领域。**
      依《伯尔尼公约》，版权**自动产生**。**没有声明 = 默认保留全部权利**，
      不是「随便用」。
- [ ] **`403` / Cloudflare 质询 ≠ 页面不存在。**
      `acm.org` / `dl.acm.org` 会向非浏览器客户端返回 JS 质询页。此时**换渠道**
      （reader 代理、作者主页、机构镜像、官方发布页），而不是写「无法核实」了事。
- [ ] **商用与学术用途是两套问法。**
      申请许可时必须**主动声明是否商用**。ACADEMIC / personal 的许可**不覆盖**商业用途。
- [ ] **记录 `evidence_url` + `checked_at`。** 没有出处的「已核实」等于没核实。
- [ ] **查不到就写「未确认」。** 不要用「大家都这么用」「应该可以」来填空 ——
      这正是本文档里 `⚠️ 未确认` 存在的意义。

---

## 6. 未确认事项（诚实清单）

| # | 未确认项 | 具体缺口 | 影响 |
| --- | --- | --- | --- |
| 1 | **USENIX 的复用/翻译政策** | 穷举了 12 个候选 URL + 站内搜索 + 5 篇 PDF 全文，**未找到任何政策**。既找不到政策页，也找不到论文上的声明 | USENIX 五篇的**翻译权利整体未知**。只能靠直接联系 USENIX 解决 |
| 2 | **USENIX 五篇的版权持有方** | 论文上**根本没有版权行** | 无法确定是 USENIX 还是作者持有；申请许可时可能需要两边都问 |
| 3 | **Paxos Made Live 的论文级声明** | 11 个候选副本**全部失败**（Cloudflare / 404 / 000）。**未能取得该论文任何原文** | 该篇判定**仅基于 ACM 出版社政策**，未经论文声明佐证。翻译前必须重做一次核实 |
| 4 | **ACM 是否有专门的「翻译」表单页** | 5 个候选地址全部 404；现行政策全文 `translat` 命中 **0 次**。历史政策把 translations 归为 blanket republication request | 已给出实际路径（`permissions@acm.org` + CCC），但**无法确认** ACM 是否另有内部表单流程 |
| 5 | **各篇的实际授权费用** | 政策只说 `payment of release fees` / `per copy fee`，未给价目 | 商业化前必须询价 |
| 6 | **Internet Archive / Wayback 不可用** | 实测返回 **"Internet Archive services are temporarily offline"** | 无法用历史快照补证已下线的 ACM 旧政策页（仅 2018 年快照在早些时候取得成功） |
| 7 | **6.824 讲座视频的权利** | 与论文无关，未核实；需单独查视频平台（YouTube）条款 | 不影响论文翻译决策 |
| 8 | **IEEE** | 6.824 阅读列表无 IEEE 论文，本次未核实 | 将来引入 IEEE 论文时须单独走 §5 |

---

## 7. 取证环境限制（供复现者参考）

- **必须用 SOCKS5**：`curl.exe -s -L -x socks5h://127.0.0.1:7892 "<URL>"`。
  端口 `7892` 是 **SOCKS5 only**；写成 `http://127.0.0.1:7892` 会**静默返回 `000`**，
  看起来像「整台机器被墙」，实则是协议用错。
- **`web_search` 永远失败**（无 API key）；**`web_fetch` 拒收**本机域名
  （Clash fake-IP 把所有域名解析到非公网段 `198.18.0.x`）。
- **`acm.org` / `authors.acm.org` / `dl.acm.org`** 对非浏览器客户端返回 Cloudflare JS 质询页。
  可用 **reader 代理**绕开：`https://r.jina.ai/<原始 URL>`。
  但 `dl.acm.org` 的具体文章页**经代理后仍返回 0 字节**，属**不可达**。
- **`dl.acm.org` 文章页不可达是本文件的已知盲区**：ACM 五篇的声明因此改由
  **作者/机构托管的官方 PDF 副本**取得（Google Research、Amazon allthingsdistributed、MIT PDOS、Microsoft Research）。
  这三者交叉验证了 GFS 的声明**完全一致**，可信度高。
