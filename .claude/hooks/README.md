# Resonance Claude Code hook (opt-in)

This directory ships a ready Claude Code hook config, so the deterministic guard
can run at edit time, not only at commit time. It is opt-in: nothing here fires
until you enable it.

## What it does

`settings.snippet.json` registers a PostToolUse hook on Write and Edit that runs
`py .forge/hooks/guard.py --hook` on the file you just changed. On a violation
(an em or en dash, a committed secret, an edit to the Soul) it hands the problem
back to the model so it fixes it before moving on. Set `RESONANCE_STRICT_VOCAB=1`
in your environment to also flag slop vocabulary in Markdown.

## Enable it

One command merges the hook into your personal `.claude/settings.local.json`:

```
py .forge/hooks/install.py --claude
```

Or paste the contents of `settings.snippet.json` into your Claude Code settings
by hand. Disable by removing the hook from `.claude/settings.local.json`.

The git hooks (`py .forge/hooks/install.py`) are the cross-tool enforcement and
work in any editor. This Claude Code hook is the extra, editor-level check for
faster feedback while you write.
