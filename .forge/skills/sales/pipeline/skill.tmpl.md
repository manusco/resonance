---
name: resonance-sales-pipeline
description: Ingests sales pipeline deal data from CSV, HubSpot, or Salesforce, and renders a fully interactive, visual pipeline analytics dashboard with velocity calculations and forecasting. Use when asked to audit deal pipelines, forecast monthly sales goals, or track rep quota performance.
archetype: procedure
---

# /resonance-sales-pipeline: analyze sales pipelines

> **Role:** resonance-frontend
> **Input:** Deal data via CSV paste, HubSpot API records, or Salesforce Opportunity queries.
> **Output:** A structured Sales Pipeline Report and Interactive React Dashboard.
> **Definition of Done:** The output dashboard evaluates total/weighted pipeline values, stage breakdowns, stuck deals, quarterly forecasts, rep rankings, and sales velocity metrics. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] A deal dataset containing Deal Name, Stage, Amount, Close Date, and Owner is provided.
- [ ] You have mapped custom stages to standard probability defaults.

## Algorithm

Copy this checklist and tick items as you go.

1. **Ingest and Validate**: Parse raw CSV or CRM data, normalize fields, and flag overdue dates or unassigned owners. → verify: data warnings are displayed at top of the report.
2. **Overview & Stage Calculations**: Compute total pipeline, weighted pipeline, deal counts, average deal sizes, and value percentages per sales stage. → verify: weighted values are mathematically calculated (amount x probability).
3. **Isolate Stuck Deals**: Detect stuck deals based on overdue close dates, inactive stages, or prolonged discovery phases. → verify: recommended actions are mapped to the deal's specific stage.
4. **Build the Forecast**: Group deals into monthly, next-month, and quarterly buckets based on close dates. → verify: top 5 high-value deals are highlighted in the forecast summary.
5. **Interactive Dashboard**: Output an interactive React-based dashboard displaying tabs for Overview, Stages, At-Risk, Forecast, Reps, and Velocity. → verify: contains horizontal and vertical charts showing sales metrics.

## Recovery

- Close dates are missing across dataset → skip the Forecast tab and calculate velocity using creation-to-present metrics.
- Probability values are missing → apply standard defaults (Prospecting 10%, Demo 30%, Proposal 50%, negotiation 70%, won 100%) and note it in the overview.
- Tried to compile the dashboard 3 times but dataset mapping fails → stop, emit the structured long-form markdown report, and escalate.

{{RESOLVER:decision_brief}}

{{RESOLVER:completion}}

{{RESOLVER:voice}}

{{OVERLAY}}
