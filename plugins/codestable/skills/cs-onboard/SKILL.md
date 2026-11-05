---
name: cs-onboard
description: 仓库接入 CodeStable：在 AGENTS.md 建项目事实段、写 docs/README.md 文档契约与最小骨架，或为存量项目做无损升级说明。
disable-model-invocation: true
---

# cs-onboard

给仓库一个最小的 CodeStable 骨架。规则和纪律都在 skill 包里，项目目录只放项目自己的知识；团队要读的
内容放在 `AGENTS.md` 与 `docs/`，`.codestable/` 只放临时游标。

## 骨架（目标状态）

```text
AGENTS.md
└── ## 项目事实      # 每次会话必读的高频事实，≤25 条，从空开始
CLAUDE.md            # 只有一行 @AGENTS.md
docs/
├── README.md        # 文档契约：各类文档的位置、更新时机与确认者
└── notes/           # 待验证经验，一条一文件（cs-keep 首次写入时创建）
.codestable/
└── work/            # 活动中的跨会话任务游标，完成即清
```

- `AGENTS.md` 已存在时只追加缺失的 `## 项目事实` 段，不改其他内容；段内初始只写一句用途说明。
- `CLAUDE.md` 不存在时写入只含一行 `@AGENTS.md` 的文件；已存在但缺这一行时只追加这一行，不改其他
  内容。项目事实只写在 `AGENTS.md`，不复制进 `CLAUDE.md`。
- `docs/README.md` 不存在时按 `references/docs-contract.md` 中分隔线以下的模板写入。`docs/` 已有其他
  内容时，先把模板表格的路径映射到项目已有位置并请 owner 确认，确认后再写；已有文档契约时不覆盖，只
  报告差异。
- 只建 `.codestable/work/`；`docs/notes/`、`docs/spec/`、`docs/adr/`、`docs/epics/` 等目录在首次写入时
  由 owning skill 创建，不预建空目录。
- 创建后确认 `AGENTS.md`、`CLAUDE.md`、`docs/` 与 `.codestable/` 未被 .gitignore 忽略（必须入库共享）；发现被忽略时
  停下报告，由用户决定怎么改，不擅自修改 .gitignore。

## 硬门槛

- **存量文件一律不动**：v1 知识目录 `.codestable/roadmap/`、`.codestable/features/`、`.codestable/issues/`、`.codestable/refactors/`、`.codestable/goals/`、`.codestable/compound/`、`.codestable/audits/`、`.codestable/brainstorms/`、`.codestable/feedback/`，既有 `.codestable/requirements/`，以及 legacy runtime 资产 `.codestable/reference/`、`.codestable/tools/`、`.codestable/gates/`、`.codestable/hooks/`、`.codestable/runtime-manifest.json` 全部原样保留，不删除、不覆盖、不迁移格式。
- 上述 9 个 v1 知识目录及其他未被 v2 明确拥有的既有 `.codestable/` 目录默认只读：不得继续生成、原地改写或批量迁移；新结论进入 v2 Epic、项目文档、ADR 或 lesson。owning task skills 只按当前任务关键词检索存在的历史目录，命中时报告来源路径。
- 既有 `.codestable/requirements/` 仅在 `## 项目事实` 明确记录其为 canonical requirement 位置时可继续维护；owner 首次指定时先记录到 `## 项目事实`，否则按只读历史处理。目录不存在时不默认创建。
- **不复制**任何 skill 包内文件到项目（v1 的 reference/gates/tools 分发机制已废止）。
- 已有 `.codestable/` 的仓库只补缺失的骨架项，其余不碰。存在旧版 `.codestable/attention.md` 或
  `.codestable/lessons/` 时，说明新位置并经 owner 同意后迁移：条目并入 `## 项目事实`，lesson 用 `git mv`
  移到 `docs/notes/`；不同意则原样保留为只读历史。

## v1 项目升级说明

对存量 v1 项目，创建缺失目录后向用户说明三点即可：

1. 旧产物与旧沉淀全部保留；owning task skills 按任务关键词只读检索存在的历史目录并报告命中路径；
2. 新工作不再生成 v1 形态产物（阶段文档、checklist、goal 包），普通任务零产物，跨会话任务一个 work 文档；
3. gate 与 runtime 工具不再由 skill 调用；项目侧 `.codestable/tools/` 若被用户自己的 hook 引用则继续自行维护。

## 收尾

报告创建了哪些文件、保留了哪些存量、`docs/README.md` 登记的文档位置、新增文件的 git 状态。不写入任何业务判断。
