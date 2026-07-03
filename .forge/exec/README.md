# The Execution Surface (the agent's eyes)

> Resonance's Verify Lock says "loop until proven, not until it looks right." Proof
> means executed reality, not the model's own read of its work. This directory is
> where the agent actually runs things: the project's tests, and a real browser.

A model cannot reliably grade its own reasoning without an external signal (Google
DeepMind showed it can even degrade). The SWE-bench generation went from under 10%
to over 70% by iterating against *executed* tests. `/test` and `/goal` ground on
these tools, not on described results.

## `run_checks.py` - the grounded verifier (universal)

Detects the project's toolchain and runs its real test, build, or lint command,
capturing pass or fail and the output. Works on Node (npm/pnpm/yarn/bun), Python,
Go, Rust, and Make. Pure stdlib, no dependency.

```
python .forge/exec/run_checks.py [dir] [--only test|build|lint|typecheck] [--all] [--json]
```

Exit `0` all passed, `1` a check failed, `3` no runnable check found (a gap to
surface, never a silent pass). `--json` emits the structured result `/goal` reads.

## `browser_check.mjs` - real browser grounding (optional)

Opens a headless browser, loads a URL, and reports what actually rendered: the
title, console and page errors, whether required elements exist, and a screenshot.
This is how `/design` and `/test` stop guessing and start seeing.

```
node .forge/exec/browser_check.mjs <url> [--assert "css"]... [--shot out.png] [--json]
```

Exit `0` healthy, `1` a problem rendered, `3` Playwright not available.

Playwright is **not** a Resonance dependency (clone-and-go stays light). The check
uses whatever Playwright the target project has. If it is missing, it prints the
one-line install hint (`npm i -D playwright && npx playwright install chromium`)
instead of failing hard.

## How the skills use it

- `/test` (`ops/qa`) runs `run_checks.py` to reproduce and confirm a fix against
  executed tests, and `browser_check.mjs` to verify a UI in a real browser.
- `/goal` (`ops/goal`) uses both as its grounded done-condition: a slice is done
  when the checks pass by execution, never because the output looks right.
