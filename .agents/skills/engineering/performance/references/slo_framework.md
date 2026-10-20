# SLO Framework (The Happiness Metric)

> **Objective**: Move from monitoring "Server Health" (CPU) to "User Happiness" (Experience).
> **Rule**: "If the user is happy, the CPU spike doesn't matter."

## 1. Fundamentals
*   **SLI (Indicator)**: What we measure (Latency).
*   **SLO (Objective)**: The service target chosen for the product and workload, such as a latency threshold.
*   **SLA (Agreement)**: The consequence defined by an applicable agreement, such as a refund threshold.

## 2. Example tiers, not defaults

The values below are examples only. Set targets from the product's user promise, risk, and observed workload; do not assign a tier or inherit a target without that context.

### Tier 1: Critical Path (Login, Checkout)
*   **Latency**: p95 < 200ms
*   **Availability**: 99.99%
*   **Rationale**: If this breaks, we lose money immediately.

### Tier 2: Important (Search, Profiles)
*   **Latency**: p95 < 500ms
*   **Availability**: 99.9%
*   **Rationale**: Annoying if broken, but not fatal.

### Tier 3: Background (Reports, Analytics)
*   **Latency**: p95 < 5s
*   **Availability**: 99%
*   **Rationale**: Can be retried later.

## 3. Example performance budgets

These sample values are not defaults. Set budgets only when the product's user promise, workload, and operating policy support them. Measure weight as well as speed when it affects those goals.

```json
{
  "javascript": "300kb (gzip)",
  "images": "500kb",
  "requests": "50",
  "time-to-interactive": "2.5s"
}
```

## 4. Checks when they apply

When optimizing a service without an established project target, agree the relevant objective and percentile with its owner. Apply an error budget only when an active service policy defines one.

- Consider a criticality tier when it is part of the product's service policy.
- Set or use the SLO that applies to this service and decision.
- Choose a percentile and population that fit the user promise and workload.
- Apply the error budget and release policy defined by the service owner.
