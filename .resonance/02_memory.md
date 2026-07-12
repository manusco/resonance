# Project Memory

The compound-knowledge index for this repo. One line per durable lesson; longer detail goes in a leaf file under `memory/`. This file loads at the start of every session (through the root `CLAUDE.md` bridge on Claude Code, and through `AGENTS.md` on other tools), so a lesson written here once is read every time after. The rule is simple: never solve the same problem twice.

How to use it: add a one-line entry under Lessons when you learn something durable, a bug and its fix, a project convention, a research finding, a user preference, or a correction, newest first. Keep each line specific and greppable. If a lesson needs more than a line, write `memory/<slug>.md` and link it. This is curated, not append-only: when a lesson stops being true, correct or remove it, so the memory stays trustworthy.

## Lessons

- **The carrier: Claude Code loads `CLAUDE.md`, not `AGENTS.md`.** Without a root `CLAUDE.md` that imports `@AGENTS.md`, the operating standard and this memory never reach the model at session start in Claude Code, so the whole compound loop stays dark. The Forge now emits a per-host context bridge (`CLAUDE.md` for Claude Code, `.cursor/rules/resonance.mdc` for Cursor; Codex, opencode, and Antigravity read `AGENTS.md` natively). This exact lesson sat in a downstream repo's `learnings.jsonl` for five weeks, unread, while the flagship's own loop was broken. That is what a dead loop costs.
- **Memory deposits go here, not to `learnings.jsonl`.** `learnings.jsonl` was never loaded by any host, so lessons written to it were never read. Durable lessons land in this file (the loaded index) and in `memory/` leaf files. `recall.py` still reads legacy `learnings.jsonl`, so nothing already captured is lost.

---

[View State (active context)](01_state.md) | [View Soul (vision and laws)](00_soul.md)
