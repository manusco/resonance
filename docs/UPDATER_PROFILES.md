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
checks the target's generated skills. This keeps meaningful verification without
installing source tooling into the project. Source targets continue to validate
from their own `.forge` tree.

Both profiles use the same staged backup, hash comparison, atomic replacement,
manifest write, and rollback journal. Profile changes are migrations, not an
implicit inference. Run an explicit dry run first:

```text
python .forge/update.py --source <pinned-resonance-checkout> --target <project> --profile compiled
```

The first pilot should cover one real compiled consumer and one real source
installation before any fleet update. The updater must never replace the
existing `v2.5.2` tag; this change belongs in a later deliberate release.
