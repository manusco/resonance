# Support Desk observed implementation

- `src/tickets/TicketTable.tsx` renders search, status filters, row selection, and a selected-count toolbar.
- `src/tickets/TicketTable.tsx` keeps status visible in each row and disables archive for already archived tickets.
- `src/tickets/archiveTickets.ts` performs archive requests and returns per-ticket failures; the UI currently reports only a total success count.
- No approved design contract or approval provenance was found. These are source observations, not approved rules.
