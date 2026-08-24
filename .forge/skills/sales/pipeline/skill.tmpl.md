---
name: resonance-sales-pipeline
description: Sales pipeline analyst. Ingests deal data from CSV, HubSpot, or Salesforce and produces deal-level pipeline inspection, velocity, forecast views, and rep performance analysis. Use when the immediate job is to understand the current pipeline. RevOps owns durable funnel definitions, coverage policy, capacity, territories, quotas, compensation, and forecast governance.
archetype: procedure
---

# /resonance-sales-pipeline: analyze sales pipelines

> **Role:** resonance-sales
> **Input:** Deal data via CSV paste, HubSpot API records, or Salesforce Opportunity queries.
> **Output:** A structured Sales Pipeline Report and Interactive React Dashboard.
> **Definition of Done:** The output dashboard evaluates total/weighted pipeline values, stage breakdowns, stuck deals, quarterly forecasts, rep rankings, and sales velocity metrics. Free of AI slop and em dashes. Passed the validator.

## Prerequisites (fail fast)

- [ ] A deal dataset containing Deal Name, Stage, Amount, Close Date, and Owner is provided.
- [ ] You have observed stage-to-close rates by cohort. If not, mark the forecast unweighted or assumption-based.

## Algorithm

Copy this checklist and tick items as you go.

1. **Ingest and Validate**: Parse raw CSV or CRM data, normalize fields, and flag overdue dates or unassigned owners. → verify: data warnings are displayed at top of the report.
2. **Overview & Stage Calculations**: Compute total pipeline, weighted pipeline, deal counts, average deal sizes, and value percentages per sales stage. → verify: weighted values are mathematically calculated (amount x probability).
3. **Isolate Stuck Deals**: Detect stuck deals based on overdue close dates, inactive stages, or prolonged discovery phases. → verify: recommended actions are mapped to the deal's specific stage.
4. **Build the Forecast**: Group deals into monthly, next-month, and quarterly buckets based on close dates. → verify: top 5 high-value deals are highlighted in the forecast summary.
5. **Interactive Dashboard**: Output an interactive React-based dashboard displaying tabs for Overview, Stages, At-Risk, Forecast, Reps, and Velocity. → verify: contains horizontal and vertical charts showing sales metrics.

## Recovery

- Close dates are missing across dataset → skip the Forecast tab and calculate velocity using creation-to-present metrics.
- Probability values are missing → do not pretend a weighted forecast is measured. Use observed cohort conversion if available; otherwise show an unweighted forecast and a clearly labeled assumption scenario.
- Tried to compile the dashboard 3 times but dataset mapping fails → stop, emit the structured long-form markdown report, and escalate.

## Reference Library

- **[B2B Sales Pipeline](references/b2b_sales_pipeline.md)**: Qualification frameworks (BANT, MEDDIC, MEDDPICC, SPICED), pipeline stage definitions, objection handling, and forecasting methodology.

{{RESOLVER:operating_standard}}

{{OVERLAY}}
