# Done Conditions: grounded verification only

> This is the load-bearing rule of the whole loop. The signal that a slice or the goal is done must be an executed check against the environment, never the model's own judgment that it should work. A model cannot reliably grade its own reasoning without an external signal, and when it tries, it tends to report success it did not earn. So do not let it.

## Why this is settled, not a preference

Measured, not asserted: a model told to self-correct its reasoning with no external signal tends to degrade, not improve (DeepMind, "Large Language Models Cannot Self-Correct Reasoning Yet", ICLR 2024). The apparent gains from self-correction come from an oracle, a real check, deciding when to stop. And the jump in agent reliability on hard software tasks came from iterating against executed tests, not from better self-assessment. Treat this as a closed question: the done-signal is the executed check. Do not reopen it inside a run.

## What counts as done

A slice or goal is done only when a real check confirms it:

- A **test suite that ran and is green**, and that would go red if you broke the code. Run it via `/test` live execution; read the full output, not just the exit code.
- The **validators clean**: `validate_skill.py`, `validate_library.py`, `run_evals.py --check` for framework work; the project's own linters and type checks for product code.
- **`/audit` returns APPROVE** on the diff, with no P0 or P1 open.
- A **page that actually rendered** with the expected text and no console errors, confirmed by driving the browser, for UI work.
- A **build that completed**, a **request that returned the expected status and body**, a **migration that applied and reversed**.

## What does not count

- "The code looks correct." Looking is not running.
- "This should render / should pass / probably works." Should is not evidence.
- A green suite you did not run this iteration, or one you did not watch fail before the fix.
- A screenshot you did not inspect, or a model, including a second model, asserting it is fine.
- The goal loop's own summary. The loop reports evidence; it does not certify itself.
- File presence, dashboard green, progress percent, certification marker, stale receipt repair, or a regenerated admin hash. These can describe a run; they do not prove the product behavior works.

## When the check does not exist

If there is no way to verify a slice (no test, no runnable path), that is a gap in the plan, not a pass. Build the check first: write the test, add the script, make the intermediate output verifiable. A DoD you cannot execute is a DoD that is not written yet. Either make it checkable or stop and say so; never mark unverifiable work done.

## Evidence receipts

The overall goal DoD, set during `/grill` and approved by the human, must itself be checkable the same way. "Users can export their data" is not a done condition. "The export button downloads a CSV that opens in a spreadsheet, and an end-to-end test covers it" is. If the goal DoD is not executable, the frame step is not finished; go back and make it so before building.

For `/goal`, each acceptance check needs an evidence receipt before the loop can
mark the goal achieved:

```bash
py .forge/skills/ops/goal/scripts/loop_state.py exec act-check -- py -c "print('ok')"
py .forge/skills/ops/goal/scripts/loop_state.py evidence evidence.json
py .forge/skills/ops/goal/scripts/loop_state.py achieve
```

Evidence is rejected when the contract hash, plan hash, or goal revision is
stale, or when it does not point to an execution receipt recorded by the current
goal run. Overrides require an approval receipt with a matching scope hash.

Some metadata is substantive because it identifies the work being checked. Keep
contract hashes, plan hashes, pinned revisions, product checksums, signatures,
benchmarks, and execution receipts that state command, input, result, and
expected condition. Treat metadata as administrative only when it describes the
orchestrator's progress record rather than the product, target identity, or
evidence for a current acceptance claim.
