# Test Value Audit

Tests earn their place by protecting behavior, an invariant, or an independent contract. A test that must change for a behavior-preserving refactor is suspect unless the source shape itself is the public contract.

## Authoring Gate

Before adding or changing a test, answer four questions:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression would make it fail?
3. Why does existing coverage not already catch that failure?
4. Does it require a production seam no production caller needs?

If any answer is missing, do not add the test yet. Prefer extending the existing owner-boundary test over adding a near duplicate.

## Junk Patterns

Treat these as deletion or rewrite candidates:

- assertion-free coverage probes;
- tests that compare a value with itself or copy expected values from the helper under test;
- exact source, import-list, manifest, class-name, or string-grep checks where behavior is the real contract;
- private predicate, call-shape, or mock-interaction tests duplicated by a public behavior test;
- mocks that implement the behavior being asserted;
- duplicate tests for the same contract at weaker layers;
- production exports, globals, wrappers, flags, or injection hooks used only by tests;
- negative controls that pass because of a different guard than the one under review.

A pattern match is not automatic deletion. Keep a test when it independently guards a public API, plugin SDK, protocol, storage contract, security rule, migration, release artifact, generated output, or known regression with a credible failure mode.

## Audit Workflow

Read before editing:

- the complete test;
- the production owner it claims to cover;
- non-test callers of any support seam;
- sibling tests that might already own the contract;
- relevant history when it explains why the test exists.

Record candidate evidence before deleting:

- test name and location;
- the failure it can actually detect;
- stronger remaining proof, or why proof is no longer needed;
- production or test-support simplification unlocked;
- risk and focused validation command.

Delete obsolete test-only seams with the tests that required them. Do not preserve aliases or replacement tests just to keep the deletion count comfortable.

## Reporting

Separate production/tooling changes from test changes. Report retained false positives and why they are valuable.