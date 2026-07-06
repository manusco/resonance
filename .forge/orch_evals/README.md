# Orchestration Evals (grounded outcomes)

The completion scorecard (`run_evals.py --score`) grades a single chat answer against a rubric. That cannot measure the skills whose value is a runtime: `/goal` drives a build-and-verify loop, `/audit` runs a review swarm, `/second-opinion` dispatches a second model, `/ship` drives a release. A one-shot completion can only DESCRIBE those, so it scores near zero even when the skill is excellent (on the 2026-07-06 run, `/audit` wrote a 4300-character audit and still scored 0 because it could not actually spawn the four sub-agents).

These evals measure by grounded outcome instead. Each case (`.forge/orch_evals/*.json`) sets up a fixture with planted ground truth, runs a real, tools-capable AGENT against the task in that fixture, then checks the world:

- **`goal_fix_failing_test`** (`/goal`): a repo with a failing test. Assert: `node --test` passes after the agent runs. Did the goal actually reach its done-condition?
- **`audit_planted_vuln`** (`/audit`): a route with a string-concatenated SQL query and no auth check. Assert: the audit names the vulnerability. Did the swarm find the planted bug?
- **`reviewer_catches_authz`** (`/reviewer`): a promote-to-admin endpoint with no authorization check. Assert: the review flags it.

## Run it

The agent must be a real agent that can use tools (not a bare completion):

```
RESONANCE_AGENT_CMD="opencode run" python .forge/orch_eval.py     # grounded run
python .forge/orch_eval.py --check                                # structure only
```

`command` assertions run in the fixture directory and the exit code decides. `contains` assertions check the agent's final output for any of the given patterns. To add a case, drop a JSON file here following the shape documented in `.forge/orch_eval.py`'s header.

This is the eval-first philosophy applied to the orchestration layer: judge the skills that act by what they make true in the world, not by what they say.
