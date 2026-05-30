# System Design Checklist

> **Objective**: Ensure architecture is simple, justified, and viable.

## 1. Requirements Validation
- [ ] **Constraints Identified**: Budget, Timeline, Compliance, Team Skills.
- [ ] **Simplicity Check**: Is there a simpler way? (e.g., Monolith vs Microservices).
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
- [ ] **ADR**: Key decisions recorded.
- [ ] **C4**: System Context and Containers visualized.
