---
name: resonance-ops-second-opinion
description: Independent second-model code review. Dispatches a diff to a different model than the author or primary reviewer, then reconciles the two reviews so cross-model disagreement surfaces the bug one model rationalizes away. Use before merging a risky change, as the final gate in a goal loop, or when the user asks for a second opinion, a cross-model review, or an independent check on a diff.
archetype: procedure
---

# /resonance-ops-second-opinion: two models catch what one misses

> **Role:** the independent second reviewer, on a different model.
> **Invoked as:** `/second-opinion` (to cross-check a change with another model).
> **Input:** A diff, a PR, or "cross-check this change." Optionally the primary review.
> **Output:** A reconciled findings list: what both models agree on (high-confidence, fix first) and where they disagree (investigate), ranked P0-P3.
> **Definition of Done:** A second model has reviewed the diff (or the manual prompt was produced when none is configured). Agreements and disagreements are explicit. Every finding is verified against the actual code, not accepted on the second model's word.

After grounded tests, an independent second model is the strongest quality multiplier there is. One model rationalizes its own blind spots; a different model does not share them. This skill runs that check and reconciles the two views. It does not replace the primary review; it pressures it.

## Prerequisites (fail fast)

- [ ] There is a concrete diff or change to review. A vague "is my code good" is not a second-opinion request.
- [ ] You know what the change is supposed to do (so the second model can judge intent, not just syntax).

## Algorithm

Copy this checklist and tick items as you go.

1. **Have a primary review.** Use the findings from `/review-pr`, or read the diff yourself against the reviewer taxonomy. This is the baseline the second model pressures. → verify: a primary list of findings exists (may be empty).
2. **Dispatch to a second model.** Run `py .forge/second_opinion.py --context "<what it does>"` (it reviews `git diff HEAD` by default; pass `--diff` for a file). Configure the second model with `--model-cmd` or `RESONANCE_REVIEW_CMD`; without one, it prints the prompt to run by hand. → verify: a second-model review exists, or the manual prompt was produced and answered.
3. **Reconcile.** Compare the two:
   - **Agreements**: both flagged it. High confidence, fix first.
   - **Only the second model flagged it**: investigate. It may see a real blind spot, or it may be wrong for this codebase. Verify against the code before acting.
   - **Only the primary flagged it**: keep it; the second model missing it is not exoneration.
   → verify: every finding is tagged agreement, second-only, or primary-only.
4. **Verify each finding against the actual code.** Do not accept the second model on its word. Cross-model reviews still hallucinate, and a model can flatter or contradict for reasons unrelated to the code. Open the file, confirm the path. → verify: each surviving finding traces to a real line.
5. **Report.** Rank P0-P3 by user harm. Lead with the agreements. Note where the models disagreed and how you resolved it. → verify: the report separates confidence levels.

## Recovery

- No second-model command configured → run the printed prompt in another model (Codex, Gemini, a local model) and paste its findings back, then reconcile. Note the manual step in the report.
- The second model floods low-value nits → keep only what verifies against the code and matters to the user. A second opinion is signal, not a second style guide.
- The two models flatly contradict on a P0 → do not average them. Read the code path and decide on the evidence. If still unresolved, escalate with both views.

## Out of Scope

- The primary review itself (delegate to `/review-pr`, `resonance-ops-reviewer`).
- Fixing the findings (delegate to the engineer).

## Reference Library

- **[Multi-Model Review](references/multi_model_review.md)**: How to dispatch, reconcile, and account for cross-model bias.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (log durable learnings to `.resonance/learnings.jsonl`).

> **Model note (Claude):** Strong native reasoning. Do not narrate "let me think step by step" or pad with chain-of-thought; think, then act. Prefer the dedicated file and search tools over shell. State assumptions briefly, then proceed.
