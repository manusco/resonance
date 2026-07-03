# The Loop Protocol: bounded, grounded, re-planning

> The reliable autonomous loop is not a leap of faith. It is a reason-act-observe cycle where every observation is ground truth from the environment, the number of turns is capped by code, and a failing plan gets replaced instead of retried forever. This is the opposite of the open-ended goal-chaser that judges its own progress and never stops.

## The cycle

For each slice, one turn of the loop is:

1. **Reason:** decide the smallest next action that moves the slice toward its Definition of Done. Recall memory and settled decisions first so you do not re-solve solved problems.
2. **Act:** build that action (`/build`).
3. **Observe (grounded):** run the real check. Tests via `/test` live execution, the validators, `/audit` on the diff. Read the actual output. See done_conditions for what qualifies.
4. **Record and decide:** call `loop_state.py check <slice> advanced|progress|failed`. Obey the directive. Record any real decision with `decisions.py add`.

Repeat until the slice DoD is met, then move to the next slice. Repeat across slices until the goal DoD is met.

## Why bounded

An unbounded loop is how AutoGPT burned money and never finished: no stopping point, so "not done yet" was the default answer forever. `loop_state.py` makes the bound real in code, not in prose the model can talk itself past:

- **max_slice_attempts:** a single slice that will not advance after a few tries is a signal, not a reason to keep trying. Re-plan it or escalate.
- **max_iters:** a total ceiling so a drifting goal cannot run away.
- **stuck detector:** if nothing has advanced in the last several turns, stop. Motion is not progress.

A STOP directive is a stop. Do not override it. Report what was done and what blocked it.

## Why re-plan instead of retry

Retrying the same failing action is how loops thrash. When a slice fails its bound, the plan for that slice was probably wrong, not just unlucky. Re-plan the one slice (`/plan` scoped to it) with what you learned from the failure. If the re-planned slice also fails, the problem is above your pay grade for autonomy: stop and hand it back with the real output. This is plan-and-execute with a re-planning step, which is the pattern that beats naive retry loops on long tasks.

## Plan-and-execute, not improvise

Frame the whole goal into slices up front (via `/grill` and `/plan`), then execute slice by slice. Do not discover the plan by wandering. A slice is small enough to build and verify in one short cycle and produces something independently checkable. If a slice cannot be verified on its own, it is too big or too vague; split it.
