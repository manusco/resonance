---
name: resonance-ops-retro
description: The Analytics Officer. Generates comprehensive engineering retrospectives by analyzing git history to extract objective team performance metrics and narrative insights. Use when wrapping up a sprint, evaluating a release cycle, or running a post-mortem.
archetype: procedure
---

# /resonance-ops-retro: data-driven retrospectives

> **Role:** the Analytics Officer.
> **Invoked as:** `/retro` (to analyze git history and generate a retro).
> **Input:** Timeframe (e.g., "last 7 days").
> **Output:** A highly structured Retro Report in `docs/retros/`.
> **Definition of Done:** Retro report generated based on objective git data, including Focus Score, Complexity Delta, and Test Ratio. Narrative balances mathematical truths with human empathy.

Most retros are feeling-based. This protocol is data-based. Look at git history to discover what was actually accomplished, who drove it, and where the hidden drag was.

## Prerequisites (fail fast)

- [ ] Must be run inside a valid git repository.
- [ ] Clean working tree.

## Algorithm (Execution)

Copy this checklist and tick items as you go.

1. **Data Gathering (The Git Sweep)**: Run `git log --since="X days ago" --oneline --stat`. Group commits by author. Identify code churn vs adding new capability. Determine Test Ratio (Lines of tests vs Lines of application code).
2. **Metric Computation**: Calculate Retro Metrics:
   - **Shipping Streak**: Consecutive days code was shipped.
   - **Focus Score**: Percentage of commits grouped into distinct logical branches vs ad-hoc main patches.
   - **Complexity Delta**: Lines removed vs lines added (did complexity strictly increase?).
3. **Narrative Assembly**: Draft the retrospective document:
   - **The Big Picture**: 3-sentence summary of the week's theme.
   - **Objective Metrics**: Commits, LOC Changed, Active Days.
   - **Highlights & Praise**: Give credit where credit is due.
   - **Growth Opportunities**: Where did we stumble?
   - **The Core Question**: "Are we moving faster this week than last week?"
4. **Governance**: Write `retro_YYYY_MM_DD.md` in `docs/retros/`. Ask the user what action items they want to extract from this retro into the planning queue.

## Recovery

- Git command fails → verify the repository history exists. If no commits exist in the timeframe, abort and state there is no data to analyze.

## Out of Scope

- Evaluating individual developer performance for HR purposes (focus on the system and the code).

## Cognitive Frameworks

### Objective Truth
Balance mathematical truths with human empathy (Constructive Praise + Growth Opportunities). Let the data drive the conversation, not feelings.

## Reference Library

- **[Karpathy Rules](../core/references/karpathy_rules.md)**: Universal coding standards (Simplicity, Surgical).

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
