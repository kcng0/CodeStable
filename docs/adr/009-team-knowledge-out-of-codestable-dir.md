---
adr: "009"
title: "kcng0 fork：团队知识迁出 .codestable、收敛的学习契约与独立验收"
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
enforcement: test
stage: [onboard, deliver, keep]
lint: "python3 -m pytest tests/test_skill_contracts.py tests/test_v2_documentation_contract.py"
---

# ADR-009: kcng0 fork：团队知识迁出 .codestable、收敛的学习契约与独立验收

## Context

本 fork 基于上游 `codestable/CodeStable` `19c796de`（2026-08-18，2.0.2 之后）。目标是多人协作、以文档
与长期维护为重点：团队需要一套不依赖 agent 工具也能维护的文档约定，流程层则随模型能力继续变薄。

上游 v2 流程薄、普通任务零产物，但不规定团队文档结构；CodeStable-Lite 的知识分层（Vision / 当前真相
spec / ADR / 术语）和「只回写仍成立结论」更适合团队，但流程偏重（强制 `ff`、递增编号、`o|x` 命名、
开工全量扫描）。上游把高频事实放在 `.codestable/attention.md`，只有调用 cs skill 时才会被读，普通会话与
不用 cs 的成员看不到。四个 task skill 还各自复制了同一套强信号与 lesson 窄维护细则。

## Decision

### 两层分离

- **文档层**属于目标项目、由团队拥有，团队要读的内容全部放在宿主会加载或人会打开的位置：
  - `AGENTS.md` 的 `## 项目事实`（≤25 条，替代上游 `.codestable/attention.md`）；`CLAUDE.md` 只有一行
    `@AGENTS.md`，让不自动读 `AGENTS.md` 的宿主也随会话加载。
  - `docs/README.md` 文档契约：表格规定 Vision、spec、ADR、永久 Epic、术语、经验的位置、更新时机与确认者，
    也是唯一的位置登记；PR 写 `Spec impact: none | updated | drift`。模板在 `cs-onboard/references/docs-contract.md`。
  - 经验进 `docs/notes/`（替代 `.codestable/lessons/`，生命周期不变）；永久 Epic 默认 `docs/epics/`。
  - `.codestable/` 只留 `work/` 临时游标。
- **流程层**是本 fork 的 skill，可替换。skill 按 `docs/README.md` 的登记写入；没有契约时沿用项目既有
  位置，仍不存在则请 owner 选择。

### 接入与调用

- `cs-onboard` 创建上述骨架：`AGENTS.md` 已存在时只追加 `## 项目事实` 段；`docs/` 已有内容时先把契约路径
  映射到既有位置并经 owner 确认；目录在第一次写入时创建，已有文档契约不覆盖。旧版
  `.codestable/attention.md` / `lessons/` 经 owner 同意后迁移，否则保留为只读历史。
- `cs-onboard` 设 `disable-model-invocation: true`，只由用户调用；`cs` 路由到接入时提示运行 `/cs-onboard`。

### 当前真相与学习

- `cs-keep` 增加：只写仍成立的结论；冲突优先级 owner 最新确认 > 当前代码与测试证据 > 可能过期的文档；
  Vision 只在 owner 确认后改；ADR 必列被否决方案，取代时新建并把旧条标 `Superseded`；同步索引。
- 强信号、候选门槛与 lesson 窄维护细则只留在 `cs-keep` 的「task skill 的候选门槛」。四个 task skill
  保留读取修复、3 条内存候选上限、授权门槛和按名称指向 `cs-keep` 的一段话，不跨目录引用文件。

### 交付

- `cs-feat` / `cs-issue` 走真实入口验证时优先用项目内 verification skill 或 `## 项目事实` 记录的驱动方式；
  没有时建议用 `create-verification-skill` 生成。
- feat / issue 收尾在改变已有行为时附 `Spec impact`；refactor 只在发现文档漂移时附 `drift`；`cs-epic`
  收尾在登记了 Vision 时只提出 Vision 候选。

### 独立验收取代审查协议

- 删除 `cs-review` 与兼容别名 `cs-code-review`，本 fork 交付 7 个 skill。上游的 reviewer 创建发现、
  fresh lineage、冻结目标与 hash、findings 分级、3 轮上限和等待协议全部移除；审查与审计交给宿主或项目
  已有的 review 能力。
- `cs-feat` / `cs-issue` / `cs-refactor` 的 `独立验收` 段：默认作者在真路径上自验；只在 schema 或数据迁移、
  鉴权/权限判定、计费/金额计算、并发/锁/幂等逻辑、对外 API 不兼容变更，或用户要求时，按项目或宿主已有的
  委派方式派独立上下文验收，用业务正确性措辞在真路径上找反例；拿不准时不派并在交付末尾说明可复核；
  最多 2 轮；项目或用户另有验收规则时以其为准。
- 风险映射表不再附加独立 review，只保留各风险自身的定向证据、备份/恢复与确认。Epic 拆解与契约变化只经
  owner 确认，不另做 design / contract review；整体验收在真路径上跑集成验证，命中硬条件时按同一规则加
  独立验收。本节取代 ADR-007 中「独立 review」保障与 review 门槛的部分，ADR-007 的风险映射其余部分仍有效。

## Rejected Alternatives

- **以 CodeStable-Lite 为流程基座**：知识模型好，但 `ff`、递增编号和全量扫描重复 git 职能，编号在并行
  分支上结构性冲突，上下文成本随历史线性增长。只吸收其知识模型与冲突规则。
- **OpenSpec**：CLI 状态机与 delta spec 适合变更提案，但没有 Vision、决策与经验的位置，spec 漂移是其
  主要批评点；要补齐需另建文档层，等于双重维护。
- **保留 `.codestable/attention.md` / `lessons/`，用 attention 内的 `## 文档归宿` 间接登记团队文档**（本 ADR
  初稿）：与上游差异最小，但高频事实只在调用 skill 时被读，团队知识分散在隐藏目录与 `docs/` 两处。
- **位置登记放在 `AGENTS.md`**：与 `docs/README.md` 的表格重复，一个事实两个 owner。
- **删除与用户全局规则重复的授权条款**（原计划）：skill 要在没有该全局规则的协作者机器上同样成立，
  重复是独立安装单元的必要代价。
- **项目 ADR 用递增编号**：并行分支撞号。模板改用 `YYYY-MM-DD-{slug}` 或语义 slug；本仓库自身 ADR
  沿用既有 `NNN` 约定以便与上游对照。

- **保留 `cs-review` 作为独立 reviewer 执行器**：其创建发现、lineage 与轮次规则和团队已有的宿主委派与
  验收规则重叠且冲突（两者同一优先级，冲突时无胜者），并把「风险较高」变成默认的额外 review。
- **只在 prompt 中写“请 review”，不要求独立上下文**：作者在同一上下文中复核会沿用自己的假设，找不到
  需求理解层面的反例；硬条件命中时仍需独立上下文。

## Consequences

- 与上游的差异集中在 skill 中的知识路径、上述段落、一个 reference 模板和对应测试锚点；上游涉及
  attention / lessons 路径的更新需要手工合并。
- `AGENTS.md` 同时承载行为规则与 `## 项目事实`，两者合计需遵守项目对该文件的长度约束。
- 团队文档层可被不使用 CodeStable 的成员按 `docs/README.md` 独立维护。
- 学习契约只有 `cs-keep` 一个 owner；task skill 需要细则时加载 `cs-keep`，多一次按需加载。
- 与上游的 review 相关改动（reviewer 编排、`cs-review` 本体）不再可合并，需要按本节规则手工取舍。
- 静态测试只证明契约文本存在；真实模型是否按登记写入、是否附 `Spec impact`，由试点项目的真路径会话验证。
