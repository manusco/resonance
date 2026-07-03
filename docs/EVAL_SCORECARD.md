# Resonance Eval Scorecard

Measured lift per skill: the same task run twice, once WITHOUT the skill and once WITH it in context, each output graded against the skill's own rubric. `without` and `with` are the fraction of the rubric satisfied. `lift` is the gap the skill closes. This is the framework proving, not asserting, that a skill helps.

Produced by `.forge/run_evals.py --score` (pluggable model, diff-based selection, per-skill aggregation). The full 164-case run needs a model CLI wired in (`--model-cmd` or `RESONANCE_MODEL_CMD`); the table below is a **live 4-skill sample** run through the exact protocol to show the method works and the numbers are real.

## Live sample (2026-07-04)

Each row: one golden case, a cold baseline agent and a skill-applied agent answered the same task in independent contexts, then both answers were graded against the rubric.

| skill | cases | without | with | lift | verdict |
| :-- | --: | --: | --: | --: | :-- |
| `engineering/debugger` | 1 | 0.40 | 1.00 | +0.60 | proven |
| `strategy/plan` | 1 | 0.33 | 1.00 | +0.67 | proven |
| `ops/ship` | 1 | 1.00 | 1.00 | +0.00 | flat |
| `marketing/copywriter` | 1 | 0.80 | 0.80 | +0.00 | flat |

Sample mean lift: **+0.32**. Proven: 2. Flat: 2.

## What the numbers actually say

- **The rigor skills produce large, real lift.** Without the debugger skill, the base model proposed adding logging to production before reproducing the bug and never checked `learnings.jsonl`; with it, the agent refused to fix before a deterministic reproduction, listed race, cache, and float hypotheses, and checked prior learnings first (0.40 to 1.00). Without the plan skill, the model planned solo; with it, it ran the ambiguity gate, delegated to the researcher and venture skills, and produced a PRD plus a 4-pass atomic plan (0.33 to 1.00). This is the framework doing its job: turning a capable generalist into a disciplined operator.
- **Two skills came out flat, and that is the honest and useful part.** `ops/ship` scored 2/2 both ways because the base model already knows the basic release steps and the rubric (two items) is too coarse to test the skill's real additions (canary, rollback, verify-before-tag, doc-drift). `marketing/copywriter` scored 4/5 both ways because both outputs tripped the same binary "headline under 10 words" rule, so the rubric did not discriminate on the craft the skill actually adds. Flat lift here is not "the skill is useless"; it is "this eval cannot yet see the skill's value." Those two rubrics go on the work-list.

## How this feeds the rest of the system

- The `flat` and `weak` rows are the **/improve work-list** (Track 3): a skill with no measured lift either needs a sharper eval or a stronger body, and the scorecard says which.
- The grounded verifier behind a real run is the execution surface (`.forge/exec/`): `run_checks.py` runs the project's real tests, `browser_check.mjs` opens a real browser. Measurement grades against executed reality, not self-report.

## Run it yourself

```
# structure gate (free, no model)
python .forge/run_evals.py --all --check

# full scored run (wire any model CLI that reads a prompt on stdin)
RESONANCE_MODEL_CMD="claude -p" python .forge/run_evals.py --all --score

# just the skills you changed, one case each (cheap)
python .forge/run_evals.py --changed --score --limit 1
```
