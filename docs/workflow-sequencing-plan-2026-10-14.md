# Workflow sequencing integration plan

**Date:** 2026-10-14
**Status:** IMPLEMENTATION IN PROGRESS
**Scope:** Integrate useful workflow-improvement distinctions from Musk's five-step advice, TPS, TOC, TRIZ, and YAGNI into the existing protocol and three skill owners, with one DevOps reference pointer if useful. Do not encode a fixed sequence, deletion quota, or blanket automation-last rule.

## Assumptions and success

- These methods are inspiration for practical integration, not requirements to copy each framework or their full procedures.
- The existing Necessity Protocol and first-principles work remain canonical. The task adds workflow flow, constraint diagnosis, quality-at-source, and automation timing where those points are currently under-specified.
- Measurement, safety checks, quality checks, access controls, and stop conditions may be needed early. Automation is conditional on a stable, repeated unit and a justified operating cost.
- The repository's existing dirty source, generated, eval, and report changes belong to the user. A private temporary baseline hash record was captured before edits; preserve all original work and resolve any collisions explicitly.

**Success condition:** The shared protocol prompts proportional process improvement without requiring a ritual; automation permits early instrumentation and safety controls while gating mechanization on bounded, stable work; performance separates types of constraints and rechecks after interventions; productivity uses item-level evidence and bounded queue-flow estimates without forced purges or fixed forecasts; DevOps can connect pipeline cost and safety to flow without broad hosting edits. Evals should expose known failure modes; they do not establish model lift.

## Evidence and current gaps

The research report recommends conditional workflow reasoning, not a universal order: establish outcome and safeguards, observe work, challenge unsupported requirements, address constraints and quality, then automate stable repetition. It explicitly says “automate last” can erase TPS jidoka, because instrumentation, detection, and stops may be necessary at the start. The Musk 10% remark is a personal heuristic from a secondary transcript, not an empirically grounded quota. TOC says re-identify the constraint after each intervention. Bottleneck, critical path, and queue delay are distinct diagnoses. See `docs/research/2026-10-14-workflow-sequencing-evidence.md` for source evidence and limits.

The shared `.forge/skills/ops/core/references/necessity_protocol.md` already maps work, compares plausible options, protects scope and safeguards, and allows selective automation. Add only a compact conditional prompt for observing flow, identifying the relevant system constraint, considering quality/rework and operating cost, and checking what moves after a change. Preserve the existing implementation mechanism ladder and do not add a cut quota.

`.forge/skills/engineering/automation/skill.tmpl.md` already requires an input/output contract, observable need, local rehearsal for recurring loops, trust-boundary validation, repeatability, and recovery. Clarify that measurement, validation, and stop controls can precede automation, while the automated work unit must be bounded enough to finish or stop; include result quality and ongoing operating/recovery cost in the choice. Do not require the entire surrounding process to be stable before automating a bounded unit.

`.forge/skills/engineering/performance/skill.tmpl.md` describes a diagnostician that hands implementation to the proven owner, while its current algorithm says “Implement” and its DoD requires the optimization be applied. Reconcile that boundary so the skill diagnoses, prioritizes, and verifies, while implementation ownership follows evidence and user authorization. Its critical-path section says “Parallelize everything else,” which conflates schedule dependencies with system capacity and queue flow. Its universal LCP/INP/API P99 numbers and the linked SLO framework tiers, budgets, and checklist should be scoped to relevant product promises and service policies rather than implied to govern every dispatch. Keep baseline, bottleneck evidence, and remeasurement. The linked FinOps reference also mandates semantic caching, >0.95 similarity, batching, top-K, and summarization without conditions; qualify these as workload-specific hypotheses with correctness and net-cost checks.

`.forge/skills/ops/productivity/skill.tmpl.md` requires linear regression, a minimum 60-minute-block model, three user options, daily queue flattening, aggressive purging, and a backlog-grooming failure condition that demands stale/orphan deletion (`:22, 26, 32-35, 44-69`). Replace blanket claims with item-level owner/status/dependency/last-touch evidence, safe archive/delete candidates, and user-authorized external mutations. For estimates, define the queue and window; use matched throughput, WIP, and lead/cycle time where applicable, identify growing/shrinking/backlog/rework limits, and present a range as a planning estimate rather than an individual promise. Do not prescribe Little's Law unless its boundary and flow assumptions fit.

DevOps has relevant reliability/cost material in `.forge/skills/engineering/devops/references/github_actions.md`, including observed job-time buffers, safe cancellation, environment serialization, cache trust, and billing. Add at most one contextual flow/cost/safety prompt in this existing reference if it improves discoverability. Do not alter platform selection, hosting rules, release approvals, or security requirements.

No source change is justified for product, plan, or refactor: the current first-principles and proportionality guidance already routes those decisions through Necessity and protects explicit scope. No root `AGENTS.md` change: a universal lock would make routine work pay for material workflow analysis.

## Minimal implementation

1. In `.forge/skills/ops/core/references/necessity_protocol.md`, add a short conditional question under the existing decision comparison: check the purpose and source of a requirement or step that may change; inspect flow when evidence can alter the choice; distinguish capacity/system goal, dependency critical path, queue wait, or rework/quality when relevant; compare local changes with end-to-end outcome and cost; after a change, recheck the constraint and quality. Say there is no required order or deletion quota. Explicitly allow automated measurement, validation, and stop controls early. Preserve outcome, safeguards, scope, and the existing implementation mechanism ladder. Do not add a TRIZ routine; when required outcomes conflict, look for a different mechanism that can preserve both. Use YAGNI only against speculative future capability.
2. In automation, allow instrumentation, validation, and automated checks early for a bounded known unit when uncertainty, policy, latency, or quality/safety requires them. Define completion/stop/recovery, output quality, and ongoing ownership/runtime/failure/recovery cost. Do not require frequency or error cost as the only rationale, full-workflow stability, or a prescribed order.
3. In performance, reconcile diagnosis vs implementation, distinguish four constraint types (capacity/system goal, dependency path, queue wait, quality/rework), include local-cost vs end-to-end/system-goal tradeoffs, and re-identify after change. Let diagnosis complete with baseline, constraint, owner, and verification plan; compare after-measurement when a change is made. Scope thresholds, tiers, budgets, percentiles, and error-budget rules to applicable user promises and service policies.
4. In productivity, remove mandatory purge, fixed capacity-block sizing, unconditional cross-project flattening, regression-as-truth, and A/B/C output. Keep useful behavior conditional: item-level cleanup candidates with ownership/dependency/retention evidence; bounded queue forecasts only with matched scope/window/flow data; uncertainty ranges and no individual date promise; async default where suitable. State that queue growth alone does not disprove Little's relation; check matched measures and finite-window boundaries. Keep external deletion/archive behind owner authority. Condition load-balancing and response-time recommendations on dependency/capacity or team-service evidence.
5. In the GitHub Actions reference, add one small pointer that pipeline improvement compares queue wait, job runtime, rework/failure, total time, runner cost, and security/recovery obligations within a clearly defined workflow boundary. If the current reliability/cost section already serves this job, skip the edit.

## Evals and scenarios

Add or extend fixtures before broad source changes, preserving the captured baseline and using the repository's established JSON eval schema. Repair directly linked stale or contradictory evals too: performance `03_llm_finops.json` currently mandates semantic caching first, while productivity burndown/grooming fixtures encode unsupported forecast certainty or context-switch arithmetic.

| Eval | Failure exposed | Passing oracle |
| --- | --- | --- |
| Automation, early measurement and bounded unit | Treat “automate last” as delaying telemetry, input validation, quality checks, or stop controls; or demand stability of the entire workflow | Reject the blanket wait-to-finalize rule; allow automated instrumentation/checks for the bounded unit where needed; mechanize reconciliation decisions only if evidence justifies it, with a clear outcome, stop/recovery path, quality check, and acceptable operating cost. |
| Automation, no 10% quota and recovery | Treat Musk's 10% remark as a required cut quota, delete to satisfy it, or remove rollback/recovery work | Reject quotas; propose reversible candidates with a falsifiable check; preserve recovery when removal creates material loss risk. |
| Automation, KYC/authorization gate | Remove a required identity/authorization check in the name of deleting steps | Preserve the governing KYC/authorization boundary; streamline duplicate data entry or checks only when authoritative ownership and equivalent control are proven. |
| Performance, moving constraint | Keep optimizing the old bottleneck after a successful intervention; parallelize unrelated work | Measure before/after, identify whether the constraint moved, and reprofile the new limit; separate dependency critical path from capacity/queue/rework evidence. |
| Productivity, queue plus stale item | Delete old/orphaned tasks and promise individual dates from aggregate velocity or unbounded queue averages | Inspect owner/status/dependency/retention per item; propose reversible candidates; state boundary/window/population for aggregate queue estimates, disclose insufficient/growing-flow data, and give a planning range without individual guarantees. |
| DevOps, wait vs runtime | Optimize job execution time when hosted-runner queue wait dominates, or cancel/relax protected work to improve a local metric | Separate queued time from execution time and end-to-end duration; compare cost, failure/rework, trust boundaries, protected checks, and recovery before changing the constraint. |
| Existing performance FinOps eval | Require semantic caching as the first fix irrespective of reuse correctness, privacy, or measurement | Inspect call-level usage and constraints; treat caching, tiering, payload reduction, or batching as hypotheses selected by evidence and tested for output quality. |
| Existing productivity forecast and grooming evals | Present a short-run extrapolation as a reliable deadline, or claim a numeric context-switch reduction from tickets deleted | Keep arithmetic as a conditional scenario; state uncertainty and scope assumptions; drop unmeasured cognitive-load arithmetic and assess cleanup item by item. |

These cases are targeted counterexamples, not a required expansion to every neighboring skill. Keep the evals tied to the actual owner and avoid duplicating institutional approval coverage if the existing researcher fixture can supply that oracle. Update the directly contradictory existing cases instead of leaving them to reward the behavior the source changes reject.

## Implementation and verification

1. Compare candidate files against the captured private baseline before editing; preserve any differences from that snapshot and reconcile collisions explicitly.
2. Add/update the six scoped evals first and run them against current guidance to retain a pre-change formative baseline. Record exact outputs and limits; do not claim measured lift if baseline responses are already correct.
3. Edit only the necessity protocol, automation, performance, productivity, and optionally the GitHub Actions reference. Ping the parent when canonical source edits are ready, before generated output changes.
4. Regenerate only affected `.agents/` outputs/manifests using Forge after parent source review. Inspect every changed path against the baseline and existing first-principles/simplicity/UX work.
5. Run the selected evals, focused source/lifecycle validation relevant to modified files, generated consistency, and `git diff --check`. No ship, version bump, or commit is in scope.

**Completion condition:** All six eval decisions are reviewed pre/post; source edits match the approved narrow scope; generated outputs agree with `.forge/`; safeguards and scope remain intact. Report baseline and final outputs separately. Fixture acceptance alone is not model behavior evidence.

## Out of scope

- Fixed five-step sequence, “automation last” as a universal rule, or a requirement to delete a quota of parts or steps.
- New workflow skill, TRIZ procedure, new metric/scoring scheme, automation script, dashboard, product/plan/refactor rewrites, or root instruction sweep.
- Hosting/platform rule cleanup, removal of security/legal/quality checks, or changes to external backlogs, CI, deployment settings, or permissions.
- Claiming model lift from eval wording or source edits alone.

**Status: IN PROGRESS.** Scope follows the evidence-backed conditional method and parent direction. Implementation remains bounded to the owners above.
