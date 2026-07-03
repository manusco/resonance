# The Hooks Layer (opt-in, deterministic enforcement)

> Resonance's Prime Directive is to push complexity into Layer 3 (deterministic code), not to hope the model remembers a rule. The hooks layer enforces the rules that should never be optional: no em or en dashes, no edits to the Soul, no committed secrets, a clean library, and no shipping a broken release. It is opt-in, so it never surprises you.

## What the guard blocks

`guard.py` blocks a commit when a staged text file:
- contains an **em or en dash** (the house rule bans them everywhere; use a hyphen, comma, or period),
- **edits `.resonance/00_soul.md`**, the immutable Soul (override a deliberate change with `RESONANCE_ALLOW_SOUL=1`),
- contains an **obvious secret** (private key, API key, token).

And when skills change, the pre-commit hook also runs `validate_library.py`, so orphan references, diverged duplicates, eval name-drift, and leaks cannot land.

## The ship-gate (pre-push)

`pre-push` blocks a release-shaped push (a tag, or an update to `main`) when the release gate is not green: the skill validator, the library validator, the eval structure check, and doc-drift all have to pass first. This is the deterministic form of "do not ship without a passing test." Bypass once with `git push --no-verify`. For a non-Resonance project, swap the four checks in `pre-push` for that project's own test and build command.

## Slop vocabulary (copy mode, opt-in)

The dash, Soul, and secret checks are always on because they are safe everywhere. The banned-vocabulary scan is not, because "robust" or "leverage" are legitimate in technical writing. Run it on generated copy on demand:

```
py .forge/hooks/guard.py --copy path/to/copy.md
```

Or set `RESONANCE_STRICT_VOCAB=1` to fold it into the pre-commit and the edit-time hook. Framework internals and the files that teach the rules are exempt, so the scan never fights itself.

## Enable it (git hooks, cross-tool)

```
py .forge/hooks/install.py
```

This copies the guards into `.git/hooks/pre-commit` and `.git/hooks/pre-push`. They run on every `git commit` and `git push`, in any tool. Bypass once with `--no-verify`. Disable by deleting the files in `.git/hooks`. Git hooks are the cross-tool choice: they work whether you drive the repo from Claude Code, Cursor, Codex, or the terminal.

## Enable it in Claude Code (editor-level, optional)

A ready config ships in `.claude/hooks/`. Enable the edit-time guard with:

```
py .forge/hooks/install.py --claude
```

This adds a PostToolUse hook that runs the guard after each Write or Edit and hands any violation back to the model to fix. See `.claude/hooks/README.md` for details. It lives in your personal `.claude/settings.local.json`, so it stays your choice.

## Why opt-in

Enforcement that fires without consent is a good way to get disabled in anger. The rules are strict on purpose, so you turn them on when you want them. Once on, they are deterministic: the same input always blocks or passes, with no model judgment involved.
