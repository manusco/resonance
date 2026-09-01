---
name: resonance-marketing-run-search-operating-cycle
description: Search operating-cycle conductor. Use when recurring or one-off search performance evidence must be collected, checked, interpreted through the SEO specialist, and turned into an owner-ready audit report. It keeps artifacts private by default, requires joint query-page evidence for cannibalization claims, and uses the canonical P0-P3 audit taxonomy. It prepares a run but does not schedule one.
archetype: orchestration
owner: marketing.search-operations
activation: manual
authority: consequential
triggers:
  - run a search performance operating cycle
  - produce a governed SEO evidence report
entrypoints:
  - /search-cycle
negative_triggers:
  - schedule a recurring search job
  - write search exports into the repository without approval
inputs:
  - user_request
  - search_run_scope
  - search_evidence
outputs:
  - user_request
  - search_run_scope
  - seo_scope
  - evidence
  - recommendation
  - audit_report
side_effects:
  - may_coordinate_work
  - may_execute_checks
  - may_write_files
write_sets:
  - private:search-operating-cycle
failure_policy: stop
invokes:
  - resonance-marketing-seo
---

# /resonance-marketing-run-search-operating-cycle: turn search evidence into governed action

> **Role:** search operating-cycle conductor.
> **Input:** a property registry, cadence, timezone, credential reference, artifact destination, comparison window, prior-run reference, and current search evidence.
> **Output:** a validated evidence bundle and an owner-ready audit report using the canonical seven categories and P0-P3 severities.
> **Definition of Done:** The run contract is complete, evidence limits are disclosed, every scoped property has an outcome, SEO interpretation comes from `resonance-marketing-seo`, findings use the canonical taxonomy, and artifacts stay private unless the user explicitly approves a named repository write.

This skill owns the run spine. It does not replace the SEO specialist, create a scheduler, or treat a dashboard as proof.

## Pipeline

1. **Contract:** Read [Run Contract](references/run_contract.md). Record the property registry, cadence, timezone, credential reference, private artifact destination, comparison window, and prior-run reference. Use role labels, never names of people. -> gate: `scripts/validate_search_run.py contract.json` passes.
2. **Authority:** Default every artifact to a private destination outside the repository. If a repository write would help, present the exact path and redacted content for explicit approval before writing. Never put raw query rows, raw page rows, credentials, tokens, or individual information in Git. -> gate: write authority and destination are explicit.
3. **Evidence:** Collect or accept evidence for every scoped property. Preserve source, property, dimensions, time window, comparison window, extraction time, row limits, truncation, filters, and freshness. Read [Evidence and Report Contract](references/evidence_and_report_contract.md). -> gate: missing, partial, stale, and truncated evidence are labeled.
4. **Joint grain:** Use evidence with both `query` and `page` dimensions before making a cannibalization claim. Separate query-only and page-only exports cannot prove that relationship. -> gate: every cannibalization finding cites joint query-page rows or remains a candidate.
5. **Interpretation:** Invoke `resonance-marketing-seo` with the validated evidence and known limits. Ask it for diagnosis and recommended action, not invented metrics. -> gate: claims trace to evidence and uncertainty remains visible.
6. **Classification:** Classify each proven finding into exactly one canonical category and one severity from P0 through P3. Do not invent an SEO-specific severity ladder. -> gate: the validator accepts every finding.
7. **Disposition:** Produce the report defined in the evidence contract. Give every scoped property a state: clean, candidate, finding, rejected, fixed, skipped, or incomplete. -> gate: no property disappears silently.
8. **Close:** Name the owner role, next action, verification method, and next run boundary. Mark later outcome proof as `DONE_PENDING_OUTCOME`; do not create the schedule here.

## Recovery

- A required contract field is missing -> stop with `NEEDS_CONTEXT` and name the missing field.
- Credentials cannot be resolved -> stop. Never request a token in a repository file or report.
- Evidence is stale, truncated, capped, or dimensionally incomplete -> label the limit and narrow the claim. Do not infer clean health.
- Joint query-page rows are missing -> keep cannibalization as a candidate and request the correct export.
- The requested repository destination lacks explicit approval -> keep the artifact private and present the proposed write.
- The SEO specialist cannot support a claim -> remove it or mark it incomplete.

## Out of Scope

- Creating cron jobs, automations, reminders, or background workers.
- Owning SEO diagnosis that belongs to `resonance-marketing-seo`.
- Publishing, deploying, or changing production search configuration.
- Storing credentials, raw search exports, or individual information in the repository.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory; when `.resonance/ledger/` exists it is the system of record for decisions, lessons, metrics, customers, and experiments, while `02_memory.md` keeps `[lib]` notes and pointers).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
