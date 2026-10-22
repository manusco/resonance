# Application design contract

**Status:** APPROVED
**Application:** Example workspace, record inspection on desktop web
**Approval owner and evidence:** Example product design owner, DEC-EX-001 (fixture approval record)
**Canonical source:** this file

## Scope and variants

- Applications and surfaces covered: Example workspace record inspection
- Explicit exclusions: Full record editing
- Approved variants and observable selectors: Full record editing uses a route; inspection uses the shared drawer at or above the supported wide-layout minimum and the route below it.

## Approved patterns

| Task family and scope | Approved default and reference | Approved variant and selector | Verification evidence |
| --- | --- | --- | --- |
| Workspace record inspection, Customers and Suppliers | Shared contextual drawer, see `CustomersDetail.tsx` | At widths below `--layout-wide-min`, use the full route component; selector is the existing layout constraint | Same task, state, and viewport; compare context restoration and keyboard focus |

## Foundations and user-facing conventions

- Color, typography, spacing, shape, depth, motion: See the shared workspace theme and components.
- Interaction, navigation, data, content, and lifecycle vocabulary: Preserve the table query and filters when returning from detail.
- Accessibility, input, responsive, and platform constraints: Keyboard focus returns to the originating row.
