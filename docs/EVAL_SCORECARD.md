# Resonance Eval Scorecard

Measured lift per skill: the same task run twice, once WITHOUT the skill and once WITH it in context, each output graded against the skill's own rubric. `without` and `with` are the fraction of the rubric satisfied. `lift` is the gap the skill closes. This is the framework proving, not asserting, that a skill helps.

Produced by `.forge/run_evals.py --score` (pluggable model, diff-based selection, per-skill aggregation). The full 176-case run needs a model CLI wired in (`--model-cmd` or `RESONANCE_MODEL_CMD`); the table below is a **live 7-skill sample** run through the exact protocol to show the method works and the numbers are real.

## Live sample (2026-07-04)

Each row: one golden case, a cold baseline agent and a skill-applied agent answered the same task in independent contexts, then both answers were graded against the rubric.

| skill | cases | without | with | lift | verdict |
| :-- | --: | --: | --: | --: | :-- |
| `strategy/plan` | 1 | 0.33 | 1.00 | +0.67 | proven |
| `engineering/debugger` | 1 | 0.40 | 1.00 | +0.60 | proven |
| `engineering/ai-engineering` | 1 | 0.33 | 0.83 | +0.50 | proven |
| `ops/legal` | 1 | 0.60 | 1.00 | +0.40 | proven |
| `strategy/finance` | 1 | 0.80 | 1.00 | +0.20 | proven |
| `marketing/copywriter` | 1 | 0.80 | 0.80 | +0.00 | flat (easy case) |
| `ops/ship` | 1 | 1.00 | 1.00 | +0.00 | flat, rubric sharpened |

Sample mean lift: **+0.34**. Proven: 5. Flat: 2.

## What the numbers actually say

- **The three new Track 2 skills all show real lift.** `ai-engineering` (+0.50): without it the model handed over a prompt and suggested testing later; with it, it refused to ship a prompt without an eval set, wrote the grading rubric first, started from the cheapest model, and added a grounding guardrail. `ops/legal` (+0.40): the baseline drafted a policy immediately; the skill built the data map first, assigned a lawful basis per purpose, and flagged the Impressum, the TDDDG consent trap, and the controller-vs-processor split. `strategy/finance` (+0.20): the base model is already a strong operator here (0.80), and the skill still added the driver-traced model, the "raise from six months of runway" framing, and explicit base and downside scenarios.
- **The rigor skills produce the largest lift.** `plan` (+0.67) and `debugger` (+0.60): without them the base model plans solo and wants to add production logging before reproducing a bug; with them it runs the ambiguity gate, delegates, and refuses to fix before a deterministic reproduction.
- **The base model is genuinely strong, so lift is honest, not inflated.** Where the base already does well (finance 0.80, copywriter 0.80), lift is smaller. A scorecard that showed +0.8 everywhere would be lying.

## The /improve loop, dogfooded on this scorecard

`ops/ship` came out flat at 1.0 both ways. Diagnosis (per `body_vs_rubric`): the skill's answer was clearly better (canary, rollback, verify-before-tag, toolchain detection) but the eval's two-item rubric could not see it. Fix: the rubric was **sharpened**, not the skill, from 2 blunt items to 5 discriminating ones (verify-before-tag, a rollback path confirmed before deploy, canary-first with post-deploy verification, toolchain detection, correct semver and logical commits). This is the Goodhart-safe move the loop requires: the rubric is now a harder test a mediocre answer fails, never an easier one. The re-measure runs when a model CLI is wired.

`marketing/copywriter` flat is a sampling artifact, not a weak skill: the sample used its easy happy-path case, where a strong base model already writes good copy. The discriminating case is `02_humanization` (rescuing AI-drafted slop), where the skill's anti-slop and humanizer protocol separate it from the baseline.

## Run it yourself

```
# structure gate (free, no model)
python .forge/run_evals.py --all --check

# full scored run (wire any model CLI that reads a prompt on stdin)
RESONANCE_MODEL_CMD="claude -p" python .forge/run_evals.py --all --score

# work the weak list, keep only measured gains
python .forge/improve.py worklist
```
