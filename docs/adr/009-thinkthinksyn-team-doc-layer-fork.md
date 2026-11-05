---
adr: "009"
title: "ThinkThinkSyn fork：owner 同意后的团队文档层与收敛的学习契约"
status: Accepted
date: 2026-11-05
applies-to:
  - "plugins/codestable/skills/cs/"
  - "plugins/codestable/skills/cs-onboard/"
  - "plugins/codestable/skills/cs-keep/"
  - "plugins/codestable/skills/cs-feat/"
  - "plugins/codestable/skills/cs-issue/"
  - "plugins/codestable/skills/cs-refactor/"
  - "plugins/codestable/skills/cs-epic/"
  - "plugins/codestable/skills/cs-code-review/"
enforcement: test
stage: [onboard, deliver, keep]
lint: "python3 -m pytest tests/test_skill_contracts.py tests/test_v2_documentation_contract.py"
---

# ADR-009: ThinkThinkSyn fork：owner 同意后的团队文档层与收敛的学习契约

## Context

本 fork 基于上游 `codestable/CodeStable` `19c796de`（2026-08-18，2.0.2 之后）。目标是多人协作、以文档
与长期维护为重点：团队需要一套不依赖 agent 工具也能维护的文档约定，流程层则随模型能力继续变薄。

上游 v2 流程薄、普通任务零产物，但不规定团队文档结构；CodeStable-Lite 的知识分层（Vision / 当前真相
spec / ADR / 术语）和「只回写仍成立结论」更适合团队，但流程偏重（强制 `ff`、递增编号、`o|x` 命名、
开工全量扫描）。四个 task skill 还各自复制了同一套强信号与 lesson 窄维护细则。

## Decision

### 两层分离

- **文档层**属于目标项目、由团队拥有：`docs/README.md` 文档契约规定 Vision、spec、ADR、永久 Epic、术语
  各回答什么、何时更新、谁确认，以及 PR 内 `Spec impact: none | updated | drift`。模板在
  `cs-onboard/references/docs-contract.md`。
- **流程层**是本 fork 的 skill，可替换。skill 不硬编码 `docs/` 路径，只按 `attention.md` 的
  `## 文档归宿` 登记写入；未登记时沿用上游「请 owner 选择」的行为。

### 接入与调用

- 团队文档层不进基础骨架。`cs-onboard` 先问 owner；同意后在缺少 `docs/README.md` 时写入模板、登记
  文档归宿，目录在第一次写入时创建，已有文档不覆盖。
- `cs-onboard` 与纯转发的 `cs-code-review` 设 `disable-model-invocation: true`，只由用户调用；`cs` 路由
  到接入时提示运行 `/cs-onboard`。

### 当前真相与学习

- `cs-keep` 增加：只写仍成立的结论；冲突优先级 owner 最新确认 > 当前代码与测试证据 > 可能过期的文档；
  Vision 只在 owner 确认后改；ADR 必列被否决方案，取代时新建并把旧条标 `Superseded`；同步索引。
- 强信号、候选门槛与 lesson 窄维护细则只留在 `cs-keep` 的「task skill 的候选门槛」。四个 task skill
  保留读取修复、3 条内存候选上限、授权门槛和按名称指向 `cs-keep` 的一段话，不跨目录引用文件。

### 交付

- `cs-feat` / `cs-issue` 走真实入口验证时优先用项目内 verification skill 或 attention 记录的驱动方式；
  没有时建议用 `create-verification-skill` 生成。
- feat / issue 收尾在改变已有行为时附 `Spec impact`；refactor 只在发现文档漂移时附 `drift`；`cs-epic`
  收尾在登记了 Vision 时只提出 Vision 候选。

## Rejected Alternatives

- **以 CodeStable-Lite 为流程基座**：知识模型好，但 `ff`、递增编号和全量扫描重复 git 职能，编号在并行
  分支上结构性冲突，上下文成本随历史线性增长。只吸收其知识模型与冲突规则。
- **OpenSpec**：CLI 状态机与 delta spec 适合变更提案，但没有 Vision、决策与经验的位置，spec 漂移是其
  主要批评点；要补齐需另建文档层，等于双重维护。
- **把 attention / lessons 迁到 `AGENTS.md` 与 `docs/notes/`**（原计划）：会改动上游大量锚点与测试，
  并让 `AGENTS.md` 承载项目事实，违反仓库「`AGENTS.md` 只写行为规则」的边界。改为保留 `.codestable/`
  路径，团队文档靠 `## 文档归宿` 间接定位。
- **删除与用户全局规则重复的授权条款**（原计划）：skill 要在没有该全局规则的协作者机器上同样成立，
  重复是独立安装单元的必要代价。
- **项目 ADR 用递增编号**：并行分支撞号。模板改用 `YYYY-MM-DD-{slug}` 或语义 slug；本仓库自身 ADR
  沿用既有 `NNN` 约定以便与上游对照。

## Consequences

- 与上游的差异集中在上述 skill 段落、一个 reference 模板和对应测试锚点，可按主题 cherry-pick 上游更新。
- 团队文档层可被不使用 CodeStable 的成员按 `docs/README.md` 独立维护。
- 学习契约只有 `cs-keep` 一个 owner；task skill 需要细则时加载 `cs-keep`，多一次按需加载。
- 静态测试只证明契约文本存在；真实模型是否按登记写入、是否附 `Spec impact`，由试点项目的真路径会话验证。
