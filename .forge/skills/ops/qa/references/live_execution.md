# Live Execution: verify against reality, not vibes

> A plan for tests is not a test. The agent has eyes only when it runs the actual thing and reads the actual output. This is the grounded-verification surface: the done-condition is an executed check passing (tests green, the page renders, no console errors), never the model's own claim that it should work.

## Contents
- The rule: execute, then believe
- The test-execution loop
- The browser-execution loop
- What counts as ground truth
- Bounds and escalation
- What to capture

## The rule: execute, then believe

Before claiming a change works, run it and read the full output. "It should pass" is not evidence. The field's whole jump in reliability (coding agents went from failing most tasks to solving most, on suites graded by executed tests) came from iterating against real execution, not self-assessment. A model cannot reliably grade its own reasoning without an external signal, so get the external signal.

## The test-execution loop

1. **Find the command.** Detect the project's runner (`package.json` scripts, `pytest`, `go test`, `cargo test`, a Makefile). Do not assume npm.
2. **Run it and read all of it.** Run the suite (or the focused test). Read the entire output, not just the exit code. A failing test IS the reproduction case.
3. **Fix, then re-run.** Apply the minimal fix, run again. Loop until green. Never mark done on a red or unrun suite.
4. **Lock it in.** For a bug, add the regression test that failed before the fix and passes after. If you did not watch it fail, you do not know it tests the right thing.

## The browser-execution loop

For UI and end-to-end behavior, running unit tests is not enough. Drive the real thing.

1. **Launch the app.** Start the dev server or preview (use the project's run/preview capability).
2. **Drive a headless browser.** Use the available browser tool (a preview/browser control surface, or `npx playwright`). Navigate to the page, perform the user action, and observe.
3. **Look with real signals.** Read the rendered DOM and the exact text, the console for errors, the network for failed requests, and take a screenshot. Inspect computed styles for visual claims rather than trusting a screenshot's colors.
4. **Reproduce, fix, reload, re-verify.** Confirm the bug live, apply the fix, reload, and confirm it is gone with the same steps. Capture before and after.
5. **Write the end-to-end test** that encodes the flow so the regression cannot silently return. Wait on real conditions, never a fixed sleep (see async_test_stability).

## What counts as ground truth

- A test suite that ran and is green (and would go red if you broke the code).
- A page that actually rendered, with the expected text present and no console errors.
- A build that completed, a request that returned the expected status and body.
Not ground truth: "the code looks correct", "this should render", a green suite you did not run, or a screenshot you did not inspect.

## Bounds and escalation

Execution loops must be bounded. Cap attempts (roughly 3 to 5 on the same failure), and if it still fails, stop and report what was tried with the real output. An unbounded fix-and-rerun loop burns tokens and drifts. When stuck, widen the scope or escalate; do not keep guessing.

## What to capture

Every live verification returns evidence, not adjectives: the exact command run, the relevant output, the screenshot or the rendered text, and the regression test that now guards the fix. That evidence is what lets a caller (including a `/goal` loop or a reviewer) trust the result without re-running it.
