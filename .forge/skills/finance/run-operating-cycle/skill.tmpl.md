---
name: resonance-finance-run-operating-cycle
description: Finance operating-cycle conductor. Use when a user wants actuals, runway, forecast, scenarios, budget decisions, investor updates, or operating metrics governed from source data to decision record.
archetype: orchestration
owner: finance.operating-cycle
activation: manual
authority: consequential
triggers:
  - run a finance operating cycle
entrypoints:
  - skill:finance-run-operating-cycle
negative_triggers:
  - produce finance decisions from unsourced numbers
inputs:
  - user_request
  - plan
  - finance_scope
outputs:
  - user_request
  - artifact
  - evidence
  - decision
  - finance_scope
  - analytics_scope
  - legal_scope
side_effects:
  - may_coordinate_work
  - may_write_files
write_sets:
  - project:finance-cycle
failure_policy: stop
invokes:
  - resonance-strategy-finance
  - resonance-marketing-analytics
  - resonance-ops-legal
---

# resonance-finance-run-operating-cycle: turn numbers into governed decisions

> **Role:** finance operating conductor.
> **Input:** actuals, cash balance, revenue drivers, costs, forecast question, investor update, or budget decision.
> **Output:** sourced actuals, reconciliation notes, forecast scenarios, decision options, approval log, and metric follow-up.
> **Definition of Done:** Every number has a source, runway uses net burn or is labeled gross coverage, assumptions are explicit, decisions are recorded, and external outcomes get due dates.

## Pipeline

1. **Source actuals:** identify source systems, date range, currency, cash balance, revenue, costs, liabilities, and data owner. -> gate: no unsourced number enters the model.
2. **Reconcile:** separate actuals from assumptions and flag gaps. -> gate: unknowns remain visible.
3. **Model:** invoke `resonance-strategy-finance` for driver-based model, unit economics, runway, or fundraising materials. -> gate: top-line numbers trace to drivers.
4. **Measure:** invoke analytics when product, marketing, or revenue metrics feed the forecast. -> gate: metric definitions are consistent.
5. **Legal or tax boundary:** invoke legal or escalate when commitments, financing terms, payroll, tax, or regulated reporting enter scope.
6. **Decide:** present options, tradeoffs, and approval-needed actions. Record approved decisions in the ledger when available.

## Recovery

- Revenue is missing -> call cash divided by spend gross cash coverage, not runway.
- Actuals and assumptions are mixed -> split them before modeling.
- Binding finance or tax action is requested -> escalate before action.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
