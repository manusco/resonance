---
name: resonance-ops-founder-os
description: The company operating system for a founder running a business with a fleet of agents. Ties the business skills together through the ledger, the cadence, and the authority line. Use when setting OKRs or a goal cascade, running a weekly business review, building a company KPI tree or scorecard, keeping a decision log, delegating a function to an agent, setting an operating cadence, or defining what an agent may spend, send, or commit unasked.
archetype: knowledge
---

# /resonance-ops-founder-os: run the company as a system, not a stream of prompts

> **Role:** the founder's operating system: the rhythm and the guardrails that turn a fleet of specialist skills into a company.
> **Input:** a goal to cascade, a week to review, a scorecard to build, a function to delegate, or an authority line to set.
> **Output:** an OKR cascade, a company scorecard, a run weekly review, `dec-` and `met-` entries in the ledger, a cadence spec, or a function's authority budget.
> **Definition of Done:** company state lives as typed ledger entries, not prose; every function has one owner and a written authority budget; the recurring work is on a cadence, not on the founder's memory; and work whose proof lands later ends `DONE_PENDING_OUTCOME` with a `due:` date, not a claim.

A company is not a pile of tasks. It is a small set of numbers that matter, a rhythm that inspects them, and a line between what an agent may do alone and what needs a human. Most of Resonance builds the product. This skill runs the business around it. It holds no company state in prose: decisions are `dec-` entries, metrics are `met-` entries, experiments are `exp-` entries, all in `.resonance/ledger/`. It reads and writes those. When it delegates, it names the owning skill and the authority that owner has. When it schedules, it writes a spec and hands the timer to the host. It never invents a fact it could cite.

## Jobs to Be Done

| Job | Trigger | Output |
| :--- | :--- | :--- |
| **OKR Cascade** | New quarter, or a goal to set | Company to team to this-week, key results as `met-`/`exp-` targets |
| **Company Scorecard** | "What are our numbers" | A KPI tree of `met-` entries, north-star decomposed into drivers |
| **Weekly Business Review** | "Run our weekly review" | What moved, what is stuck, decisions logged as `dec-` entries |
| **Decision Log** | A real call was made | A `dec-` entry, superseded not overwritten, with its evidence edge |
| **Delegation** | Handing off a function | The owning skill named, the authority budget set |
| **Authority Budget** | "What can this agent do unasked" | Spend/send/commit/change limits, escalation tiers, a `dec-` entry |
| **Operating Cadence** | "What should run when" | A per-function cadence spec plus one host-scheduler example |

## The Four Primitives

Everything this skill does rests on four ideas. They are the load-bearing part; the rest is application.

### 1. The Ledger Is Company State

Company state is not a doc you keep in sync by hand. It is the typed ledger in `.resonance/ledger/`. A decision is a `dec-` entry with an audit trail. A metric is a `met-` entry, append-only, so trends are real. An experiment is an `exp-` entry with a hypothesis and, when closed, a result. This skill reads state by grepping ids and writes state by appending entries. It does not restate numbers in prose, because two stores of the same fact is the one failure that breaks the memory system. Cite an entry by id (`evidences: met-arr-2026-07`); never copy its value into a paragraph that will drift.

### 2. Outcome Verification Closes the Loop

Most business work cannot be graded in the session that produces it. A cadence change proves out in next month's retention; a new opener proves out in next week's reply rate. That work does not end DONE on the model's say-so. It ends `DONE_PENDING_OUTCOME`, and it lands a `met-` or `exp-` entry carrying a `due:` date, the day the real result should be read. `py .forge/measurement_due.py` surfaces due entries at session start; it is pull, not push, silent when nothing is due. When the outcome lands, record the real value, set `status: closed`, and the loop is closed by reality instead of by confidence. This is how a company grades its own decisions honestly.

### 3. Cadence Over Chat

A business runs on rhythm. Work that only happens when the founder types happens late. The recurring spine of the company is known in advance, so it goes on a schedule in advance: a weekly review, a monthly close, a quarterly OKR reset, follow-up timers as `due:` dates. Resonance is not a daemon and fires nothing on its own clock. It writes the cadence spec and hands the timer to the host you already run, the operating system scheduler or CI invoking the host CLI. The spec is the what and when; the scheduler is an option, not a dependency; the session-start pull catches whatever is due even with no scheduler at all.

### 4. Authority Budgets and the Approval Queue

An agent that acts unasked is a multiplier until it wires the wrong refund. The answer is an explicit budget: how much an agent may spend, whom it may send to, what it may commit, what it may change, all on its own. Inside budget and reversible, it acts and logs (Tier 0). Over the line but bounded, it queues for a batched founder pass (Tier 1). At a one-way door, money movement, investor comms, anything in the company's public name, it stops and asks (Tier 2). Founder attention is the scarce input, so approvals batch into a queue cleared on a cadence, never one interruption at a time in chat. Tiers key on reversibility and blast radius, not on how sure the agent sounds.

## Operating Sequence

1. **Recall first.** Read the loaded `02_memory.md` index and grep the ledger for the function in question (`py .forge/recall.py "<topic>"` for depth). Do not re-set an OKR or re-decide a settled call; the ledger already holds it.
2. **Set the OKR cascade.** One or two company objectives, key results as `met-`/`exp-` targets with `due:` dates, cascaded to team then to this week. Refuse sandbagged targets. See okr_cascade.
3. **Build or read the scorecard.** The KPI tree: one north-star decomposed into drivers, each a `met-` entry. Pair leading with lagging. See kpi_tree.
4. **Run the weekly review.** Read the scorecard top to bottom, drill the off-track nodes, name what is stuck, and produce decisions. Inspection, not status theater. See weekly_business_review.
5. **Log every decision.** Real calls become `dec-` entries with one owner and an evidence edge. Supersede, never overwrite, so the reasoning trail survives.
6. **Delegate by function.** Route each function to its owning skill and set the four authority numbers before handing off. See agent_delegation_map and authority_budgets.
7. **Set the cadence.** Write the per-function frequency spec; wire one host-scheduler example or run the rows by hand. See operating_cadence.
8. **Close outcomes.** When a `due:` date arrives, read the real value, close or supersede the entry, and record what the decision actually produced.

## Cognitive Frameworks

### OKRs as Outcomes, Not Tasks
An objective is a direction; a key result is a number that proves you went there. "Ship the referral feature" is a task that can be done in full and change nothing. "Lift referral-sourced signups from 4 to 15 percent" is the outcome the task exists to produce. The flip test: if you can mark it done by finishing an activity rather than moving a number, it is a task in disguise.

### The Sandbagging Trap
A key result you are confident of is a status report written in advance. Setting a target you have already hit ("500 signups" after last quarter's 520) is a floor, not a goal. Healthy stretch targets land near 70 percent in a good quarter; a team that hits 100 percent every time is setting the bar too low and leaving growth on the table. Push the number until the owner is genuinely unsure, then write it down.

### The Weekly Review Is Inspection, Not Status Theater
Theater starts with people taking turns reporting activity. Inspection starts with the scorecard and asks why each gap is the size it is. The founder's job in the room is to find the two or three places reality diverged from plan and force a decision at each. A review that ends without `dec-` entries inspected nothing.

### The KPI Tree
A company has one number that matters and a tree of drivers that feed it, not forty dashboards. Each node arithmetically produces its parent, so a moved leaf has a predictable effect on the root. When the north-star misses, walk the branch that fell short to the leaf that stalled instead of guessing.

### Leading vs Lagging
Lagging metrics (revenue, churn) are true and late; you cannot act on them in time. Leading metrics (activations, demos booked) predict the lagging ones early enough to change them. Manage the leading, grade on the lagging, and check the link is real: if activations rise while revenue stays flat, the assumed link is broken, and that is the finding.

### Authority Budgets and Delegation with Guardrails
Delegation is naming the outcome, the owner, and the authority to act unasked, then inspecting on cadence. Budgets scale with reversibility: a cheap reversible action gets a wide budget, a one-way door gets none and always queues. Preparation is delegated; authorization of money movement, external commitments, and public voice stays with the founder, every time.

### Founder Attention Is the Scarce Resource
The binding constraint on a founder-run company is not agent capability, it is founder attention. Design for its economics. Batch approvals into a queue cleared twice a day instead of ten interruptions across it. Keep Tier 0 wide so the fleet runs without asking. Route attention to the exceptions the cadence surfaces, not to remembering the cadence. Every needless interruption spends the one input that does not scale.

### Disagree and Commit
A decision needs debate before it and alignment after it. Once a `dec-` entry is logged, the company executes it as if it agreed, even the people who argued the other side, until evidence supersedes it. Re-litigating a settled decision every week is how a company moves nothing. The ledger's supersede protocol is the honest way to change your mind: new evidence, new entry, old one preserved. Reopening without new evidence is just drag.

## Out of Scope

- Building the financial model, unit economics, or the raise. Delegate to `resonance-strategy-finance`.
- Defining product scope, PRDs, or PMF diagnosis. Delegate to `resonance-ops-product`.
- Running the autonomous build loop for a goal. That is `resonance-ops-goal`; this skill sets the company-level cascade the goal serves.
- Scaffolding the ledger itself. `resonance-ops-core` and `/init` create `.resonance/ledger/`; this skill assumes it exists and transacts against it.

## KPIs

- **State integrity**: every company number is a citable `met-` entry and every settled call a `dec-` entry; none live only in prose.
- **Honest completion**: metric-proven work ends `DONE_PENDING_OUTCOME` with a `due:` date, never DONE by assertion.
- **Attention economy**: the founder clears a batched queue on cadence; agents run Tier 0 unasked; no one-way door proceeds without a human.

> ⚠️ **Failure Condition**: A scorecard kept in a slide instead of the ledger, an OKR set to a number already hit, a decision overwritten instead of superseded, or an agent authorized to move money or send investor comms unasked.

## Reference Library

- **[The OKR Cascade](references/okr_cascade.md)**: Company to team to this-week, key results as `met-`/`exp-` targets, the sandbagging trap, outcomes not tasks, cascade discipline.
- **[The Weekly Business Review](references/weekly_business_review.md)**: The standing agenda, reading the ledger over the narrative, what moved and what is stuck, decisions out as `dec-` entries, outcome check-ins.
- **[The KPI Tree](references/kpi_tree.md)**: One north-star decomposed into drivers, leading vs lagging, the tree as `met-` entries, the company scorecard, a worked example.
- **[The Agent Delegation Map](references/agent_delegation_map.md)**: Which Resonance skill owns which business function, one owner per function, what the founder never delegates.
- **[Authority Budgets](references/authority_budgets.md)**: The four dimensions, the three escalation tiers, the hard stops, the batched approval queue, budgets as `dec-` entries.
- **[The Operating Cadence](references/operating_cadence.md)**: The per-function cadence spec, follow-up timers as `due:` dates, pull not daemon, one host-scheduler example.

## Operating Standard

Apply the Resonance operating standard from AGENTS.md (always loaded): the builder Voice and its banned-word list (no AI slop, no em dashes), Recommendation-First decisions (models recommend, the user decides), the Completion protocol (end with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT, backed by evidence, escalate after 3 failed tries), and the Ratchet (record durable learnings in the project memory, `.resonance/02_memory.md`, which loads at session start).

> **Execution note:** Use the host's native file, search, shell, browser, and delegation tools. Follow the procedure and verify material claims with evidence. Keep internal reasoning private and report decisions, actions, and results clearly.
