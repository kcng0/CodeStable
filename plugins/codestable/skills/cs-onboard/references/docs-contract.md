# 文档契约

本文件是 `docs/README.md` 的模板。`cs-onboard` 在项目没有文档契约时写入；`docs/` 已有内容时先按项目
实际位置调整路径并经 owner 确认。不预置业务内容。

---

# 文档契约

`docs/` 是团队共享的项目知识。人和 agent 按同一套约定读写；agent 工作流只是写入者之一，不使用它的人
也能照本文维护。下表就是各类文档的位置登记：路径变化时改这里，agent 按本表写入。

## 各类文档回答什么

| 位置 | 回答 | 何时更新 | 确认者 |
|---|---|---|---|
| `docs/vision.md` | 产品要成为什么；候选或互斥方向 | 方向变化时 | owner |
| `docs/spec/`（入口 `index.md`） | 系统现在怎样工作：按能力或场景组织的当前真相 | 改变已有行为的 PR 内 | PR reviewer |
| `docs/adr/`（入口 `index.md`） | 难逆转的决定及其被否决的方案 | 做出难逆转决定时；只追加或取代 | owner |
| `docs/epics/{slug}.md` | 一段有边界的大变化：目标、范围、子项、验收 | Epic 生命周期内 | owner |
| `GLOSSARY.md` | 团队术语、定义与排除含义 | 出现新术语或歧义时 | PR reviewer |
| `AGENTS.md` 的 `## 项目事实` | 每次会话必读的高频事实（≤25 条） | 事实变化时 | PR reviewer |
| `docs/notes/` | 尚待验证的经验（staging，可纠偏、可删除） | agent 提出、人确认后 | PR reviewer |
| `.codestable/work/` | 进行中任务的临时游标，不是文档 | 任务完成即删 | — |

## 规则

1. **文档与代码同 PR。** 改变外部可观察行为的 PR 同时更新 `docs/spec/`；还没有覆盖该行为的 spec 时只为
   本次改动的行为新建一篇，spec 随开发逐步长出。PR 描述写一行 `Spec impact: none | updated | drift`：
   `none` 表示未改变外部可观察行为，`updated` 表示 spec 已在同一 PR 更新或新建，`drift` 表示发现文档与
   代码不一致但不在本 PR 范围，需列出路径。测试、README 与 agent 用的 verify 说明不算 spec。
2. **只写仍成立的结论。** 讨论过程、尝试记录和进度留在 PR 或 issue，不进 `docs/`。
3. **冲突优先级：** owner 最新确认 > 当前代码与测试证据 > 可能过期的文档。发现不一致先报告，不静默用
   代码覆盖文档里记录的取舍。
4. **ADR 门槛：** 难回退、缺少上下文会令人意外、源于真实取舍，三者同时满足才写；必须列出被否决的方案。
   取代旧决定时新建一条，并把旧条状态改为 `Superseded`，不改写旧条正文。
5. **索引先行：** `docs/spec/index.md` 与 `docs/adr/index.md` 一行一条（路径 + 一句话）。读者和 agent
   先读索引，命中才打开全文；新增或取代条目时同步更新索引。
6. **按需创建：** 目录和索引在第一次写入时创建，不预建空目录。
7. **命名：** 新文件用 `YYYY-MM-DD-{slug}.md` 或语义化 slug，不使用递增编号，避免并行分支撞号。

## PR 审阅顺序

1. PR 描述中的 `Spec impact` 与相关 ADR；
2. `docs/` 的变化：「完成」是否定义正确；
3. 代码 diff：是否恰好交付上面的定义。

## ADR 格式

```markdown
---
status: Proposed | Accepted | Superseded | Deprecated
date: YYYY-MM-DD
superseded-by: docs/adr/{file}.md   # 仅在 Superseded 时填写
---

# {决定标题}

## 背景
## 决定
## 被否决的方案
## 后果
```
