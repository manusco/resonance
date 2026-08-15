---
name: resonance-ops-second-opinion
description: Independent second-model review for concrete diffs and decision artifacts. Dispatches a diff or confirmed plan/ADR/goal contract to a configured independent reviewer, then reconciles the result so disagreement surfaces the bug or assumption one model rationalizes away. Use before merging a risky change, as the final gate in a goal loop, before a high-risk one-way decision, or when the user asks for a second opinion, cross-model review, independent check, or decision review.
archetype: procedure
---

# /resonance-ops-second-opinion: two models catch what one misses

> **Role:** the independent second reviewer, on a different model.
> **Invoked as:** `/second-opinion` (to cross-check a change with another model).
> **Input:** A diff, PR, confirmed goal contract, ADR, or concrete plan. Optionally the primary review.
> **Output:** For diff mode, a reconciled findings list ranked P0-P3. For decision mode, a reconciled decision critique: assumptions, evidence gaps, tradeoffs, reversal conditions, and strongest objection.
> **Definition of Done:** A configured independent reviewer has reviewed the artifact, or a manual prompt was produced and then answered by a separate reviewer. Agreements and disagreements are explicit. Every finding is verified against the actual artifact, not accepted on the second model's word. Empty, failed, same-identity, or unanswered reviews do not satisfy the gate.

After grounded tests, an independent second model is the strongest quality multiplier there is. One model rationalizes its own blind spots; a different model does not share them. This skill runs that check and reconciles the two views. It does not replace the primary review; it pressures it.

## Independent Review Policy

Use independent review as a policy, not as a model ranking.

- Routine and reversible work uses the primary model plus grounded checks.
- A concrete high-risk artifact gets one configured independent reviewer.
- Unresolved evidence, model conflict, or a one-way decision goes to the human or a qualified domain authority.

Independence means a different configured reviewer identity, not a role-played persona and not an unverified command alias. A second model is evidence to reconcile. It is never the done signal.

Do not recurse. Run at most one decision review per artifact hash and the final diff review before ship.

## Prerequisites (fail fast)

- [ ] There is a concrete artifact to review: a diff for `diff` mode, or a confirmed goal contract, plan, or ADR for `decision` mode. A vague "is this good" is not a second-opinion request.
- [ ] You know what the artifact is supposed to do, so the second reviewer can judge intent.
- [ ] Reviewer identity is configured and independent, or the manual path is explicitly marked incomplete until answered.
- [ ] The artifact is not too large and does not contain secrets that would leave the machine.

## Algorithm

Copy this checklist and tick items as you go.

1. **Choose the mode.** Use `diff` for code changes and PRs. Use `decision` for confirmed goal contracts, ADRs, adoption verdicts, migration plans, and one-way decisions before code exists. Do not use this for vague brainstorming or creative taste. → verify: the artifact has a mode.
2. **Have a primary view.** Use the findings from `/review-pr`, or read the diff/decision yourself against the right rubric. This is the baseline the second model pressures. → verify: a primary list of findings or decision risks exists (may be empty).
3. **Dispatch to a second model.** Run `py .forge/second_opinion.py --mode diff --context "<what it does>"` for diffs, or `py .forge/second_opinion.py --mode decision --artifact decision.md --context "<decision>"` for decisions. Configure the reviewer with `--model-cmd` or `RESONANCE_REVIEW_CMD` and an independent `--reviewer-id` or `RESONANCE_REVIEWER_ID`. Without a configured reviewer, it prints the manual prompt and exits incomplete. → verify: a second-model review exists and is independent, or the manual prompt was produced and later answered.
4. **Reconcile.** Compare the two:
   - **Agreements**: both flagged it. High confidence, fix first.
   - **Only the second model flagged it**: investigate. It may see a real blind spot, or it may be wrong for this codebase. Verify against the code before acting.
   - **Only the primary flagged it**: keep it; the second model missing it is not exoneration.
   → verify: every finding is tagged agreement, second-only, or primary-only.
5. **Verify each finding against the actual artifact.** Do not accept the second model on its word. Cross-model reviews still hallucinate, and a model can flatter or contradict for reasons unrelated to the artifact. Open the file, confirm the path or decision text. → verify: each surviving finding traces to real evidence.
6. **Report.** In diff mode, rank P0-P3 by user harm and lead with agreements. In decision mode, do not invent file lines or P severities; report assumptions, evidence gaps, tradeoffs, reversal conditions, strongest objection, and required change. → verify: the report separates confidence levels.

## Recovery

- No second-model command configured → run the printed prompt in another model (Codex, Gemini, a local model) and paste its findings back, then reconcile. Until then the gate is incomplete.
- Reviewer identity is missing or the same as the author/primary reviewer → do not claim independence. Reconfigure or use manual review.
- Dispatch fails or returns empty output → treat the gate as failed or incomplete, not green.
- Artifact is too large or contains secrets → reduce, redact, or keep review local. Do not send sensitive dumps to an external reviewer.
- The second model floods low-value nits → keep only what verifies against the code and matters to the user. A second opinion is signal, not a second style guide.
- The two models flatly contradict on a P0 → do not average them. Read the code path and decide on the evidence. If still unresolved, escalate with both views.

## Out of Scope

- The primary review itself (delegate to `/review-pr`, `resonance-ops-reviewer`).
- Fixing the findings (delegate to the engineer).
- Creative direction, open-ended brainstorming, or final business judgment. Domain skills recommend; the user decides.

## Reference Library

- **[Multi-Model Review](references/multi_model_review.md)**: How to dispatch, reconcile, and account for cross-model bias.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
