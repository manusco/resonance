# Eval coverage review, 2026-10-21

The framework eval set now has 461 fixtures across 73 skills, up from 365 fixtures at `5a5fcc4e10b1dbc43d42e1924421b62af07d65d6`. Every skill has at least six cases. No live model scoring or paid API run was performed, so this is a coverage and fixture-quality review, not a measured skill-lift claim.

The validator enforces six cases for framework-owned skills. Installed project-owned skills retain the legacy three-case floor when a valid ownership manifest shows they are unowned; malformed manifests fail closed. Private skills were not rewritten to meet the framework floor.

Domain reviews: [Operations](operations-review.md) with [machine-readable inventory](operations-review.json), [Technical](../2026-10-21-technical-coverage.md), and [Business](../2026-10-21-business-coverage.md).

## Independent-review follow-up

Primary and independent reviews identified nine concrete findings. All repairs are implemented, and the final Astra review is complete: [independent review](astra-review.md).

1. **Invalid UTF-8 manifest crash.** Manifest decoding errors now include `UnicodeError`; a regression test verifies malformed bytes produce an ownership error and retain the six-case framework floor.
2. **Missing repository evidence.** Explain cases 01-06 and update-roadmap case 01 now supply the concrete code, diff, test, state, and history fixtures their rubrics require.
3. **Unearned lexical checks.** Removed deterministic checks that searched for rubric vocabulary instead of enforcing a literal contract. Audit case 05 has supplied brief and old/new copy evidence for its APPROVE/REJECT contract. System-health case 06 supplies the changed payment rule and stale test assertion for both named flags.
4. **Invented ledger prerequisite.** Librarian case 06 now supplies the canonical decision record and conflicting runbook, and grades the supported list and provenance from those files without assuming an unspecified ledger.
5. **Copywriter eval contradiction.** Case 02 now asks for a rewrite only; its rubric does not require diagnosis or a sentence-length constraint. The clean rewrite passes its deterministic checks and a rewrite containing the banned term `robust` fails as intended.
6. **Roadmap fixture contradicted its evidence.** The supplied webhook implementation persists an event before applying it, so failed applies are suppressed on redelivery. The negative-control case now marks only the two evidence-supported tasks complete and keeps webhook idempotency and dashboard work open; the source defect remains intact for the eval to detect.
7. **Fixture evidence was outside the oracle.** The eval oracle now resolves referenced files with the runner's shared containment rules and hashes each existing dependency. Required missing files and unsafe paths fail closed; explicitly optional missing files remain optional. Tests prove that changing or deleting a fixture is detected without changing the case JSON.
8. **Source-profile packaging omitted public evidence.** Public eval evidence now lives under `.forge/fixtures/`, which the source profile already owns. Only that precise framework namespace is allowed by the shared resolver. The updater regression builds a clean temporary source checkout, selects its source-profile files, installs them into a target, and verifies the installed oracle. Public cases use explicit, self-contained fixture files rather than consumer application files.
9. **Framework fixture aliases could cross into a private sibling.** A symlink at `.forge/fixtures/alias.md` targeting `.forge/private-config.md` remained inside the repository and bypassed the general containment check. Framework fixture paths now also have to resolve physically under `.forge/fixtures/`; sibling and root-directory symlinks are rejected. A regression covers the in-repository alias.

## Verification

- Forge build: `python3 .forge/forge.py build --all --host all` passed.
- Full test suite: 349 tests run, 348 passed, 1 skipped.
- Strict skill validation: 73 skills, 0 errors, 0 warnings.
- Strict library validation: 73 skills, 0 errors, 0 warnings.
- Eval structure check: 461 cases, 0 structural problems.
- Orchestration structure check: 23 cases, 0 structural problems.
- Eval fixture integrity: 596 files, 0 problems, including all required referenced evidence files.
- Documentation drift and `git diff --check` passed.
