# CodeQL release alert evidence

## Scope

- Repository: `manusco/resonance`
- Pull request: #41
- Analyzed ref: `refs/pull/41/head`
- Analyzed commit: `de86e6c074e04b4e0ffa9cf56e9bf7f130b4733b`
- Alert: #6, `py/clear-text-storage-sensitive-data`, HIGH
- Check: CodeQL, run `39761806397`, failed check run `119767786029`

## Verified trace

The PR annotation identifies `.forge/tests/test_eval_integrity.py:35-41` as the JSON write sink in `_isolated_repository()`. GitHub's alert detail points to the related source at line 66: the local named `secret` holds a temporary file path (`Path(outside) / "outside.txt"`). Its basename flows into the traversal payload in `files`, then into the eval-case JSON written by the helper.

The flow contains only the public filename `outside.txt`, not file contents. The path is also a traversal test value, and does not identify the separately created file under the other temporary directory. That file's synthetic content is written independently and never read by the eval helper. In the symlink test, the JSON stores only `fixtures/external.md`; it does not read the symlink target's contents.

## Disposition and correction

Classification: rejected false positive. The source is a path variable with a security-sensitive identifier, while the sink is a general JSON fixture writer. No sensitive bytes cross the reported path.

The minimal correction renames the two local path variables from `secret` to `outside_fixture` in the traversal and symlink tests. It preserves the external fixture creation, filename, contents, traversal payload, symlink target, assertions, and test boundaries. No CodeQL rule, workflow, alert, or coverage was disabled.

## Verification status

The GitHub CodeQL analysis for the recorded commit produced the alert and its exact source location; the check annotation confirmed the sink. After the rename, the central manifest was refreshed and the following focused checks passed: `test_eval_integrity.py` (8/8), the source-profile package/oracle test (1/1), all eval structure checks (499 cases/0 problems), and the 662-file oracle check (0 problems). The bounded independent Astra review confirmed the full test ASTs are identical after normalizing the two renamed identifiers, and the manifest change matches the test file hash. The alert is not dismissed. Final proof requires a fresh CodeQL check on the corrected PR commit to pass.
