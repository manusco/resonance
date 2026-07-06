# Resonance Eval Scorecard

Measured lift per skill: the same golden case run twice, once WITHOUT the skill and once WITH it in context, each answer graded against the skill's own rubric. `without` and `with` are the fraction of the rubric satisfied; `lift = with - without` is what the skill adds. `verdict` is by lift: proven `>= +0.20`, flat in between, negative `<= -0.05`.

**Full library run through the tool, 57 skills, model GLM-5 (2026-07-06).** Produced by `.forge/run_evals.py --score` shelling to a real model CLI, with GLM-5 as both answerer and judge. Mean lift **+0.38** (rubric satisfaction 0.19 without the skill, 0.57 with). **40 of 57 skills show measured lift** (>= +0.20); 15 flat, 2 negative.

This is the conservative, reproducible number. GLM-5 is a deliberately weaker, independent model, so it is a floor: the same library scored by a stronger model (Claude, answerer and judge) averaged +0.68. Measured lift is model-dependent, so read it as a band, not a constant.

| skill | without | with | lift | verdict |
| :-- | --: | --: | --: | :-- |
| `engineering/ai-engineering` | 0.00 | 1.00 | +1.00 | proven |
| `engineering/frontend` | 0.00 | 1.00 | +1.00 | proven |
| `engineering/mobile` | 0.00 | 1.00 | +1.00 | proven |
| `sales/call-intelligence` | 0.00 | 1.00 | +1.00 | proven |
| `sales/lead-ops` | 0.00 | 1.00 | +1.00 | proven |
| `strategy/architect` | 0.00 | 1.00 | +1.00 | proven |
| `engineering/game-dev` | 0.00 | 0.80 | +0.80 | proven |
| `ops/security` | 0.00 | 0.80 | +0.80 | proven |
| `research/market-research` | 0.20 | 1.00 | +0.80 | proven |
| `strategy/gtm-thinker` | 0.00 | 0.80 | +0.80 | proven |
| `strategy/researcher` | 0.20 | 1.00 | +0.80 | proven |
| `sales/outbound-sequence` | 0.00 | 0.75 | +0.75 | proven |
| `engineering/database` | 0.20 | 0.80 | +0.60 | proven |
| `engineering/debugger` | 0.20 | 0.80 | +0.60 | proven |
| `ops/core` | 0.00 | 0.60 | +0.60 | proven |
| `ops/observability` | 0.40 | 1.00 | +0.60 | proven |
| `ops/product` | 0.20 | 0.80 | +0.60 | proven |
| `ops/qa` | 0.20 | 0.80 | +0.60 | proven |
| `ops/refactor` | 0.20 | 0.80 | +0.60 | proven |
| `marketing/lifecycle` | 0.50 | 1.00 | +0.50 | proven |
| `ops/incident` | 0.50 | 1.00 | +0.50 | proven |
| `ops/system-health` | 0.00 | 0.50 | +0.50 | proven |
| `design/studio` | 0.60 | 1.00 | +0.40 | proven |
| `engineering/automation` | 0.00 | 0.40 | +0.40 | proven |
| `engineering/devops` | 0.40 | 0.80 | +0.40 | proven |
| `ops/legal` | 0.40 | 0.80 | +0.40 | proven |
| `ops/librarian` | 0.00 | 0.40 | +0.40 | proven |
| `ops/voice` | 0.00 | 0.40 | +0.40 | proven |
| `sales/cold-call` | 0.60 | 1.00 | +0.40 | proven |
| `strategy/grill` | 0.40 | 0.80 | +0.40 | proven |
| `strategy/growth` | 0.60 | 1.00 | +0.40 | proven |
| `marketing/analytics` | 0.00 | 0.33 | +0.33 | proven |
| `strategy/plan` | 0.00 | 0.33 | +0.33 | proven |
| `design/designer` | 0.20 | 0.40 | +0.20 | proven |
| `engineering/backend` | 0.80 | 1.00 | +0.20 | proven |
| `marketing/copywriter` | 0.60 | 0.80 | +0.20 | proven |
| `marketing/seo` | 0.40 | 0.60 | +0.20 | proven |
| `sales/pipeline` | 0.00 | 0.20 | +0.20 | proven |
| `strategy/finance` | 0.40 | 0.60 | +0.20 | proven |
| `strategy/venture` | 0.00 | 0.20 | +0.20 | proven |
| `engineering/build` | 0.00 | 0.00 | +0.00 | flat |
| `engineering/performance` | 0.60 | 0.60 | +0.00 | flat |
| `marketing/conversion` | 0.20 | 0.20 | +0.00 | flat |
| `marketing/paid-acquisition` | 0.33 | 0.33 | +0.00 | flat |
| `ops/audit` | 0.00 | 0.00 | +0.00 | flat |
| `ops/goal` | 0.00 | 0.00 | +0.00 | flat |
| `ops/improve` | 0.00 | 0.00 | +0.00 | flat |
| `ops/productivity` | 0.60 | 0.60 | +0.00 | flat |
| `ops/retro` | 0.00 | 0.00 | +0.00 | flat |
| `ops/reviewer` | 0.20 | 0.20 | +0.00 | flat |
| `ops/second-opinion` | 0.00 | 0.00 | +0.00 | flat |
| `ops/ship` | 0.00 | 0.00 | +0.00 | flat |
| `ops/update-resonance` | 0.00 | 0.00 | +0.00 | flat |
| `ops/update-roadmap` | 0.00 | 0.00 | +0.00 | flat |
| `sales/account-intelligence` | 0.00 | 0.00 | +0.00 | flat |
| `ops/handover` | 0.09 | 0.00 | -0.09 | negative |
| `ops/skill-author/resonance-skill-author` | 0.40 | 0.20 | -0.20 | negative |

## What it says

- **40 of 57 skills measurably help, even under a weak model and a strict judge.** Mean +0.38. The largest lifts are where the skill adds discipline the base model skips: reproduce-before-fix, evals-before-prompts, the data map before the privacy policy, the shadow-state and motion set, the persona ladder.
- **The flat rows are not all weak skills.** 9 of the 17 no-lift skills are orchestration or runtime skills (`/audit`, `/goal`, `/second-opinion`, `/ship`, `/retro`, `/update-*`, `/handover`) whose value is spawning other agents, dispatching a second model, or driving git and a plan. A single chat completion cannot DO those, so it writes a description that the rubric (rightly) scores 0. `ops/audit` wrote a 4300-character audit and still scored 0 because it could not actually spawn the four sub-agents. These are under-measured here, not broken; judge them by the grounded runtime.
- **The rest of the flat and negative rows are the real /improve work-list**: either GLM-5 is already competent so the skill adds little, or the single-case judge was noisy (two skills read slightly negative on one case). `python .forge/improve.py worklist` reads this file.

### Work-list (no measured lift, excluding runtime-bound orchestration skills)

- `engineering/build` (lift +0.00)
- `engineering/performance` (lift +0.00)
- `marketing/conversion` (lift +0.00)
- `marketing/paid-acquisition` (lift +0.00)
- `ops/productivity` (lift +0.00)
- `ops/reviewer` (lift +0.00)
- `sales/account-intelligence` (lift +0.00)
- `ops/skill-author/resonance-skill-author` (lift -0.20)

## How to read this honestly

- **Lift is model-dependent.** GLM-5 executes the elaborate skills less fully than a top model and grades more strictly, so its numbers are lower than Claude's +0.68. Both are real; the truth is a band, from large under a strong model to solid under a weak one.
- **One case per skill.** A weaker judge adds variance; a couple of knowledge skills read slightly negative on their single case. A multi-case run smooths that.
- **Orchestration skills need the runtime, not a chat turn.** Skills that spawn subagents, dispatch a second model, or drive git cannot show their value in one completion. That is a property of the test, not the skill. The grounded orchestration evals (`.forge/orch_evals/`, run with `python .forge/orch_eval.py`) close that gap by judging outcomes instead of prose: did `/goal` make a failing test pass, did `/audit` name the planted vulnerability.
- **Reproducible.** Swap `RESONANCE_MODEL_CMD` for any model CLI and re-run. This table was produced against the opencode.ai GLM-5 gateway at `--parallel 6`.

## Run it yourself
```
python .forge/run_evals.py --all --check                      # structure gate, free

# score against any OpenAI-compatible model; the adapter bakes in the UTF-8, browser
# User-Agent and bare-params lessons, so you only supply the endpoint via env:
MODEL_BASE_URL=... MODEL_NAME=... MODEL_API_KEY=... \
  RESONANCE_MODEL_CMD="python .forge/exec/model_cli.py" python .forge/run_evals.py --all --score

python .forge/improve.py worklist                             # work the weak list
RESONANCE_AGENT_CMD="<agent-cli>" python .forge/orch_eval.py  # grounded orchestration evals
```
