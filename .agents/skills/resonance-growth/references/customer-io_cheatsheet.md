# Customer.io CLI Reference

> **Context**: Tool-specific reference for `customer-io-pp-cli`. Kept here for automated broadcast/journey tasks if needed.

## Installation
```bash
npx -y @mvanhorn/printing-press install customer-io --cli-only
```

## Notable Commands
*   `campaigns funnel`: Step-by-step journey funnel (sent -> delivered -> opened -> clicked -> converted).
*   `segments overlap`: Venn diagrams of segment memberships.
*   `customers timeline`: Chronological event stream for 360 view.
*   `broadcasts preflight`: Check segment size, overlap, and last-sent recency before a broadcast.
*   `deliveries triage`: Generate incident bundles for bounce/delivery spikes.
*   `suppressions audit`: Attribute suppressions to bounce/complaint events.

Add `--agent` to any command for JSON output. Filter with `--select`.
