# Async Test Stability: kill the flake at the source

> A flaky test is not random. It is a race you have not named yet. The fix is almost never a longer sleep.

Most async test flakiness comes from one anti-pattern: pausing for a fixed duration and hoping the work finished. Under load, on a slow CI runner, or on a colleague's faster laptop, the guess is wrong and the test flaps. Wait for the actual condition instead of guessing at the clock.

## The core rule: wait for the condition, not the clock

- Do NOT `sleep(500)` and then assert. The 500 is a guess that is too long on a fast machine and too short on a slow one.
- DO poll or await the real signal: the element is visible, the response arrived, the row exists, the queue drained. Assert the moment the condition is true, and fail only after a generous timeout.

```
// Fragile: a guess about timing
await sleep(500)
expect(result).toBe("done")

// Stable: wait for the actual state, with a ceiling
await waitFor(() => result === "done", { timeout: 5000 })
expect(result).toBe("done")
```

The stable version is faster on average (it proceeds the instant the condition holds) and does not flap (it only fails when the condition genuinely never arrives).

## Control the sources of nondeterminism

- **Time**: freeze it. Use fake timers or an injected clock so "one hour later" is a function call, not a real wait. Never test a timeout by actually waiting for it.
- **Randomness**: seed it. A test that fails one run in fifty because of an unseeded random value is a real defect in the test.
- **Order**: isolate it. Tests that share mutable state pass alone and fail in a suite. Each test sets up and tears down its own world.
- **External services**: pin them. A test that depends on a live network call fails for reasons that have nothing to do with your code. Stub the boundary, or mark it as an integration test that is allowed to be slow.

## Retries hide bugs, they do not fix them

Auto-retrying a failed test until it passes converts a signal into silence. If a test needs three attempts, it is telling you about a real race in the product or the test. Fix the race. Reserve retries for genuinely external flakiness (a third-party sandbox), and when you use one, log it so the flake stays visible instead of vanishing.

## The tell

If a test contains a bare `sleep`, `setTimeout`, or a magic-number delay before an assertion, treat it as a latent flake even if it is green today. Replace the wait with a condition before it costs someone a red build they cannot reproduce.
