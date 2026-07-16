# Project Memory

The compound-knowledge index for this project. One line per durable lesson; longer detail goes in a leaf file under `memory/`. This file loads at the start of every session, so a lesson written here once is read every time after. The rule is simple: never solve the same problem twice.

How to use it: when you learn something durable, a bug and its fix, a project convention, a research finding, or a user preference, add a one-line entry under Lessons, newest first. Keep it specific and greppable. If it needs more than a line, write `memory/<slug>.md` and link it. Curate the file: when a lesson stops being true, correct or remove it.

## Lessons

<!-- Add lessons here, newest first. For example:
- **Postgres over SQLite for the job queue.** SQLite locks the whole file under concurrent writers; the queue needs row-level locking. See memory/queue-db.md. -->

## Decisions

Settled decisions live here so they resurface every session and never get re-litigated. One line each: date, the decision, the why. Supersede by editing the line; git history keeps the audit trail.

<!-- - 2026-01-15 **Postgres over SQLite.** Concurrent writers need row-level locking. -->

---

[View State (active context)](01_state.md) | [View Soul (vision and laws)](00_soul.md)
