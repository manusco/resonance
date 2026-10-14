# Architecture Decision Records (ADR) Protocol

> "We will document architecture decisions effectively."

## 1. The Why

Architecture is a series of trade-offs. We must document:
1.  **What** we decided.
2.  **Why** we decided it (Context).
3.  **What** we rejected (Alternatives).
4.  **Consequences** (Good and Bad).

## 2. The Format (Markdown)

File: `docs/adr/0001-record-architecture-decisions.md`

```markdown
# [Short Title]

* Status: [Proposed | Accepted | Deprecated | Superseded]
* Deciders: [List everyone involved]
* Date: [YYYY-MM-DD]

## Context and Problem Statement
[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

## Decision Drivers
* [driver 1, e.g., a force, facing concern, ...]
* [driver 2, e.g., a force, facing concern, ...]

## Considered Options
* [Option 1]
* [Option 2]
* [Option 3]

## Decision Outcome
Chosen option: "[Option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | … | comes out best (see below)].

### Positive Consequences
* [e.g., improvement of quality attribute satisfaction, follow-up decisions required, …]

### Negative Consequences
* [e.g., compromising quality attribute, follow-up decisions required, …]
```

## 3. The Mandate

Create an ADR when the choice changes a durable cross-system boundary or carries material, long-lived trade-offs. Typical examples include adding a system-of-record database, changing a major framework, adding an external service dependency, or defining a monorepo structure. For a local or reversible choice, use the project's existing decision record or the plan instead of creating an ADR solely to satisfy this template.

Record the decision, alternatives, and consequences in a discoverable project artifact. A consequential architecture decision must not live only in an ephemeral conversation; use the ADR format when the choice meets the criteria above.
