---
name: course-validate-publish
description: Run the CourseLingo validation and build pipeline — execute validate.py, interpret exit codes and fix each error class, run build.py, verify the rendered site locally, then publish. Use before every commit or pull request, when validate.py fails, or when building and deploying the static site.
---

# course-validate-publish · 校验、构建与发布

**命令只有两个**（spec §6 / §7 是冻结契约）：

```bash
python scripts/validate.py
python scripts/build.py --out site
```

**不要使用 spec 未定义的参数。** `build.py` 只定义了 `--out`（默认 `site`）与 `--base-url`（默认 `/`）。

> ⚠️ **实现与 spec 的分歧**：当前 `template/scripts/` 的实现**另有** `--root`（`validate.py` / `build.py`）、`--quiet`（`validate.py`），且 `build.py` 的 `--base-url` 默认是 `"./"` 而非 spec §7 写的 `"/"`。
> 这些**都不在冻结契约里** —— 本 skill 只使用 spec 定义的用法；发现分歧请回报给脚本维护者（`docs/SOP.md` §14-11）。
`new_course.py` / `new_lecture.py` 的 CLI 在 spec 中未定义 —— 不要臆造参数（见 `docs/SOP.md` §14-1）。

零依赖：Python 3.11+ 标准库即可（`tomllib` 内置），**不需要** `npm install` / `pip install`。

---

## 第一部分 · 校验

### 1.1 跑

```bash
# 在课程仓库根目录
python scripts/validate.py
```

### 1.2 读退出码（spec §6）

| 退出码 | 含义 | 你的动作 |
| --- | --- | --- |
| `0` | 通过（**可能仍有 WARN**） | 读完 WARN 再往下走，**不要直接忽略** |
| `1` | **有 ERROR** | **不得进入复核 / 发布**。按 1.3 逐条修复后重跑 |
| `2` | 用法 / IO 错误 | 检查：是否在课程仓库根目录、`course.toml` / `glossary.toml` / `content/` 是否齐全，脚本路径是否正确 |

CI 行为（spec §8）：`validate.yml` 在 push / PR 时跑，有 ERROR 即失败。

### 1.3 ERROR 修复映射表（spec §6 的 6 类）

| # | ERROR | 根因 | 修法 |
| --- | --- | --- | --- |
| 1 | `course.toml` 不可解析，或缺 `[course]` 必填字段 | 缺 `id` / `title` / `title_zh`；TOML 引号或段落写错 | 补齐 `id` / `title` / `title_zh`；检查 TOML 语法（`[course]` 段名、`= "…"` 引号、不要中文引号）。注意**当前实现还要求** `institution` / `source_language` / `target_language` 非空（spec §2 只标 3 个必填，见 `docs/SOP.md` §14-11） |
| 2 | 存在 `output_mode = "transcript"` 的讲座，而 `license.verified != true` | 有人在未授权时做了逐字稿 | **默认改回 `"explanation"`**。只有拿到**该材料类型**的书面授权、并把 `[license]` 证据补齐（`terms` / `evidence_url` / `checked_at` / `allows_derivatives`）后，才允许把 `verified` 改成 `true`。**绝对不要为了过校验而改 `verified`** |
| 3 | front matter 必填字段缺 / `lecture` 或 `slug` 重复 / `source_url` 为空 | 手搓骨架、并行写多讲时编号撞车 | 补字段；`lecture` 重新编号（保持全课程唯一）；`slug` 改唯一；`source_url` 填**官方**地址。预防：开工前一人先分配编号表 |
| 4 | `[[term:key]]` 的 key 不在 `glossary.toml` | 拼写错误；**多词术语漏了连字符**（写成 `[[term:leader election]]`）；或用了未登记的新术语 | 拼错 → 改正；多词 → 按 key 派生规则连字符化（`leader election` → `leader-election`，见 `docs/SOP.md` §14-10）；确实是新术语 → **回 `course-init` 走评审加词**，不要就地写中文替代词 |
| 5 | `glossary.toml` 中 `en` / `zh` 为空，或 `en` 重复 | 漏填；同一概念建了两个 key | 补空值；`en` 重复（**大小写不敏感**）→ 合并为一个条目，其余写进 `aliases` |
| 6 | 正文有「几乎全为 ASCII 且长度 > 400 字符」的连续段落 | 整段照抄原文 | **删掉，重写成中文讲解**（精确判定口径见下） |

**ERROR 6 的实际判定口径**（当前实现，spec §6.6 未写细节）：段落须同时满足 `长度 > 400 字符` 且 `ASCII 占比 ≥ 90%` 且 `空格数 ≥ 40`；
判定前会**剥离行内代码、链接与 Markdown 标记**，并**跳过围栏代码块、标题行与表格行**。
→ **成段的英文散文**（照抄原文的特征）会被拦下；代码块不会；长 URL 不会。所以「单块代码 ≤ 400 字符」是**可读性要求，不是校验要求**（见 `docs/SOP.md` §14-6）。

**另有一条 ERROR 不在 spec §6 的清单里**：`content/` 下**没有任何讲座**时，当前实现会报 ERROR。
所以在**新建的空课程仓库**上跑校验会 exit 1 —— 那是预期的，不是配置错误。建好第一讲骨架后应当 exit 0（见 `docs/SOP.md` §14-12）。

### 1.4 WARN 的处理（两类，都要看）

| # | WARN | 为什么必须处理 |
| --- | --- | --- |
| 7 | glossary 的 `en` 原词出现在正文但未打 `[[term:]]` 标记 | **两种可能，都是真缺陷**：① 漏标术语 → 补 `[[term:key]]`；② 术语漂移（用了中文替代词）→ 改回 `glossary.toml` 的 `zh`。**WARN 7 不允许「忽略」** |
| 8 | `status = "draft"` 的讲座在 `build` 时会被标注「草稿」 | 发布前把状态推到 `reviewed` / `approved`；不要在线上留草稿标记 |

### 1.5 校验通过后

- [ ] `python scripts/validate.py` **exit 0**
- [ ] WARN 7 已归零，或每条都有明确理由
- [ ] 送复核的稿子已经过 `course-explain` 的自检清单

---

## 第二部分 · 构建与本地验证

### 2.1 构建

```bash
python scripts/build.py --out site
```

部署到 GitHub Pages 项目子路径时：

```bash
python scripts/build.py --out site --base-url /<repo>/
```

### 2.2 产物（spec §7）

```
site/index.html            课程首页 + 讲座目录
site/<slug>/index.html     每篇讲座
site/glossary/index.html   术语表
site/assets/style.css
```

`site/` 是构建产物，**不入库**（检查 `.gitignore`）。

### 2.3 本地目视验收（必须真的打开看，不要只看 Markdown）

- [ ] 打开 `site/index.html`：讲座目录顺序正确；`status = "draft"` 的讲座已标注「草稿」
- [ ] 打开 `site/<slug>/index.html`：**侧边栏导航**、**面包屑**、`<meta name="description">` 都在
- [ ] 打开 `site/glossary/index.html`：术语表完整
- [ ] **术语渲染**：**首次**出现显示「中文（English）」，**后续**只显示中文
- [ ] Markdown 渲染正确：标题 / 段落 / 围栏代码块（含语言类名与 HTML 转义）/ 列表 / 表格 / 引用 / 分割线 / 链接 / 图片 / 行内 `code`、**粗体**、*斜体*
- [ ] 明暗色都看一遍；中文行高与字距可读（`lang="zh-CN"`）
- [ ] 页脚有**署名**与「**非官方 · 社区项目**」声明
- [ ] **站点里没有任何英文原文段落、课件、视频、作业答案**
- [ ] 无任何学校校徽 / 课程 Logo / 官方背书暗示（brand.md 禁止事项）

### 2.4 常见构建期问题

| 症状 | 原因 | 处理 |
| --- | --- | --- |
| 图片 404 | 路径写成了绝对路径，或图不在 `content/<NN>-<slug>/figures/` | 用相对路径 `figures/xxx.svg`；确认文件存在 |
| 站内链接 404 | 部署到子路径但没传 `--base-url` | 加 `--base-url /<repo>/` 重新构建 |
| 术语没渲染成 `<abbr>` | 标记语法写错（漏了 `[[ ]]` 或冒号） | 必须是 `[[term:<en-key>]]`，key 与 glossary 的 `en` 完全一致 |
| 代码块格式错乱 | 围栏没闭合，或语言类名写错 | 检查成对的 ``` 与语言标识 |
| 表格不渲染 | 缺少分隔行或首尾 `|` | 用标准 Markdown 表格并前后留空行 |
| 页面出现整段英文 | 误把原文粘进 `index.md` | 删掉重写；`validate.py` 的 ERROR 6 本该拦住它 |

---

## 第三部分 · 发布

### 3.1 发布前闸门（人工，全部必过）

- [ ] 目标讲座 `status = "approved"`（`draft` / `reviewed` 不发）
- [ ] 术语与授权相关的改动已由**两名维护者**确认（CONTRIBUTING §3）
- [ ] 2.3 目视验收全过
- [ ] `site/` 未被提交
- [ ] 提交信息用祈使句 + 范围前缀（CONTRIBUTING §4）：
  ```
  6.824: 讲解 Lecture 3 主从复制
  glossary: 统一 raft 相关术语
  docs: 补充课程授权说明
  ```

### 3.2 分支与 PR（CONTRIBUTING §3）

```bash
git checkout -b translate/<course>-<lecture>   # 或 fix/<topic>
```

PR 描述必须写明：
1. **对应课程与讲座**
2. **授权依据**（`[license]` 的 `terms` / `evidence_url`，或明确写「未核实，产出为讲解」）
3. **术语表变更**（有就列，没有就写「无」）

### 3.3 CI 与部署（spec §8）

| 工作流 | 触发 | 行为 |
| --- | --- | --- |
| `validate.yml` | push / PR | 跑 `validate.py`，有 ERROR 即失败 |
| `deploy.yml` | push to `main` | `validate.py` → `build.py` → 部署 `site/` 到 GitHub Pages |

CI 环境是 `ubuntu-latest` + `actions/setup-python@v5`（3.12），**不需要 npm**。

### 3.4 发布后

- [ ] 线上首页与至少一篇讲座页可正常打开
- [ ] 线上「非官方 · 社区项目」声明可见
- [ ] 术语在线上渲染正确（首现「中文（English）」）

### 3.5 下线机制（content-policy，优先于一切讨论）

任何内容一旦被指出**超出授权范围**：

1. **立即下线** —— 不回退讨论、不等核实结论。
2. 在对应仓库开 issue 记录决策。
3. 复盘该课程的授权判断是否有系统性偏差。

> 宁可错杀，不可拖延。

---

## 失败时不要做的事

- ❌ 为了过校验把 `[license].verified` 改成 `true`（这是伪造授权证据，红线）
- ❌ 为了让 `transcript` 通过而删掉闸门检查或改脚本（`scripts/` 是冻结契约的消费方）
- ❌ 把 ERROR 当成 WARN 忽略，或直接跳过校验去发布
- ❌ 使用 spec 未定义的脚本参数
- ❌ 把 `site/` 提交进版本库
- ❌ 发布 `status != "approved"` 的讲座
- ❌ 用「再打磨一下」这类不可执行的评语驳回（复核意见要落到行号 + 具体修改）
