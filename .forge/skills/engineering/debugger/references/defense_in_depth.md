# Defense in Depth: fix the class, not the instance

> A fix that only stops today's reproduction case is half a fix. The same bug class comes back wearing a different input.

Once the Root Cause Analysis names the exact logic gap, do not stop at the single line that failed. Harden every layer the bad data crossed on its way to the crash, so the whole class of bug becomes structurally impossible, not just patched once.

## The layer trace

Follow the bad value from where it entered to where it exploded. At each boundary it passed through, ask what should have rejected it and did not.

1. **Entry point**: where untrusted or unexpected data first arrived (request handler, file read, message consumer, user input). Validate shape and range here. Reject early with a specific error.
2. **Boundary crossings**: every function or module that accepted the value and passed it on. Each public boundary should assume its input can be wrong and guard its own preconditions.
3. **Business logic**: the layer that made the wrong decision. Fix the actual gap here. This is the primary fix.
4. **Storage and output**: what persisted or emitted the bad state. Add the constraint (database check, type, enum) that makes the illegal state unrepresentable at rest.

## Make the illegal state unrepresentable

The strongest fix removes the possibility, not just the occurrence.

- Prefer a type or enum over a validated string. If only three values are legal, a union of three values cannot hold a fourth.
- Prefer a non-null constructor over a nullable field plus a null check scattered across callers.
- Prefer a database constraint (not-null, unique, foreign key, check) over application code that "always sets it correctly".
- Prefer parsing input into a known-good shape once at the edge over re-checking the same raw value in ten places.

## Calibrate, do not gold-plate

Defense in depth is not "validate everything everywhere". Add a guard at a layer only when a wrong value reaching that layer would cause real harm. A guard that can never fire is noise that the next reader has to understand and dismiss. The test: could bad data plausibly arrive here from a path other than the one you just fixed? If yes, guard it. If no, one layer is enough.

## Close with a regression test

The reproduction script that triggered the bug becomes a permanent test. It must fail on the old code and pass on the new. Without it, the next refactor silently reopens the hole, and the RCA you just wrote is lost.
