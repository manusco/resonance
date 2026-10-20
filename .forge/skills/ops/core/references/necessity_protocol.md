# Necessity Protocol

Use this when a proposal adds complexity or reduces what already exists. First state the requested outcome, constraints, and observable behavior that must survive. Simplicity governs how the outcome is delivered, never how much of the user's requested scope is delivered.

## Map the current work

Trace the code, architecture, workflow, automation, or interface affected by the decision. Name the owner and path, its job, and what fails if it is missing. Map who bears the work when that changes the choice; include users, developers, operators, support, platform, or auditors as relevant. Record unknowns instead of inventing reasons.

## Compare options

For implementation choices, stop at the first option that fully satisfies the requirement: Delete or decline; Reuse the codebase; Use the language runtime; Use the native platform; Use an installed dependency; then Write the smallest local implementation. Across surfaces, consider only plausible choices that could change the decision, such as absorbing work into an existing owner, redesigning the domain or flow, simplifying or optimizing the remainder, automating selectively, or retaining it. This is not a required checklist or cut quota.

For material choices, state what burden or risk the preferred option removes or creates and who bears it, plus relevant migration, training, maintenance, operational, or recovery cost. Show present evidence for additions. For reductions, say what disappears, what handles its job afterward, and which behavior check makes the change safe. A valid shared contract or boundary can justify an abstraction with one implementation. Choose the option that meets the full outcome and safeguards with the least unsupported burden, not the fewest lines or concepts by rule. Do not treat an optional or rare current capability as unused without checking who relies on it and what scope its removal changes.

For a material workflow change, first state the outcome and safeguards, and check the purpose and source of the requirement or step that may change. Inspect current flow when evidence can change the choice; do not turn this into a fixed review of every step. Distinguish a capacity constraint, dependency critical path, queue wait, or quality/rework limit when it matters. Consider deletion or simplification, flow changes, and selective automation in the order the evidence supports, with no deletion quota. Measurement, validation, and stop controls, including automated ones, may be needed early. Compare local speed with end-to-end flow, quality, operating cost, and recovery, then recheck the constraint after a change. Use YAGNI to defer speculative capability, not current safeguards. When required outcomes conflict, look for another mechanism that preserves both before proposing a scope change. This prompt is for material workflow decisions, not routine edits.

## Worked anchors

These illustrate decisions, not default patterns; use them only when the stated conditions hold.

- **Form:** Before, users re-enter a required value already held by an authoritative record. After, derive it from that record while keeping other required data visible and recoverable on failure. Do not hide a required field to shorten the form.
- **Workflow:** Before, separate states only repeat handoffs. After, consolidate those states while retaining retries, idempotency, recovery from partial failure, and a visible outcome.
- **Permissions:** Before, duplicated checks drift. After, centralize the shared rule while preserving tenant, resource, and action scope, default deny, and denial audit; keep a one-implementation abstraction when its shared contract has real callers.

## Preserve and verify

Never remove or weaken trust-boundary validation, authorization, error handling that prevents corruption or data loss, accessibility, required fallbacks, operational observability needed for recovery, tests for non-trivial logic or known regressions, explicit user scope, or approved constraints. Include edge and failure paths when they affect those guarantees. A smaller implementation is not evidence that a cut is safe.

Before a material change, state a falsifiable prediction and its baseline or representative task. Use an observable measure suited to the decision, such as completion time, errors, handoffs, maintained parts, or recovery effort. Do not invent a combined complexity score or imply that burden is conserved: work can disappear, move, or change form. If evidence is unavailable, say so. For an outcome that can only be observed later, record how and when it will be checked; do not claim the outcome is proven early.

If no simpler option meets the requirement, keep the current design. If the full scope itself should change, present that as a recommendation with its consequence and wait for the user's decision; do not report a silent reduction as completion.
