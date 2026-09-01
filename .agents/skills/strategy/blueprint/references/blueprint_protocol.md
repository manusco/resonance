# Blueprint protocol

Use this protocol to create or revise a project-owned architecture constitution.
The output path follows the project's documentation convention. Do not impose a
framework-specific path on the project.

## Required artifact

1. **Authority and scope**
   - purpose, audience, approval owner, scope, exclusions, status, version
   - evidence sources and last verified revision
2. **System outcomes and quality attributes**
   - what the system must enable
   - ranked qualities with observable tests or thresholds
3. **Stable principles**
   - short rules with rationale, consequence, and verification method
   - principles describe direction, not current compliance
4. **Current state**
   - observed context, containers, boundaries, dependencies, stores, providers
   - canonical data owners, business-rule owners, state machines, side effects
   - known failure modes and evidence gaps
5. **Target state**
   - approved boundaries, contracts, ownership, dependency direction, trust zones
   - required runtime evidence, recovery behavior, and deployment invariants
6. **Evolution map**
   - gaps between current and target
   - safe seams and ordered slices
   - for each gap: keep, constrain, migrate, replace, or remove
   - compatibility, rollback, and behavior-preservation evidence
7. **Decision index**
   - links to durable architecture decisions and supersession status
8. **Exception register**
   - controlled deviations from the target or principles
9. **Conformance gates**
   - checks used during framing, planning, review, and release
10. **Change policy**
    - who may approve revisions
    - what requires a decision record
    - evidence required to change a stable principle

## Derive principles from first principles

For each candidate rule, answer:

1. Which system outcome or required quality does it protect?
2. Which recurring failure does it prevent?
3. What concrete decision does it constrain?
4. How can a reviewer detect compliance or violation?
5. Does it stay useful across implementation changes?

Reject a principle when it is a technology preference, duplicates another rule,
cannot guide a decision, or has no verification method.

## Brownfield rules

- Map what exists before naming the target.
- Treat code, schemas, runtime evidence, incidents, tests, and operator workflows
  as evidence. None alone defines intended behavior.
- Do not erase accidental behavior silently. Classify it as preserve, correct, or
  unresolved.
- Separate current, transition, and target diagrams. Never draw the target as if
  it already exists.
- Prefer seams that reduce coupling while keeping a working path available.
- Require behavior characterization before changing a poorly understood path.

## Controlled exception schema

Every exception records:

- identifier and status
- violated rule or boundary
- narrow scope
- reason the compliant path is not currently viable
- risk and blast radius
- named owner
- compensating controls
- evidence and monitoring
- review trigger
- removal condition
- linked replacement plan or decision, when one exists

A date can trigger review. It is not enough by itself as a removal condition.
