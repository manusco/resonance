---
name: resonance-marketing-weekly-search-audit
description: Portfolio search-performance operator. Runs a restrained weekly Google Search Console, technical SEO, and GEO audit across approved properties, writes evidence-backed reports, and produces a ranked action queue without changing application code. Use when running a recurring search audit, reviewing GSC performance across sites, or deciding the next safe SEO and GEO actions.
archetype: procedure
---

# /resonance-marketing-weekly-search-audit: measure, explain, prioritize

> **Role:** search-performance operator for a portfolio of sites.
> **Input:** an approved property registry, GSC credentials, repository roots, and the previous audit report.
> **Output:** one dated report per property, one portfolio roll-up, and a small ranked queue of proposed actions.
> **Definition of Done:** every property was attempted, every data limitation is named, every finding traces to evidence, no application file was changed, reports have machine-readable frontmatter, and the weekly run used a bounded resource budget.

This is an audit and decision procedure. It does not implement SEO, content, link, schema, redirect, or deployment changes. A separate approved delivery task owns implementation.

## Operating contract

- Preserve user value and human editorial quality. Never create templated or obviously machine-written copy as an audit shortcut.
- Technical health comes before content expansion. Broken crawlability, indexation, canonicalization, sitemap, security, or rendering gets priority.
- Treat GSC as evidence, not as a complete model of demand. Keep property, date window, dimensions, filters, row limits, pagination, data freshness, and retrieval time in every report.
- Keep SEO and GEO separate. A page can rank without being easy to cite, and a page can be citable without earning search demand.
- Use only approved cross-site links. A relevant reference that helps a reader is useful. A network of artificial links is not.
- Do not infer an action from a single anomalous day. Require a comparable window or label the finding as a hypothesis.
- Do not delete, redirect, rename, or rewrite a page because its purpose is unclear. First identify its intent, owner, links, traffic, and conversion role.

## Weekly timing

Run once each week on **Tuesday at 09:30 Europe/Berlin**. This leaves room for Google's usual reporting delay while producing a useful mid-week decision queue. The run timezone is Europe/Berlin; Search Analytics date boundaries and freshness are interpreted in Google's data timezone, America/Los_Angeles. First probe the last ten days with a date dimension to identify the most recent day with data. Select the last seven complete days ending at least two days before retrieval, unless the probe and `dataState` prove a later final window is available. Record the actual window and `first_incomplete_date`. Do not run a second routine job to compensate for preliminary data. Run an exceptional check only for a suspected outage, security issue, indexing incident, or owner-requested release validation.

The scheduler must be external to GitHub Actions by default. Use a local or hosted scheduler that calls the audit runner and stores reports in the repositories. GitHub Actions are reserved for small, deterministic verification jobs or an explicitly approved release. Never create a matrix job for every site without a measured need.

## Resource budget

- One bounded GSC retrieval session per property per weekly window: maximum 12 requests. Use exactly one freshness probe with `dataState=all` grouped by `date`, four current-window dimension requests (`query`, `page`, `country`, `device`), four preceding-window dimension requests for the same dimensions, one aggregate trailing 28-day baseline request with no dimensions, and at most two continuation pages total. Use a documented row cap of 1,000 rows per request and stop at the cap. Decision queries use `dataState=final`; if final data is unavailable, mark the property concerned and do not make a period comparison. Record requested and response `aggregationType`, dimensions, `dataState`, rows returned, pages read, and whether truncation occurred.
- One technical fetch pass per public origin. Reuse the result for related checks.
- One repository inspection pass limited to routing, metadata, sitemap, robots, structured data, templates, and the previous report.
- No paid crawler, large language model batch, backlink crawler, or full-site rendering job unless the finding is high priority and the owner approves the extra budget.
- Stop when the budget is reached. Report untested properties and queue them; do not silently broaden the run.

## Prerequisites

- [ ] Property registry maps each domain to its exact GSC property, repository, primary market, language, business intent, owner, and approved cross-site links.
- [ ] Credentials are loaded from the approved local secret path. Never commit credentials, tokens, raw exports, or personally identifiable query data.
- [ ] The current date, timezone, previous report path, and prior action status are known.
- [ ] The target repository is confirmed. Never use the portfolio directory as a working directory.
- [ ] The run mode is `routine`, `incident`, or `release-check`.

## Algorithm

### 1. Freeze scope

Read the property registry and record the ordered list. Do not discover extra repositories by scanning a parent directory. For each property, record whether it is active, intentionally paused, new, redirected, or retired.

### 2. Retrieve GSC evidence

For every active property:

1. Verify the property name and type, URL-prefix or domain.
2. Probe the last ten days grouped by `date` to identify the latest available day, then choose the complete comparison window using the freshness rule above. Record `dataState` and `first_incomplete_date`.
3. Query Search Analytics for the agreed complete window with dimensions `query`, `page`, `country`, and `device` in separate bounded requests, including the immediately preceding comparable window and a trailing 28-day baseline for context. Keep within the request and row caps above.
4. Capture clicks, impressions, CTR, and position. Preserve zero rows as unknown, not as zero demand.
5. Record pagination, row limits, filters, run timezone, Google data timezone, retrieval timestamp, requested/response aggregation type, search type (`web`), and whether the data is final or preliminary. Mark every capped or truncated result.
6. Compare with the immediately preceding comparable window only when both windows are complete. Use the trailing 28-day baseline before promoting a noisy seven-day movement to a priority action.
7. Flag striking-distance queries, high-impression low-CTR pages, declining pages, query cannibalization, country mismatch, device gaps, and branded versus non-branded movement.
8. Never publish raw query data if it could identify an individual or expose a secret. Suppress raw query and page rows below 10 impressions, aggregate them into a low-volume bucket, and retain detailed exports outside Git.

### 3. Check technical search health

Inspect the public origin and repository implementation for:

- HTTP status, HTTPS, redirect chains, canonical URLs, language alternates, and accidental noindex.
- `robots.txt`, sitemap discovery, sitemap validity, indexable URL count, and orphaned sitemap entries.
- Server-rendered title, meta description, H1, headings, visible answer, internal links, and image alternatives.
- JSON-LD validity and connected entity graph. Use the page-appropriate type, not every available type.
- Core Web Vitals evidence when available. Do not claim a field score without a measured source.
- JavaScript-only content, blocked assets, soft 404s, duplicate URLs, parameter handling, and stale dates.
- Security and trust surfaces: HTTPS, contact details, authorship, legal pages, editorial ownership, and claims that need sources.

### 4. Check GEO readiness

For each priority page, assess:

- The first answer appears in plain language near the top.
- The page contains a self-contained answer passage that can be quoted without surrounding context.
- Headings, lists, tables, definitions, dates, units, and sources are easy to parse.
- Claims show first-hand experience or a named source.
- Organization, person, service, place, and `sameAs` relationships are consistent where appropriate.
- Important content is server-rendered and accessible to ordinary crawlers.
- AI crawler policy is deliberate and documented. Do not treat `llms.txt` or crawler access as a guaranteed ranking factor.

### 5. Inspect intent and architecture

Map each important URL to one primary intent: service, place, event, tool, education, person, directory, or editorial reference. Identify the canonical target, supporting pages, competing pages, and the next useful internal link. For programmatic or location pages, require a distinct user purpose and local evidence before recommending expansion.

For cross-site linking, propose a link only when all are true:

1. It answers a real reader question.
2. The destination is authoritative for that question.
3. The source page can explain the relationship naturally.
4. The link does not create duplicate doorway pages or a circular self-promotion pattern.
5. The destination owner and target language are recorded.

Reject sitewide reciprocal links and exact-match anchor-text schemes. Require approval from both source and destination owners before implementation. GSC observations can support a link hypothesis, but never prove that a link caused a ranking change or an AI citation.

### 6. Produce findings

Every finding must contain:

- `id`, property, URL or repository path, observed evidence, date, and source.
- Intent and affected audience.
- Reasoning that connects evidence to likely impact.
- Priority: `P0` outage or security, `P1` indexation or severe search loss, `P2` measurable opportunity, `P3` polish or research.
- Recommendation with the smallest safe next step.
- Acceptance criteria and a measurement window.
- Owner, dependency, estimated effort, and whether implementation needs approval.
- Confidence: `confirmed`, `probable`, or `hypothesis`.

### 7. Rank the weekly queue

Select at most five actions for the portfolio and at most three per property. Rank by expected search or user benefit divided by effort and risk. Break ties in this order: outage prevention, indexability, high-intent conversion, evidence quality, then growth experiments. Carry forward unfinished actions with their original evidence. Do not create a new action merely to make the report look active.

### 8. Write reports

Write one report in each repository's `.resonance/docs/` directory and one portfolio roll-up in the designated portfolio repository. Use a filename such as `YYYY-MM-DD-weekly-search-audit.md`; if a rerun is required, append a run identifier so no report is overwritten. Reports are written only to an isolated clean worktree or approved external staging area. Do not commit, open a PR, merge, deploy, or modify application files without explicit owner approval.

Required frontmatter:

```yaml
---
schema_version: 1
report_type: weekly-search-audit
run_id: YYYY-MM-DDTHH-mm-ssZ-property
report_date: YYYY-MM-DD
period_start: YYYY-MM-DD
period_end: YYYY-MM-DD
run_timezone: Europe/Berlin
data_timezone: America/Los_Angeles
property: example.com
gsc_property: sc-domain:example.com
run_mode: routine
status: DONE
gsc_retrieval: YYYY-MM-DDThh:mm:ss+02:00
data_freshness: final
first_incomplete_date: null
source_commit: null
runner_version: unknown
previous_report: null
search_type: web
properties_attempted: 1
properties_completed: 1
properties_blocked: 0
rows_truncated: false
raw_data_retention: external-only
findings: 0
proposed_actions: 0
implementation: none
---
```

The body must include: executive result, scope, data provenance, technical findings, SEO findings, GEO findings, cross-site opportunities, reasoning, recommendations, acceptance criteria, carried-forward actions, blocked checks, and the redacted command names or canonical endpoint paths used. Never include secrets, token paths, query strings, raw low-volume queries, or credential locations. Keep raw exports outside Git.

### 9. Verify and close

- [ ] Every registry property has `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` status.
- [ ] Every finding has evidence, confidence, priority, owner, and acceptance criteria.
- [ ] Report frontmatter parses and counts match the body.
- [ ] No application files were changed.
- [ ] No credentials, raw query exports, or generated crawler dumps were written to a repository.
- [ ] The previous report was not overwritten.
- [ ] Any rerun has a unique `run_id` and filename.
- [ ] The next run date and any exceptional follow-up are recorded.

## Release and GitHub Actions policy

Routine reports are not releases and do not bump application versions. Prefer a local or external scheduler. If a GitHub workflow is approved, it must use one scheduled orchestrator job, minimal read permissions, explicit concurrency, a hard timeout, cached dependencies, bounded retries, credentials from a secret manager, and only the report artifact needed for review. Scheduled workflows are not made safe by a path filter alone. The job must not deploy, open PRs, or rewrite site content automatically. A release workflow is separate from the audit workflow and runs only on an owner-approved tag.

## Recovery

- GSC authentication fails: mark the property blocked, continue technical checks, and do not guess performance conclusions.
- Property is ambiguous: stop that property's data analysis until the exact property is confirmed.
- Data is preliminary or truncated: report the limitation and avoid period-over-period claims.
- Site is unreachable: capture status and timestamp, classify as incident if confirmed, and do not rewrite content.
- Repository contains unrelated changes: inspect and report them by path. Dirty does not mean broken. Do not reset, stash, clean, or overwrite them.
- A page's intent is unclear: preserve it, investigate ownership and links, and ask for a decision before deletion or redirect.
- The budget is exhausted: stop, report the untested scope, and schedule the next bounded pass.

## Out of scope

- Implementing code, redirects, schema, content, links, deployments, or releases.
- Inventing search volume, backlink authority, AI citations, rankings, or conversion impact.
- Treating a single GSC row, crawler score, or model opinion as proof.
- Bulk-generating location pages or answer blocks without distinct user value and evidence.
