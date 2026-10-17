# Resonance updater profiles

Resonance has two different installation shapes. A source installation contains
the compiler and validation tools. A compiled installation contains generated
skills and host adapters only. Treating both shapes as one installation caused
the old updater to copy `.forge` into compiled consumers and then run validators
that could not exist there.

## Ownership contract

The framework manifest records `profile`, version, source revision, and hashes
for every path the updater owns. Older manifests remain readable.

- `source` owns the framework compiler, `.forge`, generated skills, host
  adapters, bridges, and launchers.
- `compiled` owns generated skills, host adapters, and launchers. It does not
  own `.forge`, project `AGENTS.md`, project `CLAUDE.md`, or project memory.

The updater preserves an absent profile as unknown. It fails closed when a
legacy target looks compiled but has no profile, while a legacy source target
can continue in source mode when its `.forge` tree is present. A legacy target
without a profile can be upgraded only after the operator explicitly chooses a
profile.
Adoption accepts only byte-identical released files and requires an explicit
profile for a target without `.forge`. A modified or unowned file remains a
conflict. The updater never regenerates a private project-skill lock to make an
upgrade pass.

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

For a source-profile consumer, use `python3 .forge/consumer_check.py --root .`.
It verifies owned hashes, generated output, skills, eval integrity, project-skill
locks, and available launcher parsers without comparing project-owned docs to
the Resonance repository scaffold. `.forge/tests/run.py` is source-repository
test infrastructure and refuses to run in an installed consumer.

## Validation and transaction

Compiled targets are validated from the pinned source checkout. The source
checkout runs its Forge dry run and integrity checks, while the source validator
checks the target's generated skills and any project-skill lock. This keeps
meaningful verification without installing source tooling into the project.
Source targets use the verifier in their own `.forge` tree. Neither profile
regenerates a project-owned lock during an update.

Both profiles use the same staged apply and per-path recovery journal. A live
file can be reconciled when it matches the selected source, its recorded
ownership hash, or the verified installed release commit or exact local version
tag available in the pinned source checkout's local history. The updater does
not fetch tags or history. The consumer's Git status never proves framework
ownership. Profile migration is unsupported. Once a manifest records a
profile, every requested profile must match it. Run an explicit summary
preview first, or use `--json` for the complete machine-readable plan.

Before changing managed files, apply pins target `HEAD` and records each
preimage in `.resonance/updates/<id>/journal.json`. It uses a Git blob only when
the path is an ordinary tracked file and its raw bytes and executable mode
match `HEAD`; it copies only preimages that Git cannot recover. A Git-only
transaction creates no `.resonance/backups/` directory. Older
`.resonance/backups/.../journal.json` transactions remain supported by rollback
and doctor.

Before creating the receipt or staging files, apply probes reversible file
creation and deletion in each existing managed destination directory. This catches denied `.agents`,
`.forge`, adapter, launcher, or ownership-manifest directories before the
transaction begins. A source-profile or compiled consumer can preview with:

```text
python resonance_update.py --source <pinned-resonance-checkout> --target <project> --profile compiled --summary
```

If apply or validation fails, the updater attempts rollback before returning.
If rollback also fails, the error reports both causes and the exact recovery
journal path. Profile migration is unsupported. The first pilot should cover a
synthetic compiled consumer and a synthetic source installation. Never replace
an existing release tag.

## Optional release notices

Release notices are disabled by default. Enable them per installation with
`python3 resonance_update.py notice enable`. The setting and its small cache
live in the operating system's user configuration directory, outside every
project. The notice request has a three-second timeout, a 64 KiB response cap,
rejects redirects, drafts, and prereleases, and never sends project paths or
project data. Launchers only run the quiet check when enabled. A failed check
does not block startup, and no notice command can apply an update.

The installed `resonance_update.py` runtime performs preview and apply for both
profiles. `.forge/update.py` is a compatibility entrypoint for source installs.
Apply requires the exact version, full source commit, and plan digest printed by
the reviewed preview. It stages released files from the pinned checkout and
never imports or executes Python fetched during the notice request.
