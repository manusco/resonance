---
name: <skill-name>
description: <Third person: what pipeline this runs> by coordinating <skills/agents>. Use when <trigger 1>, <trigger 2>.
archetype: orchestration
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
