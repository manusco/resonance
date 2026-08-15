# Multi-Model Review: dispatch, reconcile, and de-bias

> The value is independence. A second model does not share the first model's blind spots, so agreement is strong evidence and disagreement is where the interesting bugs hide. The risk is treating the second model as an oracle. It is not. Verify everything against the code.

## Why two models beat one

A model reviewing its own or a sibling model's work tends to rationalize the same mistakes and flatter the same choices. A different model family, given only the diff and a strict rubric, brings a genuinely independent read. In practice, the findings both models agree on are almost always real, and the ones only the second model raises are the highest-value thing to investigate, because they are what your primary process missed.

## How to dispatch

Use `.forge/second_opinion.py`. It has two modes:

- `--mode diff`: reads `git diff HEAD` by default and uses the code-review rubric.
- `--mode decision --artifact decision.md`: reviews a concrete goal contract, ADR, adoption verdict, or plan before code exists.

Configure a reviewer with `--model-cmd "codex exec"` or `RESONANCE_REVIEW_CMD`, and set an identity with `--reviewer-id` or `RESONANCE_REVIEWER_ID`. Set `--author-id` or `RESONANCE_AUTHOR_ID` when you know the primary reviewer. If the identity is unknown or the same, the review is not independent.

With nothing configured, the script prints the prompt so you can run it in another model by hand and paste the result back. That is incomplete until answered and reconciled.

Give it context (`--context "adds JWT refresh rotation"` or `--context "adopts auth provider"`) so the second model judges intent, not just syntax.

## How to reconcile

Sort every finding into three buckets:

- **Agreement (both models):** highest confidence. Fix these first.
- **Second-model-only:** a candidate blind spot in your primary review. Investigate each. It is either a real miss or a model error for this codebase. The code decides.
- **Primary-only:** keep it. The second model not seeing it is not a clearance.

Then rank the survivors P0-P3 by user harm, using the same taxonomy as `resonance-ops-reviewer`, and lead the report with the agreements.

Decision mode uses a different report shape. It does not invent line numbers or P severities. It asks:

- Which assumptions are unproven?
- Which constraints conflict?
- Which tradeoff is hidden?
- What would make the decision reversible?
- What is the strongest objection?
- What evidence must change the recommendation?

## De-bias: the second model is not an oracle

- **Verify against the code.** Cross-model reviews still hallucinate lines, misread context, and invent problems. Open the file and confirm the path before you act on any finding.
- **Watch for sycophancy and its opposite.** A model may agree to be agreeable, or contradict to look rigorous. Neither is evidence. Only the code is.
- **Do not average disagreements.** If the two models split on a P0, read the path and decide on the evidence, do not split the difference.
- **Keep it to substance.** A second opinion is for correctness, safety, and integrity, not a second pass of style nits. Drop the noise.
- **Protect the boundary.** Do not dispatch oversized artifacts or secrets. Redact first or keep review local.

## When to run it

- Before merging a risky or security-sensitive change.
- As the final gate in a `/goal` loop, before proposing `/ship`.
- Before a concrete one-way decision where the wrong call has material cost.

Do not run it for vague brainstorming, simulated councils, or taste calls.
