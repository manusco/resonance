# Updater ownership recovery, 2026-10-17

## Verified synthetic result

A temporary compiled consumer was built from the local v2.5.40 release and committed with 867 stale ownership hashes. The source checkout retained the real release history and tag. Old release commit: `295a6101f3d21e2e47aa5e103af93a73b034b79d`. Selected current source commit: `6cfc45db006b97a75aa9efae9dfda54b0ea0d6a4`.

Before the fix, the committed updater previewed **867 conflicts and 23 writes** for this same clean target and stale manifest. The candidate updater resolved the old release, previewed **0 conflicts and 142 writes**, and left the 867 stale hashes untouched during preview. The 142 writes comprise 119 changed files and 23 additions. Preview took **0.564 s**. Full apply took **1.619 s**, including validation. Its receipt had 143 entries: 120 prior paths recovered from Git, 23 new paths with no prior bytes, and zero copied fallback payloads. All 890 resulting files matched the new manifest. No `.resonance/backups/` directory was created.

A committed customization changed from both old and incoming release bytes remained a conflict even while the target Git tree was clean. It was the only conflict and the plan had zero writes.

The permanent regressions include `.forge/tests/test_update.py::UpdateTests::test_stale_hash_matching_verified_old_release_can_upgrade` and `.forge/tests/test_update.py::UpdateTests::test_committed_customization_is_still_a_conflict`. The updater module passed **38 tests**. Full Forge test discovery ran **337 tests: 336 passed, 1 skipped**. Strict library validation passed for 73 skills with 0 errors and 0 warnings; the updater skill validator passed; eval integrity passed for 474 fixtures; generated-skill and command dry-runs were fresh; and `git diff --check` passed. A synthetic harness and captured output remain under `/private/tmp/resonance-updater-incident/` as supporting evidence.

## Limits

This is a synthetic fixture using local official Git blobs. It matches the reported version pair and stale-hash count, but it does not prove the adopter's actual file contents or explain how their manifest became stale. No adopter repository, website, infrastructure, or deployment system was accessed. The adopter-specific cause remains unknown.

The implementation and review plan are tracked in the current change set. See [the updater reliability plan](../updater-reliability-plan-2026-10-17.md).
