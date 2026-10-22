# Independent eval review and reconciliation

Date: 2026-10-21. Reviewer: Astra, independent of the Luna authors. Baseline: `5a5fcc4e10b1dbc43d42e1924421b62af07d65d6`. Artifact: the working tree and untracked additions on `codex/eval-coverage-six`.

Status: **DONE** for the bounded independent review. All nine accepted findings are resolved, including the P1 source-profile packaging blocker. Final independent checks passed against the refreshed manifest. No remaining blocker was found within this review scope.

## Scope and limits

The initial review covered all 73 suite inventories, all 96 new canonical cases, the validator and policy changes, all three author coverage reports, and targeted existing cases checked against their owning skills. It was not a second exhaustive semantic reread of all 461 cases. Follow-up review covered the actual repairs, their fixtures, the extracted containment helper, oracle dependency protection, source-profile packaging, and three legacy cases converted to hermetic inputs. A1 through A7 and A9 are P2; A8 is P1.

I independently confirmed 461 canonical cases across 73 skills, a minimum of six, and matching generated copies. Distribution: 59 suites with six, eight with seven, four with eight, one with nine, and one with ten.

No live model trials, paid evaluations, judge calibration, or comparative skill-lift measurement were run. The full global suite results belong to the coordinator's evidence, not an independent rerun here. Passing fixture and integrity checks do not establish behavioral lift or production performance.

## Findings and final dispositions

| ID | Origin | Original finding and evidence | Reconciliation |
|---|---|---|---|
| A1 | Second-only | `.forge/validate_skill.py` did not catch invalid UTF-8 while reading a consumer ownership manifest. A manifest containing byte `0xff` raised `UnicodeDecodeError`. | Resolved. `eval_floor` catches `UnicodeError`; the added regression verifies an ownership error and the six-case floor. I reran the original counterexample successfully. |
| A2 | Second-only | `ops/explain/05_reader_unknown` required real payment-retry names with no source fixture. `ops/update-roadmap/01_case` required exactly three completed tasks without supplying their state or implementations. | Resolved. All six Explain cases now attach source, diff, or test evidence. Roadmap attaches a state snapshot, ten-commit log, and implementation excerpts; its query requires proposed text and forbids unsupported execution or save claims. I verified every attachment exists and enters `build_prompt`. |
| A3 | Second-only | New Operations lexical checks rejected correct equivalent wording. A valid page-audit refusal scored zero because it omitted the exact strings `cannot verify` and `evidence`. | Resolved. The 35 new Operations cases were rechecked. Remaining deterministic checks cover the audit verdict format and defined system-health flags. The audit case now supplies the actual brief and copy; the health case supplies a concrete outdated assertion, rather than inferring staleness from age. The page-audit lexical restriction is gone. |
| A4 | Second-only | `ops/librarian/06_canonical_reference` required reading a typed ledger although its query only named `decisions.md`. | Resolved. The case explicitly supplies a canonical decision record and a conflicting runbook, names the active decision ID, and grades the actual provider facts. Both artifacts enter the prompt. |
| A5 | Second-only | `marketing/copywriter/02_humanization` required naming banned phrases in a diagnosis while banning those phrases from the entire output. A compliant diagnosis failed the global check. | Resolved. The task now requests only the rewritten paragraph. A clean rewrite passes the deterministic checks; adding `robust` fails. The unsupported-claim guard remains. |
| A6 | Second-only, repair follow-up | The first Roadmap evidence repair treated webhook idempotency as complete, but `.forge/fixtures/update-roadmap/src_webhooks.ts` records an event before applying payment. I executed the fixture with a failing payment call: redelivery returned `{duplicate: true}`, with only one payment attempt and a persisted receipt. | Resolved by preserving the faulty source as a negative control. The rubric now leaves webhook idempotency open for this failure window and the unproven atomic check/record boundary. It marks only the two evidence-supported tasks complete and keeps webhook idempotency and the proposed dashboard open. |
| A7 | Primary finding, independent agreement | `eval_integrity.oracle_files()` excluded the files referenced by case `files[]`. Those evidence files could change without the before/after oracle check noticing; a per-run prompt hash did not enforce immutability. | Resolved. Oracle snapshots include deduplicated contained fixture dependencies. The runner reuses the same containment rules. Required missing inputs fail closed; explicit optional missing inputs remain allowed. Mutation, deletion, traversal, and symlink escape checks pass. |
| A8 | Primary finding, independent agreement | Source-profile updates copy `.forge` but exclude root `fixtures/`. Their post-update checks execute the target's integrity tool, which now requires those excluded evidence files and therefore fails the update. Severity: P1. | Resolved. All public evidence is stored under `.forge/fixtures/`, and only this precise namespace is added to the shared containment rule. The updater regression creates a clean source checkout, verifies that required public dependencies are selected by `source_files(profile="source")`, copies the package into a target, and runs the target oracle successfully. |
| A9 | Primary finding, independent agreement | A path under `.forge/fixtures/` could be a symlink to `.forge/private-config.md`. The general same-repository check accepted it even though the new namespace is intended to expose only public framework evidence. | Resolved. The resolver rejects symlinked `.forge` or fixture roots and requires resolved fixture files to remain physically beneath the repository-anchored `.forge/fixtures` directory. Regression verifies the private-sibling alias is rejected; the sibling is an in-repository plaintext fixture, so the check does not access external user data. |

## Independently executed evidence

- Invalid-UTF-8 ownership-manifest counterexample: reports the ownership error and returns floor six without raising.
- Copywriter positive and negative controls: a clean rewrite passes; the same rewrite with the banned word fails.
- Audit verdict positive and negative controls: `APPROVE` passes; an equivalent phrase lacking the required verdict token fails as intended by the output contract.
- `build_prompt` attachment checks: all six Explain cases, Roadmap case 01, and Librarian case 06 include every referenced fixture's content.
- Webhook false-completion reproduction: first payment application fails; redelivery is incorrectly classified as a duplicate. This now supplies the expected negative evidence for the Roadmap case.
- `python3 -m unittest discover -s .forge/tests -p test_eval_integrity.py`: eight tests passed, including mutation/deletion detection, traversal, external symlink escape, and an in-repository private-sibling symlink.
- Source-profile packaging regression `UpdateTests.test_source_profile_packages_required_eval_fixtures_and_oracle`: passed independently against the final refreshed manifest, with every required eval dependency selected and the installed target oracle reporting zero problems. An earlier run caught four stale Explain hashes before the manifest refresh; the final rerun passed.
- Public dependency inventory: 23 unique required `.forge/fixtures` inputs, all present, with no optional consumer application paths in canonical cases.
- Physical namespace controls: sibling escape rejected; an alias to another public file within the fixture subtree accepted.
- Oracle verification: 596 files, zero problems. Every existing canonical `files[]` dependency is included in the snapshot.
- Canonical/generated comparison: all 461 eval copies match after the repairs.

The review establishes repaired fixture contracts and integrity checks. Model behavior, discriminative lift, and judge reliability remain unmeasured.
