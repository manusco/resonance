# System Design Checklist

> **Objective**: Ensure architecture is simple, justified, and viable. Apply the checks relevant to the changed boundary; this list is not a requirement to produce every artifact or model every system concern for every task.

## 1. Requirements Validation
- [ ] **Constraints Identified**: Budget, Timeline, Compliance, Team Skills.
- [ ] **Boundary Evidence**: For each proposed boundary, name its current owner and the present scaling, deployment, failure, security, or data-ownership need. Would the simplest single-deploy topology meet the contract? Do not use hypothetical future growth alone as evidence.
- [ ] **Buy vs Build**: Evaluated SaaS alternatives before building custom.

## 2. Trade-Off Analysis
- [ ] **Decision**: Every major choice supports a requirement.
- [ ] **Cost**: Complexity cost vs Business value is positive.
- [ ] **Lock-in**: Exit strategy for major vendors/frameworks.

## 3. Structural Integrity
- [ ] **Boundaries**: Domains are loosely coupled (Context Maps).
- [ ] **Dependency Graph**: No circular dependencies between modules.
- [ ] **Scaling**: Identify horizontal/vertical scaling paths.
- [ ] **Single Points of Failure**: No "God Services" that can kill the entire system.
- [ ] **Data flow**: Mapping clear paths from input to persistence.
- [ ] **Data Ownership**: Single source of truth defined for every entity.

## 4. Documentation
- [ ] **Decision Record**: Record durable boundary, contract, and material operating-cost choices.
- [ ] **C4**: Visualize context and containers when the topology decision needs them.
