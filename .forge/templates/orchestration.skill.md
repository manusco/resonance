---
name: <skill-name>
description: <Third person: what pipeline this runs> by coordinating <skills/agents>. Use when <trigger 1>, <trigger 2>.
archetype: orchestration
contract_version: 1
job_id: <stable.domain.job-id>
stage: <FRAME | PLAN | EXECUTE | VERIFY | APPROVE | PUBLISH>
contributes_to:
  - <job_id this orchestrator contributes to, if any>
reviews:
  - <job_id this orchestrator independently reviews, if any>
finalizes:
  - <artifact finalized by this orchestrator, if any>
artifact_access:
  - <artifact>:<read,create,append_evidence,modify,review,approve,publish,execute>
dispatch_conditions:
  - <specific condition that activates this participant>
compatibility: <active | provisional | deprecated | alias | retired>
---

# /<skill-name>: <one-line pipeline job>

> **Role:** orchestrator. Drives: <skill A>, <skill B>, <skill C>.
> **Input:** <what must exist before this runs>
> **Output:** <the consolidated artifact / report>
> **Definition of Done:** <every stage reported; blocking findings surfaced>

## Prerequisites (fail fast)

- [ ] <precondition>

## Pipeline

Run stages in order. Each stage is a skill or subagent. Pass its output forward.
Do not skip a stage; if one is not applicable, say why.

1. **<Stage>**: invoke `<skill>` with <input>. → gate: <what must hold to proceed>.
2. **<Stage>**: invoke `<skill>` with <prior output>. → gate: <check>.
3. **Synthesize**: consolidate findings into <output>. Rank by severity.

## Recovery

- A stage fails or blocks → halt the pipeline, report which stage and why, do not
  fabricate downstream results.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
