---
name: <skill-name>
description: <Third person: what this procedure does> + <when to run it>. Use when <trigger 1>, <trigger 2>. <Note "manual-only" if it has side effects (deploy, send, delete).>
archetype: procedure
contract_version: 1
job_id: <stable.domain.job-id>
stage: <FRAME | PLAN | EXECUTE | VERIFY | APPROVE | PUBLISH>
contributes_to:
  - <job_id this procedure contributes to, if any>
reviews:
  - <job_id this procedure independently reviews, if any>
finalizes:
  - <artifact finalized by this procedure, if any>
artifact_access:
  - <artifact>:<read,create,append_evidence,modify,review,approve,publish,execute>
dispatch_conditions:
  - <specific condition that activates this participant>
compatibility: <active | provisional | deprecated | alias | retired>
---

# /<skill-name>: <one-line job>

> **Role:** <which knowledge skill(s) drive this, e.g. resonance-backend>
> **Input:** <what must exist before this runs>
> **Output:** <the verifiable artifact this produces>
> **Definition of Done:** <the checkable bar: tests pass, file written, deploy verified>

## Prerequisites (fail fast)

- [ ] <precondition. If missing, stop and say so before doing any work>
- [ ] <precondition>

## Algorithm

Copy this checklist and tick items as you go.

1. **<Step>**: <action>. → verify: <the check that proves it worked>.
2. **<Step>**: <action>. → verify: <check>.
3. **<Step>**: <action>. → verify: <check>.

## Recovery

- <expected failure> → <exact recovery step>.
- Tried a fix 3 times without success → stop, report what was tried, escalate.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
