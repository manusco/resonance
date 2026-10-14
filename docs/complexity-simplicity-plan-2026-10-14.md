# Complexity and simplicity protocol plan

**Status:** Proposed implementation plan
**Date:** 2026-10-14
**Owner:** Resonance maintainers

## Outcome

Make the existing Necessity Protocol apply before complexity enters a solution and when reducing complexity already present in code, architecture, workflows, automation, and UI. Keep one shared protocol and add short, discoverable decision gates only at the skills that own those decisions. Preserve the user's full scope and all safety, accessibility, data integrity, recovery, and operability requirements.

## Assumptions and boundaries

- The existing `.forge/skills/ops/core/references/necessity_protocol.md` remains the single detailed protocol. This work extends it beyond code without creating a second manifesto.
- `.forge/` is the editable source. `.agents/` and other Forge outputs are regenerated and reviewed as derived artifacts.
- The root `AGENTS.md` is the early, always-loaded place for a short universal lock. Extend its existing Four Locks through the actual source/generation path rather than creating another always-loaded document.
- The current dirty UI/UX work belongs to the user and must remain intact. Do not reset, overwrite, or fold it into this work.
- Avoid a blanket edit across skills. Add a gate only where the skill makes the relevant decision.
- User scope is the floor. If a smaller outcome is recommended, show the complete requested result and the smaller option with its tradeoff, then wait for the user's choice.

## Baseline captured before planning

Before inspection, saved `git status --short`, `git diff --stat`, and `git diff --name-only` to:

- Private temporary baseline status and diff-path snapshots (118 status rows, 104 tracked paths); those execution files are not part of the repository.

The pre-existing edits include source and generated changes to designer, frontend, mobile, conversion, and page-audit skills and evals, `.forge/eval_fixture_manifest.json`, `docs/skill-manifest.json`, plus `docs/reports/2026-10-14-uiux-skill-improvements.md` and untracked research material. Preserve every one. This plan is the only repository file added by this planning task.

## Evidence and diagnosis

- The shared protocol already says to trace the real flow, stop at the first sufficient option, preserve protected behavior, and judge ownership surface instead of line count. Its framing and examples are code-oriented.
- `/build` has a late, subjective “would a senior engineer say this is overcomplicated?” check. Backend rejects unrequested abstractions. `/refactor` and `/reviewer` invoke the Necessity Protocol. These do not prevent unnecessary deliverables, workflow steps, architectural machinery, or UI controls from entering the plan.
- `/plan` describes a four-pass process, deep research, architecture sketches, and pass-by-pass check-ins. `/goal` already combines approval gates and suppresses redundant plan approvals. The planning check should remove steps that do not change an outcome or reduce material risk, while preserving the required gate and goal's combined approval.
- Architecture has a simplicity checklist and accidental-complexity prompt, but no evidence test for whether an abstraction or component boundary has a present owner/job and what current demand justifies it.
- The designer already protects simultaneous comparison and makes progressive disclosure conditional on detail being rare/advanced and discoverable before needed. Frontend preserves dense comparison fields. These are good foundations; improve their decision rule with task evidence instead of flattening interfaces or hiding information to make them look simpler.
- Automation has one-job/composable language, but no explicit choice test for when a script, agent, service, memory store, recurring loop, or extra handoff is warranted.
- QA is the verification owner. Avoid requiring an eval change for every skill; use a small number of discriminating cases where the counterexample tests a shared behavior.
- The parallel evidence review identifies an important calibration risk: build's “absolute minimum code” and frontend's Atomic Design guidance can turn “smallest sufficient” into “fewest pieces.” Existing build, refactor, reviewer, and designer rules already cover parts of the method; strengthen only where a specific failure remains.
- The evidence review recommends six eval fixtures split across build (architecture choice and workflow-state preservation), refactor (workflow-state consolidation and permission truth), frontend (form information, recovery, and scope), and automation (recurring report). It also confirms evals judge decision text, not runtime behavior, so preserve real tests as the proof for code changes.

The weakness is discoverability and timing, not absence of the word “simplicity”: core has one late-stage code protocol, while early decisions live in separate owners and several gates use slogans or fixed ceremony without a proportionality test.

## Proposed protocol shape

Extend the current protocol with two concise applications under the same name:

1. **Before adding:** name the user's requested outcome and constraints; find the current owner/path; compare the smallest sufficient alternatives across the relevant surface; state the present demand that warrants every additional component, step, field, option, delegation, memory store, or abstraction. Keep it only when it delivers a required behavior or materially lowers a named risk/cost. Do not use raw line count as the measure.
2. **When reducing:** identify the current job and owner of each candidate; describe what disappears, what handles the job afterward, and the behavior evidence that makes the reduction safe. If nothing simpler preserves the requirement, keep the current design.

The protocol must say plainly that simplicity is not scope reduction. It must retain validation, authorization, accessibility, error recovery, data safety, observability needed to operate/recover, and verification. Abstractions can be justified by multiple real callers, a stable boundary, isolated change, a trust/ownership boundary, a measured operational need, or a tested failure mode. These are evidence prompts, not mandatory architecture patterns.

## Implementation slices

### Slice 1: Shared rule and early lock

**Owner:** Worker A
**Files:** `.forge/skills/ops/core/references/necessity_protocol.md`, `AGENTS.md`, and the verified Forge source/template that emits the root operating standard, if one exists. Add one small regression case to `.forge/tests/test_necessity_lifecycle.py` only if the existing test can meaningfully enforce a durable shared-protocol invariant.

- Extend the current protocol to cover proposed and existing complexity across code, architecture, workflows, automation, and interfaces. Do not create a new named framework or another ladder.
- Add one short early lock to the existing Four Locks: before adding complexity, show its current user/task benefit and simplest sufficient owner; retain complexity when the evidence says a simpler choice would fail a requirement or material safeguard. State that this never silently shrinks requested scope.
- Keep protected-behavior safeguards adjacent to the shared rule.

**Done when:** one source contains the full cross-surface rule; root instructions point to or state the compact version; existing lifecycle checks still have a single canonical protocol path.

### Slice 2: Decision gates at owning skills

**Owner:** Worker B
**Files:** Source templates only where inspection confirms a gap: `.forge/skills/strategy/plan/skill.tmpl.md`, `.forge/skills/strategy/architect/skill.tmpl.md` and `references/system_design_checklist.md`, `.forge/skills/engineering/build/skill.tmpl.md`, `.forge/skills/engineering/automation/skill.tmpl.md`, `.forge/skills/design/designer/skill.tmpl.md`, and `.forge/skills/engineering/frontend/skill.tmpl.md`. Refactor and reviewer already invoke the shared protocol, so prefer eval coverage over duplicating their guidance. Change `.forge/skills/ops/goal/skill.tmpl.md` or `.forge/skills/strategy/brief/skill.tmpl.md` only if inspection finds a specific redundant-ceremony or scope-loss failure not already prevented by their combined-approval and proportionality rules. Do not change backend or QA skill text unless a concrete gap emerges.

- Plan: compare proposed steps, research, artifacts, and handoffs against the requested result; keep only those that change a decision, reduce a material risk, or are needed to verify it. Preserve complete scope and all real approval requirements.
- Architect: justify each new boundary, service, datastore, abstraction, or pattern with present demand, and explicitly keep a simpler topology when it meets the requirements. Use the existing checklist.
- Build: retain the existing gate, but read “minimum” as minimum sufficient ownership against the full approved outcome. Avoid a second gate; make sure it accepts justified boundaries and rejects silent scope cuts.
- Automation: justify triggers, agents, persistent state, retries, and handoffs by an observable need. Do not put hidden maintenance or recovery burden onto the operator.
- Designer/frontend: keep information visible when people need to compare, discover, or act on it together; disclose detail only when users can find it before it is needed. Judge simplification by task completion, missed information, wrong-action rate, and recovery, while preserving accessibility and responsive behavior.
- Reviewer/QA: review complexity at the relevant surface, and test the meaningful failure case rather than adding ceremony or a mechanical complexity checklist.

**Done when:** each edited skill has one concise gate at its actual decision point and points to the shared protocol; no unchanged skill receives a boilerplate insertion.

### Slice 3: Eval coverage and generated integration

**Owner:** Integrator
**Files:** Use the smallest set that covers the evidence-backed counterexamples, initially six source fixtures across `.forge/skills/engineering/build/evals/`, `.forge/skills/ops/refactor/evals/`, `.forge/skills/engineering/frontend/evals/`, and `.forge/skills/engineering/automation/evals/`. Prefer extending an existing eval if its prompt/rubric can carry the case cleanly; otherwise add a fixture. Add plan or architecture cases only if their owners need a distinct oracle after slice 2. Regenerate only corresponding `.agents/skills/**` outputs and relevant manifests using the documented Forge path. Do not overwrite currently dirty UI/UX files; reconcile generated collisions with the baseline and existing authored edits.

Representative cases:

- A clear, small change: do not route it through discovery, council, multiple reviewers, and an approval chain when no material decision or external action requires those steps. Requested deliverables still all appear.
- A bounded application where no independent scaling, deployment, failure, or ownership need exists: decline speculative service decomposition; in the paired case, retain separation when independent scaling and an isolated failure boundary are explicit.
- A workflow-state reduction: keep retries, idempotency, partial-failure recovery, visible outcomes, and authorization. Pair planning and review/refactor cases so one catches omissions before code and one catches them in a diff.
- Duplicated permission checks plus an abstraction with one implementation but a real shared contract: centralize duplicated truth and retain the current abstraction when callers rely on its contract; preserve tenant/resource/action scope, default deny, validation, and denial audit.
- Dense operational comparison: keep the fields that must be compared together; reveal only rare detail that remains discoverable, and verify narrow-width access and screen-reader labels.
- Repeated automation: select the lightest mechanism that meets the stated frequency/reliability need; do not invent a recurring agent, persistence layer, or extra handoff. Preserve recovery and human approval for irreversible actions.
- A shorter form or plan that hides required information, loses entered context on failure, or drops a requested deliverable: reject the cut and explain the lost behavior.

**Done when:** eval expectations reward justified simplicity and justified complexity; generated skills and manifests match their `.forge/` source; the existing UI/UX baseline remains present in the final diff.

## Verification and proof

- Check the final diff against the captured pre-task path list before regeneration, and inspect every collision in `.agents/`, `.forge/` UI/UX files, manifests, and the existing report/research artifacts.
- Run the focused necessity lifecycle test and the changed evals. Verify the six fixtures pass both sides of the decision: needless machinery is rejected, while justified boundaries and required invariants survive. Run the repository's skill generation/check command and confirm generated outputs match source. These are later implementation checks, not claimed as run for this plan.
- Manually evaluate each representative case against scope completeness, unnecessary ceremony, justified abstraction, comparison/discoverability, safeguards, and operator burden. A shorter answer or fewer files alone is not a pass.
- Confirm no eval passes by merely repeating a keyword and no process update adds a blanket gate to unrelated skills.

## Explicit non-goals

- No 75-skill-wide instruction sweep, new manifesto, new general-purpose automation or complexity scoring system, or changes to the user's existing UI/UX work.
- No shrinking an explicitly requested scope, removing safety or accessibility requirements, or equating visible simplicity with hiding information.
- No edits to generated outputs by hand unless Forge tooling cannot safely regenerate a file; if that exception is needed, document the exact file and reason.

## Open implementation evidence

The parallel research artifacts `docs/research/2026-10-14-complexity-simplicity-evidence.md` and `docs/research/2026-10-14-simplicity-eval-plan.md` informed this plan. Their source-derived recommendations are useful calibration; their proposed vocabulary and fixture list do not require new measures or blanket gates. The first implementation review should settle whether the root lock belongs in `AGENTS.md` alone or also needs a Forge-owned source, based on the actual generation path.
