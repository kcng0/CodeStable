---
name: cs-keep
description: 管理有证据的项目事实、lesson 生命周期与 canonical 归宿。触发：记录踩坑、教训、调研结论、纠偏，或用户说"记住这个"。
argument-hint: "[要沉淀的内容]"
---

# cs-keep

把这次学到的东西沉淀成下次能被检索到的项目记忆。落点由你判断，不追问用户分类。

## 开工与授权

- 先读 `AGENTS.md` 的 `## 项目事实`（已随会话加载则不重复读）；写前检索 `docs/notes/` 与 v1 只读
  `.codestable/compound/`，核实证据、scope、重复项与已有 canonical owner。
- 用户明确要求“记住 / 更新 / 退役”、接受普通 owning task 给出的晶化候选，或在 Epic 最终毕业
  gate 批准候选，就是本次精确内容的写入授权，不追问分类。新建、改写规则/scope、晋升、删除或
  跨项目分享仍需用户显式授权，不能从历史操作或“这可能有用”推断。
- 没有可追溯证据不写；不编造，不从模型记忆、命中次数或自评置信度泛化。

## 落点判断

按单一 owner 和以下顺序路由：

1. **机械 guard 优先**：能由测试、checker、lint、类型或 deterministic helper 阻止的重复错误，
   在 owning task 已有实现授权且不扩大 scope 时直接机械化，不另写重复 lesson；否则只建议进入
   对应 owning task，不把记忆写入授权扩成代码修改授权。
2. **高频必读事实进入 `AGENTS.md` 的 `## 项目事实`**：该段保持 ≤25 条，只改本段、不动 `AGENTS.md` 其他
   内容，保留存量分节；超限先合并再新增。
3. **结构性决定进入 ADR**：必须同时满足难回退、缺少上下文会令人意外、源于真实取舍；沿用项目
   惯例位置，不用 lesson 复制决定。
4. **其他稳定方法进入项目既有文档**（含当前真相）；位置以 `docs/README.md` 文档契约登记为准，
   目标不存在时请 owner 选择，不发明目录。
5. 其余尚未被更强 owner 承接的可复用经验，进入
   `docs/notes/YYYY-MM-DD-{slug}.md`，作为可纠偏、可删除的 staging。

## 当前真相与决策

- 写入 spec 等当前真相文档时只写合并后仍成立的结论；讨论过程、尝试与进度不进项目文档。
- 文档与代码或用户说法冲突时按 `owner 最新确认 > 当前代码与测试证据 > 可能过期的文档` 判断；先报告
  冲突与依据，不静默用代码覆盖文档中记录的取舍。
- Vision 等目标内容只在 owner 确认后修改；实现结论会改变目标时只给候选。
- 新建或取代 ADR 时写明被否决的方案；取代时新建条目并把旧条标为 `Superseded`，不改写旧条正文。
  项目有 ADR 或 spec 索引时同一更新内同步索引。

`## 项目事实` 段或 `docs/notes/` 不存在时可按需创建，不要求先跑 cs-onboard。临时状态、
本周计划或 git 已完整表达的事实不沉淀。`codestable-eval` 只标记未来上游候选；本轮不导出、不上传、
不改 skill，也不恢复 `cs-feedback`。

## lesson 格式

一条一文件，slug 用小写连字符、≤30 字符：

```markdown
---
status: observed
scope: 模块 / 命令 / 场景关键词
date: YYYY-MM-DD
---
规则：未来可执行的结论。
适用 / 不适用：边界与停止应用信号。
证据：最多三个代表性路径、测试、diff 或任务指针。
候选归宿：test | checker | project-facts | project-doc | adr | codestable-eval
```

## 生命周期

| status | 判据 |
|---|---|
| `observed` | 单次任务已有证据，尚未在独立后续任务验证 |
| `validated` | 非创建该 lesson 的任务和 agent invocation 中有效命中，真实改善行为并验证成功；具体表现为改变计划或验证，或明确排除一个具体且合理的错误路径 |
| `retired` | 被仓库事实反证、scope 完全失效或已有更强 canonical owner；不得应用且不再复活原结论 |

- 新 lesson 一律从 `observed` 开始；不能把创建该 lesson 的同一任务自证为 validated，也不因命中
  次数或模型自评晋级。
- 旧 lesson 缺 `status` 按 `observed` 读取，不批量迁移；只在真实状态变化或本来就要更新时补字段。
- `observed -> validated` 只在独立后续任务确实采用并验证成功时发生，并只补一次代表性证据；必须记录 lesson 实际改变的计划或验证，或明确排除的具体且合理错误路径，以及本次通过的验收证据。
- `observed|validated -> retired` 只写反证/替代原因与指针。retired 条目上的新结论必须另建 observed
  lesson，不继承旧条目的 validated 身份。
- 稳定 validated 命中不产生文件 churn。不得保存原始对话、逐次命中日志或无限 evidence history。

## task skill 的候选门槛

owning task skill 在任务中静默收集候选时按以下门槛；本节是这些规则的唯一 owner。

强信号只包括：owner
纠正实际改变方案/代码/术语/验证；可复现证据推翻根因；同一路径失败两次后更换假设；
blocking/important finding 暴露未编码不变量；新 red -> green 捕获可复发失败；lesson 真实改变本次行为
或被反证；重复 workaround；方法显著降低重试、成本或风险。

候选还必须同时有可追溯证据、能写成未来动作、适用于本次精确 diff 之外、且没有现成 canonical
owner。网络波动、拼写、泛化口号、活动记录，以及已被机械 owner 完整覆盖的事实直接丢弃。

创建、改写规则/scope、晋升、删除与跨项目反馈仍须用户显式授权。为不中断 read-repair，仅对已有且
有效命中的 lesson 开放两种窄维护：`observed -> validated` 仅在独立后续任务确实采用并验证成功时
发生，只补一次代表性证据；必须记录 lesson 实际改变的计划或验证，或明确排除的具体且合理错误路径，
以及本次通过的验收证据。`observed|validated -> retired` 仅在当前仓库事实直接反证或发现已有
canonical owner 时发生，只写原因与替代/反证指针。窄维护不新建事实、不改规则、不扩 scope、不新增
gate，随当次代码、证据和
游标进入同一语义原子 milestone；稳定 validated 命中不写文件。需要改写结论或证据不足时只给
候选，新结论不得通过复活 retired 条目获得 validated 身份；窄维护必须在最终报告列出文件变化。

## 写入纪律（硬门槛）

- 命中同域 lesson 时查重、合并到原条目，不新增重复；继续维持约 50 条预算，达到预算先整理、
  晋升、合并或删除，不简单扩容。
- `.codestable/compound/` 是只读历史知识源：命中且结论完整时只引用来源、不新建；有增量时只合并进现有 lesson 或新建 lesson，并引用旧 compound 来源，绝不更新 compound。
- 晋升前先验证新 owner 已写入且能承接完整事实，再在同一更新中删除重复 lesson；若 task skill
  只发现已有 owner，则先标 retired，删除留待显式 `cs-keep` 整理。
- 一次只写用户拍板过的内容，不顺手多写。

## 检索约定

日后找回：`grep -ri "关键词" docs/notes/ .codestable/compound/`。应用前以当前代码、测试或
canonical 文档核实；`retired` 不应用，`compound/` 命中仍按只读规则处理。

## 完成

报告写入、更新或删除的文件路径与一句话摘要即可，不设写后确认。
