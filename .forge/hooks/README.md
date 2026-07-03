# The Hooks Layer (opt-in, deterministic enforcement)

> Resonance's Prime Directive is to push complexity into Layer 3 (deterministic code), not to hope the model remembers a rule. The hooks layer enforces the rules that should never be optional: no em or en dashes, no edits to the Soul, no committed secrets, and a clean library. It is opt-in, so it never surprises you.

## What the guard blocks

`guard.py` blocks a commit when a staged text file:
- contains an **em or en dash** (the house rule bans them everywhere; use a hyphen, comma, or period),
- **edits `.resonance/00_soul.md`**, the immutable Soul (override a deliberate change with `RESONANCE_ALLOW_SOUL=1`),
- contains an **obvious secret** (private key, API key, token).

And when skills change, the pre-commit hook also runs `validate_library.py`, so orphan references, diverged duplicates, eval name-drift, and leaks cannot land.

## Enable it (git hooks, cross-tool)

```
py .forge/hooks/install.py
```

This copies the guard into `.git/hooks/pre-commit`. It runs on every `git commit`, in any tool. Bypass once with `git commit --no-verify`. Disable by deleting `.git/hooks/pre-commit`. Git hooks are the cross-tool choice: they work whether you drive the repo from Claude Code, Cursor, Codex, or the terminal.

## Enable it in Claude Code (editor-level, optional)

If you also want the check at edit time in Claude Code, add a hook to your Claude Code settings that runs the guard after a Write or Edit. Example shape:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit",
        "hooks": [ { "type": "command", "command": "py .forge/hooks/guard.py" } ] }
    ]
  }
}
```

Keep this in your own settings, not committed, so it stays your choice.

## Why opt-in

Enforcement that fires without consent is a good way to get disabled in anger. The rules are strict on purpose, so you turn them on when you want them. Once on, they are deterministic: the same input always blocks or passes, with no model judgment involved.
