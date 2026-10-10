# Private behavioral baseline protocol

This protocol prepares a real skill-lift baseline without putting protected cases, human judgments, raw outputs, or run records in the repository. The repository harness can produce scores; only an approved private dataset and reviewed evidence can make those scores suitable as a baseline.

## Before a scored run

- Pin the repository revision and record the run's `--baseline-id`.
- Store holdout JSON and the evidence root outside the repository. A holdout case has `skill_path`, `skill`, `query`, and a non-empty `expected_behavior` array. Optional deterministic `checks` use the same schema as public eval cases.
- Select an answerer and a separate judge. Record stable provider/model IDs and revisions. The judge must not be the answerer under another command alias.
- Prepare a human-gold calibration sample before scoring. Blind and randomize answer arms, reverse response order across comparisons, and include both known-good and known-bad outputs. Have qualified reviewers label each rubric item independently, resolve disagreements under a written tie rule, then compare the judge with those labels. Set an agreement threshold and disqualify the judge if it misses that threshold or shows position bias. Keep examples and individual labels private.
- Estimate a spend ceiling and wall-clock limit from the provider, planned case count, and repetitions. Obtain the required approval before starting. The harness does not enforce a provider billing ceiling.

The runner's repeated generations and `improve.py calibrate` measure pipeline variance. They do not replace the human-gold judge calibration above. If the holdout, approval, distinct identities, human calibration result, or cost ceiling is missing, record the baseline as `INCOMPLETE` and do not publish a lift claim.

## Run and report

Use explicit, distinct commands and identities, and separate external directories:

```sh
python .forge/run_evals.py --score \
  --holdout-dir /private/evals/holdout \
  --evidence-root /private/evals/evidence \
  --model-cmd "<answerer command>" --model-id "<provider/answerer-version>" \
  --judge-cmd "<independent judge command>" --judge-id "<provider/judge-version>" \
  --baseline-id "<approved baseline ID>" --reps 3
```

Keep case-level files, holdout labels, and raw outputs in the governed private evidence store. A shared report may include only the pinned revision, dataset and evidence hashes, model IDs and revisions, sample counts, aggregate scores, uncertainty, regressions, judge-agreement result, latency, measured cost with provenance, and any incomplete gates. State separately whether the evidence covers skill lift, routing, orchestration, or only one of those.

Do not use the public `.forge/eval_results.json` scratch scorecard or a raw runner exit code as a release verdict. A cost gate is incomplete unless the manifest records a measured finite non-negative amount; measured zero is `0`, while unmeasured cost is `null`.
