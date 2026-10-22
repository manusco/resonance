# Resonance installation and updater

A normal Resonance installation contains the complete framework, including
`.forge`, generated skills, host adapters, bridges, and launchers. It records
the `source` profile. The old `source` and `compiled` profile arguments remain
accepted as compatibility aliases for this complete installation.

## Ownership contract

The framework manifest records the complete `source` profile, version, source
revision, and hashes for every path the updater owns. Manifests with either old
profile remain readable. Their recorded profile is used only to prove which
paths belonged to the installed release. Newly included paths are treated as
additions: absent paths can be installed, matching bytes are adopted, and
unknown existing bytes are preserved as conflicts. Missing-profile legacy
manifests are reconciled from recorded hashes or a verified installed release
revision or exact version tag. The updater never guesses ownership from a clean
worktree and never regenerates a private project-skill lock to make an upgrade
pass.

For an installation without a manifest, use the new updater with a verified
checkout of the installed release and `--adopt`. Adoption records ownership
without rewriting framework files and accepts only byte-identical released
files. A modified or unowned file remains a conflict.

Framework validation never reads project-owned generated documentation as
runtime authority. Command targets and skill metadata come from the
framework-owned templates installed with `.forge`. A consumer may keep an older
`docs/skill-manifest.json`; the updater neither changes it nor uses it to decide
whether the framework is valid. Required validation invokes Forge in explicit
consumer mode. In that mode Forge never reads or writes root project
documentation. Existing unowned `README.md`, `AGENTS.md`, `CLAUDE.md`, and host
bridges are preserved byte-for-byte, excluded from framework ownership, and
reported as non-blocking integration notes. Framework-repository builds remain
strict about Resonance's own generated documents.

Use `python3 .forge/consumer_check.py --root .`. It verifies owned hashes,
generated output, skills, eval integrity, project-skill locks, and available
launcher parsers without comparing project-owned docs to the Resonance
repository scaffold. `.forge/tests/run.py` is source-repository test
infrastructure and refuses to run in an installed consumer.

## Validation and transaction

During apply, the installed Forge runs in consumer dry-run mode, strict skill
validation, eval integrity, and project-skill lock verification when a lock is
present. Afterward, run `python3 .forge/consumer_check.py --root .` for the
broader ownership and generated-output check. These checks never regenerate a
project-owned lock.

Updates use staged apply and a per-path recovery journal. A live
file can be reconciled when it matches the selected source, its recorded
ownership hash, or the verified installed release commit or exact local version
tag available in the pinned source checkout's local history. The updater does
not fetch tags or history. The consumer's Git status never proves framework
ownership. Run an explicit summary preview first, or use `--json` for the
complete machine-readable plan.

Before changing managed files, apply pins target `HEAD` and records each
preimage in `.resonance/updates/<id>/journal.json`. It uses a Git blob only when
the path is an ordinary tracked file and its raw bytes and executable mode
match `HEAD`; it copies only preimages that Git cannot recover. A Git-only
transaction creates no `.resonance/backups/` directory. Older
`.resonance/backups/.../journal.json` transactions remain supported by rollback
and doctor.

Before creating the receipt or staging files, apply probes reversible file
creation and deletion in each existing managed destination directory. This
catches denied `.agents`, `.forge`, adapter, launcher, or ownership-manifest
directories before the transaction begins. Preview with:

```text
python3 resonance_update.py --source <pinned-resonance-checkout> --target <project> --summary
```

If apply or validation fails, the updater attempts rollback before returning.
If rollback also fails, the error reports both causes and the exact recovery
journal path. Legacy profile values remain historical provenance only. Never
replace an existing release tag.

## Optional release notices

Release notices are disabled by default. Enable them per installation with
`python3 resonance_update.py notice enable`. The setting and its small cache
live in the operating system's user configuration directory, outside every
project. The notice request has a three-second timeout, a 64 KiB response cap,
rejects redirects, drafts, and prereleases, and never sends project paths or
project data. Launchers only run the quiet check when enabled. A failed check
does not block startup, and no notice command can apply an update.

The installed `resonance_update.py` runtime performs preview and apply.
`.forge/update.py` remains a compatibility entrypoint.
Apply requires the exact version, full source commit, and plan digest printed by
the reviewed preview. It stages released files from the pinned checkout and
never imports or executes Python fetched during the notice request.
