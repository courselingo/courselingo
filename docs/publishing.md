# 发布方案决策 · GitHub Pages vs GitBook

> 决策日期：**2026-09-28** · 状态：**已决策，Phase 0 生效**
> 消费方：[pipeline-spec.md](./pipeline-spec.md) §8、`template/.github/workflows/`、各课程仓维护者

## 0. 结论（TL;DR）

**采用 GitHub Pages**：由本仓自带的零依赖构建脚本产出静态站（`python scripts/build.py --out site --base-url <url>`），再用 GitHub Actions 部署 `site/`。整个发布路径不安装任何依赖。

**不采用 GitBook 作为主站。** 它是托管型 SaaS，内容的真相源会搬到 GitBook 的 block 模型里；这与本项目"内容就是仓库里的纯 Markdown、任何时候都能换个渲染器重新部署"的原则正面冲突（§4）。

**第三方案（MkDocs Material / VitePress on Pages）**：技术上完全可行，渲染能力还强过我们自己的 `build.py`；但两者都必须 `pip` / `npm` 装依赖，直接违反 [pipeline-spec.md](./pipeline-spec.md) §0 的零依赖约束。列为**将来的迁移路径**，不是现在的选择（§8）。

一句话理由：**本项目的核心资产是仓库里的纯 Markdown 和那条能硬失败（hard-fail）的授权闸门；GitHub Pages 让两者都留在 Git 里，GitBook 让两者都离开 Git。**

---

## 1. 约束条件（来自本项目，不是通用偏好）

| 约束 | 出处 | 对发布方案的要求 |
| --- | --- | --- |
| 授权尚未核实，闸门必须先于发布 | [architecture.md](./architecture.md)、spec §6 | 发布路径上必须存在一个**能拒绝部署**的程序化检查点 |
| 零依赖 Python 3.11+（仅标准库） | spec §0 | 不能依赖 `npm install` / `pip install`；本机代理不稳 |
| 内容与渲染器解耦 | spec §0 | 内容必须是纯 Markdown + TOML，换渲染器不改内容 |
| 中文站点、移动端可读 | spec §7 | `lang="zh-CN"`、中文排版；托管方不得改写内容 |
| 内联 SVG 配图 | spec §7（`figures/*.svg`） | 必须能渲染自定义内联 SVG |
| 每门课一个仓、可单独授权单独下线 | [architecture.md](./architecture.md) 设计目标 3 | 每仓独立部署、独立域名或路径、独立权限 |

---

## 2. 选项对比

| 维度 | **GitHub Pages（推荐）** | **GitBook** | MkDocs Material / VitePress on Pages |
| --- | --- | --- | --- |
| 成本（公开仓） | **$0**；站点 ≤1 GB、软带宽 100 GB/月 | 免费版 $0（1 用户，无自定义域名）；Premium **$65/站点/月 + $12/用户/月** | $0（托管在 Pages） |
| 内容真相源 | **仓库里的 Markdown/TOML** | **GitBook 的 block 模型**（Git 只是同步的一侧） | 仓库里的 Markdown |
| 内容形态 | 我们的 Markdown 子集，原样保留 | Git 同步时被规范化/结构化，往返可能改写 | Markdown，但要求更严格的语法/目录约定 |
| 自定义域名 | 免费，任意域名（**Actions 发布无需 CNAME 文件**） | **仅 Premium（$65/月起）** | 免费（走 Pages） |
| HTTPS | 免费自动签发（Let's Encrypt）+ Enforce HTTPS | 付费版提供 | 同 Pages |
| 搜索 | ❌ 无内置；需自建静态索引（仍是零依赖：构建时生成 JSON + 少量 JS） | ✅ 内置全文搜索；AI 搜索（Ask）在 Premium | ✅ MkDocs 内置（lunr）/ VitePress 内置 MiniSearch |
| i18n | ❌ 无内置，靠目录结构 + 自己加 `lang` 切换 | 有内置 Translations（AI 翻译是 Agent 能力，层次/价格另算） | MkDocs 有 i18n 插件；VitePress 有 locale 支持 |
| 贡献流（PR） | ✅ **原生**：fork → PR → CI 校验 → 合并即发布 | Git Sync 双向同步；GitBook 侧编辑与 change request 是另一套协作模型 | 同 Pages |
| 内联 SVG | ✅ 完全自由（我们输出什么就是什么） | ⚠️ 编辑器是结构化 block 模型，没有"原始 HTML/SVG"块；SVG 只能当**图片文件**上传，或改用 Mermaid/Drawing block | ✅ 自由 |
| 授权闸门能否阻断发布 | ✅ **能**：`validate.py` 退出非 0 → job 失败 → 部署不执行 | ⚠️ 未找到可在发布路径上插入自定义校验并阻断的官方钩子 | ✅ 能 |
| 厂商锁定 | 低：产物是纯静态文件，换主机只改 DNS | 高：内容与协作都沉淀在平台里 | 中：绑定某一 SSG 生态 |
| 中国大陆可达性 | ⚠️ `*.github.io` 不稳，需自有域名 + 可选 CDN 镜像 | ⚠️ 同样不保证 | 同 Pages |
| 维护负担 | 自己维护 `build.py`（零依赖，约几百行） | 平台维护渲染，但配置/升级/账单归你 | 依赖链升级（pip/npm） |

---

## 3. 逐项论证（只讲对本项目成立的）

- **成本**：GitHub Pages 对公开仓免费，我们的用法（纯静态、无大图）离 1 GB / 100 GB 的软限制很远；而且"用自定义 Actions 工作流构建"不受每小时 10 次构建的限制。GitBook 免费版每人只能有 1 个协作者、并且**不给自定义域名**——对一个要对外发布的中文课程站来说这是硬伤；要域名就得 Premium，$65/站点/月 × 每门课一个站点，成本随课程数线性增长。
- **锁定**：Pages 的产物就是 `site/` 目录，明天想换 Cloudflare Pages / Netlify / 自建 nginx，只需改 DNS，内容是同一份 Markdown。GitBook 上内容的真相源是它的 block 模型，离开时要走导出/迁移。
- **内容是否留在仓库**：这是我们最重要的判据。spec §0 明确写了为了"将来可整体迁移到 VitePress / MkDocs 而无需改内容"，内容必须与渲染器解耦。GitBook 的 Git Sync 是**双向**的（官方文档原话：编辑器里的改动会自动同步，GitHub/GitLab 上的提交也是），也就是 GitBook 的编辑器同样在写内容——真相源不再是仓库。
- **自定义域名**：Pages 免费且任意域名；GitBook 把自定义域名放在 Premium。
- **搜索**：Pages 没有内置搜索，这是它最实在的短板（见 §5）。但站内搜索对静态站而言是可以在构建期解决的：`build.py` 顺手产出 `search-index.json` + 一个小 JS，仍是零依赖、离线可用，不引入服务端。
- **i18n**：本站的"i18n"其实是**中英对照**（术语首现"中文（English）"），不是多语言站点。这由内容与渲染器决定，托管平台帮不上忙，所以这一项对两个选项都不构成决定性优势。
- **PR 贡献流**：这是社区项目的命脉。Pages 的流程就是 `fork → PR → validate.yml 跑红/跑绿 → 合并 → deploy.yml 发布`，每一步都在 GitHub 上可见、可审计、可回滚。GitBook 引入的是第二套协作模型，社区贡献者要学的就不止 git 了。
- **内联 SVG**：我们的配图是手写 SVG（能跟随明暗色、能被读屏、能选中文字）。Pages 原样输出；GitBook 是结构化 block，SVG 只能作为图片文件上传（GitBook 自家文档确实用 `.svg` 图片资源），内联能力丢失。
- **授权闸门**：见 §7，这是把决定权从"偏好"推向"必须"的那一项。

---

## 4. 为什么不是 GitBook（针对本项目的具体理由）

### 4.1 内容真相源会搬出仓库
Git Sync 是双向同步。一旦有人在 GitBook 编辑器里改动内容，改动会同步回仓库；反过来仓库里的 Markdown 也会被 GitBook 解析成它的 block。**Markdown 的"原样"就不再是保证**，而 spec §0 把"内容与渲染器解耦"写成了设计前提，不是偏好。

### 4.2 授权闸门找不到可插入的钩子
本项目的闸门要求非常具体：某讲座声明 `output_mode = "transcript"`、而 `course.toml` 里 `license.verified != true` 时，**构建必须失败、站点必须不更新**。
GitHub Pages 路径下这是机制保证（§7）。GitBook 路径下我们没有找到等价物：它确实有 Merge rules / change requests 这类发布前要求，但那是 GitBook 侧协作语言里的审查流程；我们**没有验证到**"仓库里某个提交被 Git Sync 拉进来发布时，会先跑我们的校验、失败则拒绝发布"这种官方能力。对一份默认产出踩在法律灰线上的项目，这一条足以否决。

### 4.3 GitBook 的现状与定价（2026-09-28 实测）
`www.gitbook.com/pricing` 页面（Framer 发布版本标注 Published Sep 25, 2026）原文：

- **Free**：$0/站点/月，面向个人，含 block 编辑器与自定义 block、GitHub/GitLab 同步、预览部署、LLM 优化（`llms.txt`）；**1 个用户**，无自定义域名。
- **Premium**：**$65/站点/月 + $12/用户/月**，含自定义域名、AI 搜索（Ask）、高级品牌、分析。
- **Ultimate**：**$249/站点/月 + $12/用户/月**，含 AI Assistant、AI insights、GitBook Agent 等。
- **Enterprise**：定制报价。
- 年付省 2 个月；有 14 天试用。

也就是说：要用自定义域名（对外发布的基本要求），起点是 **$65/月/站点**。若按"每门课一个课程仓"的架构为每门课建一个站点，成本随课程数增长。

### 4.4 内联 SVG 与中文排版
我们的构建契约要求自己控制输出（`lang="zh-CN"`、行高字距、明暗色、页脚署名与"非官方 · 社区项目"声明，见 [brand.md](./brand.md) 禁止事项）。GitBook 的排版模板由平台决定，品牌声明的呈现受平台布局约束；内联 SVG 也会退化成图片。

### 4.5 公平地说，GitBook 强在哪
不是一无是处：**内置搜索（含 AI 检索）、内置编辑器、内置分析、内置多语言、几乎零运维**。如果这个项目的主要矛盾是"让不会 git 的人也能参与写作"，GitBook 的性价比立刻反转。问题在于本项目当前的主要矛盾是**授权与内容自主**，不是编辑体验。

---

## 5. 推荐方案的主要缺点（诚实版）

**最主要的缺点：GitHub Pages 只是一个静态文件托管，除了"托管文件"什么都不提供。** 具体是：

1. **没有内置搜索**——读者只能靠目录和浏览器搜索（`Ctrl+F`）。要做站内搜索，得自己在构建期生成索引。
2. **没有内置 i18n、重定向、鉴权、访问统计**——想要就得自己写静态实现（或干脆不要）。
3. **没有编辑器**——不熟悉 Markdown / git 的贡献者门槛偏高，只能靠 PR 流程与（将来可能的）Issue 模板缓解。
4. **`*.github.io` 在中国大陆访问不稳定**——对一个中文读者为主的站点，这不是小事。缓解办法是尽早绑定自有域名，必要时把同一份 `site/` 产物镜像到 Cloudflare Pages / Netlify。注意：要走**国内** CDN 加速则涉及域名 ICP 备案，社区开源项目通常不愿意承担这个合规成本，所以镜像方案默认选海外 CDN。
5. **`build.py` 是我们自己的**——渲染 Markdown 子集、术语标记、导航、样式全归我们维护。这是零依赖换来的代价。

如果这些缺点里有一条变得致命（尤其是第 3 条成为主要矛盾，或 §4.2 的闸门能被平台满足），就该重新评估（§8）。

---

## 6. 自定义域名 + HTTPS 设置步骤（GitHub Pages）

每一步都做过核实（GitHub 官方文档 `pages/.../managing-a-custom-domain-for-your-github-pages-site`，2026-09-28 读取）。

### 6.1 仓库设置
1. Settings → Pages → Build and deployment → **Source 选 "GitHub Actions"**。
   - 这一步必须先做：`actions/configure-pages` 在 Pages 未启用时拿不到站点信息会失败。
2. 在 **Custom domain** 里填域名（比如 `courselingo.example.com`），点 **Save**。
   - 顺序很重要：**先**在 GitHub 里登记域名，**再**去 DNS 服务商配置。反过来做，别人可能抢先在 GitHub Pages 上占用你的子域。

### 6.2 DNS 记录（在域名服务商处配置）
- **子域名**（推荐，如 `courselingo.example.com`）：`CNAME` 记录，Name 填子域名，Target 填 `<owner>.github.io`（**不要**带仓库名，也**不要**指向设置页里那个 `*.pages.github.io` 的独有子域）。
- **裸域**（如 `example.com`）：`A` 记录指向 `185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`；若需要 IPv6，再加 `AAAA` 指向 `2606:50c0:8000::153`、`2606:50c0:8001::153`、`2606:50c0:8002::153`、`2606:50c0:8003::153`。（也可用服务商提供的 `ALIAS`/`ANAME` 记录替代这一组 A 记录。）
- **裸域 + `www`**：GitHub 官方**推荐**这种组合用于 HTTPS 站点——先配裸域，再给 `www` 加一条指向 `<owner>.github.io` 的 `CNAME`。
- DNS 生效最多 24 小时（通常几分钟）。Windows 上可用 `Resolve-DnsName` 验证（`dig` 在 Windows 上不自带）。

### 6.3 强制 HTTPS
DNS 生效后回到 Settings → Pages，勾选 **Enforce HTTPS**。证书由 GitHub 自动签发（Let's Encrypt）；刚配好时可能显示"暂不可用"，等几分钟到一小时再试。

### 6.4 不需要 `CNAME` 文件
GitHub 文档明确：**用自定义 Actions 工作流发布时，不会创建 `CNAME` 文件，已有的 `CNAME` 文件会被忽略、也不需要**。自定义域名存在 Pages 设置里。所以本模板**不生成** `CNAME`，也不要手工往 `site/` 里塞。

### 6.5 多课程仓的域名规划
- 方案 A（推荐）：**每个课程仓一个子域**，如 `mit-65840.example.com`、`cs144.example.com`。理由：课程仓独立部署、独立授权、可单独下线，子域天然隔离，DNS 各自一条 `CNAME`。
- 方案 B（不推荐现在做）：主站用路径聚合（`example.com/mit-65840/`）。这需要主站反向代理或聚合构建，和"课程仓独立可下线"的架构目标相冲突。

---

## 7. 授权闸门如何在部署上生效

闸门不是文档里的君子协定，而是 CI 里的依赖链。`template/.github/workflows/deploy.yml` 是三个 job 串联：

```
validate  ──(needs)──>  build  ──(needs)──>  deploy
   │                       │                    │
validate.py            build.py             deploy-pages
退出非 0 → job 失败 → 后面的 job 在 GitHub 上根本不会被执行 → 站点不更新
```

具体失败场景：某位贡献者为一节课提交了逐字稿翻译，`content/03-xxx/index.md` 里写了 `output_mode = "transcript"`，而 `course.toml` 仍是 `license.verified = false`。`validate.py` 命中 spec §6 检查项 2（授权闸门）→ 退出码 `1` → `validate` job 失败 → `build` 与 `deploy` 被 `needs` 挡住 → **线上站点保持上一版不变**。同一份检查也会在 `validate.yml` 里对每个 PR 跑一次，红叉出现在合并之前。

补充建议（人工设置，无法写进 YAML）：给 `main` 加分支保护，要求 `Validate` 的检查通过才能合并，把闸门提前到合并前而不是 push 后。

---

## 8. 何时该改用另一个方案

**改用 GitBook（作为主站）的条件**——建议以下几条**同时**成立时再迁移：
1. 主要矛盾从"授权与内容自主"变成"大量非技术贡献者要直接编辑"；
2. 接受内容真相源搬到 GitBook、仓库降级为同步目标；
3. 授权问题已经解决（各课程许可核实完毕、或产出形态稳定在法律安全区），"硬失败闸门"不再是刚需；
4. 能承担 **$65/站点/月**起的成本，且愿意按站点数（≈课程数）线性付费。

**改用 MkDocs Material / VitePress（仍部署在 Pages）的条件**：
1. 内容的 Markdown 需求超出 spec §7 定义的子集（例如需要数学公式、Mermaid、自动 API 文档、版本化文档）；
2. 并且愿意放弃 spec §0 的零依赖约束——能接受在 CI 里 `pip install`/`npm install`（runner 网络正常，这一步本身没问题），代价是本机在代理不稳时无法复现构建、以及依赖升级维护。
   → 由于内容与渲染器已解耦，这个迁移**只需要换构建步骤**，内容一行不改。这正是当初坚持零依赖 + 纯 Markdown 的回报。

**保留 Pages、另加 Cloudflare Pages 镜像的条件**：大陆读者反馈 `github.io` 打不开或太慢时。产物同为 `site/`，是"加一个发布目标"，不是"换方案"；绑定自有域名后同样免费。

**不推荐的路径**：把内容搬进 GitBook 后又在 Pages 上保留一份——两份真相源必然漂移，术语一致性和授权闸门都会失控。

---

## 9. 未能核实的事项（不要当成已验证）

1. **GitBook 双向同步下的发布控制**：官方文档只说双向同步是自动的，没有说明 GitBook 侧编辑发布时是否会经过仓库的分支保护/CI。因此"GitBook 无法阻断违反授权闸门的内容上线"是**基于文档缺失的推断**，不是实测结论。要推翻它，需要一次真实的 Git Sync 试用（14 天试用可做）。
2. **GitBook 对内联原始 HTML/SVG 的支持**：我们只核实到它把内容组织成结构化 block、支持上传 `.svg` 图片文件、有 Mermaid 与 Drawing block；没有找到"支持原始 HTML/内联 SVG"的文档，也没有实测。结论"内联 SVG 会退化成图片"有依据但未经实测。
3. **中国大陆的可达性**：本机处于 Clash fake-IP 代理环境，无法做可信的对照测速。`github.io` 的稳定性会随时间和运营商变化，需要真实读者反馈。
4. **GitBook Free 版"自定义 block"的边界**：定价页把 custom blocks 列在 Free 套餐，但自定义 block 通常与集成/企业能力相关，未实测其限制。
5. **GitHub Pages 相关配额**（站点 ≤1 GB、软带宽 100 GB/月、Actions 构建不受 10 次/小时限制、部署 10 分钟超时）来自官方 limits 文档，数值未实测。

---

## 附：本次核实过的外部来源

- GitHub Pages 用量限制：<https://github.com/github/docs/blob/main/content/pages/getting-started-with-github-pages/github-pages-limits.md>
- GitHub Pages 自定义域名（DNS 记录、Actions 发布无需 CNAME）：<https://github.com/github/docs/blob/main/content/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site.md>
- GitBook 定价：<https://www.gitbook.com/pricing>
- GitBook Git Sync（双向同步）：<https://docs.gitbook.com/getting-started/git-sync>
- GitBook 自定义域名文档：<https://gitbook.com/docs/publish/custom-domain>
- `actions/configure-pages`：<https://github.com/actions/configure-pages>（最新主版本 v6）
- `actions/upload-pages-artifact`：<https://github.com/actions/upload-pages-artifact>（最新主版本 v5）
- `actions/deploy-pages`：<https://github.com/actions/deploy-pages>（最新主版本 v5）
