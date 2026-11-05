# Claude Rules

## 核心原则

言简意赅。先读仓库事实、现有 skill 文档和 ADR，再修改规则；只把可复用且能验证的做法写进规则文件。

## 语言与文档

- 默认用中文写面向人的回复、报告和文档；代码、命令、路径、协议字段、YAML/JSON key 保持原格式。
- 单个 Markdown 文件不得超过 300 行；超过必须拆分。
- 增加或更新 skill 时，同步检查相关 skill、README/reference、测试和 ADR 中的表述。
- 本仓库的 `AGENTS.md`/`CLAUDE.md` 只写 agent 行为规则；目标项目的高频事实写在目标项目 `AGENTS.md` 的 `## 项目事实` 段，其余项目事实进 `docs/`、work 文档或 ADR。

## Skill 边界

- 不同 skill 之间不要相互耦合；A skill 在非必须情况下不要读取或依赖 B skill 的内部文件。仅约束文件级依赖，按名称提及或路由到其他 skill 不受此限。
- skill 是独立安装单元，运行时每个 skill 只能稳定看到自己包内文件；不要在 SKILL.md 中写 `B-skill/reference/xxx.md` 这类 sibling 引用。
- fork 基础骨架（目标项目）：`AGENTS.md` 的 `## 项目事实`（≤25 条）、只含 `@AGENTS.md` 的 `CLAUDE.md`、`docs/README.md` 文档契约（模板 `cs-onboard/references/docs-contract.md`，表格即文档位置登记）与 `.codestable/work/`；经验首次写入时进 `docs/notes/`，永久 Epic 优先沿用项目既有 Epic/RFC/initiative 归宿，否则首次创建时才按需建立 `docs/epics/`，onboard 不预建空目录。旧版 `.codestable/attention.md` 与 `lessons/` 只在 owner 同意后迁移。
- v1 的 `.codestable/roadmap/`、`.codestable/features/`、`.codestable/issues/`、`.codestable/refactors/`、`.codestable/goals/`、`.codestable/compound/`、`.codestable/audits/`、`.codestable/brainstorms/` 与 `.codestable/feedback/` 只作只读历史知识源：四个 owning task skills（`cs-feat`、`cs-issue`、`cs-refactor`、`cs-epic`）按任务关键词覆盖全部九目录并引用命中路径；其他 skill 仅检索自身契约明确点名的历史源。不得继续生成、原地改写或批量迁移。
- `.codestable/requirements/` 仅在目标项目 `## 项目事实` 明确记录其为 canonical requirement 位置时才可维护；owner 首次指定时先写入 `## 项目事实`，未记录时按只读历史知识处理且不得默认创建。
- skill 专属 context 和确定性 helper 分别放在 owning skill 的 `references/` 与 `scripts/`；跨 skill 通用规则应归宿主策略、项目事实或独立安装单元。

## Epic 生命周期

- 永久 Epic 文档是目标、范围、非目标、验收、已批准子项、关键决策、最终交付、整体验收、遗留风险和长期状态的唯一 owner；`.codestable/work/epic-{slug}.md` 只是临时执行游标，只写永久文档指针、批准 revision、phase、子项进度、下一步、阻塞、`item_progression`、`milestone_commit`、`remote_publish`、parallel 策略下的 `active_items` 和证据，不复制稳定契约或最终结论。
- 保留三道 owner gate：owner 确认拆解；目标、边界、验收、子项定义或重大风险变化时更新永久文档并重新确认；全部子项完成后在真路径上对最新 owner 已批准的验收标准做集成验证（命中独立验收硬条件时加独立上下文验收），再由 owner 最终接受。
- 不交付 reviewer skill、reviewer 创建或轮次协议；独立验收沿用 task skill 的 `独立验收` 硬条件，审查交给宿主或项目已有能力。
- 普通子项完成不是 owner gate：`continuous` 策略下串行自动推进下一项，`parallel` 策略下主流程唯一编排并行推进依赖互不阻塞的子项并串行集成里程碑，均不询问是否继续或终态返回；只有显式 `per-item` 策略、owning-skill 门槛、真实阻塞、新权限或最终验收才暂停。
- Epic 进入 `accepted`、`superseded` 或 `cancelled` 终态后保留永久文档，幂等清理临时 Epic/子项 work；不恢复 `cs-goal` 入口、goal package、`state.yaml`、逐轮 iteration 报告或 legacy runtime gate。

## v1 兼容边界

- v1 的 `.codestable/reference/`、`tools/`、`gates/`、`hooks/`、`runtime-manifest.json` 原样保留，但 v2 skill 不把它们作为入口或执行其中的 legacy runtime。
- 不要新增、同步或刷新 repo-local CodeStable runtime；确定性行为由 owning skill 自己的 helper 或项目已有工具负责。
- CodeStable skills 不拥有默认 worktree/branch 策略；是否创建 worktree、如何命名分支、如何 merge，应由宿主、owner 或未来独立 skill 决定。

## 验证

- skill/runtime 改动完成前至少运行相关 pytest 与 `git diff --check`。
- plugin 分发或退役清单变更还要运行 `tests/test_skills_cli_distribution.py` 与 `tools/check-plugin-package.py`。
