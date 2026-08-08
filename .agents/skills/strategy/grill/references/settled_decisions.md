# Settled Decisions: provenance that survives the pipeline

A decision the user made in conversation must travel to plan and build without being silently re-opened, and without a bare assertion being mistaken for a considered choice. This is the provenance layer for the grill brief.

## The settlement test

Classify each resolved decision by HOW it was decided, not how confidently it was stated:

- **settled**: a tradeoff was surfaced and the user chose with it in view. This is the only class that counts as an examined decision. Confidence of tone is not settlement; only a choice made against a named alternative is.
- **directive**: the user asserted it without examining an alternative. Honor it, but it earns exactly one challenge downstream if evidence warrants, then it is recorded and not re-litigated.
- **inferred**: you proposed it and no one pushed back. The weakest class. A later stage may revisit it freely.

Never label your own unexamined proposal as settled.

## The label that travels

Stamp each resolved decision in the brief, in plain English so it stands on its own:

`session-settled: <settled | directive | inferred>. chose <X> over <Y> because <reason>.`

Downstream stages read the label and do not re-ask a settled decision. They augment it, never silently contradict it.

## The contradiction ladder

Research or implementation may overturn a settled decision only on evidence, and the response scales with the evidence:

- **nothing found**: proceed silently.
- **suboptimal but workable**: proceed, and attach a one-line conflict note to the brief.
- **invalidating** (the decision cannot work as chosen): stop, mark the work blocked, and hand back with the evidence.

A settled decision is never re-opened on preference, only on evidence at one of these levels.
