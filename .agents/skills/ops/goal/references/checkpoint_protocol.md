# Checkpoint Protocol: autonomous, but not unaccountable

> The loop runs on its own most of the time. It stops and checks in only where human judgment genuinely matters: before a one-way door, when it is stuck, and at the finish. The goal is momentum with the two or three brakes that keep it safe, not a pause after every step.

## The default cadence (more autonomous)

Proceed through slices without pausing. Build, verify, advance, repeat. Do not narrate every micro-step or ask permission to continue on green. The human set the direction at the frame gate; your job now is to reach it and surface only what they need to decide.

## When to stop and check in

1. **Before a one-way door, always.** A one-way door is a change that is hard or impossible to reverse: a deploy, a destructive data change, a schema migration, an architectural commitment, deleting or overwriting something you did not create, or anything outward-facing. Stop and get explicit confirmation. No exceptions, no matter how confident. This is User Sovereignty, and it is not negotiable for autonomy's sake.
2. **When the bound says stop.** A STOP_SLICE, STOP_STUCK, or STOP_CAP from `loop_state.py` is a checkpoint. Stop, report progress and the blocker, and either re-plan the one slice or hand back.
3. **At the finish.** When the goal DoD verifies, stop and present the result for the ship approval. Never auto-ship.

Between those, keep going.

## How to present a checkpoint

A checkpoint is a decision brief, not a status dump. Give the human what they need to decide in a few seconds:

- **What is done and proven** (the evidence: which checks are green).
- **The decision at hand** (the one-way door, or the blocker), in plain terms.
- **What breaks if it goes wrong**, one sentence.
- **Your recommendation** with a reason, and the concrete options.

Then wait. Do not walk through the door while asking about it.

## Confidence, not ceremony

Move on green confidence and pause on doubt. If a step is routine and reversible and verified, do it and continue. If you are unsure whether something is a one-way door, treat it as one and ask. The cost of an unnecessary check-in is a few seconds; the cost of an unasked one-way door can be the whole project. When in doubt, surface it.
