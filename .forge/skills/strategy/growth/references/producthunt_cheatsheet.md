# Product Hunt CLI Reference

> **Context**: Tool-specific reference for `producthunt-pp-cli`. Kept here for launch day tracking and category scouting.

## Installation
```bash
npx -y @mvanhorn/printing-press install producthunt --cli-only
```

## Notable Commands
*   `posts launch-day`: Trajectory vs top 5 launches.
*   `posts benchmark`: Percentile curves for a category at hour N.
*   `posts compare`: Side-by-side launch comparison.
*   `posts questions`: Filter launch comments to genuine questions requiring maker replies.
*   `category snapshot`: Leaderboard and momentum for a topic.
*   `posts lookalike`: Find similar launches by tagline tokens.

Add `--agent` to any command for JSON output. Filter with `--select`.
