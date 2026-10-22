# Application design contract

**Status:** PROPOSED
**Application:** Ledger Desk, reconciliation workspace
**Approval owner and evidence:** Finance product lead, approval not yet recorded.
**Canonical source:** `.resonance/05_design.md`

## Scope and variants

- Applications and surfaces covered: Reconciliation workspace.
- Explicit exclusions: Customer-facing billing pages.
- Approved variants and observable selectors: None approved.

## Proposed patterns

| Task family and scope | Proposed default and evidence | Approved variant and selector | Verification evidence |
| --- | --- | --- | --- |
| Review a reconciliation batch | Keep date, account, and payment state filters visible together. Existing `src/reconciliation/BatchTable.tsx` uses a persistent filter panel; this is observed implementation. | None approved. | Pending comparable keyboard and narrow-width review. |
| [unfinished] | [no evidence collected] | [none] | [pending] |

## Open decisions

- Decide whether the persistent panel is the proposed default after checking its narrow-width behavior.
