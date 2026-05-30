# Eval protocol (build evals before prose)

The rule the whole craft turns on: **create evals before writing the skill.** This
forces the skill to solve a real, observed gap instead of an imagined one. A skill
without evals is unfalsifiable, and unfalsifiable skills rot.

## The loop

1. **Identify the gap.** Run the task with no skill. Write down the exact failure.
2. **Write >= 3 cases** in `evals/`. Cover happy path, an edge case, and a failure the skill must prevent.
3. **Baseline.** Measure the no-skill result against the cases.
4. **Write the minimum skill** that passes.
5. **Iterate.** Re-run, compare to baseline. Keep only what moves the score.

## Case format

```json
{
  "skill": "resonance-copywriter",
  "query": "Write a hero headline + subhead for a B2B payroll tool. No AI clichés.",
  "files": [],
  "expected_behavior": [
    "Produces exactly one headline and one subhead",
    "Contains zero banned phrases (delve, robust, seamless, landscape, ...)",
    "Headline is benefit-led and reads at <= grade 8",
    "Makes no claim not supported by an actual product feature"
  ]
}
```

`expected_behavior` is a rubric of observable, gradeable statements, not "is it good".

## Grading

Two ways, cheapest first:
- **Deterministic** where possible. A banned-phrase check, a JSON-shape check, a line count. These are free and exact; prefer them. (E.g. resonance-copywriter already ships `banned_phrase_scan.py` as a grader.)
- **Model-graded** for judgment ("is the headline benefit-led"). A grader model scores the output against the rubric. Make it score the justification first, then the verdict, so the reasoning is not retrofitted to the score.

## Tiers (keep it affordable)

- **Static** (validator, shape checks): free, run every change.
- **Model-graded**: cents per run, run before shipping a skill.
- **End-to-end** (drive the real skill in a real tool): dollars per run, run on the skills you change, selected by diff.

Run the cheap tier always; the expensive tiers only on what changed.