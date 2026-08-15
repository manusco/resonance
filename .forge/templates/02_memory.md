# Project Memory

The compound-knowledge index for this project. In legacy projects, keep one line per durable lesson here and put longer detail in a leaf file under `memory/`. In projects with `.resonance/ledger/`, the ledger is the typed system of record for decisions, lessons, metrics, customers, and experiments; this file keeps `[lib]` notes, pointers to ledger ids, and prose that is not one of those five types. This file loads at the start of every session, so a lesson written here once is read every time after. The rule is simple: never solve the same problem twice.

How to use it: when there is no ledger, add a one-line entry under Lessons, newest first. Keep it specific and greppable. If it needs more than a line, write `memory/<slug>.md` and link it. When there is a ledger, write a `les-` entry instead, with `confidence:` and `review_due:`. Curate the file: when a lesson stops being true, correct or remove it. Retire a lesson only when the code or system demonstrably contradicts it, never for lack of proof that it still holds. A repo rarely witnesses its own operational truths, so unverifiable is not false.

## Lessons

<!-- Add lessons here, newest first. For example:
- **Postgres over SQLite for the job queue.** SQLite locks the whole file under concurrent writers; the queue needs row-level locking. See memory/queue-db.md. -->

## Decisions

Settled decisions live here only in legacy projects without `.resonance/ledger/`. When the ledger exists, write `dec-` entries there and keep only pointer lines here if helpful. One line each: date, the decision, the why. Supersede by editing the line in legacy mode; in ledger mode, supersede with a new entry and a back-reference.

<!-- - 2026-01-15 **Postgres over SQLite.** Concurrent writers need row-level locking. -->

---

[View State (active context)](01_state.md) | [View Soul (vision and laws)](00_soul.md)
