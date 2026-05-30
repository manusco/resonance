# Slack CLI Reference

> **Context**: This is a tool-specific reference document for the `slack-pp-cli`. It is kept here for reference if automated API-based workspace analysis is needed in the future.

## Installation
```bash
npx -y @mvanhorn/printing-press install slack --cli-only
```

## Auth Surfaces
*   `SLACK_BOT_TOKEN` (xoxb-): Workspace-scoped read/post.
*   `SLACK_USER_TOKEN` (xoxp-): User-scoped actions (DMs, stars).

## Notable Commands
*   `search <query>`: Full-text search (live or local sync).
*   `digest`: Daily/weekly activity summary.
*   `health`: Channel activity, engagement, stagnation.
*   `quiet`: Find dead channels.
*   `response-times`: Thread responsiveness.
*   `threads-stale`: Unanswered threads.
*   `activity`: User/channel summary.
*   `sync`: Populate local SQLite store for offline analytics.

Add `--agent` to any command for JSON output. Filter with `--select`.
