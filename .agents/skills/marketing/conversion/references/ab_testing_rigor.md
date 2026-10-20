# A/B Testing Rigor Protocol

> "Opinion is the enemy of revenue."

## 1. Evidence and Hypothesis

Do not propose a change before the issue is supported by page or user evidence. If evidence is missing, request it and defer the hypothesis.
*   **Formula**: "If we [Change X], then [Metric Y] will change because [Reason Z]," grounded in the observed issue.
*   Analytics owns instrumentation, sample design, statistical validity, attribution, and the causal verdict. Ask analytics for a sample target and stopping rule; do not calculate them here.

## 2. Statistical Significance

Follow analytics' predeclared sample target, stopping rule, and safety criteria. Do not peek at results to stop opportunistically; use any approved sequential method or safety stop defined in the plan.

## 3. The "One Thing" Rule

Test ONE variable at a time.
*   ❌ Change Headline + Button Color + Layout. (Multivariate is complex).
*   ✅ Change Headline only.

> 🔴 **Rule**: A "Failed" test is a success if you learned *why* it failed.
