# Simplicity evaluation design

**Status:** design proposal, no eval fixtures changed
**Scope:** distinguish a smaller safe design from both needless machinery and a superficially shorter design that loses required behavior. Cover decisions before implementation (`plan`/`build`) and after implementation (`refactor`/`review`).

## Evidence and current behavior

The project memory is still a scaffold. `.resonance/01_state.md` has placeholder phase and goal fields; `02_memory.md` has no lessons or decisions; `.resonance/memory/` is absent. `python3 .forge/recall.py "simplicity necessity evals architecture refactor"` returned template text from `00_soul.md` and `04_systems.md`, not a usable lesson. There is no evidence here for project-specific complexity thresholds.

The shared [necessity protocol](../../.agents/skills/ops/core/references/necessity_protocol.md) already says to trace the real flow, stop at the first sufficient option, protect behavior, and optimize ownership surface rather than line count. Existing refactor fixtures cover a browser-native date field, duplicate discount logic, and one-implementation abstractions; reviewer and build fixtures cover similar implementation selection. They do not test the hard counterexample: a shorter result that removes a required invariant or contracts the user's requested scope.

Forge grades `expected_behavior` with a language-model judge. Its deterministic `checks` are text/regex, section-heading, or maximum-line checks in `.forge/run_evals.py`; they do not inspect source or prove semantics. The source eval cases under `.forge/skills/**/evals/` are hashed by `.forge/eval_integrity.py` and registered in `.forge/eval_fixture_manifest.json`. A new eval case should therefore keep the rubric semantic, and use deterministic checks only for a small explicit artifact marker where wording itself is part of the output contract. Do not use keywords such as “microservice”, “idempotency”, or “audit” as proof that the behavior survived.

## Design rule for the judge

Use paired, contrastive cases with an explicit requirement baseline. The judge should ask whether the proposal removes an unneeded owned concept while preserving every named invariant and requested outcome. It must accept a justified component or service boundary when its current job is evidenced (independent scaling/failure/security/ownership, a real caller, or a separately changing contract). It must reject extra boundaries supported only by hypothetical future flexibility. Count concepts and owners as evidence, never as the verdict.

The judge must also reject silent scope contraction. If an agent recommends a smaller scope, it must first state that recommendation and its consequence; it may not report the reduced scope as completion. A tie between two designs is not resolved by choosing fewer files, lines, components, or states.

## Small fixture set and owners

Keep six focused additions, with a paired build/refactor check for workflow preservation. Reuse existing fixture layout and rubric fields. Owners below are the skill that owns the oracle; do not copy the same case into both `.agents` and `.forge`, since `.forge/skills/.../evals/` is the source hashed by the integrity manifest and `.agents` is the compiled copy.

| Owner and fixture | Context | Required distinction |
| --- | --- | --- |
| `engineering/build`, architecture choice | Before implementation | Given a bounded single-deploy application with no independent scaling, deployment, failure, or ownership requirement, decline speculative service decomposition and event bus. In a contrast arm, a separately scaled, isolated workload with an explicit failure boundary justifies separation. Judge against evidence in the prompt, not a blanket “monolith good” or “fewer services” rule. Preserve the full requested feature scope. |
| `engineering/build`, workflow state change | Before implementation | Simplifying an existing multi-step sync is allowed only if retries, deduplication/idempotency key behavior, partial-failure recovery, and visible outcome remain in the plan. State names may consolidate only when those observable guarantees still have an owner. Reject inventing a queue/retry platform if the supplied runtime retry is sufficient. |
| `ops/refactor`, workflow state consolidation | After implementation | Supplied diff merges states and drops an idempotency key or retry recovery path. Require a concrete finding and preservation fix; do not accept passing happy-path tests as proof. Paired positive variant consolidates redundant states while retaining the invariants and makes no behavioral change. |
| `ops/refactor`, permission truth | After implementation | Centralization is warranted across duplicated checks, but the proposed helper must preserve resource, action, and tenant scope, default-deny behavior, boundary validation, and the existing denial audit event. Also include an existing one-implementation policy abstraction that genuinely centralizes the rule: retain it if callers depend on its shared contract, despite the single implementation. Reject replacing it merely to lower component count. |
| `engineering/frontend` (with designer baseline), form and scope | Build/refinement | A proposed shorter form hides a required field and discards entered values/context on validation or network failure. Require task-critical data, accessible labels/errors, and recovery. The request explicitly includes the whole workflow, so a “simpler first screen” cannot quietly omit later required steps. A truly optional detail can be progressively disclosed if users can find it before it is needed. |
| `engineering/automation`, recurring report | Before automation | Prefer the existing report command/library if it already owns the transformation and output; add only the missing scheduling/parameter glue. Reject a new agent loop, MCP server, or multi-stage framework for a deterministic one-command report without a measurable need. Preserve required validation and idempotent output; require dry-run only when the real side effect cannot otherwise be previewed safely. |

The table has six rows and proposes six fixture files. Keep form and scope contraction together in one fixture because both concern preservation of the requested task; keep the workflow pair separate because one tests planning and one tests preservation in an actual diff. This is a bounded suite across the named failure modes without duplicating each case across skills.

## Rubric shape

Keep each case to four or five judgeable outcomes:

1. Identifies the requested outcome and names explicit non-negotiable behavior before recommending a cut.
2. Traces current callers/ownership and separates evidenced current needs from speculative future options.
3. Chooses the least owned design that satisfies the full contract; retains boundaries or abstractions that currently own a real contract.
4. Preserves the case-specific invariants (workflow recovery, authorization, form information/recovery, or automation side-effect behavior).
5. Reports any proposed scope reduction as a recommendation with its consequence, never as completed work.

Use fixture text containing small, realistic before/diff contexts with the relevant callers and safety checks. Avoid enormous mock repositories. A source excerpt alone cannot establish all call sites, so give the case the caller list and contract needed to make the judgment answerable.

## Deterministic checks

Use only checks that can genuinely be decided from output text. For example, one `regex_absent` check may continue enforcing the repository's no-em-dash rule. Do not add checks that look for words like “minimum”, “audit”, “retry”, or “tenant” and count them as semantic proof. `contains_all` is useful only where the output must literally name a known artifact or command, such as a plan file. Existing rubric outcomes should carry the behavioral judgment.

Do not add parser/code-analysis logic to `run_evals.py` for this suite. If a future claim must be proven from an actual source diff or executed behavior, use an outcome fixture with a real harness or an integration/e2e test that exercises the behavior; the current completion-text runner cannot prove it.

## Direct-protocol conflicts and calibration

- `ops/refactor` and `ops/reviewer` are aligned with the necessity protocol: they protect behavior and reject line-count reasoning. The fixture gap is failure detection, not a need for another general checklist.
- `engineering/build` says “absolute minimum code” and the plan skill says to split any item that fails the “5-second rule.” Read those as minimum sufficient ownership and action clarity, not as minimum components or literal shortest code. A plan can preserve a necessary service boundary while keeping actions executable.
- `strategy/architect` asks for topology and durable boundaries when architecture actually changes; do not grade its diagrams/ADRs as needless ceremony in an architecture task. Its scope should be proportional to the boundary decision.
- `engineering/automation` mandates Zod, structured output, idempotency, `--help`, and a test in its current DoD; the existing happy-path eval additionally demands `--dry-run` for a Monday report even though no side effect is specified. This can over-specify simple scripts. The proposed fixture should assess whether the protocol made a needless permanent tool, but should not silently rewrite the tool's procedural contract. Separately, a future protocol revision should make schema/test/dry-run requirements conditional on tool interface, side effects, and project stack.
- `engineering/frontend` says “atomic” and promotes Atomic Design, while its task-first guidance already requires only reachable states, required information, and recovery. The eval should favor that evidence over mandatory component decomposition.
- The designer skill already states not to hide information needed by a real task, to retain context on error, and to disclose rare detail only when findable before needed. It is a useful baseline for the form fixture, not a new component-count oracle.

Treat these as calibration notes, not an invitation to edit the protocols in the fixture-authoring pass. If skills and fixtures are revised later, preserve the existing user-owned dirty UI/UX edits and review each precise overlap in context.

## Acceptance and limits

The suite is useful only if it passes both directions: it catches needless machinery in an under-specified architecture and it catches “simplification” that removes a stated contract. It must also leave a justified separation and a truthful existing abstraction unflagged. Include at least one build-before case and one refactor-after case for each key decision family where practical; the two workflow cases establish that cross-stage check without duplicating every fixture.

A model judge can still mistake plausible explanation for real implementation evidence. These cases evaluate the agent's decision and review behavior, not runtime safety. Where a code change is proposed, actual tests and review remain the proof of preserved behavior. No implementation or fixture edits were made as part of this design audit.
