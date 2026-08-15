#!/usr/bin/env python3
"""
Resonance Forge - Eval Runner and Scorecard (R1 + Track 1).

Skills ship golden cases in evals/*.json. `validate_skill.py` checks they EXIST;
this actually RUNS them and measures the lift each skill produces.

Modes:
  --check      structural gate, free, <1s. Every case has a matching skill name,
               a query, and a non-empty rubric. CI-safe. (Default with no model.)
  live         for each case, prompt a model WITH and WITHOUT the skill body, then
               have a judge grade both against the rubric. Reports with-minus-without.
  --score      live run aggregated into a per-skill scorecard: the measured proof
               that a skill helps, and the list of skills that do not (the /improve
               work-list). Results are written to local scratch
               (.forge/eval_results.json) and, when a private results directory is
               configured (~/.resonance/machine.json), the scorecard and the
               per-skill baseline land there. Results never land in the repo.

Honesty rules for scored runs:
  - the judge is never the answerer: set RESONANCE_JUDGE_CMD (or --judge-cmd)
    to a DIFFERENT model; --score refuses to run when they are equal.
  - k generations per arm per case (--reps; scored runs force >= 3) so a single
    lucky completion cannot decide a verdict.
  - cases may carry deterministic `checks` (regex_absent, regex_present,
    contains_any, contains_all, section_present, max_lines) graded in pure Python at zero cost; they merge
    into the rubric fraction and shrink the judged surface.
  - a case whose without-arm passes the full rubric discriminates nothing and
    gets flagged as a dead case.

The model is pluggable so this stays cross-tool and never locks a vendor:
  --model-cmd "claude -p"        (default when the claude CLI is present)
  env RESONANCE_MODEL_CMD="..."  (same)
Any CLI that reads a prompt on stdin and prints the completion works.

Selection:
  path (e.g. marketing/seo) | --all | --changed [ref]   (only skills changed vs ref)
  --limit N   cap cases per skill (cheap sampling)
  --parallel N   concurrent model calls (default 4)

Usage:
  python .forge/run_evals.py --all --check
  python .forge/run_evals.py --all --score --model-cmd "claude -p"
  python .forge/run_evals.py --changed --score --limit 1

Exit: 0 pass, 1 a case failed / structural problem / a skill showed no lift, 2 bad args.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_integrity

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FORGE = Path(__file__).resolve().parent
REPO = FORGE.parent
SKILLS = REPO / ".agents" / "skills"
NAME_RE = re.compile(r"(?m)^name:\s*(.+?)\s*$")
SENSITIVE_NAMES = {".env", ".npmrc", ".pypirc", "credentials", "credentials.json"}
SENSITIVE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
ALLOWED_FIXTURE_ROOTS = {"src", "docs", "tests", "fixtures", "examples"}


@dataclass
class ModelFailure(RuntimeError):
    command: list[str]
    returncode: int | None
    stdout: str
    stderr: str

    def __str__(self) -> str:
        return f"model command failed with exit {self.returncode}: {self.stderr.strip() or 'no stderr'}"


def contained_fixture(relpath: str) -> Path:
    if not isinstance(relpath, str) or not relpath.strip():
        raise ValueError("eval file path must be a non-empty repository-relative path")
    candidate = Path(relpath)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"eval file escapes repository: {relpath}")
    if not candidate.parts or candidate.parts[0] not in ALLOWED_FIXTURE_ROOTS:
        raise ValueError(f"eval file is outside approved fixture roots: {relpath}")
    resolved = (REPO / candidate).resolve(strict=False)
    try:
        resolved.relative_to(REPO.resolve())
    except ValueError as exc:
        raise ValueError(f"eval file escapes repository: {relpath}") from exc
    if resolved.name.lower() in SENSITIVE_NAMES or resolved.suffix.lower() in SENSITIVE_SUFFIXES:
        raise ValueError(f"eval file is sensitive and cannot be sent to a model: {relpath}")
    return resolved


def skill_name(skill_md: Path) -> str:
    m = NAME_RE.search(skill_md.read_text(encoding="utf-8", errors="replace")[:2000])
    return m.group(1).strip().strip('"').strip("'") if m else ""


def skill_body(skill_md: Path) -> str:
    t = skill_md.read_text(encoding="utf-8", errors="replace")
    end = t.find("\n---", 3)
    return t[end + 4:].strip() if t.startswith("---") and end != -1 else t


def skill_rel(sk: Path) -> str:
    return sk.parent.relative_to(SKILLS).as_posix()


def skill_md_for_rel(path: str) -> Path:
    candidate = Path(path)
    if not path or candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"skill path escapes canonical skills: {path}")
    resolved = (SKILLS / candidate / "SKILL.md").resolve(strict=False)
    try:
        resolved.relative_to(SKILLS.resolve())
    except ValueError as exc:
        raise ValueError(f"skill path escapes canonical skills: {path}") from exc
    return resolved


def changed_skill_paths(ref: str) -> set[str]:
    """Skill dirs (domain/name) whose source or output changed vs a git ref."""
    try:
        r = subprocess.run(["git", "diff", "--name-only", ref], cwd=str(REPO),
                           capture_output=True, text=True, timeout=30)
    except Exception:
        return set()
    out: set[str] = set()
    for f in r.stdout.splitlines():
        m = re.search(r"(?:\.agents|\.forge)/skills/(.+?)/(?:SKILL\.md|skill\.tmpl\.md|references/|evals/)", f)
        if m:
            out.add(m.group(1))
    return out


def find_cases(path: str, changed_ref: str | None) -> list[tuple[Path, Path]]:
    out = []
    roots = sorted(SKILLS.glob("**/SKILL.md")) if path == "--all" else [skill_md_for_rel(path)]
    changed = changed_skill_paths(changed_ref) if changed_ref else None
    for sk in roots:
        if changed is not None and skill_rel(sk) not in changed:
            continue
        evdir = sk.parent / "evals"
        if evdir.is_dir():
            for ev in sorted(evdir.glob("*.json")):
                out.append((sk, ev))
    return out


def holdout_cases(root: str) -> list[tuple[Path, Path]]:
    if not root:
        raise ValueError("scored runs require --holdout-dir or RESONANCE_HOLDOUT_DIR")
    directory = Path(root).resolve(strict=True)
    try:
        directory.relative_to(REPO.resolve())
        raise ValueError("protected holdout must be outside the repository")
    except ValueError as exc:
        if str(exc) == "protected holdout must be outside the repository":
            raise
    cases = []
    for ev in sorted(directory.glob("*.json")):
        data = json.loads(ev.read_text(encoding="utf-8"))
        rel = data.get("skill_path", "")
        sk = skill_md_for_rel(rel)
        if not sk.is_file():
            raise ValueError(f"holdout references unknown skill_path: {rel}")
        cases.append((sk, ev))
    if not cases:
        raise ValueError("protected holdout contains no JSON cases")
    return cases


def file_hashes(paths: list[Path]) -> dict[str, str]:
    return {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def same_command(left: str, right: str) -> bool:
    return shlex.split(left) == shlex.split(right)


def run_model(cmd: list[str], prompt: str) -> str:
    try:
        # force UTF-8 on stdin/stdout: skill bodies use non-ASCII (arrows, quotes)
        # that the Windows locale (cp1252) cannot encode, which would silently fail.
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=300,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            raise ModelFailure(cmd, r.returncode, r.stdout or "", r.stderr or "")
        output = (r.stdout or "").strip()
        if not output:
            raise ModelFailure(cmd, r.returncode, r.stdout or "", "model returned empty output")
        return output
    except Exception as e:
        if isinstance(e, ModelFailure):
            raise
        raise ModelFailure(cmd, None, "", str(e)) from e


def build_prompt(case: dict, body: str | None, selected_path: str | None = None) -> str:
    parts = []
    if body:
        parts.append("Apply the following selected skill to the task.\n\n"
                     "<skill role=\"selected\">\n" + body + "\n</skill>\n")
    for relpath in case.get("baseline_skills", []) or []:
        if selected_path and relpath == selected_path:
            continue
        fp = skill_md_for_rel(relpath)
        if fp.exists():
            parts.append(f"Also consider this existing Resonance skill when routing ownership.\n\n"
                         f"<skill role=\"baseline\" path=\"{relpath}\">\n"
                         f"{skill_body(fp)}\n</skill>\n")
    for f in case.get("files", []) or []:
        fp = contained_fixture(f)
        if fp.is_file():
            parts.append(f"<file path=\"{f}\">\n{fp.read_text(encoding='utf-8', errors='replace')}\n</file>")
    parts.append("Task: " + case["query"])
    return "\n\n".join(parts)


def judge(cmd: list[str], query: str, output: str, rubric: list[str]) -> list[bool]:
    items = "\n".join(f"{i+1}. {r}" for i, r in enumerate(rubric))
    p = (f"You are grading an AI output against a rubric. Be strict and literal.\n\n"
         f"TASK:\n{query}\n\nOUTPUT:\n{output}\n\nRUBRIC (each item pass or fail):\n{items}\n\n"
         f"Reply with ONLY a JSON array of booleans, one per rubric item, e.g. [true,false,true].")
    raw = run_model(cmd, p)
    m = re.search(r"\[[^\]]*\]", raw)
    try:
        vals = json.loads(m.group(0)) if m else []
        if (not isinstance(vals, list) or len(vals) != len(rubric)
                or any(type(v) is not bool for v in vals)):
            return [False] * len(rubric)
        return vals
    except Exception:
        return [False] * len(rubric)


CHECK_KINDS = ("regex_absent", "regex_present", "contains_any", "contains_all",
               "section_present", "max_lines")


def det_checks(output: str, checks: list) -> int:
    """Deterministic check kinds, evaluated in pure Python at zero cost.
    Returns how many passed. Six kinds, hard cap (resist check-kind sprawl):
      regex_absent:    value regex must NOT match the output
      regex_present:   value regex must match the output
      contains_any:    at least one of the value literals appears (case-insensitive)
      contains_all:    all value literals appear (case-insensitive)
      section_present: value text appears in a markdown heading
      max_lines:       output has at most value lines
    """
    passed = 0
    for c in checks or []:
        kind, val = c.get("kind"), c.get("value")
        ok = False
        try:
            if kind == "regex_absent":
                ok = re.search(str(val), output) is None
            elif kind == "regex_present":
                ok = re.search(str(val), output) is not None
            elif kind == "contains_any":
                low = output.lower()
                vals = val if isinstance(val, list) else [val]
                ok = any(str(v).lower() in low for v in vals)
            elif kind == "contains_all":
                low = output.lower()
                vals = val if isinstance(val, list) else [val]
                ok = all(str(v).lower() in low for v in vals)
            elif kind == "section_present":
                ok = re.search(r"(?mi)^#{1,6}\s+.*" + re.escape(str(val)), output) is not None
            elif kind == "max_lines":
                ok = len(output.splitlines()) <= int(val)
        except Exception:
            ok = False
        passed += 1 if ok else 0
    return passed


def private_eval_dir() -> Path | None:
    """Scored results are internal. When ~/.resonance/machine.json wires this
    repo (publicMirror) to a private memory (flagshipMemory), results land in
    the sibling eval/ directory there. Everywhere else: None, and results stay
    in local scratch. Public artifacts never carry results."""
    gb = Path(os.environ.get("RESONANCE_GLOBAL_BRAIN", str(Path.home() / ".resonance")))
    try:
        cfg = json.loads((gb / "machine.json").read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    pm, fm = cfg.get("publicMirror", ""), cfg.get("flagshipMemory", "")
    if not pm or not fm:
        return None
    try:
        if Path(pm).resolve() != REPO.resolve():
            return None
    except Exception:
        return None
    d = Path(fm).parent / "eval"
    return d if d.parent.is_dir() else None


def evals_dir_hash(skill_path: str) -> str:
    """Hash of a skill's SOURCE eval cases. A changed hash means the rubric
    changed, which resets the improvement baseline (a rubric edit can never
    count as lift)."""
    evdir = REPO / ".forge" / "skills" / skill_path / "evals"
    if not evdir.is_dir():
        evdir = SKILLS / skill_path / "evals"
    h = __import__("hashlib").sha1()
    if evdir.is_dir():
        for f in sorted(evdir.glob("*.json")):
            h.update(f.name.encode("utf-8"))
            h.update(f.read_bytes())
    return h.hexdigest()[:16]


def load_baseline(out_dir: Path) -> dict:
    p = out_dir / "eval_baseline.json"
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def save_baseline(out_dir: Path, data: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "eval_baseline.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_case(sk: Path, ev: Path) -> list[str]:
    problems = []
    try:
        d = json.loads(ev.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"invalid JSON: {e}"]
    if d.get("skill") != skill_name(sk):
        problems.append(f"skill field '{d.get('skill')}' != frontmatter name '{skill_name(sk)}'")
    if not d.get("query", "").strip():
        problems.append("empty query")
    rub = d.get("expected_behavior")
    if not isinstance(rub, list) or not rub:
        problems.append("expected_behavior is missing or empty")
    for c in d.get("checks") or []:
        if not isinstance(c, dict) or c.get("kind") not in CHECK_KINDS or "value" not in c:
            problems.append(f"invalid check (kind must be one of {CHECK_KINDS}, with a value): {c}")
    for relpath in d.get("baseline_skills", []) or []:
        try:
            found = isinstance(relpath, str) and skill_md_for_rel(relpath).is_file()
        except ValueError:
            found = False
        if not found:
            problems.append(f"baseline skill not found: {relpath}")
    for relpath in d.get("files", []) or []:
        try:
            fixture = contained_fixture(relpath)
            if not fixture.is_file() and not d.get("fixture_optional", False):
                problems.append(f"fixture file not found: {relpath}")
        except (OSError, ValueError) as exc:
            problems.append(str(exc))
    return problems


def run_case(cmd: list[str], judge_cmd: list[str], sk: Path, ev: Path, threshold: float,
             reps: int = 1, body: str | None = None) -> dict:
    d = json.loads(ev.read_text(encoding="utf-8"))
    rub = d["expected_behavior"]
    checks = d.get("checks") or []
    the_body = skill_body(sk) if body is None else body
    selected_path = skill_rel(sk)
    n = len(rub) + len(checks)
    wf: list[float] = []
    wof: list[float] = []
    evidence = []
    for rep in range(max(1, reps)):
        prompts = (build_prompt(d, the_body, selected_path=selected_path), build_prompt(d, None))
        if rep % 2:
            without, with_out = run_model(cmd, prompts[1]), run_model(cmd, prompts[0])
            order = ["without", "with"]
        else:
            with_out, without = run_model(cmd, prompts[0]), run_model(cmd, prompts[1])
            order = ["with", "without"]
        sw = sum(judge(judge_cmd, d["query"], with_out, rub)) + det_checks(with_out, checks)
        swo = sum(judge(judge_cmd, d["query"], without, rub)) + det_checks(without, checks)
        wf.append(sw / n)
        wof.append(swo / n)
        evidence.append({"rep": rep + 1, "order": order, "with_output": with_out,
                         "without_output": without, "with_score": wf[-1],
                         "without_score": wof[-1]})
    with_frac = sum(wf) / len(wf)
    without_frac = sum(wof) / len(wof)
    return {"skill": skill_name(sk), "path": skill_rel(sk), "eval": ev.name,
            "rubric_n": len(rub), "checks_n": len(checks), "reps": len(wf),
            "with_frac": with_frac, "without_frac": without_frac,
            "with_reps": wf, "without_reps": wof,
            "evidence": evidence,
            "pass": with_frac >= threshold and with_frac >= without_frac}


def verdict(with_avg: float, lift: float, threshold: float) -> str:
    if with_avg >= threshold and lift > 0.05:
        return "proven"
    if lift < -0.05 or with_avg < threshold - 0.2:
        return "weak"
    return "flat"


def write_scorecard(results: list[dict], threshold: float, judge_label: str = "",
                    reps: int = 1) -> tuple[str, dict]:
    by_skill: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_skill[r["path"]].append(r)
    rows = []
    dead: list[str] = []
    for path, rs in sorted(by_skill.items()):
        n = len(rs)
        wavg = sum(r["with_frac"] for r in rs) / n
        woavg = sum(r["without_frac"] for r in rs) / n
        lift = wavg - woavg
        total_items = sum(r["rubric_n"] + r["checks_n"] for r in rs)
        det_items = sum(r["checks_n"] for r in rs)
        det_ratio = det_items / total_items if total_items else 0.0
        rows.append({"path": path, "skill": rs[0]["skill"], "cases": n,
                     "with": round(wavg, 3), "without": round(woavg, 3), "lift": round(lift, 3),
                     "det_ratio": round(det_ratio, 2),
                     "grounded": det_ratio >= 0.5,
                     "verdict": verdict(wavg, lift, threshold)})
        for r in rs:
            # a case whose without-arm passes the whole rubric discriminates nothing
            if r["without_frac"] >= 0.999:
                dead.append(f"{path}/{r['eval']}")
    rows.sort(key=lambda x: x["lift"], reverse=True)
    proven = sum(1 for r in rows if r["verdict"] == "proven")
    weak = [r["path"] for r in rows if r["verdict"] == "weak"]

    lines = ["# Resonance Eval Scorecard", "",
             "Measured lift per skill: the same task graded with and without the skill "
             "in context. `with` and `without` are the mean fraction of the rubric satisfied "
             "(LLM-judged items plus deterministic checks). `lift` is the gap the skill closes. "
             "Produced by `.forge/run_evals.py --score`.", "",
             f"Method: {reps} generation(s) per arm per case; judge: `{judge_label or 'same as answerer (structure runs only)'}`. "
             f"Per-skill verdicts at low case counts are indicative, not proof; keep/revert "
             f"decisions use the calibrated paired rule in `improve.py remeasure`, never this table alone. "
             f"`grounded` marks skills whose items are >= 50% deterministic.", "",
             f"- Skills measured: **{len(rows)}**  |  proven (real lift): **{proven}**  |  "
             f"weak (no lift, the /improve work-list): **{len(weak)}**  |  dead cases: **{len(dead)}**", "",
             "| skill | cases | without | with | lift | det | verdict |",
             "| :-- | --: | --: | --: | --: | --: | :-- |"]
    for r in rows:
        g = " (grounded)" if r["grounded"] else ""
        lines.append(f"| `{r['path']}` | {r['cases']} | {r['without']:.2f} | {r['with']:.2f} | "
                     f"{r['lift']:+.2f} | {r['det_ratio']:.0%} | {r['verdict']}{g} |")
    if weak:
        lines += ["", "## Work-list (skills showing no measured lift)", ""]
        lines += [f"- `{p}`" for p in weak]
    if dead:
        lines += ["", "## Dead cases (the without-arm already passes; they discriminate nothing)", ""]
        lines += [f"- `{c}`" for c in dead]
    md = "\n".join(lines) + "\n"
    data = {"threshold": threshold, "reps": reps, "judge": judge_label, "skills": rows,
            "dead_cases": dead,
            "summary": {"measured": len(rows), "proven": proven, "weak": len(weak),
                        "dead": len(dead)}}
    return md, data


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Run Resonance golden evals and score skill lift.")
    ap.add_argument("path", nargs="?", default=None, help="skill path (e.g. marketing/seo); omit for all")
    ap.add_argument("--all", action="store_true", help="run every skill's evals")
    ap.add_argument("--check", action="store_true", help="structure only, no model")
    ap.add_argument("--score", action="store_true", help="live run, write the per-skill scorecard")
    ap.add_argument("--changed", nargs="?", const="HEAD~1", default=None,
                    help="only skills changed vs a git ref (default HEAD~1)")
    ap.add_argument("--limit", type=int, default=0, help="cap cases per skill (0 = all)")
    ap.add_argument("--parallel", type=int, default=4, help="concurrent model calls")
    ap.add_argument("--model-cmd", default=os.environ.get("RESONANCE_MODEL_CMD", ""),
                    help="model command reading the prompt on stdin (default: claude -p)")
    ap.add_argument("--judge-cmd", default=os.environ.get("RESONANCE_JUDGE_CMD", ""),
                    help="judge model command; must differ from the answerer for --score")
    ap.add_argument("--reps", type=int, default=1,
                    help="generations per arm per case (scored runs force >= 3)")
    ap.add_argument("--threshold", type=float, default=0.8, help="fraction of rubric to pass")
    ap.add_argument("--model-id", default=os.environ.get("RESONANCE_MODEL_ID", ""),
                    help="stable provider/model identity for the answerer")
    ap.add_argument("--judge-id", default=os.environ.get("RESONANCE_JUDGE_ID", ""),
                    help="stable provider/model identity for the judge")
    ap.add_argument("--holdout-dir", default=os.environ.get("RESONANCE_HOLDOUT_DIR", ""),
                    help="external protected holdout directory used by --score")
    args = ap.parse_args(argv)

    target = "--all" if (args.all or args.changed or not args.path) else args.path
    cases = find_cases(target, args.changed)
    if args.limit:
        seen: dict[str, int] = defaultdict(int)
        capped = []
        for sk, ev in cases:
            k = skill_rel(sk)
            if seen[k] < args.limit:
                seen[k] += 1
                capped.append((sk, ev))
        cases = capped
    if not cases:
        print(f"no evals found for '{target}'" + (" (changed selection)" if args.changed else ""))
        return 2

    model_cmd = args.model_cmd or ("claude -p" if _has("claude") else "")
    live = bool(model_cmd) and not args.check

    if not live:
        print(f"eval CHECK (structure only): {len(cases)} cases\n")
        bad = 0
        for sk, ev in cases:
            probs = check_case(sk, ev)
            if probs:
                bad += 1
                print(f"  FAIL  {ev.relative_to(REPO).as_posix()}")
                for p in probs:
                    print(f"        {p}")
        print(f"\n{len(cases)} cases | {bad} structural problem(s)")
        if not args.check and not model_cmd:
            print("(no model command found; ran structure check only. Set --model-cmd or "
                  "RESONANCE_MODEL_CMD, e.g. 'claude -p', for a live scored run.)")
        return 1 if bad else 0

    judge_cmd_s = args.judge_cmd.strip()
    reps = max(1, args.reps)
    if args.score:
        try:
            cases = holdout_cases(args.holdout_dir)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"refusing --score: {exc}")
            return 2
        if not judge_cmd_s:
            print("refusing --score: no judge configured. The judge is never the answerer; "
                  "set RESONANCE_JUDGE_CMD (or --judge-cmd) to a DIFFERENT model.")
            return 2
        if not args.model_id or not args.judge_id or args.model_id == args.judge_id:
            print("refusing --score: set distinct RESONANCE_MODEL_ID and RESONANCE_JUDGE_ID. "
                  "Command inequality does not prove independent model identity.")
            return 2
        if same_command(judge_cmd_s, model_cmd):
            print("refusing --score: judge command equals the answerer command")
            return 2
        if reps < 3:
            print(f"scored run: raising --reps {reps} -> 3 (a single generation per arm "
                  f"cannot carry a verdict).")
            reps = 3

    cmd = shlex.split(model_cmd)
    jcmd = shlex.split(judge_cmd_s) if judge_cmd_s else cmd
    print(f"eval LIVE run via `{model_cmd}` (judge: `{judge_cmd_s or model_cmd}`): "
          f"{len(cases)} cases, reps={reps}, parallel={args.parallel}\n")
    manifest_problems = eval_integrity.verify()
    if manifest_problems:
        print("eval aborted: committed eval oracle verification failed")
        for problem in manifest_problems:
            print(f"  ERROR {problem}")
        return 1
    oracle = eval_integrity.snapshot()
    holdout_before = file_hashes([ev for _, ev in cases]) if args.score else {}
    try:
        with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
            results = list(pool.map(
                lambda ce: run_case(cmd, jcmd, ce[0], ce[1], args.threshold, reps=reps), cases))
    except ModelFailure as exc:
        print(f"eval aborted: {exc}")
        print(f"stdout: {exc.stdout[:1000]}")
        print(f"stderr: {exc.stderr[:1000]}")
        return 1
    mutations = eval_integrity.verify(oracle)
    if args.score and holdout_before != file_hashes([ev for _, ev in cases]):
        mutations.append("protected holdout changed during execution")
    if mutations:
        print("eval aborted: the eval oracle changed during execution")
        for mutation in mutations:
            print(f"  ERROR {mutation}")
        return 1

    if args.score:
        md, data = write_scorecard(results, args.threshold, judge_label=judge_cmd_s, reps=reps)
        evidence_dir = FORGE / "eval_evidence"
        evidence_dir.mkdir(exist_ok=True)
        evidence = {"model_id": args.model_id, "judge_id": args.judge_id,
                    "judge_command": judge_cmd_s, "reps": reps, "results": results}
        (evidence_dir / "latest.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        (FORGE / "eval_results.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        s = data["summary"]
        print(f"scorecard: {s['measured']} skills measured, {s['proven']} proven, "
              f"{s['weak']} weak, {s['dead']} dead case(s)")
        out = private_eval_dir()
        if out:
            out.mkdir(parents=True, exist_ok=True)
            (out / "EVAL_SCORECARD.md").write_text(md, encoding="utf-8")
            base = load_baseline(out)
            skills_base = base.setdefault("skills", {})
            import datetime as _dt
            today = _dt.date.today().isoformat()
            for r in data["skills"]:
                skills_base[r["path"]] = {"lift": r["lift"], "with": r["with"],
                                          "without": r["without"], "cases": r["cases"],
                                          "reps": reps, "judge": judge_cmd_s, "date": today,
                                          "evals_hash": evals_dir_hash(r["path"])}
            save_baseline(out, base)
            print(f"wrote {out / 'EVAL_SCORECARD.md'} and updated {out / 'eval_baseline.json'} "
                  f"(results stay private) plus .forge/eval_results.json scratch")
        else:
            print("wrote .forge/eval_results.json (local scratch). No private results directory "
                  "is configured, and results never land in the repo; see docs/EVALS.md.")
        return 1 if s["weak"] else 0

    failed = 0
    for r in results:
        failed += 0 if r["pass"] else 1
        tag = "PASS" if r["pass"] else "FAIL"
        print(f"  {tag}  {r['path']}/{r['eval']}  with={r['with_frac']:.2f} "
              f"without={r['without_frac']:.2f} (reps={r['reps']})")
    print(f"\n{len(results)} cases | {failed} failed")
    return 1 if failed else 0


def _has(exe: str) -> bool:
    from shutil import which
    return which(exe) is not None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
