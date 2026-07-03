# Memory Recall: retrieve by meaning, do not load the whole brain

> As `.resonance/` and `learnings.jsonl` grow, reading whole files is wasteful and blunt. Retrieve the slices that matter for the task, and keep settled decisions in a log you can query, so you never re-litigate a call you already made.

## The two tools

- **Recall relevant memory:** `py .forge/recall.py "<what you need to know>"` returns the top matching chunks from `.resonance/*.md`, `learnings.jsonl`, and the active decisions, ranked by relevance. Use it before a task instead of opening every file. Default retrieval is pure-Python BM25 (offline, no dependency); set `RESONANCE_EMBED_CMD` to an embedding command to rank by meaning instead.
- **The decision log:** `py .forge/decisions.py` records settled decisions append-only.
  - `add "<decision>" --why "<reason>" --files a,b` when a real decision is made.
  - `list` at session start to resurface active decisions.
  - `search "<topic>"` before re-opening a question that may already be settled.
  - `supersede <id> "<new decision>" --why "..."` when a decision changes (the old one is marked, not deleted).
  - `redact <id>` if an entry contained something it should not.

## When to use each

- **Session start:** run `decisions.py list` and skim the active decisions. Settled calls are not up for re-debate (Zero Divergence).
- **Before a task:** run `recall.py "<the task topic>"` to pull the relevant soul, state, memory, and learnings, rather than reading `.resonance/` end to end.
- **Before proposing a choice that feels familiar:** `decisions.py search "<topic>"`. If it was decided, honor it or supersede it with a reason; do not silently re-choose.
- **After a real decision:** record it with `add`, so the next session starts ahead.

## The rules

- `.resonance/*.md` stays the source of truth. Recall is an index over it, not a replacement. The decision log is the queryable record that `02_memory.md` prose could not be.
- Decisions are append-only. To change one, `supersede` it. Never edit history in place; the trail is the point.
- Recall is a starting point, not the last word. If the retrieved slices are thin, read the specific file. If they conflict, surface the conflict rather than guessing.
