# SLO Framework (The Happiness Metric)

> **Source**: AI Design Components (`ancoleman`)
> **Objective**: Move from monitoring "Server Health" (CPU) to "User Happiness" (Experience).
> **Rule**: "If the user is happy, the CPU spike doesn't matter."

## 1. Fundamentals
*   **SLI (Indicator)**: What we measure (Latency).
*   **SLO (Objective)**: The target (Latency < 200ms).
*   **SLA (Agreement)**: The consequence (Refund if > 500ms).

## 2. The Hierarchy of Needs (Tiered SLOs)

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

## 3. Performance Budgets (The Ceiling)
Don't just measure speed. Measure weight.

```json
{
  "javascript": "300kb (gzip)",
  "images": "500kb",
  "requests": "50",
  "time-to-interactive": "2.5s"
}
```

## 4. Implementation Checklist
When optimizing a service:

- [ ] **Define the Tier**: Is this Critical, Important, or Background?
- [ ] **Set the SLO**: What is the "Happy" threshold? (e.g., 200ms).
- [ ] **Measure p95**: Ignore the average. Look at the 95th percentile.
- [ ] **Error Budget**: If we have budget left, we can ship risky features. If not, we freeze.
