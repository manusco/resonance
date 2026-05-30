# Klaviyo CLI Reference

> **Context**: Tool-specific reference for `klaviyo-pp-cli`. Kept here for automated lifecycle tasks if needed. The core `resonance-growth` skill relies on flow decay and cohort retention models.

## Installation
```bash
npx -y @mvanhorn/printing-press install klaviyo --cli-only
```

## Notable Commands
*   `flow-decay`: Identify flows with decaying open/click rates over time.
*   `cohort`: Group profiles by first event to compute retention curves.
*   `attribution`: Join orders with campaign/flow properties.
*   `dedup`: Find duplicate profiles splitting revenue history.
*   `campaigns deploy`: End-to-end template/campaign creation.
*   `plan qa-gate`: Launch-readiness checklist for links, offers, dates.

Add `--agent` to any command for JSON output. Filter with `--select`.
