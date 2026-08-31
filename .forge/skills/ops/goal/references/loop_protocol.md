# The Loop Protocol: bounded, grounded, re-planning

> The reliable autonomous loop is not a leap of faith. It is a reason-act-observe cycle where every observation is ground truth from the environment, the number of turns is capped by code, and a failing plan gets replaced instead of retried forever. This is the opposite of the open-ended goal-chaser that judges its own progress and never stops.

## Earn the loop (do not spin one you do not need)

Before starting an autonomous loop, take the cheapest tool that verifies the outcome. A single skill, or a fixed prompt chain, beats a self-directing loop when the path is known. Reach for the loop only when the work needs the model to decide its own next step against feedback it cannot predict. An autonomous loop is the most expensive and least predictable option, so it is the last resort, not the default. If the goal is really one step, do the step.

## Every iteration must add information

A loop that re-samples the same model on the same context is a slot machine, not progress. Each turn has to inject something new: a test result, a fetched fact, a tool error, a field outcome, a human answer. If a turn would run on exactly the inputs of the last one, stop and change the inputs, do not pull the lever again.

## The cycle

For each slice, one turn of the loop is:

1. **Reason:** decide the smallest next action that moves the slice toward its Definition of Done. Recall memory and settled decisions first so you do not re-solve solved problems.
2. **Act:** build that action (`/build`).
3. **Observe (grounded):** run the real check. Tests via `/test` live execution, the validators, `/audit` on the diff. Read the actual output. See done_conditions for what qualifies.
4. **Record and decide:** call `loop_state.py check <slice> advanced|progress|failed`. When a check fails, pass `--sig "<tool>:<error-class>"` so a loop on one identical error is caught early. Obey the directive. Record any real decision in the project ledger or memory (see the operating standard for where).
5. **Attach evidence:** when an acceptance criterion is proven, write an `EvidenceReceipt` and add it with `loop_state.py evidence <receipt>`. A later `achieve` command fails until every criterion has accepted current evidence.

## Three clocks

The loop runs at three speeds, and all three must turn:

- **Inner (seconds):** the deterministic checks inside one slice, tests, validators, a build. Ground truth for "did this action work".
- **Middle (a session):** evals and a second opinion across the whole change. Ground truth for "is the change good", not just green.
- **Outer (weeks):** the field outcome comes back and either confirms the work or does not, and a confirmed lesson becomes a skill or doctrine change kept only if it raises measured lift. Ground truth for "did it work in the world".

Most loops build only the inner clock and call it done. The inner clock proves the code ran; it cannot prove the decision was right. Close the outer clock or the system only ever grades itself.

Repeat until the slice DoD is met, then move to the next slice. Repeat across slices until the goal DoD is met.

## Why bounded

An unbounded loop is how AutoGPT burned money and never finished: no stopping point, so "not done yet" was the default answer forever. `loop_state.py` makes the bound real in code, not in prose the model can talk itself past:

- **max_slice_attempts:** a single slice that will not advance after a few tries is a signal, not a reason to keep trying. Re-plan it or escalate.
- **max_iters:** a total ceiling so a drifting goal cannot run away.
- **stuck detector:** if nothing has advanced in the last several turns, stop. Motion is not progress.

A STOP directive is a stop. Do not override it. Report what was done and what blocked it.

## Why re-plan instead of retry

Retrying the same failing action is how loops thrash. When a slice fails its bound, the plan for that slice was probably wrong, not just unlucky. Re-plan the one slice (`/plan` scoped to it) with what you learned from the failure. If the re-planned slice also fails, the problem is above your pay grade for autonomy: stop and hand it back with the real output. This is plan-and-execute with a re-planning step, which is the pattern that beats naive retry loops on long tasks.

## Verified cursor, not admin status

In staged work, the cursor moves on implemented behavior and executed checks, not on progress metadata. Missing or stale status rows, receipts, dashboards, presence markers, or administrative hashes do not prove output is wrong, and they do not justify replaying completed slices outside the changed dependency cone.

Replay a slice only when the input meaning, target revision, product contract, output shape, or observed behavior changed. If an orchestrator refuses an authorized path only because its own metadata is stale, run the smallest valid stage manually, validate the output, record the evidence needed for the current claim, and remove the admin-only gate from the plan. Do not weaken product integrity checks, pinned input identity, benchmarks, or execution receipts that carry command, input, result, and expected condition.

## Plan-and-execute, not improvise

Frame the whole goal into slices up front (via `/grill` and `/plan`), then execute slice by slice. Do not discover the plan by wandering. A slice is small enough to build and verify in one short cycle and produces something independently checkable. If a slice cannot be verified on its own, it is too big or too vague; split it.
