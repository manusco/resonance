# Automatic design proposal population integration report

**Status:** DONE. Source generation, structural checks, repository tests, and six isolated behavior cases passed.

## Objective

Normal UI work in a new or existing app should automatically produce a useful, source-backed `PROPOSED` design artifact when the app has no filled design entry point or the task adds a shared pattern. The user does not need to invoke `/design`. Existing pointers and approved content remain authoritative, repeated preparation is stable, and read-only work does not write.

## Implementation ownership

Designer owns `project:design-contract` writes and file side effects. Core, Plan, and Build route relevant work to Designer and declare `design_scope`; Plan and Build read the contract but do not claim its writes. Frontend and Mobile provide the normal workflow trigger. A broken pointer or unresolved conflicting source does not trigger a competing replacement. The Designer output requirement calls for a saved, populated proposal when a trigger applies.

The source templates, contract reference, generated skills, eval fixtures, and routing evals are in the assembled change. The public `.resonance/05_design.md` remains template-clean.

## Behavioral evidence

A fresh agent executed six natural-language tasks in isolated app fixtures under `/tmp/resonance-auto-design-smoke`, following the generated workflow instructions. I independently inspected the resulting files and fixture hashes.

1. **Greenfield brief:** created a bounded `PROPOSED` dashboard baseline and implementation plan from the brief. It contains concrete choices, rationale, and assumptions; it makes no unsupported implementation-file claims.
2. **Existing app:** read Customers and Invoices sources and created a proposed shared status summary plus a scoped plan. It cites existing files and leaves unsupported query semantics open.
3. **Resume:** filled blank sections in an existing `PROPOSED` entry. A second preparation produced no edits; SHA-256 stayed `b6809399304e1f9c54c8067c8c1503fdd998957cba2ae01a0d27fb00e8f7ccd4`.
4. **Canonical pointer:** followed the declared pointer and wrote a task-scoped note. The pointer and canonical source retained their baseline hashes (`b4826f2ec3adebb0e21d86aa0a4590699a4b87694fe00e53ff4cf37bffad8364` and `287cf1fca23156338c309f7446ee184de714685bcf7a8035f48c1a1b77a12b1f`).
5. **Read-only new app:** created no design file; the brief hash and file listing remained unchanged.
6. **Approved shared pattern:** appended a `PROPOSED` batch section while preserving the existing approved content byte-for-byte (approved prefix hash `2355c4cb7ec6409695391b2b5fa04bf71dd28dbdde8ceff352f4c15786a03d83`) and retaining `APPROVED` status. The obsolete empty “No proposed changes” block was removed.

The behavior report is at `/tmp/resonance-auto-design-behavior.md`; fixture inputs, outputs, and baseline hashes are under `/tmp/resonance-auto-design-smoke/` and `/tmp/resonance-auto-design-baseline.json`. No repository files were written by the behavior run.

## Verification

- `python3 .forge/forge.py build --all` completed successfully.
- `python3 .forge/kernel/manifest.py` generated the skill manifest; `python3 .forge/job_composition.py` generated job compositions; `python3 .forge/eval_integrity.py --update` refreshed the fixture oracle after intentional eval/fixture changes; `python3 .forge/skill_graph.py` refreshed the generated skill graph after the full-suite freshness test identified it as stale.
- `python3 .forge/forge.py build --all --dry-run`: passed, generated skills fresh.
- `python3 .forge/validate_library.py`: passed, 73 skills, 0 errors, 0 warnings.
- `python3 .forge/eval_integrity.py`: passed, 657 oracle files, 0 issues.
- `python3 .forge/run_evals.py --all --check`: passed, 494 cases, 0 structural problems. The assembled change adds 9 cases: 7 Designer, 1 Core, and 1 Frontend.
- `python3 .forge/tests/run.py`: passed, 353 tests, 1 skipped. The first run found only the stale generated skill graph; after regeneration, the rerun passed.
- `git diff --check`: passed.

## Limits

These checks prove source freshness, structural eval validity, repository tests, and actual proposal-file behavior in bounded fixtures. They do not run an app implementation, browser rendering, accessibility audit, or visual regression check. The smoke fixtures are intentionally small; unresolved product or data semantics remain open questions rather than fabricated decisions.
