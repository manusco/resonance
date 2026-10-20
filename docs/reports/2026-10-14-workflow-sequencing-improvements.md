# Workflow sequencing improvements

**Status:** DONE_WITH_CONCERNS
**Date:** 2026-10-14
**Scope:** Conditional workflow-improvement guidance across Necessity, automation, performance, productivity, and GitHub Actions reliability/cost guidance.

## Result

The workflow material now treats requirement review, removal, simplification, acceleration, and automation as candidate interventions, not a fixed sequence. It checks why a requirement exists and what outcome it protects, then follows evidence about the work. It rejects a deletion quota and does not impose “automate last.” Measurement, validation, quality checks, and stop controls may happen early. Automation still needs a bounded unit, clear completion and recovery behavior, and a reason to carry its runtime and maintenance cost.

The source is `.forge/`. No root instruction sweep or new workflow skill was added. Product, plan, and refactor guidance was left alone because it already reaches the shared Necessity and first-principles owners; refactor also has a distinct code-level safety sequence worth preserving. The existing implementation mechanism ladder remains. Musk's reported 10% add-back is treated as a personal heuristic, not a deletion target.

## Owner changes

In `.forge/skills/ops/core/references/necessity_protocol.md`, the **Compare options** section now asks for the purpose and source of a requirement or step before a material workflow change. It asks agents to inspect flow only when that evidence can change the choice, distinguish capacity limits, dependency paths, queue wait, and rework/quality where relevant, compare local speed with end-to-end outcome and cost, and check the constraint again after an intervention. Automated measurement and stop checks may come first. It states there is no fixed order or quota, keeps user scope and safeguards, and leaves the existing implementation-mechanism ladder intact.

In `.forge/skills/engineering/automation/skill.tmpl.md`, **Choose the lightest sufficient mechanism** now permits early instrumentation, validation, or automated checks for uncertainty, policy, latency, and quality/safety needs. For example, it can instrument duplicate cases around a still-manual KYC decision process while keeping identity verification, sanctions escalation, and human stops for conflicting records. It does not require the entire process to be finalized before that bounded unit can be automated. It checks completion, stop and recovery paths, output quality, runtime, maintenance, and recovery cost.

In `.forge/skills/engineering/performance/skill.tmpl.md`, the DoD now supports a diagnostic-only result: baseline, measured constraint, implementation owner, and verification plan. After-measurement applies when a change is actually made. The algorithm hands implementation to its owner, as its skill contract says. It distinguishes a dependency path from capacity, queue delay, and rework; removes “parallelize everything else” and the blanket ranking of structural changes above syntax-level changes. It prioritizes measured impact. Its SLO targets now depend on the service promise or applicable target. The linked `references/slo_framework.md` labels tiers, budgets, percentile choices, and error-budget rules as contextual examples or service policy, not defaults.

The directly linked `.forge/skills/engineering/performance/references/llm_finops_protocol.md` and `evals/03_llm_finops.json` no longer demand semantic caching first, a 0.95 similarity threshold, prompt batching, a top-K cap, or summarization. They select caching, model tiering, payload reduction, and batching from measured usage, latency, quality, privacy, freshness, correctness, and net cost. Similarity alone does not justify sharing a response across users or contexts. Any savings estimate names its assumptions.

In `.forge/skills/ops/productivity/skill.tmpl.md`, backlog grooming now treats age or missing assignment as review signals, not deletion criteria. Each candidate needs owner, status, dependency, duplicate, and retention evidence; archive or deletion follows authorized owner action. Capacity depends on task duration and dependencies, with no fixed 60-minute block. Queues are combined only when they serve the same priority decision. Historical throughput is a planning input, not “truth.” When Little’s Law is useful, the queue boundary, population, window, arrivals, completions, and work-in-progress must match. Growth alone does not disprove the relation; finite-window boundary effects still need review. Aggregate averages do not promise an individual finish date. The skill also no longer forces linear regression, cross-project flattening, a backlog purge, a fixed three-option answer, or a 5-minute chat threshold. Communication response measures are compared with stated service expectations, and archive candidates with owner and retention needs.

In `.forge/skills/engineering/devops/references/github_actions.md`, one paragraph asks pipeline work to measure runner queue wait separately from job runtime and rework over the same workflow boundary. It compares end-to-end time with runner cost, test quality, and required security/release checks, then checks whether the constraint moved. Hosting, release gates, and permission policies were not changed.

## Before and after

- A 24-minute CI pipeline has 13 minutes of runner wait, 7 minutes in integration tests, and 4 minutes in other work. After runner capacity is added, queue wait falls to 1 minute. The performance case now expects the agent to verify whether integration work is on the dependency critical path and needed for the target before treating it as the next constraint, then measure again.
- A 40-minute KYC reconciliation sometimes duplicates cases. Automated timestamps and duplicate counters can be introduced around manual reconciliation now; KYC checks and stop/escalation behavior remain intact. The choice to automate decisions later depends on measured quality and operating cost.
- A queue grows from 50 to 80 issues in a month. “Old” and “unassigned” produce review candidates, not automatic deletion. The forecast must define the queue and period, disclose the growth and uncertainty, and avoid individual date promises.
- A suggestion to add back 10% of removed deployment steps is treated as a personal heuristic, not a target. The release rollback check and recovery owner stay unless equivalent protection is proven.

## Fixtures and verification

Added fixtures:

- `.forge/skills/engineering/automation/evals/05_early_measurement_bounded_unit.json`
- `.forge/skills/engineering/automation/evals/06_no_cut_quota_recovery.json`
- `.forge/skills/engineering/performance/evals/05_constraint_moves.json`
- `.forge/skills/ops/productivity/evals/05_queue_flow_and_item_safety.json`
- `.forge/skills/engineering/devops/evals/06_queue_wait_vs_runtime.json`

Revised contradictory oracles in performance FinOps and productivity async, burndown, grooming, and planted-defect cases. Updated `.forge/eval_fixture_manifest.json` for intentional oracle changes.

Executed checks: `python3 .forge/eval_integrity.py` reports 472 oracle files and 0 problems. After regeneration, `python3 .forge/run_evals.py <skill> --check` reports 0 structural problems for automation (7 cases), performance (5 cases), productivity (5 cases), and DevOps (6 cases). `python3 .forge/run_evals.py --all --check` reports 360 cases and 0 structural problems. `python3 .forge/validate_skill.py --all --strict .agents/skills` passes all 73 skills with 0 errors and 0 warnings. `python3 .forge/validate_library.py` passes 73 skills with 0 errors and 0 warnings. `python3 .forge/forge.py build --all --dry-run` reports all compiled skills fresh. `python3 .forge/doc_drift.py --check` reports docs and manifests in sync at v2.5.42. The repository test runner, `python3 .forge/tests/run.py`, reports 324 tests passed and one skipped because PowerShell is unavailable. `git diff --check` passes.

The parent scope review compared the candidate changes with a captured private baseline and found changes limited to approved source, generated output, and eval-manifest scope. Its path/hash snapshots are private temporary evidence and are not included here. The incremental tracked diff contained 25 approved paths: seven guidance sources, five existing evals, generated mirrors/resources, and the eval manifest. The seven canonical guidance files gained 589 net words, excluding evals and generated copies.

The formative walkthrough used six initial samples, two follow-up samples, and a final two-query read. These private temporary samples are not included here. They are source-grounded synthetic outputs, not scored evaluations. The final read correctly treats queue growth as insufficient by itself to disprove Little's relation and calls for matched measurements and finite-window checks. Its automation answer permits checks now and automating a bounded step, but does not explicitly say automated traces can start now. The source guidance and golden fixture do state that allowance. This remaining wording ambiguity is recorded rather than treated as a full pass.

The eval checks validate fixture structure only. The formative walkthrough is synthetic and does not measure behavior lift. No runtime behavior, live scored evaluation, or measured lift is claimed.

**Status: DONE_WITH_CONCERNS.** The approved sources, generated mirrors, fixture manifest, and repository checks are complete. The synthetic walkthrough leaves one wording ambiguity about explicitly starting automated traces early, and no measured model lift is available.
