"""公开文档与 authoring 规范必须描述 v2，而不是已退役的 v1 runtime。"""

from __future__ import annotations

import json
import re
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

V2_SKILLS = {
    "cs",
    "cs-epic",
    "cs-feat",
    "cs-issue",
    "cs-keep",
    "cs-onboard",
    "cs-refactor",
}

# 本 fork 不交付兼容别名；保留常量以便集合表达式不变。
SHIM_SKILLS: set[str] = set()

CURRENT_CONTRACT_DOCS = (
    "README.md",
    "README.en.md",
    "WORKFLOW.md",
    "WORKFLOW.en.md",
    "SKILL_CATALOG.md",
    "SKILL_CATALOG.en.md",
)

SUPPORTING_PUBLIC_DOCS = (
    "UPGRADE.md",
    "UPGRADE.en.md",
    "ROADMAP.md",
    "ROADMAP.en.md",
    "docs/why-codestable.md",
    "docs/why-codestable.en.md",
)

PUBLIC_DOCS = CURRENT_CONTRACT_DOCS + SUPPORTING_PUBLIC_DOCS

AUTHORING_DOCS = (
    ".claude/skills/build-cs-skill/SKILL.md",
    ".claude/skills/build-cs-skill/references/cs-skill-spec-standard.md",
    ".claude/skills/build-cs-skill/references/cs-skill-quality-gates.md",
    ".claude/skills/build-cs-skill/references/cs-skill-fixture-patterns.md",
    ".claude/skills/eval-cs-skill/SKILL.md",
    ".claude/skills/eval-cs-skill/references/author/protocol.md",
    ".claude/skills/eval-cs-skill/references/eval/protocol.md",
    ".claude/skills/eval-cs-skill/references/release/protocol.md",
)


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _contains_contract(text: str, anchor: str) -> bool:
    return "".join(anchor.split()) in "".join(text.split())


def _skill_table(text: str, start: str, end: str) -> set[str]:
    section = text.split(start, 1)[1].split(end, 1)[0]
    return set(re.findall(r"^\|[^|]+\|\s*`(cs(?:-[a-z0-9]+)*)`\s*\|", section, re.M))


def _skills_cli_upgrade_block(text: str) -> str:
    start = text.index("npx skills@latest remove")
    return text[start:text.index("```", start)]


def _upgrade_remove_tokens(text: str) -> list[str]:
    block = _skills_cli_upgrade_block(text).replace("\\\n", " ")
    command = next(
        line.strip()
        for line in block.splitlines()
        if line.strip().startswith("npx skills@latest remove")
    )
    return shlex.split(command)


def _ordinary_prose_paragraphs(text: str) -> list[str]:
    without_code = re.sub(r"```.*?```", "", text, flags=re.S)
    paragraphs: list[str] = []
    excluded_prefixes = ("#", "|", "<", ">", "- ", "* ")
    for block in re.split(r"\n\s*\n", without_code):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines or any(line.startswith(excluded_prefixes) for line in lines):
            continue
        paragraphs.append(" ".join(lines))
    return paragraphs


def test_public_docs_present_the_exact_v2_skill_family() -> None:
    zh_catalog = _read("SKILL_CATALOG.md")
    en_catalog = _read("SKILL_CATALOG.en.md")

    assert _skill_table(zh_catalog, "## 当前入口", "## v1.0.4") == V2_SKILLS
    assert _skill_table(en_catalog, "## Current Entries", "## Retired") == V2_SKILLS

    zh_readme = _read("README.md")
    en_readme = _read("README.en.md")
    assert "7 个 skill" in zh_readme
    assert "7 skills" in en_readme
    assert "cs--skills-7" in zh_readme
    assert "cs--skills-7" in en_readme
    for skill in V2_SKILLS:
        assert f"`{skill}`" in zh_readme
        assert f"`{skill}`" in en_readme
    assert "已退役，不随本 fork 交付" in zh_catalog
    assert "retired and not shipped in this fork" in en_catalog


def test_skills_cli_major_upgrade_removes_exactly_the_retired_v1_names() -> None:
    legacy = json.loads(
        _read("tests/fixtures/skills-cli/legacy-cs-inventory.json")
    )
    retired = set(legacy["skills"]) - V2_SKILLS - SHIM_SKILLS

    assert len(retired) == 25
    zh = _read("UPGRADE.md")
    en = _read("UPGRADE.en.md")

    for readme in (zh, en):
        block = _skills_cli_upgrade_block(readme)
        tokens = _upgrade_remove_tokens(readme)
        assert block.index("skills@latest remove") < block.index("skills@latest add")
        assert tokens[:3] == ["npx", "skills@latest", "remove"]
        assert tokens[-2:] == ["-g", "-y"]
        assert len(tokens[3:-2]) == len(retired)
        assert set(tokens[3:-2]) == retired

        assert "--all" not in tokens
        assert "--skill=*" not in tokens
        assert "-s=*" not in tokens
        for option in ("--skill", "-s"):
            if option in tokens:
                assert tokens[tokens.index(option) + 1] != "*"

    assert "按名称删除，不校验安装来源" in zh
    assert "name-based and does not verify the installation source" in en


def test_readme_is_a_compact_first_evaluator_entry() -> None:
    zh = _read("README.md")
    en = _read("README.en.md")
    headings = {
        "README.md": (
            "## 30 秒运行模型",
            "## 5 分钟开始",
            "## 三个核心原则",
            "## 项目记忆",
            "## 适用边界",
            "## 深入文档",
        ),
        "README.en.md": (
            "## 30-Second Model",
            "## Start in 5 Minutes",
            "## Three Principles",
            "## Project Memory",
            "## Fit",
            "## Go Deeper",
        ),
    }
    for filename, ordered_headings in headings.items():
        text = _read(filename)
        positions = [text.index(heading) for heading in ordered_headings]
        assert positions == sorted(positions)
        assert len(text.splitlines()) <= 300
        assert all(len(paragraph) <= 240 for paragraph in _ordinary_prose_paragraphs(text))
        assert "asset/PromotionalImage.png" not in text

    for anchor in (
        "轻量 skill 契约",
        "不编排 Agent 团队",
        "不为项目建立第二套文档系统",
        "你只需要告诉 `cs` 想完成什么",
        "还没讨论清楚的内容",
        "直接执行 / 当前会话讨论 / 给出建议",
        "thin harness, thick context",
        "证据先于结论",
        "一个事实，一个 canonical owner",
        "永久 Epic 文档",
        "临时 work 游标",
        "默认作者在真路径上自验",
    ):
        assert anchor in zh
    for anchor in (
        "lightweight skill contracts",
        "does not orchestrate agent teams",
        "does not create a second documentation system",
        "You only need to tell `cs` what you want to accomplish",
        "does not persist unfinished discussions",
        "execute directly / discuss in this session / advise",
        "thin harness, thick context",
        "Evidence before conclusions",
        "One fact, one canonical owner",
        "permanent Epic document",
        "temporary work cursor",
        "The author self-verifies on the real path",
    ):
        assert anchor in en

    for text in (zh, en):
        for anchor in (
            "codex plugin marketplace add kcng0/CodeStable",
            "/plugin marketplace add kcng0/CodeStable",
            "npx skills@latest add kcng0/CodeStable/plugins/codestable",
            "/cs-onboard",
            "/cs",
            "## 项目事实",
            "@AGENTS.md",
            "docs/notes/",
            "work/",
        ):
            assert anchor in text
        assert "codex plugin marketplace upgrade codestable" not in text
        assert "npx skills@latest remove" not in text

    assert "[升级指南](./UPGRADE.md#从-v104-升级到-v2)" in zh
    assert "精确删除 25 个退役入口" in zh
    assert "[upgrade guide](./UPGRADE.en.md#upgrade-from-v104-to-v2)" in en
    assert "remove the 25 retired entries" in en

    assert (
        "作者 [@liuzhengdong](https://github.com/liuzhengdong)、"
        "[@dafang](https://github.com/dafang)、Codex、Claude"
    ) in zh
    assert (
        "Authors [@liuzhengdong](https://github.com/liuzhengdong), "
        "[@dafang](https://github.com/dafang), Codex, and Claude"
    ) in en
    assert "liuzhengdongfortest" not in zh
    assert "liuzhengdongfortest" not in en


def test_readme_links_to_canonical_deep_docs() -> None:
    links = {
        "README.md": (
            ("./WORKFLOW.md", "WORKFLOW.md"),
            ("./SKILL_CATALOG.md", "SKILL_CATALOG.md"),
            ("./UPGRADE.md", "UPGRADE.md"),
            ("./docs/why-codestable.md", "docs/why-codestable.md"),
            ("./ROADMAP.md", "ROADMAP.md"),
            ("./CHANGELOG.md", "CHANGELOG.md"),
        ),
        "README.en.md": (
            ("./WORKFLOW.en.md", "WORKFLOW.en.md"),
            ("./SKILL_CATALOG.en.md", "SKILL_CATALOG.en.md"),
            ("./UPGRADE.en.md", "UPGRADE.en.md"),
            ("./docs/why-codestable.en.md", "docs/why-codestable.en.md"),
            ("./ROADMAP.en.md", "ROADMAP.en.md"),
            ("./CHANGELOG.md", "CHANGELOG.md"),
        ),
    }
    for readme, targets in links.items():
        text = _read(readme)
        for link, target in targets:
            assert link in text
            assert (ROOT / target).is_file()


def test_public_document_local_links_resolve() -> None:
    for filename in PUBLIC_DOCS:
        document = ROOT / filename
        for target in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", _read(filename)):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            relative = target.split("#", 1)[0]
            if relative:
                assert (document.parent / relative).resolve().exists(), (
                    f"{filename} links to missing local target {target}"
                )


def test_upgrade_docs_keep_legacy_assets_without_owning_runtime_policy() -> None:
    zh = _read("UPGRADE.md")
    en = _read("UPGRADE.en.md")

    assert "升级不会删除项目里的 v1 历史资产" in zh
    assert "检索与写入政策以 [WORKFLOW.md](./WORKFLOW.md#v1-升级边界) 为准" in zh
    assert "does not delete historical v1 project assets" in en
    assert "retrieval and write policy remains owned by [WORKFLOW.en.md](./WORKFLOW.en.md#v1-upgrade-boundary)" in en
    assert ".codestable/reference/" not in zh
    assert ".codestable/reference/" not in en


def test_active_docs_do_not_publish_v1_runtime_as_current_contract() -> None:
    active = "\n".join(_read(path) for path in PUBLIC_DOCS + AUTHORING_DOCS)

    for stale in (
        "refresh-runtime",
        "cs-onboard/tools",
        ".codestable/reference/",
        "长期兼容入口",
        "Long-Term Compatibility Entries",
        "long-term compatibility entries",
    ):
        assert stale not in active


def test_eval_autonomy_example_targets_a_runnable_experiment() -> None:
    autonomy = _read(
        ".claude/skills/eval-cs-skill/references/autonomy/protocol.md"
    )
    assert "experiments/cs-code-review-001" in autonomy
    assert "experiments/cs-audit-001" not in autonomy


def test_authoring_docs_assign_context_and_helpers_to_real_owners() -> None:
    build = _read(".claude/skills/build-cs-skill/SKILL.md")
    fixtures = _read(
        ".claude/skills/build-cs-skill/references/cs-skill-fixture-patterns.md"
    )
    release = _read(".claude/skills/eval-cs-skill/references/release/protocol.md")

    assert "belong to the owning skill's" in build
    assert "`references/` and `scripts/`" in build
    assert "do not require sibling skill files" in build
    assert "retired v1 CodeStable name also selects `NoActiveSkill`" in build
    assert "retired-v1-entry-remains-absent" in fixtures
    assert "tests/test_skills_cli_distribution.py" in release


def test_review_docs_publish_hard_condition_acceptance_not_reviewer_orchestration() -> None:
    zh_workflow = _read("WORKFLOW.md")
    en_workflow = " ".join(_read("WORKFLOW.en.md").split())

    for anchor in (
        "默认由作者在真路径上自验",
        "schema 或数据迁移、鉴权/权限判定",
        "计费/金额计算、并发/锁/幂等逻辑、对外 API 不兼容变更、影响面经定向核实仍不确定，或用户要求时",
        "按项目或宿主已有的委派方式",
        "用业务正确性措辞",
        "拿不准是否命中时不派",
        "最多 2 轮",
        "项目或用户另有验收规则时以该规则为准",
        "审查与审计交给宿主或项目已有的 review 能力",
        "永久文档并重新征得 owner 同意",
        "按同一独立验收规则对整体验收标准找反例",
    ):
        assert _contains_contract(zh_workflow, anchor)

    for anchor in (
        "by default the author self-verifies on the real path",
        "Only schema or data migration, authentication/authorization decisions, billing/amount calculation",
        "an impact scope still uncertain after a targeted check",
        "through the project's or host's existing delegation",
        "in business-correctness terms",
        "When unsure whether a condition applies, do not dispatch",
        "for at most two rounds",
        "Project or user acceptance rules take precedence",
        "review and audit belong to the host's or project's review capability",
        "first update the permanent document and require owner reconfirmation",
        "the same acceptance rule looks for counterexamples against the overall criteria",
    ):
        assert anchor in en_workflow

    public = "\n".join(_read(path) for path in PUBLIC_DOCS)
    for stale in ("fresh reviewer", "reviewer lineage", "独立 review"):
        assert stale not in public
    # 只有升级指南为切换用户点名旧入口，其余公开文档不再出现 `cs-review`。
    for path in PUBLIC_DOCS:
        if not path.startswith("UPGRADE"):
            assert "`cs-review`" not in _read(path)
    assert "独立 subagent 视角" not in public
    assert "independent subagent perspective" not in public


def test_minimum_sufficient_assurance_contract_is_bilingual() -> None:
    zh_readme = _read("README.md")
    en_readme = _read("README.en.md")
    for anchor in (
        "需求清楚时",
        "直接开始，并用足够的验证交付结果",
        "遇到具体风险时",
        "只增加与风险对应的确认或测试",
        "不自动启用整套流程",
    ):
        assert _contains_contract(zh_readme, anchor)
    for anchor in (
        "When the request is clear",
        "delivers the result with enough verification",
        "When it finds a concrete risk",
        "only the confirmation or tests needed for that risk",
        "does not enable the whole workflow",
    ):
        assert _contains_contract(en_readme, anchor)

    zh_docs = (
        _read("WORKFLOW.md"),
        _read("SKILL_CATALOG.md"),
        _read("docs/why-codestable.md"),
    )
    en_docs = (
        _read("WORKFLOW.en.md"),
        _read("SKILL_CATALOG.en.md"),
        _read("docs/why-codestable.en.md"),
    )

    for document in zh_docs:
        for anchor in (
            "执行流程 = 最小闭环 + 每个未排除风险所要求的最少保障",
            "任务类型只决定工程方法，实际风险决定保障强度",
            "独立验收不是默认步骤",
            "一个风险只增加与它直接对应的保障",
        ):
            assert _contains_contract(document, anchor)

    for document in en_docs:
        for anchor in (
            "Execution flow = minimum complete loop + the least assurance required by each unexcluded risk",
            "Task type determines the engineering method; actual risk determines assurance strength",
            "Independent acceptance is not a default step",
            "Each risk adds only the assurance directly required by that risk",
        ):
            assert anchor in document

    public_workflow = _read("WORKFLOW.md") + _read("WORKFLOW.en.md")
    for stale in (
        "默认；仅文案级微小改动可说明后跳过",
        "默认；仅单行级微小修复可说明后跳过",
        "default; documentation-only tiny changes may be skipped with an explanation",
        "default; single-line tiny fixes may be skipped with an explanation",
    ):
        assert stale not in public_workflow


def test_workflow_publishes_risk_mapping_bilingually() -> None:
    zh = " ".join(_read("WORKFLOW.md").split())
    en = " ".join(_read("WORKFLOW.en.md").split())

    for anchor in (
        "一次静默、有界核对",
        "不能排除时先按风险存在处理",
        "不得以“没有注意到风险”作为降级依据",
        "破坏兼容性或改变多消费者依赖的公开契约",
        "改变权限、安全、隐私或其他信任边界",
        "改变持久化数据、schema 或迁移路径",
        "改变并发、顺序或一致性语义",
        "产生不可恢复的代码外副作用",
        "性能回退或性能敏感路径变化",
        "改动影响面广或失败可跨模块传播",
        "流程太重 / 只是小改动 / 文档比代码多",
        "不是无条件跳过安全门槛",
        "连续性需要不是风险门槛",
    ):
        assert anchor in zh

    for anchor in (
        "one silent, bounded check",
        "If a risk still cannot be ruled out after the least-cost targeted check, treat it as present",
        "not noticing a risk is not a valid reason to lower assurance",
        "breaks compatibility or changes a public contract used by multiple consumers",
        "changes authorization, security, privacy, or another trust boundary",
        "changes persisted data, schema, or a migration path",
        "changes concurrency, ordering, or consistency semantics",
        "creates an irreversible effect outside the codebase",
        "addresses a performance regression or changes a performance-sensitive path",
        "has broad impact or can propagate failure across modules",
        "flow is too heavy / this is only a small change / documentation exceeds the code",
        "not an unconditional bypass of safety gates",
        "Continuity needs are not risk gates",
    ):
        assert anchor in en

    assert "公开契约、数据、权限、并发或真实方案取舍先经用户确认" not in zh
    assert (
        "Public contracts, data, authorization, concurrency, or real design "
        "tradeoffs require owner confirmation first"
    ) not in en


def test_workflow_owns_epic_and_legacy_knowledge_contracts() -> None:
    zh_workflow = " ".join(_read("WORKFLOW.md").split())
    en_workflow = " ".join(_read("WORKFLOW.en.md").split())

    legacy_dirs = (
        "roadmap/",
        "features/",
        "issues/",
        "refactors/",
        "goals/",
        "compound/",
        "audits/",
        "brainstorms/",
        "feedback/",
    )
    for directory in legacy_dirs:
        assert directory in zh_workflow
        assert directory in en_workflow

    for anchor in (
        "只读历史知识源",
        "owning task skills",
        "按任务关键词覆盖",
        "其他 skill 只检索自身契约明确点名的历史源",
        "不得继续生成",
        "原地改写",
        "批量迁移",
        "永久 Epic 文档",
        "临时执行游标",
        "按需建立 `docs/epics/{slug}.md`",
        "`cs-onboard` 不预建 `docs/epics/`",
        "Epic 保留三道 owner gate",
        "最新 owner 已批准的验收标准",
        "owner 最终接受",
        "串行约束，不是每个子项的人工 gate",
        "不得询问“是否继续下一项”",
        "不得把它作为终态返回",
        "`item_progression`",
        "`item_progression: parallel` 只能搭配 `milestone_commit: authorized`",
        "唯一编排者与游标 writer",
        "退化为串行推进",
        "全部合格 worker 创建能力或隔离能力均不可用",
        "`active_items`",
        "不恢复 `cs-goal` 入口",
    ):
        assert anchor in zh_workflow

    for anchor in (
        "read-only historical knowledge sources",
        "cover all nine by task keyword",
        "Other skills retrieve only historical sources explicitly named by their own contracts",
        "No skill may generate",
        "rewrite in place",
        "bulk-migrate",
        "permanent Epic document",
        "temporary execution cursor",
        "create `docs/epics/{slug}.md` on demand",
        "`cs-onboard` does not precreate `docs/epics/`",
        "An Epic retains three owner gates",
        "latest owner-approved criteria",
        "owner's final acceptance",
        "serialization constraint, not a per-item owner gate",
        "must not ask whether to continue to the next item",
        "return that completion as terminal",
        "`item_progression`",
        "`item_progression: parallel` requires `milestone_commit: authorized`",
        "sole orchestrator and cursor writer",
        "degrades to serial within the session",
        "every qualified worker-creation capability is unavailable",
        "`active_items`",
        "Do not restore the `cs-goal` entry",
    ):
        assert anchor in en_workflow

    for workflow in (zh_workflow, en_workflow):
        assert ".codestable/requirements/" in workflow
        assert "## 项目事实" in workflow
        assert "canonical requirement" in workflow

    zh_readme = _read("README.md")
    en_readme = _read("README.en.md")
    zh_catalog = _read("SKILL_CATALOG.md")
    en_catalog = _read("SKILL_CATALOG.en.md")
    assert "默认连续策略" not in zh_workflow
    assert "永久 Epic 文档" in zh_catalog
    assert "permanent Epic doc" in en_catalog
    assert "永久 Epic 文档" in zh_readme
    assert "临时 work 游标" in zh_readme
    assert "permanent Epic document" in en_readme
    assert "temporary work cursor" in en_readme
    assert "串行连续推进" in zh_catalog
    assert "serially and continuously" in en_catalog
    assert "`parallel` 策略时并行推进依赖互不阻塞的子项" in zh_catalog
    assert "owner-approved `parallel` policy" in en_catalog


def test_epic_wayfinding_contract_is_bilingual_and_keeps_one_document_owner() -> None:
    zh_docs = (
        _read("README.md"),
        _read("WORKFLOW.md"),
        _read("SKILL_CATALOG.md"),
        _read("docs/why-codestable.md"),
    )
    en_docs = (
        _read("README.en.md"),
        _read("WORKFLOW.en.md"),
        _read("SKILL_CATALOG.en.md"),
        _read("docs/why-codestable.en.md"),
    )

    for document in zh_docs:
        assert _contains_contract(document, "路线尚不清晰")
        assert _contains_contract(document, "路线清晰、可审查、可执行")
        assert _contains_contract(document, "永久 Epic 文档本身就是路线地图")
    for document in en_docs:
        assert _contains_contract(document, "route is still unclear")
        assert _contains_contract(document, "clear, reviewable, and executable")
        assert _contains_contract(document, "permanent Epic document itself is the route map")

    zh_workflow = " ".join(zh_docs[1].split())
    en_workflow = " ".join(en_docs[1].split())
    for anchor in (
        "永久 Epic 文档就是唯一路线文档",
        "在 proposed 阶段，永久 Epic 文档本身就是路线地图",
        "frontier 只由依赖已经解决的待决策派生",
        "待决策",
        "尚未明确",
        "不得替 owner 回答 HITL 问题",
        "HITL 不是新的 owner gate",
        "route clear 前不得保留未解决的 HITL 节点",
        "仍有效的 HITL 节点必须由 owner 明确解决或确认移入 `非目标`",
        "涉及外部权限或副作用的 prerequisite 仍须另获对应权限或确认",
        "不新增独立 issue、map 或第三套状态",
        "route clear 不是新的 owner gate",
        "现有第一道 owner 确认",
        "`current_item` 保持 `null`",
    ):
        assert anchor in zh_workflow
    for anchor in (
        "The permanent Epic document is the only route document",
        "during proposed, the permanent Epic document itself is the route map",
        "frontier is derived only from pending decisions whose dependencies are resolved",
        "Decisions pending",
        "Still unclear",
        "must not answer a HITL question for the owner",
        "HITL is not a new owner gate",
        "No unresolved HITL node may remain at route clear",
        "A still-valid HITL node must be explicitly resolved by the owner or moved out of scope with the owner's explicit confirmation",
        "a prerequisite involving external authority or side effects still requires separate permission or confirmation",
        "does not add issues, a separate map artifact, or a third state system",
        "Route clear is not a new owner gate",
        "existing first owner confirmation",
        "`current_item` stays `null`",
    ):
        assert anchor in en_workflow
    assert "`Decisions pending`" not in en_workflow
    assert "`Still unclear`" not in en_workflow


def test_shared_language_contract_is_bilingual() -> None:
    zh_docs = (
        _read("README.md"),
        _read("SKILL_CATALOG.md"),
        _read("docs/why-codestable.md"),
    )
    en_docs = (
        _read("README.en.md"),
        _read("SKILL_CATALOG.en.md"),
        _read("docs/why-codestable.en.md"),
    )
    for document in zh_docs:
        assert "共享语言" in document
    for document in en_docs:
        assert "shared language" in document

    zh_workflow = " ".join(_read("WORKFLOW.md").split())
    en_workflow = " ".join(_read("WORKFLOW.en.md").split())
    for anchor in (
        "共享语言是条件式设计纪律",
        "普通改动沿用已有单义术语时不增加产物",
        "Feature 要求局部语义清晰",
        "Epic 要求概念体系清晰",
        "仓库事实由 agent 核实",
        "产品含义与概念边界进入 HITL",
        "不自动创建 `CONTEXT.md`",
        "不是新的 owner gate",
    ):
        assert anchor in zh_workflow
    for anchor in (
        "Shared language is a conditional design discipline",
        "Ordinary changes that reuse existing unambiguous terms add no artifact",
        "A Feature requires local semantic clarity",
        "An Epic requires conceptual-system clarity",
        "The agent verifies repository facts",
        "product meaning and concept boundaries enter HITL",
        "does not automatically create `CONTEXT.md`",
        "is not a new owner gate",
    ):
        assert anchor in en_workflow


def test_public_workflows_stay_within_document_size_limit() -> None:
    assert len(_read("WORKFLOW.md").splitlines()) <= 300
    assert len(_read("WORKFLOW.en.md").splitlines()) <= 300


def test_project_learning_lifecycle_is_bilingual_and_low_interruption() -> None:
    zh_workflow = _read("WORKFLOW.md")
    en_workflow = _read("WORKFLOW.en.md")
    for anchor in (
        "任务内静默观察",
        "经验命中：{path}（{status}）；核验：{fact}；影响：{plan_or_check}",
        "一次有界、最低成本的定向核实",
        "明确排除一个具体且合理的错误路径",
        "本次通过的验收证据",
        "observed / validated / retired",
        "普通任务最多展示一条",
        "Epic 子项不新增暂停",
        "机械 guard 优先",
        "新 lesson 仍需显式授权",
        "不保存 transcript",
    ):
        assert _contains_contract(zh_workflow, anchor)
    for anchor in (
        "observes silently during the task",
        "lesson hit: {path} ({status}); check: {fact}; impact: {plan_or_check}",
        "one bounded, lowest-cost targeted check",
        "explicitly rules out a concrete, plausible wrong path",
        "the task's passing acceptance evidence",
        "observed / validated / retired",
        "at most one candidate",
        "Epic items add no pause",
        "mechanical guards first",
        "New lessons still require explicit authorization",
        "does not save transcripts",
    ):
        assert _contains_contract(en_workflow, anchor)

    public_pairs = (
        ("README.md", "README.en.md", "边做边识别晶化时刻", "recognizes crystallization moments while working"),
        ("SKILL_CATALOG.md", "SKILL_CATALOG.en.md", "observed / validated / retired", "observed / validated / retired"),
        ("docs/why-codestable.md", "docs/why-codestable.en.md", "经验不是活动日志", "Experience is not an activity log"),
        (
            "docs/why-codestable.md",
            "docs/why-codestable.en.md",
            "排除一个具体且合理的错误路径",
            "rules out a concrete, plausible wrong path",
        ),
    )
    for zh_path, en_path, zh_anchor, en_anchor in public_pairs:
        assert _contains_contract(_read(zh_path), zh_anchor)
        assert _contains_contract(_read(en_path), en_anchor)

    assert not _contains_contract(zh_workflow, "把可复用经验写成 lesson")
    assert not _contains_contract(en_workflow, "reusable experience into lessons")
    assert "| `cs-keep` | 管理有证据的项目事实、lesson 生命周期与 canonical 归宿 |" in _read("README.md")
    assert (
        "| `cs-keep` | Manage evidence-backed project facts, lesson lifecycle, and canonical homes |"
        in _read("README.en.md")
    )
    assert _contains_contract(_read("docs/why-codestable.md"), "尚未被更强 owner 承接的经验暂存于 lessons")
    assert _contains_contract(
        _read("docs/why-codestable.en.md"),
        "experience without a stronger owner is staged in lessons",
    )
