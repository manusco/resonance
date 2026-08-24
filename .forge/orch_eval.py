#!/usr/bin/env python3
"""
Resonance - Orchestration Eval (grounded outcomes for skills a single completion
cannot measure).

`run_evals.py` grades one chat completion against a rubric. That undersells the
orchestration and runtime skills (`/goal`, `/audit`, `/second-opinion`, `/ship`,
`/retro`, `/update-*`), whose value is spawning agents, running tools, or driving a
repo, not writing prose. This harness measures them by GROUNDED OUTCOME: set up a
fixture, run a real AGENT against the task, then check the world (did the test pass?
was the planted bug named?).

Cases live in `.forge/orch_evals/*.json`:
  {
    "name": "goal_fix_failing_test", "skill": "ops/goal",
    "task": "instruction given to the agent",
    "fixture": {"files": {"rel/path": "file contents", ...}},
    "assert": {"type": "command", "cmd": "node --test", "expect_exit": 0}
          |   {"type": "contains", "any": ["sql injection", "unauthenticated"]}
  }

The AGENT must be a real agent that can use tools (not a bare completion): set
`--agent-cmd "<cmd>"` or `RESONANCE_AGENT_CMD`. It is run with cwd set to the fixture
dir and the skill body plus task on stdin; it is expected to modify files there. A
`command` assertion then runs in that dir; a `contains` assertion checks the agent's
final output. Examples of an agent CLI: a headless `opencode run` or `claude -p`.
Without an agent command the harness only validates case structure.

Usage:
  python .forge/orch_eval.py --check
  RESONANCE_AGENT_CMD="opencode run" python .forge/orch_eval.py
Exit: 0 all passed / structure ok, 1 a case failed, 2 bad args.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import evidence as run_evidence
import trace_adapters

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
SKILLS = REPO / ".agents" / "skills"
CASES = FORGE / "orch_evals"


def skill_body(skill: str) -> str:
    p = SKILLS / skill / "SKILL.md"
    if not p.exists():
        return ""
    t = p.read_text(encoding="utf-8", errors="replace")
    end = t.find("\n---", 3)
    return t[end + 4:].strip() if t.startswith("---") and end != -1 else t


def case_skill_paths(case: dict) -> set[str]:
    """Return the bounded skill surface that a case is designed to exercise."""
    paths = {str(case["skill"])}
    trace = case.get("trace_assert", {})
    paths.update(str(path) for path in trace.get("allowed_skills", []))
    paths.update(str(path) for path in trace.get("forbidden_skills", []))
    for pattern in trace.get("ordered_subsequence", []):
        for field in ("target", "actor"):
            value = pattern.get(field)
            if isinstance(value, str) and (SKILLS / value / "SKILL.md").is_file():
                paths.add(value)
    return paths


def stage_framework(work: Path, case: dict) -> None:
    """Expose only the case's runtime skill surface to a disposable fixture."""
    for skill_path in sorted(case_skill_paths(case)):
        source = SKILLS / skill_path
        target = work / ".agents" / "skills" / skill_path
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("evals", "__pycache__"))
    shutil.copy2(REPO / "AGENTS.md", work / "AGENTS.md")


def check_case(c: dict) -> list[str]:
    problems = []
    for k in ("name", "skill", "task", "fixture", "assert"):
        if k not in c:
            problems.append(f"missing '{k}'")
    if "skill" in c and not (SKILLS / c["skill"] / "SKILL.md").exists():
        problems.append(f"skill not found: {c['skill']}")
    if isinstance(c.get("fixture"), dict) and not c["fixture"].get("files"):
        problems.append("fixture has no files")
    a = c.get("assert", {})
    if a.get("type") not in ("command", "contains"):
        problems.append("assert.type must be 'command' or 'contains'")
    ta = c.get("trace_assert")
    if ta is not None:
        if not isinstance(ta, dict):
            problems.append("trace_assert must be an object")
        else:
            allowed = {"run_id", "minimum_assurance", "ordered_subsequence",
                       "allowed_skills", "forbidden_skills", "max_fan_out",
                       "approval_before_side_effect", "artifact_access",
                       "correlate_world_state"}
            extra = set(ta) - allowed
            if extra:
                problems.append(f"trace_assert has unknown fields: {sorted(extra)}")
            level = ta.get("minimum_assurance", 1)
            if not isinstance(level, int) or isinstance(level, bool) or not 0 <= level <= 3:
                problems.append("trace_assert.minimum_assurance must be 0..3")
            if "max_fan_out" in ta and (not isinstance(ta["max_fan_out"], int)
                                        or ta["max_fan_out"] < 0):
                problems.append("trace_assert.max_fan_out must be a non-negative integer")
            for field in ("allowed_skills", "forbidden_skills", "ordered_subsequence",
                          "artifact_access"):
                if field in ta and not isinstance(ta[field], list):
                    problems.append(f"trace_assert.{field} must be an array")
    return problems


def run_case(agent_cmd: list[str], c: dict, timeout: int = 900,
             trace_root: Path | None = None, trace_adapter: str = "") -> dict:
    work = Path(tempfile.mkdtemp(prefix="orch_"))
    try:
        stage_framework(work, c)
        for rel, content in c["fixture"]["files"].items():
            fp = work / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content, encoding="utf-8")
        before = trace_adapters.snapshot_files(work)
        prompt = f"Apply the following skill, then do the task in this directory.\n\n<skill>\n{skill_body(c['skill'])}\n</skill>\n\nTASK: {c['task']}"
        try:
            r = subprocess.run(agent_cmd, cwd=str(work), input=prompt, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=timeout)
            out = ((r.stdout or "") + "\n" + (r.stderr or "")).strip()
            if r.returncode != 0:
                diagnostic = " ".join(out.split())[:500] or "no diagnostic output"
                return {
                    "name": c["name"], "passed": False, "status": "INCOMPLETE",
                    "detail": f"agent exited {r.returncode}: {diagnostic}", "trace": None,
                }
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout or ""
            stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr or ""
            out = (stdout + "\n" + stderr).strip()
            trace_result = None
            if trace_adapter == "opencode-json-v1" and out:
                if trace_root is not None:
                    trace_file = trace_root / f"{c['name']}.jsonl"
                    trace_file.parent.mkdir(parents=True, exist_ok=True)
                    trace_file.write_text(out + "\n", encoding="utf-8")
                loaded = trace_adapters.load_opencode_jsonl(out, work, c.get("trace_assert", {}).get("run_id", c["name"]))
                trace_result = trace_adapters.evaluate_trace(
                    c.get("trace_assert", {}), loaded,
                    trace_adapters.changed_paths(before, trace_adapters.snapshot_files(work)),
                )
            return {
                "name": c["name"], "passed": False, "status": "INCOMPLETE",
                "detail": f"agent timed out after {timeout} seconds; partial trace retained",
                "trace": trace_result,
            }
        except Exception as e:
            return {"name": c["name"], "passed": False, "status": "FAIL",
                    "detail": f"agent error: {e}"}

        a = c["assert"]
        if a["type"] == "command":
            cr = subprocess.run(a["cmd"], cwd=str(work), shell=True, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=600)
            ok = cr.returncode == a.get("expect_exit", 0)
            detail = f"`{a['cmd']}` exit {cr.returncode} (want {a.get('expect_exit', 0)})"
        else:  # contains
            hay = out.lower()
            pats = [p.lower() for p in a.get("any", [])]
            hit = [p for p in pats if p in hay]
            allp = [p.lower() for p in a.get("all", [])]
            miss = [p for p in allp if p not in hay]
            ok = (not pats or bool(hit)) and not miss
            detail = f"matched {hit or 'n/a'}" + (f", missing {miss}" if miss else "")

        trace_result = None
        if "trace_assert" in c:
            run_id = c["trace_assert"].get("run_id", c["name"])
            trace_file = trace_root / f"{c['name']}.jsonl" if trace_root else None
            if trace_adapter == "opencode-json-v1":
                if trace_file is not None:
                    trace_file.parent.mkdir(parents=True, exist_ok=True)
                    trace_file.write_text(out + "\n", encoding="utf-8")
                loaded = trace_adapters.load_opencode_jsonl(out, work, run_id)
            elif trace_adapter != "external-jsonl-v1":
                loaded = trace_adapters.TraceLoad(
                    "INCOMPLETE", [], 0,
                    f"unsupported trace adapter: {trace_adapter or 'none'}")
            else:
                loaded = trace_adapters.load_external_jsonl(trace_file, work, run_id)
            after = trace_adapters.snapshot_files(work)
            trace_result = trace_adapters.evaluate_trace(
                c["trace_assert"], loaded, trace_adapters.changed_paths(before, after))
            if trace_result["status"] != "PASS":
                ok = False
                detail += f"; trace {trace_result['status']}: {trace_result['detail']}"
        return {"name": c["name"], "passed": ok,
                "status": "PASS" if ok else (trace_result or {}).get("status", "FAIL"),
                "detail": detail, "trace": trace_result}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv: list[str]) -> int:
    started = time.monotonic()
    ap = argparse.ArgumentParser(description="Run Resonance grounded orchestration evals.")
    ap.add_argument("--check", action="store_true", help="validate case structure only")
    ap.add_argument("--agent-cmd", default=os.environ.get("RESONANCE_AGENT_CMD", ""),
                    help="a real agent CLI (tools-capable) run in the fixture dir")
    ap.add_argument("--agent-id", default=os.environ.get("RESONANCE_AGENT_ID", ""),
                    help="stable provider/model identity for the agent")
    ap.add_argument("--agent-revision", default=os.environ.get("RESONANCE_AGENT_REVISION", ""))
    ap.add_argument("--evidence-root", default=os.environ.get("RESONANCE_EVIDENCE_ROOT", ""),
                    help="external evidence directory; omitted preserves structure-check behavior")
    ap.add_argument("--baseline-id", default=os.environ.get("RESONANCE_BASELINE_ID", ""))
    ap.add_argument("--promotion", action="store_true",
                    help="fail closed unless promotion-grade provenance is configured")
    ap.add_argument("--seed", default=os.environ.get("RESONANCE_EVAL_SEED", ""))
    ap.add_argument("--trace-adapter", default=os.environ.get("RESONANCE_TRACE_ADAPTER", ""),
                    choices=("", "external-jsonl-v1", "opencode-json-v1"),
                    help="host trace adapter for external schema-v1 JSONL or OpenCode raw JSON events")
    ap.add_argument("--trace-root", default=os.environ.get("RESONANCE_TRACE_ROOT", ""),
                    help="external directory containing <case-name>.jsonl host traces")
    ap.add_argument("--operating-contract",
                    default=os.environ.get("RESONANCE_EVAL_OPERATING_CONTRACT", ""),
                    help="approved evaluation operating contract for trace runs")
    ap.add_argument("--case", action="append", default=[],
                    help="run one named case; repeat to select more than one")
    ap.add_argument("--case-timeout", type=int, default=900,
                    help="maximum seconds for each agent case")
    a = ap.parse_args(argv)

    if a.case_timeout < 1:
        print("--case-timeout must be at least 1 second")
        return 2

    if a.promotion:
        try:
            run_evidence.require_promotion_provenance(
                evidence_root=a.evidence_root, baseline_id=a.baseline_id,
                identities={"agent": a.agent_id}, revisions={"agent": a.agent_revision},
            )
        except ValueError as exc:
            print(f"refusing --promotion: {exc}")
            return 2

    if not CASES.is_dir():
        print(f"no orch_evals dir at {CASES}"); return 2
    case_files = sorted(CASES.glob("*.json"))
    loaded = [(p, json.loads(p.read_text(encoding="utf-8"))) for p in case_files]
    if a.case:
        requested = set(a.case)
        loaded = [(p, case) for p, case in loaded if case.get("name") in requested]
        found = {case.get("name") for _, case in loaded}
        missing = sorted(requested - found)
        if missing:
            print(f"unknown orchestration case(s): {', '.join(missing)}")
            return 2
    case_files = [p for p, _ in loaded]
    cases = [case for _, case in loaded]
    if not cases:
        print("no orchestration eval cases found"); return 2
    if not a.check and a.agent_cmd and any("trace_assert" in case for case in cases):
        try:
            trace_adapters.require_operating_contract(
                Path(a.operating_contract) if a.operating_contract else None,
                a.trace_adapter, os.environ.get("RESONANCE_EVAL_HOST", "local"))
        except ValueError as exc:
            print(f"refusing trace evaluation: {exc}")
            return 2

    evidence_run = None
    if a.evidence_root:
        try:
            evidence_run = run_evidence.EvidenceRun(
                root=Path(a.evidence_root), repo=REPO, runner=Path(__file__),
                runner_id="orch_eval", baseline_id=a.baseline_id, explicit_root=True,
            )
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"refusing evidence root: {exc}")
            return 2
    if a.agent_cmd and not a.check and evidence_run is None:
        print("refusing grounded eval: configure an external --evidence-root or "
              "RESONANCE_EVIDENCE_ROOT")
        return 2

    def finish(code: int, *, result_data: object | None = None, failure: str = "",
               exit_state: str | None = None) -> int:
        if evidence_run is None:
            return code
        try:
            command_items = []
            fingerprints = {}
            if a.agent_cmd:
                item, redacted = run_evidence.command_item("agent", a.agent_cmd)
                command_items.append(item)
                fingerprints["agent"] = redacted
            skill_paths = sorted({c.get("skill", "") for c in cases if c.get("skill")})
            prompt_hashes = []
            tool_call_hashes = []
            for c in cases:
                prompt = ("Apply the following skill, then do the task in this directory.\n\n"
                          f"<skill>\n{skill_body(c['skill'])}\n</skill>\n\nTASK: {c['task']}")
                prompt_hashes.append(run_evidence.hash_item(c["name"], prompt))
                if c.get("assert", {}).get("type") == "command":
                    tool_call_hashes.append(run_evidence.hash_item(
                        c["name"], run_evidence.redact_command(c["assert"]["cmd"])
                    ))
            path = evidence_run.write(
                exit_state=exit_state or ("COMPLETE" if code == 0 else "FAILED"),
                cases=[run_evidence.hash_item(p.name, p) for p in case_files],
                skills=[run_evidence.hash_item(s, SKILLS / s / "SKILL.md") for s in skill_paths],
                instructions_hash=run_evidence.sha256_bytes(run_evidence.canonical_bytes(cases)),
                models={"answerer_id": a.agent_id or "none", "judge_id": "world-state"},
                commands=command_items, command_fingerprints=fingerprints,
                repetitions=1, thresholds={"all_cases_must_pass": True},
                host=os.environ.get("RESONANCE_EVAL_HOST", "local"),
                tool_profile=os.environ.get("RESONANCE_TOOL_PROFILE", "tools-capable-agent"),
                permission_profile=os.environ.get("RESONANCE_PERMISSION_PROFILE", "fixture-sandbox"),
                results=None,
                summary={
                    "mode": "structural" if a.check or not a.agent_cmd else "grounded",
                    "case_count": len(cases), "exit_code": code, "failure": failure or None,
                    "replay_envelope": {
                        "provider_revisions": {"agent": a.agent_revision or None},
                        "decoding": {"seed": a.seed or None, "seed_honored": None},
                        "retry_history": [], "tool_call_hashes": tool_call_hashes,
                        "prompt_hashes": prompt_hashes,
                    },
                },
                latency_ms=int((time.monotonic() - started) * 1000),
                result_payloads={"results.json": result_data} if result_data is not None else None,
            )
            print(f"evidence: {path}")
        except Exception as exc:
            print(f"evidence write failed: {exc}")
            return 1
        return code

    if a.check or not a.agent_cmd:
        print(f"orch-eval CHECK (structure only): {len(cases)} cases\n")
        bad = 0
        for c in cases:
            probs = check_case(c)
            mark = "ok  " if not probs else "FAIL"
            print(f"  [{mark}] {c.get('name','?'):32} {c.get('skill','?')}"
                  + ("" if not probs else "  " + "; ".join(probs)))
            bad += 1 if probs else 0
        print(f"\n{len(cases)} cases | {bad} structural problem(s)")
        if not a.agent_cmd and not a.check:
            print("(no agent command; ran structure check only. Set --agent-cmd or "
                  "RESONANCE_AGENT_CMD to a tools-capable agent for a grounded run.)")
        return finish(1 if bad else 0, result_data={"structural_problems": bad})

    cmd = shlex.split(a.agent_cmd)
    print(f"orch-eval GROUNDED run via `{a.agent_cmd}`: {len(cases)} cases\n")
    failed = 0
    results = []
    for c in cases:
        res = run_case(cmd, c, timeout=a.case_timeout,
                       trace_root=Path(a.trace_root) if a.trace_root else None,
                       trace_adapter=a.trace_adapter)
        results.append(res)
        tag = res.get("status", "PASS" if res["passed"] else "FAIL")
        failed += 0 if res["passed"] else 1
        print(f"  {tag}  {c['name']:32} {c['skill']:22} {res['detail']}")
    print(f"\n{len(cases)} cases | {failed} failed")
    incomplete = any(res.get("status") == "INCOMPLETE" for res in results)
    return finish(1 if failed else 0, result_data=results,
                  failure="one or more grounded cases lacked required evidence" if incomplete
                          else "one or more grounded cases failed" if failed else "",
                  exit_state="INCOMPLETE" if incomplete else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
