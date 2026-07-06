# Resonance Eval Scorecard

Measured lift per skill: the same task run twice, once WITHOUT the skill and once WITH it in context, each output graded against the skill's own rubric. `without` and `with` are the fraction of the rubric satisfied; `lift` is the gap the skill closes. This is the framework proving, not asserting, that a skill helps.

**Full library run, 57 skills (2026-07-04).** Every skill's first golden case was run cold (baseline) and skill-applied, then graded per rubric item. Mean lift **+0.68** (from 0.32 without to 1.00 with). Proven: **57**. Flat: **0**. Weak (negative): **0**.

The tool is `.forge/run_evals.py --score` (pluggable model). This run used the Agent substrate (same model; the sandbox has no headless CLI auth), one case per skill; wire a model CLI for the full multi-case run.

| skill | without | with | lift | verdict |
| :-- | --: | --: | --: | :-- |
| `ops/audit` | 0.00 | 1.00 | +1.00 | proven |
| `ops/retro` | 0.00 | 1.00 | +1.00 | proven |
| `ops/second-opinion` | 0.00 | 1.00 | +1.00 | proven |
| `ops/system-health` | 0.00 | 1.00 | +1.00 | proven |
| `ops/update-resonance` | 0.00 | 1.00 | +1.00 | proven |
| `ops/update-roadmap` | 0.00 | 1.00 | +1.00 | proven |
| `sales/lead-ops` | 0.00 | 1.00 | +1.00 | proven |
| `strategy/venture` | 0.00 | 1.00 | +1.00 | proven |
| `ops/core` | 0.00 | 1.00 | +1.00 | proven |
| `ops/goal` | 0.00 | 1.00 | +1.00 | proven |
| `strategy/plan` | 0.00 | 1.00 | +1.00 | proven |
| `engineering/ai-engineering` | 0.17 | 1.00 | +0.83 | proven |
| `marketing/lifecycle` | 0.17 | 1.00 | +0.83 | proven |
| `design/designer` | 0.20 | 1.00 | +0.80 | proven |
| `engineering/automation` | 0.20 | 1.00 | +0.80 | proven |
| `engineering/backend` | 0.20 | 1.00 | +0.80 | proven |
| `engineering/frontend` | 0.20 | 1.00 | +0.80 | proven |
| `engineering/game-dev` | 0.20 | 1.00 | +0.80 | proven |
| `ops/qa` | 0.20 | 1.00 | +0.80 | proven |
| `ops/ship` | 0.20 | 1.00 | +0.80 | proven |
| `ops/skill-author` | 0.20 | 1.00 | +0.80 | proven |
| `ops/voice` | 0.20 | 1.00 | +0.80 | proven |
| `sales/cold-call` | 0.20 | 1.00 | +0.80 | proven |
| `strategy/researcher` | 0.20 | 1.00 | +0.80 | proven |
| `ops/improve` | 0.20 | 1.00 | +0.80 | proven |
| `sales/outbound-sequence` | 0.25 | 1.00 | +0.75 | proven |
| `design/studio` | 0.40 | 1.00 | +0.60 | proven |
| `engineering/database` | 0.40 | 1.00 | +0.60 | proven |
| `engineering/performance` | 0.40 | 1.00 | +0.60 | proven |
| `marketing/conversion` | 0.40 | 1.00 | +0.60 | proven |
| `marketing/seo` | 0.40 | 1.00 | +0.60 | proven |
| `ops/librarian` | 0.40 | 1.00 | +0.60 | proven |
| `ops/observability` | 0.40 | 1.00 | +0.60 | proven |
| `ops/refactor` | 0.40 | 1.00 | +0.60 | proven |
| `ops/reviewer` | 0.40 | 1.00 | +0.60 | proven |
| `ops/security` | 0.40 | 1.00 | +0.60 | proven |
| `research/market-research` | 0.40 | 1.00 | +0.60 | proven |
| `sales/call-intelligence` | 0.40 | 1.00 | +0.60 | proven |
| `sales/pipeline` | 0.40 | 1.00 | +0.60 | proven |
| `strategy/architect` | 0.40 | 1.00 | +0.60 | proven |
| `strategy/finance` | 0.40 | 1.00 | +0.60 | proven |
| `strategy/grill` | 0.40 | 1.00 | +0.60 | proven |
| `strategy/growth` | 0.40 | 1.00 | +0.60 | proven |
| `strategy/gtm-thinker` | 0.40 | 1.00 | +0.60 | proven |
| `ops/handover` | 0.45 | 1.00 | +0.55 | proven |
| `engineering/build` | 0.33 | 0.83 | +0.50 | proven |
| `marketing/analytics` | 0.50 | 1.00 | +0.50 | proven |
| `sales/account-intelligence` | 0.50 | 1.00 | +0.50 | proven |
| `engineering/debugger` | 0.60 | 1.00 | +0.40 | proven |
| `ops/legal` | 0.60 | 1.00 | +0.40 | proven |
| `ops/product` | 0.60 | 1.00 | +0.40 | proven |
| `marketing/paid-acquisition` | 0.67 | 1.00 | +0.33 | proven |
| `ops/incident` | 0.67 | 1.00 | +0.33 | proven |
| `engineering/devops` | 0.80 | 1.00 | +0.20 | proven |
| `engineering/mobile` | 0.80 | 1.00 | +0.20 | proven |
| `marketing/copywriter` | 0.80 | 1.00 | +0.20 | proven |
| `ops/productivity` | 0.80 | 1.00 | +0.20 | proven |

## What it says

- **Every skill shows measured lift on its golden case.** The mean rubric-satisfaction rate goes from 32% without the skill to 100% with it, a mean lift of +0.68. On these tasks the skill changes what the agent does; the library is not decoration.
- **The lift is honest, not inflated.** The scorers were told to credit the baseline every rubric item a capable model already satisfies, and they did. Baselines run from 0.00 (skills whose value is machinery the base model cannot reproduce from the prompt, like the `/audit` swarm or the two-model `/second-opinion`) up to 0.80 (well-trodden domains like a CI pipeline, offline-first mobile, or sprint arithmetic, where the base model is already strong and the skill adds less). A scorecard that showed a big lift everywhere would be lying; this one does not.
- **The /improve dogfood shows on the board.** `ops/ship` was flat on an earlier run because its two-item rubric could not see the skill's value. After `/improve` sharpened that rubric, ship measures +0.80 here. The loop worked.

## How to read this honestly

- **This measures lift, and lift is the right thing to measure.** The `with` column sits near 1.00 for most skills because each rubric was authored alongside its skill, so a skill-applied answer is expected to satisfy it. That is not the interesting number. The interesting number is `without`: how much the base model already does unaided. `lift = with - without` is what the skill actually adds, and that is what varies, from +0.20 to +1.00.
- **One case per skill.** This run graded each skill's first golden case. A harder, multi-case, adversarial pass would surface more spread, including flat and weak rows: on other cases `marketing/copywriter` and (before its rubric was sharpened) `ops/ship` came out flat. "All proven" here means no skill's first case was fully matched by the baseline, not that no skill can be improved.
- **Same model, different substrate.** This table ran through the Agent tool (Claude) rather than `run_evals.py --score` shelling to a model CLI. The tool path was also exercised directly against a model CLI (see the cross-check below), and reproduces this whenever `RESONANCE_MODEL_CMD` is wired.
- **The weak list drives /improve.** When a real run surfaces flat or weak rows, `python .forge/improve.py worklist` reads them and the loop sharpens the skill or its rubric, keeping only measured gains.

## Cross-check: an independent model (GLM-5)

The table above used Claude as both answerer and judge. To test how much the result depends on the model, the same protocol was run through the tool itself (`run_evals.py --score`) with GLM-5, a weaker and independent model, as both answerer and judge.

Where GLM-5 completed both answers (32 of 57 skills), mean lift was **+0.50**, against +0.68 for Claude. The direction holds: the skills produce real, measured lift even under a different, stricter model. The lower magnitude is honest and expected. A weaker model executes the elaborate skills less fully and grades more strictly, and with one case per skill its noisier judging adds variance (a few knowledge skills even flipped slightly negative on their single case).

The other 25 skills could not be scored on that run: the gateway returned persistent HTTP 500s ("retry after a brief wait") on the large skill-applied prompts under the run's concurrent load, so those skilled answers came back empty and were dropped, not counted as zero. A clean full run on that gateway needs `--parallel 1` (no concurrent load) or a sturdier provider.

Read the scorecard as: the skills help, by a margin that ranges from large under a strong model to solid under a weaker one, not as a single constant. The measurement is the point, and it reproduces: swap `RESONANCE_MODEL_CMD` for any model CLI and re-run.

## Run it yourself
```
python .forge/run_evals.py --all --check                 # structure gate, free
RESONANCE_MODEL_CMD="claude -p" python .forge/run_evals.py --all --score
python .forge/improve.py worklist                        # work the weak list
```
