# Measuring skills: the eval toolkit

Every Resonance skill ships golden eval cases. This repo ships the MEASURING TOOLS and the CASES; it ships no results. Your scorecards, baselines, and calibration numbers are yours: they land in your own results directory when configured, or in local scratch, never in the repo.

## Versioned contracts

The machine-readable contracts live in `.forge/schemas/`. They use JSON Schema Draft 2020-12 and version 1. The standard-library runtime validates the supported schema subset and fails closed on unsupported keywords. Focused tests cover schema behavior and cross-contract rules.

Every instance must declare `schema_version: 1`. Composition and evaluation operating instances also declare `contract_version: 1`. Unknown versions fail closed. A new version needs a new schema ID, migration notes, compatibility tests, and an explicit runner support change. Producers must not silently upgrade or downgrade evidence.

The contracts are:

- `evidence-manifest.schema.json`: binds a result to the repository state, runner, cases, compiled skills, instructions, models, commands, host, permissions, cost, latency, and result hashes.
- `routing-case.schema.json`: states the expected lead route, allowed contributors, forbidden skills, harm tier, ambiguity behavior, and deterministic checks.
- `invocation-trace.schema.json`: records ordered, attributable lifecycle events and their observed assurance level.
- `promotion-verdict.schema.json`: returns `PROMOTE`, `REJECT`, `INCOMPLETE`, or `INCONCLUSIVE` through a fail-closed precedence order.
- `composition-contract.schema.json`: assigns one lead and finalizer, participant roles, artifact rights, dispatch conditions, version compatibility, and semantic authority.
- `eval-operating-contract.schema.json`: fixes the approved host, model policies, judge qualification, dataset custody, sampling, budgets, retries, evidence age, and failure behavior for live evaluation.

### Composition compatibility

Version 1 supports only version 1 peers. Unknown versions fail closed. Mixed versions are rejected unless a later schema explicitly defines a safe normalization rule. Upgrade and downgrade require an explicit migration. A compatibility declaration never changes the source of truth.

Skill frontmatter owns semantic facts: skill identity, owner, activation, authority, side effects, entrypoints, inputs, outputs, invocation relationships, and failure policy. `.forge/commands.json` owns command presentation: command name, aliases, target skill ID, host exposure, help text, and host rendering. A field claimed by both authorities is a contract error.

Composition has two explicit layers. Each skill carries a declaration in its frontmatter. `.forge/job_composition.py` compiles those declarations into job-level contracts in `docs/job-compositions.json`. The generated file is the inspectable view for hosts and tooling, while frontmatter remains the source. Validation rejects stale output, multiple leads for one job, conflicting participant roles, missing artifact access, or an authority overlap.

Project-specific and private skills remain repository content so every collaborator receives the same procedures. Put them under `.agents/skills/`, commit them with the project, and run `python3 .forge/project_skills.py` after the framework has been installed. The resulting `.resonance/project-skills.lock.json` records only project-owned skill files. Framework upgrades read their own exact-file ownership manifest, preserve unowned skills, and never rewrite the project lock. Use `--check` in project CI. A skill directory containing both framework-owned and project-owned files is rejected because its upgrade behavior would be ambiguous.

### Invocation assurance

Trace levels are cumulative:

1. Level 0 is a model claim with no independent observation.
2. Level 1 is an event recorded by the host adapter outside the model response.
3. Level 2 is an event intercepted at the tool boundary with identity and ordering.
4. Level 3 corroborates the event with world state and artifact hashes.

Read-only specialist invocation requires Level 1. Approval, authority, writes, external actions, and destructive actions require Level 2. A mutating outcome claim requires Level 3. Unsupported assurance returns `INCOMPLETE`, never success.

### Operating approval and dataset custody

No live model run for S06, S09, or S12 may start without a user-approved operating-contract instance whose hash matches the reviewed artifact. The contract names one canary host and adapter, an answerer policy, a separate judge policy, confidence and abstention rules, minimum and maximum samples, spend and time ceilings, concurrency, retries, outage behavior, and evidence expiry.

## Promotion verdicts

`python .forge/promotion_eval.py --candidate-id <id> --manifest <path>` consumes immutable evidence manifests, verifies them against the current repository identity, and applies the fixed gate precedence from the promotion schema. It returns `PROMOTE`, `REJECT`, or `INCOMPLETE`. Missing protected routing evidence, grounded orchestration evidence, current provenance, or required run kinds is `INCOMPLETE`, never a pass. Use `--allow-dirty` only when every manifest records the exact current changed-path set.

Judge qualification requires blinded randomized arm labels, response-order reversal, a human-gold calibration set, an agreement threshold, a tie policy, and a disqualification rule.

Data has four custody classes:

- Public development fixtures may be inspected and used during authoring.
- Protected validation cases reveal scores and failure classes under a custodian. Exposure is logged as contamination and triggers rotation when the declared rule requires it.
- Sealed promotion cases hide prompts, labels, and case-level results from implementers. A set is retired after its approved promotion use or leakage.
- Reserve cases replace contaminated or retired protected material.

Each dataset record names its owner, external path, creation time, access log, hash manifest, permitted use, reuse count, contamination events, rotation rule, and retirement state. Protected content does not enter this repository.

### Promotion precedence

Promotion stops at the first failing gate in this order:

1. Evidence integrity and dataset eligibility
2. Security, legal, authority, approval, destructive action, incident, shipping, and external communication
3. Public entrypoint and compatibility preservation
4. Required trace assurance
5. Structural and generated-source integrity
6. Routing and orchestration harm
7. Declared safety or determinism metrics
8. Task quality or lift
9. Cost and latency budgets

A lower gate cannot offset a higher failure. Missing required evidence returns `INCOMPLETE`. A powered or sequential test that reaches its approved cap without a decision returns `INCONCLUSIVE`.

## The three layers

1. **Structure gate (free, deterministic, seconds).** `npm run eval` (`run_evals.py --all --check`) verifies every case binds to a real skill, has a query, a rubric, and valid deterministic checks. Runs in the pre-push ship-gate.
2. **Scored lift (model-priced, minutes).** `run_evals.py --all --score` answers every case twice per rep, once cold and once with the skill body in context, grades both, and reports the lift per skill. Honesty rules are enforced, not suggested:
   - the judge is never the answerer (`RESONANCE_JUDGE_CMD` must differ; the run refuses otherwise),
   - at least 3 generations per arm per case (a lucky completion cannot carry a verdict),
   - cases may carry deterministic `checks` graded in pure Python (kinds: `regex_absent`, `contains_any`, `section_present`, `max_lines`); a skill whose items are half deterministic gets a `grounded` marker,
   - a case whose cold arm already passes the full rubric is flagged as a dead case (it discriminates nothing),
   - planted-defect cases (one per skill) embed a concrete doctrine violation in the query, so grading has ground truth instead of self-agreement.
3. **Grounded orchestration evals (agent-priced).** `run_evals` grades one completion; orchestration skills (`/goal`, `/build`, `/ship`, `/audit`, `/reviewer`) are graded by outcome instead: `orch_eval.py` stands up a fixture with a planted defect, runs a real tools-capable agent, then checks the world (did the executed suite go green, did the release get refused on a red suite).

## Public routing evals

Routing has its own harness because selecting a skill is different from measuring
what that skill does after selection. `.forge/routing_eval.py` does not read or
interpret `baseline_skills`. It feeds the router the compiled startup catalog from
`docs/skill-manifest.json`, including each skill's real description, exclusions,
host activation, authority, and entrypoints. Host activation describes how a host
exposes or invokes a skill. It does not decide whether natural language may route
to that skill. Case labels and rationales never enter the
router prompt.

Routing modes have one meaning across the framework:

- `AUTO`: a normal-language request clearly matches a skill.
- `MANUAL`: the user explicitly invoked a command, skill ID, or compatibility
  entrypoint, or the requested consequential action needs deliberate confirmation.
- `ASK`: one missing answer would materially change the route.
- `NONE`: no specialist is warranted.

Skill selection does not authorize side effects. A skill selected with `AUTO` must
still honor its authority contract and any approval gate before it writes, sends,
publishes, deploys, deletes, or starts an autonomous loop.

Public fixtures live in `.forge/routing_evals/`. They cover the highest-priority
ownership collisions, high-harm boundaries, material ambiguity, and requests that
need no skill. Each case declares one expected primary, allowed contributors,
forbidden skills, expected activation mode, abstention behavior, a cluster, and a
harm tier. These fixtures support development. They do not replace protected or
sealed cases.

Run the free structure gate with:

```powershell
py .forge/routing_eval.py --check
```

Run live routing with an explicit command and attributable model ID:

```powershell
py .forge/routing_eval.py --model-cmd "<router command>" --model-id "<provider/model-version>" --results "D:/private/routing-result.json"
```

### Protected routing datasets

Routing has two private tiers. Protected validation supports bounded diagnosis. Sealed promotion is a one-use release gate and never emits case-level results. Keep both outside the repository. Never copy their prompts, labels, rationales, hashes, custody state, or access logs into `.resonance/`.

Use one private tier per run:

```powershell
py .forge/routing_eval.py --validation-holdout-dir "D:/private/validation" --model-cmd "<router command>" --model-id "<provider/model-version>"
py .forge/routing_eval.py --promotion-holdout-dir "D:/private/promotion" --model-cmd "<router command>" --model-id "<provider/model-version>"
```

The equivalent environment variables are `RESONANCE_ROUTING_VALIDATION_HOLDOUT_DIR` and `RESONANCE_ROUTING_PROMOTION_HOLDOUT_DIR`.

Each dataset directory contains:

- `dataset.json`, immutable custody policy and the declared dataset role
- `hash-manifest.json`, SHA-256 hashes for every immutable case file
- `cases/*.json`, opaque routing cases using routing case schema version 1
- `custody-state.json`, reuse count, contamination events, and retirement state
- `access-log.jsonl`, append-only access, verification, contamination, and result events

Material ambiguity cases must declare `ask_materiality.route_changes_primary: true` and at
least two possible primary skill IDs. This prevents an ASK oracle when the missing answer
only changes the method within one owner. Sealed summaries contain aggregate metrics and
violation-category counts only. An optional `--failed-run-sidecar` may write raw outputs
and case-level diagnostics after a sealed set retires, but only to an existing path outside
the repository. Passing runs never write a sidecar.

The runner rejects repository-local datasets, role confusion, inactive or exhausted sets, invalid manifests, oracle fields in prompts or outputs, and protected-file mutation. It hashes immutable inputs before and after execution. Mutation or oracle leakage contaminates and retires the set. Protected output contains only hashes and summaries. Validation may include hashed case diagnostics when its policy allows this. Sealed promotion always uses `SUMMARY_ONLY` diagnostics.

The router must return strict JSON with exactly these fields: `primary_skill`,
`contributors`, `mode`, `abstain`, `confidence`, `reason`, and `clarification`.
Invalid output fails before scoring. Live results should be written outside the
repository.

Routing reports exact-primary accuracy, contributor precision and recall,
forbidden-invocation rate, abstention quality, and confusion matrices per expected
skill and collision cluster. `STANDARD`, `HIGH`, and `CRITICAL` are separate harm
tiers. Release scoring fails on any critical forbidden selection, any routing mode
mismatch, and any high-harm primary misroute in a
changed cluster. Clear standard cases require at least 95 percent macro accuracy.
The report also states a two-sided 95 percent Wilson score interval for transparent
uncertainty. The point threshold is the gate; the interval reports sampling
precision and does not let aggregate results override a harm gate.

## Keep/revert decisions: the calibrated gate

Editing a skill and eyeballing the new score is how metrics get gamed. `improve.py` enforces the honest loop:

```
python .forge/improve.py worklist                 # skills with no measured lift
python .forge/improve.py calibrate                # one-time A/A noise floors
python .forge/improve.py remeasure <skill-path>   # paired A/B vs HEAD, verdict
```

- **Calibrate first.** Ten A/A runs (a skill measured against itself) establish the pipeline's noise floor. Floors are pooled across the calibration set and shared by all skills; the pooled floor is the minimum detectable effect of the gate, printed so nobody mistakes noise for signal. Uncalibrated remeasures print numbers but refuse verdicts.
- **Paired remeasure.** The body at `--baseline-ref` and the working tree run in the same session, same cases, same judge. KEEP only if the mean delta clears `max(0.10, pooled floor)` AND no case regressed beyond the per-case floor.
- **Rubric edits never count as lift.** The evals directory is hashed into the baseline; a changed hash means NEW BASELINE and no verdict. Make the test harder and the skill better, in that order.

## Wiring a model

Any CLI that reads a prompt on stdin and prints the completion works:

```
RESONANCE_MODEL_CMD="python .forge/exec/model_cli.py"   # answerer (OpenAI-compatible endpoint)
RESONANCE_JUDGE_CMD="<a DIFFERENT model command>"        # judge
RESONANCE_AGENT_CMD="<a tools-capable agent CLI>"        # orchestration evals
```

`.forge/exec/model_cli.py` adapts any OpenAI-compatible endpoint (`MODEL_BASE_URL`, `MODEL_NAME`, `MODEL_API_KEY`) to that contract, with UTF-8 forced and retries built in.

## Cost, so nobody skips measurement out of fear

A full-library scored run at 3 reps is roughly 240 cases x 3 reps x 2 arms plus judging: low single-digit dollars on a budget model. A per-skill remeasure is cents. Calibration is a few hundred calls, once.
