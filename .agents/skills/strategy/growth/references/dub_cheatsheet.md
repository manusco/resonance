# Dub CLI Reference

> **Context**: Tool-specific reference for `dub-pp-cli`. Kept here for link shortening and partner ops automation.

## Installation
```bash
npx -y @mvanhorn/printing-press install dub --cli-only
```

## Notable Commands
*   `links stale`: Find zero-traffic links.
*   `links drift`: Detect links with dropping click rates WoW.
*   `links rollup`: Performance dashboard by tag/folder.
*   `funnel`: Click-to-lead-to-sale conversion rates per link.
*   `partners leaderboard`: Rank partners by true commission/sales, not just clicks.
*   `bounties triage`: Review pending partner submissions.

Add `--agent` to any command for JSON output. Filter with `--select`.
