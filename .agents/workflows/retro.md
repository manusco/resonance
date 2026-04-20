---
description: Generate comprehensive engineering retrospectives by analyzing git history.
---

# Retrospective Protocol (`/retro`)

> **Role**: The Analytics Officer (`resonance-growth`, `resonance-architect`)
> **JTBD**: Extract objective team performance metrics and narrative insights from git history.
> **Input**: Timeframe (e.g., "last 7 days").
> **Output**: A highly structured Retro Report.

## 1. Prerequisites
*   [ ] Run inside a valid git repository.
*   [ ] Clean working tree.

## 2. Context (The Objective Truth)
<thinking>
Most retros are feeling-based. This protocol is data-based.
I will look at git history to discover what was actually accomplished, who drove it, and where the hidden drag was. I will balance mathematical truths with human empathy (Constructive Praise + Growth Opportunities).
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Data Gathering (The Git Sweep)
*   **Command**: Validate the timespan (default: 7 days).
*   **Action**: Run `git log --since="X days ago" --oneline --stat`.
*   **Action**: Group commits by author.
*   **Action**: Identify code churn vs adding new capability.
*   **Action**: Determine Test Ratio (Lines of tests vs Lines of application code).

### Step 2: Metric Computation
Calculate these key Retro Metrics:
1.  **Shipping Streak**: How many consecutive days was code shipped?
2.  **Focus Score**: Percentage of commits grouped into distinct logical branches, vs ad-hoc main patches.
3.  **Complexity Delta**: Did we remove more lines than we added, or did complexity strictly increase?

### Step 3: Narrative Assembly
Structure the retrospective document:
*   **1. The Big Picture**: 3-sentence summary of the week's theme (e.g., "This was a week of heavy infrastructure debt payoff").
*   **2. Objective Metrics**: Commits, LOC Changed, Active Days.
*   **3. Highlights & Praise**: Give credit where credit is due (who shipped what).
*   **4. Growth Opportunities**: Where did we stumble? (e.g., "PR #145 took 4 days to review").
*   **5. The Core Question**: "Are we moving faster this week than last week?"

## 4. Governance (Definition of Done)
*   **Output**: Generate `retro_YYYY_MM_DD.md` in `docs/retros/`.
*   **Action**: Ask the user what action items they want to extract from this retro into the planning queue.
