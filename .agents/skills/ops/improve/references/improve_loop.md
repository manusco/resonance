# The Improve Loop: refine by measurement, not by feel

> A skill is not better because it reads better. It is better when the same eval that flagged it now scores higher, with the rubric held at least as strict. Re-measurement is the gate; everything else is a proposal.

## Why the gate is non-negotiable

A model editing its own instructions and judging the result by reading it is the exact loop that drifts: it rationalizes each change as an improvement. The scorecard breaks that. You change one thing, rebuild, and run the eval again. The number decides, not the author. This is the same discipline the debugger uses (no fix without a reproduction that fails) applied to the skills themselves.

## The cycle, one skill at a time

1. **Target.** Take the weakest skill from `improve.py worklist` (lowest measured lift). Work one skill at a time so the re-measure attributes the delta to one change.
2. **Recall.** Check the decision log for prior attempts on this skill. A change that failed last week will fail again.
3. **Diagnose.** Body weak, or rubric coarse? (See body_vs_rubric.) Name it before you edit.
4. **One change.** Edit the skill body OR the rubric in `.forge` SOURCE. One hypothesis per loop, so the measurement is clean. Two changes at once and you cannot tell which one moved the number.
5. **Rebuild and validate.** Compile the skill and run both validators. A change that breaks the library is not an improvement.
6. **Re-measure.** `improve.py remeasure <path>`. IMPROVED keeps it. REGRESSED or flat reverts it. No exceptions, no "I will fix it later".
7. **Record.** Log the decision and the delta, so the next pass starts from truth.

## Bounds

Improve a handful of skills per run (roughly 3 to 5), then stop and report. An unbounded self-edit loop is how a framework rots quietly: many small unproven changes, each plausible, compounding into drift. The bound plus the re-measure gate keeps every step honest and reversible.

## What good looks like

- Each kept change has a measured before and after: `debugger 0.60 to 0.78 (+0.18)`.
- Reverted changes are logged too, so the same dead end is not retried.
- The library is cleaner or the same size, never bloated with hedging prose added to chase a rubric.
- Skills that could not be improved this pass are named honestly, not quietly skipped.
