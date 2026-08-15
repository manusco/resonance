# Migration Guide

## To v2.5.0

This is a backward-compatible minor release for installed projects.

What changed:

- Skill manifests now validate orchestration contracts.
- New ledgers use `schema: resonance-ledger/2`, which fails closed when
  records are malformed.
- Four new conductors are available as skills, not slash commands:
  `marketing/run-campaign`, `sales/run-revenue-motion`,
  `finance/run-operating-cycle`, and `leadership/run-operating-cycle`.
- Domain doctrine for SEO, legal, security, sales, finance, accessibility,
  mobile policy, performance, and database migrations was corrected.

Upgrade path:

1. Clone the release tag.
2. Run `.forge/update.py` in preview mode.
3. Review conflicts and project-owned files.
4. Apply only after the preview is clean.
5. Run `/system-health` or the local validation gate.

Projects without `.resonance/ledger/` keep the legacy memory grace rule.
Projects with `schema: resonance-ledger/1` stay readable. They do not need the
new `confidence:`, `review_due:`, body, or unknown-field checks until they opt
into schema 2. To migrate a ledger manually, update each canonical file marker
to `schema: resonance-ledger/2`, add the new required fields to decisions,
lessons, and customers, add a short body to each record, and run
`py .forge/validate_library.py --strict`.
