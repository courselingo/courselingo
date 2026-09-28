# 授权核实记录 · Licensing Research Log

> 本文件记录**实际发起过的核实动作与结果**，不是许可条款本身。
> 结论：**尚未核实任何一门课程。** 下表每一行都是 `未核实`，且没有任何数据来自记忆或推测。

## 状态：BLOCKED（工具层面受阻，非疏忽）

| 检查项 | 结果 |
| --- | --- |
| `web_search` | 全部失败：`no API key for "DEEPSEEK_API_KEY"` —— 未配置搜索后端 |
| `web_fetch` | 拒绝所有目标：`resolves to a non-public IP address` |
| DNS 解析 | 学术域名被劫持到 `198.18.0.x`（RFC 2544 保留段）：`ocw.mit.edu`→.7、`cs61a.org`→.5、`pdos.csail.mit.edu`→.4、`composingprograms.com`→.8、`cs144.github.io`→.14、`15445.courses.cs.cmu.edu`→.15 |
| 直连出口 | `curl https://ocw.mit.edu/` → `http_code=000`（无法建立连接） |
| 镜像 / 代理 | `web.archive.org`、`archive.org`、`api.github.com`、`raw.githubusercontent.com`、Bing/DDG/Brave/Google、`r.jina.ai`、`corsproxy.io` —— **全部**被劫持。无 `HTTP(S)_PROXY` 环境变量，无可用本地代理端口 |

**实际成功抓取的 URL 仅 3 个**：[github.com](https://github.com/)（200）、[github.com/cs61a](https://github.com/cs61a)（200）、[github.com/cs61a/composing-programs](https://github.com/cs61a/composing-programs)（404）。三者均**不含**任何课程许可文本。证据基础为空。

## 核实表（全部未核实）

| 课程 | 材料类型 | 许可条款 | 来源 URL | 可信度 |
| --- | --- | --- | --- | --- |
| MIT 6.5840/6.824 | 讲座笔记 / 幻灯片 | 未取得 | <https://pdos.csail.mit.edu/6.824/> —— 不可达 | **未核实** |
| MIT 6.5840/6.824 | 讲座视频 | 未取得 | 同上 | **未核实** |
| MIT 6.5840/6.824 | 作业 / Lab | 未取得 | 同上 | **未核实** |
| MIT 6.5840/6.824 | 课程 reuse 声明 | 未取得 | 同上 | **未核实** |
| Berkeley CS 61A | 幻灯片 / 视频 / 作业 / 项目 | 未取得 | <https://cs61a.org/> —— 不可达 | **未核实** |
| Composing Programs | 教材 | 未取得 | <https://composingprograms.com/> —— 不可达 | **未核实** |
| MIT OpenCourseWare | 站点许可、商用、衍生、ShareAlike、署名 | 未取得 | <https://ocw.mit.edu/> —— 不可达 | **未核实** |
| MIT 6.1810/6.S081 | reuse 声明 | 未取得 | 不可达 | **未核实** |
| CMU 15-445 | reuse 声明 | 未取得 | 不可达 | **未核实** |
| Stanford CS 144 | reuse 声明 | 未取得 | 不可达 | **未核实** |

### 为什么留空而不是「按常识填」

两个具体陷阱：

1. **MIT OCW 的许可条款极易被记错。** 其 `NC`（非商业）与 `SA`（相同方式共享）条款直接决定商业使用与翻译改编是否合法 —— 这是两个根本性问题，必须读原文。
2. **6.824 / 6.1810 的讲座笔记历史上没有声明许可。** 「未声明」的法律状态是**保留所有权利**，与「宽松开源」是完全不同的法律处境。课件公开可访问 ≠ 可以自由改编。

## 附带结论：一般著作权推理（非已核实条款）

> 以下仅为风险分级框架，可被真实条款推翻。

- **自己撰写讲解、讲同一批概念 —— 风险最低。** 思想与概念不受著作权保护，只有表达受保护。但须避免逐句改写原文、避免复制原图与幻灯片。
- **链接官方来源 + 自己的解读与署名 —— 模式安全。** 但署名本身**不能**豁免侵权。
- **翻译完整逐字稿 / 翻译视频字幕 —— 许可依赖度最高。** 翻译是衍生作品，复制了原作的完整表达，完全取决于实际条款（NC/ND 条款，或根本无许可）。
- **翻译官方作业答案 —— 风险最高。** 著作权风险叠加学术诚信规则，且答案常被故意不公开，应默认无授权。
- **转载原始课件 / 视频 —— 最高风险且通常没有必要。** 即使材料许可宽松，视频还另有平台条款。一律链接，不转载。

## 解除阻塞后的重跑清单

网络恢复后，**逐一实际访问**并逐字记录原文引用：

1. `pdos.csail.mit.edu/6.824/` 主页及其 reuse 声明
2. `github.com/mit-pdos` 下各 Lab 仓库的 `LICENSE` / `COPYING`
3. `cs61a.org` 主页与 FAQ / about 页
4. `composingprograms.com` 页脚许可声明
5. MIT OCW 的 terms of use 与 citation 页面
6. 6.1810、15-445、CS 144 主页的 reuse 声明

在此之前，**所有课程按「未核实」处理**；任何翻译逐字稿、字幕或作业答案的发布，都必须先取得书面授权（联系课程讲师或相应版权办公室）。
