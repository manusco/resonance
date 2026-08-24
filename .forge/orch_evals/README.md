# Orchestration Evals (grounded outcomes)

The completion scorecard (`run_evals.py --score`) grades a single chat answer against a rubric. That cannot measure the skills whose value is a runtime: `/goal` drives a build-and-verify loop, `/audit` runs a review swarm, `/second-opinion` dispatches a second model, `/ship` drives a release. A one-shot completion can only DESCRIBE those, so it scores near zero even when the skill is excellent (on the 2026-07-06 run, `/audit` wrote a 4300-character audit and still scored 0 because it could not actually spawn the four sub-agents).

These evals measure by grounded outcome instead. Each case (`.forge/orch_evals/*.json`) sets up a fixture with planted ground truth, runs a real, tools-capable AGENT against the task in that fixture, then checks the world:

- **`goal_fix_failing_test`** (`/goal`): a repo with a failing test. Assert: `node --test` passes after the agent runs. Did the goal actually reach its done-condition?
- **`audit_planted_vuln`** (`/audit`): a route with a string-concatenated SQL query and no auth check. Assert: the audit names the vulnerability. Did the swarm find the planted bug?
- **`reviewer_catches_authz`** (`/reviewer`): a promote-to-admin endpoint with no authorization check. Assert: the review flags it.

## Run it

The agent must be a real agent that can use tools (not a bare completion):

```
RESONANCE_AGENT_CMD="opencode run --format json" python .forge/orch_eval.py  # grounded run
python .forge/orch_eval.py --check                                # structure only
```

Invoke the host process directly. The harness already sends the prompt through standard input and sets the fixture directory. Avoid wrappers that spawn another long-running host process because the case timeout must terminate the real process.

`command` assertions run in the fixture directory and the exit code decides. `contains` assertions check the agent's final output for any of the given patterns. To add a case, drop a JSON file here following the shape documented in `.forge/orch_eval.py`'s header.

## Invocation traces

Cases may add a `trace_assert` object without changing the existing outcome assertion:

```json
{
  "trace_assert": {
    "minimum_assurance": 1,
    "ordered_subsequence": [
      {"event": "INVOKE", "target": "ops/security"},
      {"event": "REVIEW", "actor": "ops/security"}
    ],
    "allowed_skills": ["ops/security", "ops/reviewer"],
    "forbidden_skills": ["ops/ship"],
    "max_fan_out": 2,
    "approval_before_side_effect": true,
    "artifact_access": [
      {"artifact": "report.md", "owner": "ops/audit", "allowed_mutations": ["MODIFY"]}
    ],
    "correlate_world_state": true
  }
}
```

Events follow `.forge/schemas/invocation-trace.schema.json`, one event per JSONL line. The first bounded adapter is `external-jsonl-v1`. It reads `<case-name>.jsonl` from an external directory:

```text
python .forge/orch_eval.py --agent-cmd "<host command>" \
  --trace-adapter external-jsonl-v1 --trace-root D:/private/host-traces \
  --operating-contract D:/private/eval-operating-contract.json
```

The approved operating contract must name the current host and `external-jsonl-v1` adapter. The adapter assigns Level 1 only. A trace inside the agent-writable fixture is rejected as fabricated evidence. Missing adapters and missing traces return `INCOMPLETE`, never pass. Approval and side-effect boundaries require Level 2. A mutating outcome reaches Level 3 only when the trace artifact path matches the observed fixture change. This keeps read-only invocation evidence useful without treating model-authored claims as host observation.

For `opencode-json-v1`, pass an external `--trace-root` to retain the raw host JSONL. Raw OpenCode traces can contain prompts, responses, tool inputs, and cost data. Store them as private evidence outside the public repository.

This is the eval-first philosophy applied to the orchestration layer: judge the skills that act by what they make true in the world, not by what they say.
