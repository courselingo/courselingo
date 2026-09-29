# 四门新课 · 上线清单（截至第 14 轮）

> 目标：「至少全量翻译完 4 门课程。」判定标准是「**课程内容已上线且通过闸门**」。
> 本文件记录**已上线**的页面与它们的闸门证据。

## 已 reviewed 且线上可达（4 讲 · 4 门课各 1 讲）

| 课程 | 讲次 | 线上 URL | 字节 | 三道人工闸门 |
| --- | --- | --- | --- | --- |
| **mlsys-15442** | 01 `why-ml-systems` | <https://courselingo.github.io/mlsys-15442/lectures/why-ml-systems.html> | 41,929 | 事实核对 0/0/0 ✅ ｜ 视觉复核 11/11 可用 ✅ ｜ 透镜 3 ✅ 7/1/0 |
| **eth-ca** | 01 `lecture1-intro` | <https://courselingo.github.io/eth-ca/lectures/lecture1-intro.html> | 42,670 | 事实核对 0/3/3 已清 ✅ ｜ 视觉复核 11/11 可用 ✅ ｜ 透镜 3 ✅ 5/3/0 |
| **cs168** | 01 `internet-architecture-and-protocols` | <https://courselingo.github.io/cs168/lectures/internet-architecture-and-protocols.html> | 42,072 | （上一轮目标完成时已提级） |
| **mit-6.006** | 01 `algorithmic-thinking-peak-finding` | <https://courselingo.github.io/mit-6.006/lectures/algorithmic-thinking-peak-finding.html> | 45,016 | （上一轮目标完成时已提级） |

**⇒ 四门课各有一讲在线上，且四讲都过五道机检 + 各自的人工闸门。**

## 产出总览

| 课程 | 全量 | 已产出 | 已 reviewed | 自绘配图 |
| --- | --- | --- | --- | --- |
| cs168 | 52 | 5 | 1 | 46 |
| mit-6.006 | 24 | 2 | 1 | 15 |
| eth-ca | 31 | 8 | **1 ✅** | 78 |
| mlsys-15442 | 21 | 13 | **1 ✅** | 163 |
| **合计** | **128** | **28（22%）** | **4** | **302** |

## 提级路径（本会话跑通两条，可复用）

```
作者产出（status = draft）
  ↓ 五道机检：validate / check_style / audit_content --strict /
              check_figures --strict / build_site
  ↓ 三道人工闸门：
      ① 非作者事实核对   → docs/audit/<slug>-factcheck.md      （P0/P1 清零）
      ② 配图视觉复核     → docs/audit/visual-review/           （全部「可用」）
      ③ 透镜 3（陌生读者）→ 写进 docs/audit/lecture-NN-quality-audit.md 的 §5.5
  ↓ docs/audit/lecture-NN-quality-audit.md                  （§9 要求的「有审核记录」）
  ↓ check_reviewed.py --root .                              （读上面三样，全齐才过）
  ↓ Lead 改 status = "reviewed" + 建站 + push
  ↓ CI：Validate ✅ + Deploy to GitHub Pages ✅
  ↓ 实测线上 URL 返回内容
```

**★ 而 `check_reviewed.py` 要的两道人工闸门是**透镜 3 + 配图视觉复核**；
「非作者事实核对」是 Lead 另加的第三道**（它抓到了本会话全部内容级错误里的多数，但**不是**闸门要求）。
