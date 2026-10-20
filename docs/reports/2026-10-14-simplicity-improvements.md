# Complexity and simplicity implementation

**Date:** 2026-10-14
**Status:** Source changes and integration checks complete

## Result

The shared Necessity Protocol now governs decisions before complexity is added as well as refactors that reduce existing work. The protocol maps user and operator burden, preserves the requested outcome and safeguards, compares only options that could change the decision, and permits keeping the current design or recommending a scope change. It uses task evidence rather than a universal complexity score.

Decision gates now appear at the skills that own the choice:

- Plan sizes research, artifacts, stages, and handoffs to the decision while preserving full scope and required approval.
- Architect records boundary ownership and current scaling, deployment, failure, security, or data-ownership evidence. C4 and ADR artifacts follow the decision's needs; the design allows both a single deployable system and justified service boundaries.
- Build implements the complete approved plan and routes a proposed architecture change back to planning.
- Automation checks whether existing commands and runtimes meet the need before introducing triggers, agents, persistent state, retries, or handoffs. Validation uses the project stack at trust boundaries. Repeated side effects keep safe retry or recovery, and dry-run is conditional on side-effect risk.
- Designer and frontend preserve fields people need to compare, focus and recovery paths, accessible narrow-screen access, and progressive disclosure only for rare detail users can find when needed.

The earlier UI/UX changes and fixtures remain in place. The design skill's visual direction and craft guidance remains unchanged; the new task-burden gate sits alongside it.

## Eval cases

The suite adds five cases and rewrites one existing automation case. Together, the six specified scenarios cover:

1. Architecture that keeps shared booking/account/notification work together while isolating image resizing only when measured contention, independent scaling, and failure containment support it.
2. Build work that preserves an approved import contract, including idempotent retries, partial-failure recovery, validation, and visible status.
3. Refactor review that catches a lost idempotency key, resumable offset, and operator-visible status despite passing happy-path checks.
4. Permission refactoring that consolidates duplicated checks while retaining a real one-implementation policy contract, default deny, boundary validation, and denial audit details.
5. Frontend work that preserves the complete required form, entered values, and recovery, while allowing rare optional information to be disclosed when it remains findable.
6. Automation that reuses an existing Python report command and Pydantic validation, adding only needed schedule glue without a new agent loop, state store, retry framework, or dry-run for a replaceable deterministic output.

Existing automation cases now state why Zod, structured output, or a safe preview is needed when they require it. MCP schemas apply when MCP is the chosen agent-facing interface. The `/plan` command catalog describes the proportional research and artifact path. This does not claim model-judge accuracy or runtime proof.

## Evidence and limits

The implementation keeps one shared procedure in [the Necessity Protocol](../../.forge/skills/ops/core/references/necessity_protocol.md). Its review method preserves approved scope and safeguards, identifies who bears the work, weighs transition and recovery costs, and accepts justified boundaries. The [research note](../research/2026-10-14-complexity-simplicity-evidence.md) treats Brooks, Norman, cognitive-load theory, Tesler, Gall, Maeda, and manufacturing heuristics as prompts with limits, not as a validated software complexity equation. The familiar Einstein/Feynman pairing was not established as a recognized engineering bound, so the implementation adds no such score or law.

The formative Luna walkthrough covered the six specified cases. It exposed one unsupported removal assumption in the optional biography case. The gate and oracle now say that rare use does not prove disuse. The follow-up recommendation kept the optional biography discoverable, retained all four required fields, and preserved form recovery. This is a formative response check, not a governed holdout score or evidence of runtime behavior or outcome lift.

## Verification

All commands ran from the repository root on 2026-10-14.

| Check | Result |
| --- | --- |
| `python3 .forge/tests/run.py` | **PASS**, 324 tests, 1 skipped because PowerShell is unavailable. |
| `python3 .forge/validate_library.py` | **PASS**, 73 skills, 0 errors, 0 warnings. |
| `python3 .forge/validate_skill.py --all .agents/skills --strict` | **PASS**, 73 skills, 0 errors, 0 warnings. |
| `python3 .forge/run_evals.py --all --check` | **PASS**, 352 fixture structures, 0 problems. This checks structure, not model behavior. |
| `python3 .forge/eval_integrity.py` | **PASS**, 464 oracle files, 0 problems. |
| `python3 .forge/routing_eval.py --check` | **PASS**, 49 routing cases across 25 clusters. |
| `python3 .forge/orch_eval.py --check` | **PASS**, 23 orchestration cases, 0 structural problems. |
| Composition, skill graph, and skill manifest checks | **PASS**, generated contracts and docs are current. |
| `python3 .forge/forge.py build --all --host all --dry-run` and `commands --host all --dry-run` | **PASS**, 73 compiled skills and host command outputs are fresh. |
| `python3 .forge/doc_drift.py` | **PASS**, docs agree at v2.5.42, 73 skills, and 38 commands. |
| Scoped fingerprint scan | **PASS**, 166 changed text files, 0 findings. All 29 added files were included; only four pre-existing unrelated research notes were excluded by exact path. |
| `git diff --check` | **PASS**, no whitespace errors. |

The final Forge generation changed only the compiled designer and frontend skill bodies among 57 previously dirty compiled paths. Their reference, eval, script, and asset trees match `.forge` source across all 11 affected skills. The initial build attempt hit the read-only `.agents` sandbox boundary; the authorized escalation regenerated outputs successfully. No commit, version bump, PR, or release was made.
