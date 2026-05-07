# Linear CLI Reference

> **Context**: This is a tool-specific reference document for the `linear-pp-cli`. It is kept here for reference if automated API-based PM is needed in the future.

## Installation
```bash
npx -y @mvanhorn/printing-press install linear cli-only
```

## Auth
Requires `LINEAR_API_KEY`.

## Notable Commands
*   `today`: Triaged queue across all teams.
*   `velocity`: Sprint velocity trends.
*   `workload` / `bottleneck`: Team capacity and blocked issues.
*   `projects burndown`: Project landing dates via velocity regression.
*   `cycles compare`: Side-by-side metrics.
*   `stale` / `orphans`: Backlog grooming (untouched, unassigned).
*   `similar <text>`: Fuzzy-find duplicates (offline FTS5).
*   `sync`: Populate local SQLite store for fast queries.

Add `--agent` to any command for JSON output. Filter with `--select`.
