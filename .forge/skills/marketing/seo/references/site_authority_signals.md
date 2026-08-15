# Site Quality Signals

Google describes a mix of page-level, site-wide, and system-specific ranking signals. Treat leaked field names as unverified context, not as operating doctrine. Do not tell users that a specific internal field such as `siteAuthority`, `siteQualityStddev`, or `hostAge` is a deterministic control they can optimize directly.

## Source Card

- Primary source: https://developers.google.com/search/docs/appearance/ranking-systems-guide
- Verified: 2026-08-15
- Scope: Google Search public ranking-system guidance.
- Review trigger: Google Search Central ranking-system update, major core update, or leaked-signal claim used in a recommendation.

## What To Audit

- Helpful content: does the site publish pages that solve real user tasks?
- Reputation: are credible sources, customers, or communities referring to the site?
- Entity clarity: can a crawler understand who owns the site, what it offers, and why it is credible?
- Internal linking: can important pages be reached and understood through clear navigation and links?
- Indexed-quality pattern: are thin, duplicate, obsolete, or low-trust pages bloating the index?

## Guardrails

- Do not promise that deleting pages improves rankings. Recommend prune, consolidate, noindex, or improve only when the page inventory proves a user or crawl-quality reason.
- Do not claim a "sandbox" as fact. New sites often lack reputation, links, content depth, and behavioral evidence; diagnose those visible factors.
- Do not optimize for leaked fields. Translate suspected signals into observable work: better content, cleaner architecture, source-backed claims, stronger distribution, and crawlable pages.

## Audit Checklist for Site Authority

- [ ] **Reputation indicators**: Diverse backlinks, brand recognition, entity presence
- [ ] **New-site constraints**: Content depth, distribution, links, and entity clarity
- [ ] **Quality consistency**: Thin, duplicate, outdated, or unsupported pages identified
- [ ] **Internal linking**: Clear hierarchy distributing PageRank effectively
- [ ] **Direct demand**: Analytics and customer discovery show whether people seek the brand
