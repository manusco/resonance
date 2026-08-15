---
name: resonance-ops-improve
description: The self-improving loop. Reads the eval scorecard, finds the skills that show no measured lift, sharpens the skill body or its rubric, and keeps a change only when it raises the measured lift. Use when improving skill quality, working the eval work-list, or making the framework better with evidence instead of opinion. Manual-only (it edits skills and rebuilds).
archetype: orchestration
---

# /resonance-ops-improve: raise the floor, and prove you did

> **Role:** the framework improving itself, grounded in measurement.
> **Invoked as:** `/improve` (to work the eval scorecard's weak list), or `/improve <skill-path>`.
> **Input:** The eval scorecard (`.forge/eval_results.json`, from `run_evals.py --score`), or one skill path.
> **Output:** Skills with higher measured lift, each change re-measured and kept only if it helped, plus an honest list of what could not be improved this pass.
> **Definition of Done:** Every kept change was re-measured and raised the lift. Nothing was kept on a guess. No rubric was made easier to pass. Decisions were recorded. Nothing was shipped.

You do not "polish" skills by feel. A skill improves only when the number moves, measured against the same rubric that flagged it. The whole point of the scorecard is to stop trusting opinion, so this loop trusts it least of all.

## Prerequisites (fail fast)

- [ ] A scorecard exists (`.forge/eval_results.json`). If not, run `python .forge/run_evals.py --all --score` first (needs a model command).
- [ ] Answerer AND judge models are configured (`RESONANCE_MODEL_CMD` and `RESONANCE_JUDGE_CMD`, different models). Without them you can propose changes but cannot prove them, so stop and say so.
- [ ] Calibration exists (`python .forge/improve.py calibrate`, a one-time A/A noise-floor run). Without it remeasure prints numbers but refuses verdicts.

## Algorithm

Copy this checklist and tick items as you go.

1. **Get the work-list.** `python .forge/improve.py worklist` lists the skills with no measured lift (verdict `weak` or `flat`), weakest first. Take the weakest. → verify: a target skill is chosen.
2. **Recall.** Skim `## Decisions` in `.resonance/02_memory.md` (already loaded) and run `python .forge/recall.py "<skill topic>"` so you do not repeat a change that already failed. → verify: prior attempts checked.
3. **Diagnose body vs rubric.** Read the skill and its evals. Decide: is the BODY weak (the skill does not add enough over the base model), or is the RUBRIC coarse (the eval cannot see the value the skill already adds)? See body_vs_rubric. → verify: the cause is named, not guessed.
4. **Make one targeted change in `.forge` SOURCE.** Either sharpen the body (add the missing rigor, the concrete step, the decision the base model skips) or sharpen the rubric (make it a HARDER, more discriminating test). One change, one hypothesis. → verify: exactly one skill or rubric was edited.
5. **Rebuild and validate.** `python .forge/forge.py build <skill>`, then `validate_skill.py` and `validate_library.py`. → verify: clean.
6. **Re-measure (the gate).** `python .forge/improve.py remeasure <skill-path>`. Keep the change ONLY on a KEEP verdict. REVERT means revert now. NEW BASELINE means the rubric changed: run the scored re-baseline before any verdict. UNCALIBRATED means run `calibrate` once first. → verify: kept changes carry a KEEP verdict; the rest reverted.
7. **Record.** Add one line under `## Decisions` in `.resonance/02_memory.md`: improved <skill>, what changed, and the lift delta. → verify: logged.
8. **Bound the pass.** Improve a few skills (roughly 3 to 5), then stop and report the deltas. Do not grind the whole library in one run. → verify: stopped and summarized.

## The one rule that keeps this honest

**Never make a rubric easier to pass.** Raising the score by weakening the test is the failure this loop exists to prevent (optimize the metric, lose the goal). A rubric change is valid only when it makes the eval a *better* test of the skill's real value: more specific, more discriminating, closer to what a great output actually does. If you cannot make the rubric harder and still see the skill win, the body is what needs work, not the rubric.

## Checkpoints

- **Before a large rewrite of a skill body:** present the diagnosis and the plan, get a nod. Small, targeted edits proceed on their own.
- **When a skill resists improvement** (two honest attempts, no measured gain): leave it, record why, and move on. A stuck skill is a finding, not a failure to hide.
- **At the end:** report the before and after lift per skill. Never `/ship`; improvement is a separate, human-approved release.

## Recovery

- Re-measure says REVERT → revert immediately. Do not keep a change that made it worse to "clean up later".
- Re-measure says NEW BASELINE or UNCALIBRATED → no verdict exists. Re-baseline with a scored run (rubric changed) or run `calibrate` once, then remeasure again. Never keep a change on raw numbers alone.
- The model command is missing → stop. You can draft changes but you cannot keep any without the grounded re-measure. Say the loop is blind and hand back.
- Every change is flat → the eval may be genuinely coarse, or the base model is already at the ceiling for this case. Record that and move to the next skill.
- A change passes re-measure but feels like gaming → it is. Revert it and fix the rubric to be harder.

## Out of Scope

- Authoring brand-new skills (delegate to `resonance-ops-skill-author`).
- Running the full scorecard (that is `run_evals.py --score`; this loop consumes its output).
- Shipping. Improvement lands as normal commits; releasing is a separate `/ship` a human approves.

## Reference Library

- **[Improve Loop](references/improve_loop.md)**: The bounded, grounded refinement cycle and why re-measurement is the gate.
- **[Body vs Rubric](references/body_vs_rubric.md)**: Diagnosing whether the skill or its eval is the weak link, and how to fix each without gaming.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
