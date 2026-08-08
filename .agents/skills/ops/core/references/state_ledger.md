# The State Ledger: typed memory the agents transact against

> `.resonance/` holds prose (soul, state, memory, systems). The ledger adds the part that must be queried, cited, and superseded: decisions, lessons, metrics, customers, experiments. Same brain, one typed layer. Frontmatter-free, greppable, git-versioned. No database.

The ledger exists only when `.resonance/ledger/` exists. A project without it is a legacy brain and stays valid forever (see Grace Rule). New projects get the scaffold from `/init`.

## Contents

- Why a ledger
- File layout
- Entry format
- The five types
- Edges and traversal
- Supersede protocol
- schema_version and the grace rule
- Precedence (the one rule that keeps this from forking)
- Outcome verification (closing the outer loop)
- How an agent uses it

## Why a ledger

Prose memory answers "what do we know". A ledger answers "what is true now, what proves it, and what did it replace". A decision you can supersede with an audit trail, a metric you can cite as evidence for an experiment, a customer you can point a renewal play at: these are records, not paragraphs. Records need stable ids and typed fields. That is the whole idea.

## File layout

One file per type, one `##` entry per record:

```
.resonance/ledger/decisions.md
.resonance/ledger/lessons.md
.resonance/ledger/metrics.md
.resonance/ledger/customers.md
.resonance/ledger/experiments.md
```

One entry is one retrieval unit: `recall.py` splits on `##` headings, so an entry is exactly what recall returns. The prose files (00 to 04) are untouched. `02_memory.md` stays the human index; when a ledger exists it carries only `[lib]` notes and one-line pointers to entry ids.

## Entry format

No YAML, no fences. The id is in the heading. Field lines are plain `key: value`, starting on the line after the heading, ending at the first blank line. Free prose follows the blank line.

```
## dec-queue-postgres: Postgres over SQLite for the job queue
type: decision
created: 2026-07-18
status: active
evidences: met-queue-lock-2026-07

SQLite locks the whole file under concurrent writers; the queue needs
row-level locking. Revisit only if we drop to a single worker.
```

Id grammar: `(dec|les|met|cus|exp)-<lowercase-slug>`. The prefix must match the file (a `dec-` id lives only in `decisions.md`). Ids are globally unique, which is what makes an edge a stable citation.

Shared fields on every entry: `type`, `created` (ISO date), `status` (`active`, `superseded`, or `closed`). Edge fields are optional (see below).

## The five types

**decision** (`dec-`): a settled call. Optional `chose` / `over`. Supersede to change it.

**lesson** (`les-`): a durable learning. Optional `hardened: <path-or-id>` pointing at the deterministic fix that makes the mistake unrepeatable.

**metric** (`met-`): one observation, append-only. Requires `value`, `unit`, `as_of` (ISO date), `source`. The id carries the period so citations are stable.

```
## met-arr-2026-07: ARR, July 2026
type: metric
created: 2026-08-01
status: closed
value: 41800
unit: eur
target: 50000
as_of: 2026-07-31
source: stripe dashboard, manual pull
```

**customer** (`cus-`): an account the business skills act on. Optional `segment`, `mrr`, `since`.

**experiment** (`exp-`): a test. Requires `hypothesis`. A `closed` experiment requires `result`. Often `caused` a decision.

```
## exp-pricing-anchor: High-anchor pricing page
type: experiment
created: 2026-06-10
status: closed
hypothesis: showing the top tier first lifts mid-tier conversion
result: mid-tier conversion up 31 percent over 4 weeks, n=214
caused: dec-pricing-three-tier
```

## Edges and traversal

Three directed edge fields, comma-separated ids:

- `supersedes: <id>` on the new entry (new replaces old).
- `evidences: <id>, <id>` (this entry cites those as proof).
- `caused: <id>` (this entry produced that one; an experiment causes a decision).

Forward traversal is reading the field. Reverse traversal is grep: `grep -rn "met-arr-2026-07" .resonance/ledger/` returns every entry that cites it, in any direction, with no index. Wikilinks like `[[dec-queue-postgres]]` are allowed in prose but are decoration, never authoritative.

## Supersede protocol

Two writes, so the audit trail lives in the file, not only in git:

1. The new entry carries `supersedes: <old-id>`.
2. The old entry gets `status: superseded` and a `superseded_by: <new-id>` line. Nothing else on the old entry changes; it is never deleted.

The validator enforces the reciprocity (a supersede target must be `superseded` and point back).

Supersede on demonstrated contradiction, never on absence of proof. If a re-check shows the code or system demonstrably does otherwise, supersede it. If you merely cannot find in-repo evidence that it still holds, leave it: a repo rarely witnesses its own operational truths (a deploy step, an external contract, a runtime behavior), and unverifiable is not false. A self-auditing agent that retires every lesson it cannot confirm deletes exactly the hard-won operational knowledge that has no artifact. And match the record to reality, not the reverse: rewriting what a lesson recommends is a new decision that supersedes it, not a silent edit.

## schema_version and the grace rule

Line 2 of every ledger file, under the H1:

```
schema: resonance-ledger/1
```

The rule is structural, not a flag:

- No `.resonance/ledger/` directory: legacy untyped brain. The validator skips every ledger check and says nothing. This is the whole grace rule; old projects never break.
- `ledger/` exists: every file must carry the `schema:` marker. A version above the framework's known max is an error that says to upgrade.
- `/update-resonance` never creates `ledger/` in a project that lacks it. Only `/init` scaffolds it.

## Precedence (the one rule that keeps this from forking)

If `.resonance/ledger/` exists, it is the system of record for its five types. Write a decision as a `dec-` entry, not as a line under `## Decisions` in `02_memory.md`. The prose index keeps `[lib]` notes and pointer lines only. Two stores writing the same fact is the one failure that breaks Zero Divergence inside the memory system itself. When in doubt, the ledger wins for the five types; prose wins for everything else.

## Outcome verification (closing the outer loop)

A lot of business work cannot be verified in the session that produces it. A cold-email sequence's proof is a reply rate a week later; a pricing change's proof is next month's conversion. That work ends `DONE_PENDING_OUTCOME`, not DONE (see the completion protocol), and it lands a ledger entry that carries its own check-in date:

- A **metric** or **experiment** entry gets an optional `due:` field, an ISO date, the day the real result should be checked in. The entry stays `status: active` until then.

```
## exp-cold-open-v2: New cold-email opener
type: experiment
created: 2026-07-18
status: active
hypothesis: the problem-first opener lifts reply rate above 4 percent
due: 2026-08-01
```

`py .forge/measurement_due.py` scans for entries whose `due:` date has arrived and surfaces them at session start. It is pull, not push: nothing fires on a clock, and it is silent when nothing is due. When the outcome lands, the human or agent records the real result (the metric `value`, the experiment `result`), sets `status: closed`, and the loop is closed: the work is now either confirmed or refuted by reality, not by the model's own say-so. A field report that a skill misfired runs the other direction: `py .forge/field_report.py` turns it into a `les-` lesson and a stub eval case, so the miss compounds into a permanent regression check.

## How an agent uses it

- **Recall before acting:** `py .forge/recall.py "<topic>"` ranks ledger entries with the rest of the brain.
- **Cite, do not restate:** reference a metric or decision by id (`evidences: met-arr-2026-07`) instead of copying its numbers.
- **Append, do not rewrite:** a new metric reading is a new entry. A changed decision is a supersede, not an edit.
- **Traverse with grep:** to see what a decision affects, grep its id across the ledger.
