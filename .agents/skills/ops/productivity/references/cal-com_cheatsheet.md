# Cal.com CLI Reference

> **Context**: This is a tool-specific reference document for the `cal-com-pp-cli`. It is kept here for reference if automated API-based scheduling is needed in the future. The core `resonance-productivity` skill relies on the mental models of capacity planning rather than this specific CLI.

## Installation
```bash
npx -y @mvanhorn/printing-press install cal-com --cli-only
```

## Notable Commands
*   `book`: Composed booking flow (slot check + create).
*   `slots find`: Ranked slot search across event types.
*   `reschedule next`: Bump to next available slot.
*   `agenda`: Upcoming bookings from local store.
*   `conflicts`: Detect double bookings.
*   `gaps`: Find open, unbooked windows.
*   `analytics no-show`: No-show rates and capacity planning.
*   `workload`: Booking distribution across team members.
*   `link create` / `link list`: Manage bookable links.
*   `ooo set`: Manage Out of Office.

Add `--agent` to any command for JSON output. Filter with `--select`.
