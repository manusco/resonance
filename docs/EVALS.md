# Measuring skills: the eval toolkit

Every Resonance skill ships golden eval cases. This repo ships the MEASURING TOOLS and the CASES; it ships no results. Your scorecards, baselines, and calibration numbers are yours: they land in your own results directory when configured, or in local scratch, never in the repo.

## The three layers

1. **Structure gate (free, deterministic, seconds).** `npm run eval` (`run_evals.py --all --check`) verifies every case binds to a real skill, has a query, a rubric, and valid deterministic checks. Runs in the pre-push ship-gate.
2. **Scored lift (model-priced, minutes).** `run_evals.py --all --score` answers every case twice per rep, once cold and once with the skill body in context, grades both, and reports the lift per skill. Honesty rules are enforced, not suggested:
   - the judge is never the answerer (`RESONANCE_JUDGE_CMD` must differ; the run refuses otherwise),
   - at least 3 generations per arm per case (a lucky completion cannot carry a verdict),
   - cases may carry deterministic `checks` graded in pure Python (kinds: `regex_absent`, `contains_any`, `section_present`, `max_lines`); a skill whose items are half deterministic gets a `grounded` marker,
   - a case whose cold arm already passes the full rubric is flagged as a dead case (it discriminates nothing),
   - planted-defect cases (one per skill) embed a concrete doctrine violation in the query, so grading has ground truth instead of self-agreement.
3. **Grounded orchestration evals (agent-priced).** `run_evals` grades one completion; orchestration skills (`/goal`, `/build`, `/ship`, `/audit`, `/reviewer`) are graded by outcome instead: `orch_eval.py` stands up a fixture with a planted defect, runs a real tools-capable agent, then checks the world (did the executed suite go green, did the release get refused on a red suite).

## Keep/revert decisions: the calibrated gate

Editing a skill and eyeballing the new score is how metrics get gamed. `improve.py` enforces the honest loop:

```
python .forge/improve.py worklist                 # skills with no measured lift
python .forge/improve.py calibrate                # one-time A/A noise floors
python .forge/improve.py remeasure <skill-path>   # paired A/B vs HEAD, verdict
```

- **Calibrate first.** Ten A/A runs (a skill measured against itself) establish the pipeline's noise floor. Floors are pooled across the calibration set and shared by all skills; the pooled floor is the minimum detectable effect of the gate, printed so nobody mistakes noise for signal. Uncalibrated remeasures print numbers but refuse verdicts.
- **Paired remeasure.** The body at `--baseline-ref` and the working tree run in the same session, same cases, same judge. KEEP only if the mean delta clears `max(0.10, pooled floor)` AND no case regressed beyond the per-case floor.
- **Rubric edits never count as lift.** The evals directory is hashed into the baseline; a changed hash means NEW BASELINE and no verdict. Make the test harder and the skill better, in that order.

## Wiring a model

Any CLI that reads a prompt on stdin and prints the completion works:

```
RESONANCE_MODEL_CMD="python .forge/exec/model_cli.py"   # answerer (OpenAI-compatible endpoint)
RESONANCE_JUDGE_CMD="<a DIFFERENT model command>"        # judge
RESONANCE_AGENT_CMD="<a tools-capable agent CLI>"        # orchestration evals
```

`.forge/exec/model_cli.py` adapts any OpenAI-compatible endpoint (`MODEL_BASE_URL`, `MODEL_NAME`, `MODEL_API_KEY`) to that contract, with UTF-8 forced and retries built in.

## Cost, so nobody skips measurement out of fear

A full-library scored run at 3 reps is roughly 240 cases x 3 reps x 2 arms plus judging: low single-digit dollars on a budget model. A per-skill remeasure is cents. Calibration is a few hundred calls, once.
