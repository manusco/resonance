# Memory Recall: retrieve by meaning, do not load the whole brain

> As `.resonance/` and its memory grow, reading whole files is wasteful and blunt. The `02_memory.md` index (lessons plus settled decisions) loads at session start; recall pulls the deeper slices on demand.

## The tool

- **Recall relevant memory:** `py .forge/recall.py "<what you need to know>"` returns the top matching chunks from `.resonance/*.md` (including the loaded `02_memory.md` index and `memory/` leaf files), ranked by relevance. Use it before a task instead of opening every file. Default retrieval is pure-Python BM25 (offline, no dependency); set `RESONANCE_EMBED_CMD` to an embedding command to rank by meaning instead.

## Decisions live in the loaded index

Settled decisions are one-line entries under `## Decisions` in `02_memory.md`, so they are re-read every session and never re-litigated (Zero Divergence). One line each: date, the decision, the why.

- **Session start:** the index is already in context; skim `## Decisions` before proposing anything that feels familiar. Settled calls are not up for re-debate.
- **After a real decision:** add the line, newest first.
- **When a decision changes:** edit the line to the new decision with the new date and reason; git history keeps the audit trail.

## The rules

- `.resonance/*.md` stays the source of truth. Recall is an index over it, not a replacement.
- Recall is a starting point, not the last word. If the retrieved slices are thin, read the specific file. If they conflict, surface the conflict rather than guessing.
