# Updater ownership recovery plan

**Status:** implemented, verified, and passed independent review.

## Assumptions and success criteria

The report describes a compiled consumer upgraded from Resonance 2.5.40 to 2.5.43. Its framework files are tracked and clean in Git, but the ownership manifest hashes are stale. Treat that report as unverified; do not infer consumer ownership from a clean Git tree.

Success means the updater distinguishes three cases in preview and apply:

1. A live file already byte-matches the explicitly selected, pinned incoming source. It is safe to reconcile its ownership hash as metadata without rewriting that file.
2. A live file differs from incoming, but byte-matches the corresponding file in the verified installed release. It is safe to treat it as an unchanged managed file and update or remove it according to the incoming release.
3. A live file matches neither trusted source. Keep it as a conflict and explain what evidence is missing. A clean target Git status must never clear it.

The plan must produce a concrete preview with per-path reasons, retain the existing reviewed source revision and plan digest binding, avoid writes during preview, and preserve rollback for actual writes.

## Confirmed defect and evidence

`resonance_update.py:349-355` checks the prior ownership hash before comparing the live path to incoming bytes. A stale prior hash therefore conflicts even when `digest(target_path) == digest(incoming_path)`. The no-op reproduction and test evidence are in `/private/tmp/resonance-updater-incident/report.md` and `repro.py`.

The local source history contains tag `v2.5.40` at commit `295a6101f3d21e2e47aa5e103af93a73b034b79d`, and `git merge-base v2.5.40 HEAD` equals that commit. Thus the tag is an ancestor of current HEAD in this checkout. For the compiled profile, the v2.5.40 and current trees contain 867 and 890 managed paths; 119 shared paths have changed blobs, 23 paths were added, and none were removed. That is 142 changed or added paths. This establishes that the local source can support a synthetic 2.5.40-to-2.5.43 test. It does not establish the adopter's manifest contents or exact failure.

## Baseline trust and manifest evolution

Use only an explicitly selected, clean, pinned source checkout. Do not fetch tags or refs automatically. A historical baseline is eligible only when all of these checks pass:

- The manifest records `profile` and either a full `source_revision` (new manifests) or an installed `version` that maps to the exact local `v<version>` tag (legacy manifest).
- The baseline revision/tag resolves locally to a commit in the selected source checkout's history. For a tag fallback, read `package.json` at that commit and require its version to equal the manifest version.
- Read baseline file bytes from Git objects at that commit, scoped to the manifest's installation profile. Do not execute or checkout old source code.
- Compare each target path's raw bytes to that exact baseline blob. Git index equality, clean status, ignored-file status, and current HEAD are not ownership evidence.

Add `source_revision` to ownership manifests written by future successful `apply()` and by explicit adoption where the exact selected source revision is known. Preserve old manifest compatibility. The sentinel version `adopted` has no historical release baseline; do not guess one. For it, only current-source byte matches can be reconciled automatically. Other paths remain conflicts with a specific instruction to identify the original release source or review the path manually.

Never rewrite manifest ownership hashes by merely hashing current target contents. Only derive replacement hashes from verified incoming bytes or a matching verified historical release blob.

## Recovery storage and transaction receipt

Separate ownership proof from rollback proof. For each touched target path, use the target repository's current `HEAD` only to prove recoverability: the path must be tracked at `HEAD` and its working bytes must exactly equal the `HEAD` blob. Do not use that match to claim framework ownership. Pin `HEAD` under a transaction ref such as `refs/resonance/updates/<id>` before applying writes, then record each path's old blob id and recovery source in `.resonance/updates/<id>/journal.json`. The receipt is metadata, not a copied backup tree.

Only paths whose prior bytes cannot be recovered from the pinned target Git commit need fallback content copies. Keep those copies scoped to the transaction and list them in the receipt. A clean status is not enough: ignored and untracked files are outside Git, and staged or unstaged changes do not match `HEAD`. Preserve those bytes through fallback storage or stop with a path-specific conflict when ownership cannot be proven. Do not create `.resonance/backups/` for a Git-only transaction; retain legacy backup-journal recovery support for existing transactions.

For a manifest-only reconciliation, no framework content paths change. The existing manifest still needs rollback evidence: use its pinned Git blob if it is tracked and matches `HEAD`, otherwise preserve that single old manifest as fallback transaction data. The apply receipt must distinguish manifest-only from content-changing runs. A crash or failed validation must be recoverable from the receipt plus any listed fallback files.

## Minimal implementation sequence

1. Extract a read-only baseline resolver that validates manifest profile/version/revision against the explicitly selected local source history and returns Git blob hashes for profile-managed paths. Missing or ambiguous provenance returns a structured unavailable reason, not a guessed tag.
2. In `plan()`, classify paths in this order: exact incoming-byte match; exact verified-baseline-byte match; unresolved mismatch. Produce reason codes and evidence (source revision, baseline revision, path) in the plan digest.
3. For incoming-byte matches, include the incoming hash in the next manifest while excluding the path from `writes`. For verified-baseline matches, permit a normal incoming write or removal. For mismatches, preserve the conflict and include a human-readable reason. A missing target path that the manifest or baseline says existed remains a conflict until deletion semantics are explicitly proven; do not silently restore it.
4. Keep reconciliation in-memory during preview. Apply must re-run and bind to the same source revision and digest as today. Before any write, pin target `HEAD`, create the `.resonance/updates/<id>/journal.json` receipt, and copy only prior bytes that the receipt proves are not recoverable from that Git commit. Apply writes staged framework files and the manifest, validates, and marks the receipt complete. Rollback uses the pinned commit for Git-covered files and fallback copies for the rest.
5. Report whether apply is content-changing, manifest-only, or blocked. Git-only/no-op transactions use the receipt and do not create a backup directory; fallback storage is limited to unrecoverable bytes. Preserve compatibility with legacy `.resonance/backups/.../journal.json` transactions.

## Regression matrix

- Stale prior hash, live bytes equal incoming: preview has no content write and no conflict; apply updates only manifest ownership, uses the Git receipt for prior manifest bytes when recoverable, and creates no backup directory for a Git-only transaction.
- Stale prior hash, live bytes equal verified old-release blob, incoming differs: preview classifies owned-old and schedules the incoming write.
- Stale prior hash, path removed from incoming but live bytes equal verified old-release blob: preview permits the managed removal.
- Live bytes differ from incoming and verified old release: conflict, regardless of target Git clean/dirty state.
- Legacy `version: adopted`, live bytes differ from incoming: conflict with missing-provenance explanation.
- Tag absent, tag version mismatch, unrelated revision, wrong profile, or path absent from baseline: do not claim ownership; conflict.
- Missing target path: do not infer ownership from Git state or restore it automatically where stale provenance prevents confirming prior bytes.
- Changed source commit or changed plan after preview: apply rejects via existing revision/digest guard.
- Git-tracked path equal to target HEAD: receipt pins its blob and commit; no copied backup for that path.
- Staged, modified, untracked, or ignored path: target HEAD cannot recover its live bytes; use scoped fallback storage or block before writes.
- Preserve unowned private skills and unrelated project files; compiled mode continues to omit `.forge`.

## Out of scope

This plan does not access adopter repositories or deployment infrastructure, infer ownership from Git cleanliness, fetch releases, alter the compiled/source profile boundary, or change project-skill locks. Runtime changes and persistent regression tests implement the approved scope; final verification results are recorded in the companion report.
