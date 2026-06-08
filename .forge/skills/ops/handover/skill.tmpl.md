---
name: handover
description: Writes a handover document for a colleague after a coding session or sprint. Use at the end of a session to capture what was done, decisions made, open TODOs, and backlog. Produces docs/handovers/YYMMDD_handover.md. If a handover file already exists for today, appends to it. Run before closing the conversation. Session context is the richest input.
archetype: procedure
---

# /handover: capture the session for the next person

> **Role:** session scribe and context preservationist.
> **Input:** Current conversation context + git log + `.resonance/` state files + `task.md`.
> **Output:** `docs/handovers/YYMMDD_handover.md` written or appended. `.resonance/01_state.md` "Next Session" updated.
> **Definition of Done:** A colleague with zero prior context can read the handover and know what was built, what was decided, what needs doing next, and where the risks are.

The conversation history is the richest source. Run this before the session ends.

## Source Priority

Mine these in order:

1. **Current session context**: the conversation history. What was discussed, built, decided, and blocked. Use it first; it contains what no file captures.
2. **`git log --oneline -20`**: concrete evidence of what landed. Run as a shell command.
3. **`.resonance/01_state.md`**: current phase, goal, blockers.
4. **`task.md`**: checked items (done) vs. unchecked (open).
5. **`.resonance/02_memory.md`**: decisions and lessons from prior sessions.

If a source is missing, skip it silently. Do not fabricate.

## Same-Day Logic

1. Compute today's date in `YYMMDD` format.
2. Check if `docs/handovers/<YYMMDD>_handover.md` exists via {{TOOL:glob}}.
3. **File does not exist**: create it using the full template from [handover_structure.md](references/handover_structure.md).
4. **File exists**: append only. Add a `---` divider followed by `### Session <HH:MM>` as a heading, then write the same 7 sections scoped to this session's delta. Do not re-copy the earlier content.

## Operational Sequence

1. Read `.resonance/01_state.md` (if it exists).
2. Read `task.md` (if it exists).
3. Run `git log --oneline -20` as a shell command.
4. Note today's date (`YYMMDD`) from system or the git log timestamps.
5. Check whether `docs/handovers/<YYMMDD>_handover.md` already exists.
6. Synthesize from all sources. The session context leads; files confirm and fill gaps.
7. Write (new file) or append (existing file, with divider + timestamp heading).
8. Update `.resonance/01_state.md` "Next Session" to reference the handover path and the top open TODO.

## Recovery

- **No session context (running cold)**: use git log + `.resonance/` files. Add a note at the top of the handover: `> Synthesized from files. No live session context available.`
- **`docs/handovers/` does not exist**: create it before writing.
- **`task.md` not found**: synthesize Open TODOs from session context. Do not fabricate specific items not discussed.
- **No commits today**: write `No commits this session` under What Was Done. Do not guess at work done.
- **No `.resonance/01_state.md`**: skip that source. Do not error.

## Reference Library

- **[Handover Structure](references/handover_structure.md)**: Document template with section guidance and examples.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:learnings}}

{{RESOLVER:voice}}

{{OVERLAY}}
