# Resonance updater profiles

Resonance has two different installation shapes. A source installation contains
the compiler and validation tools. A compiled installation contains generated
skills and host adapters only. Treating both shapes as one installation caused
the old updater to copy `.forge` into compiled consumers and then run validators
that could not exist there.

## Ownership contract

The framework manifest records `profile`, version, and hashes for every path the
updater owns.

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

## Validation and transaction

Compiled targets are validated from the pinned source checkout. The source
checkout runs its Forge dry run and integrity checks, while the source validator
checks the target's generated skills and any project-skill lock. This keeps
meaningful verification without installing source tooling into the project.
Source targets use the verifier in their own `.forge` tree. Neither profile
regenerates a project-owned lock during an update.

Both profiles use the same staged backup, hash comparison, atomic replacement,
manifest write, and rollback journal. Profile migration is unsupported. Once a
manifest records a profile, every requested profile must match it. Run an
explicit dry run first:

```text
python .forge/update.py --source <pinned-resonance-checkout> --target <project> --profile compiled
```

The first pilot should cover one real compiled consumer and one real source
installation before any fleet update. Never replace an existing release tag.

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
the reviewed preview. It copies released files from the pinned checkout and
never imports or executes Python fetched during the notice request.
