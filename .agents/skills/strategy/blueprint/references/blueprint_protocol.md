# Blueprint protocol

Use this protocol to create or revise a project-owned architecture constitution.
In a Resonance project, write `.resonance/04_systems.md`. Outside Resonance,
locate or declare one canonical architecture artifact before writing.

## Contents

- [Canonical placement](#canonical-placement)
- [Required artifact](#required-artifact)
- [Derive principles from first principles](#derive-principles-from-first-principles)
- [Proportional depth](#proportional-depth)
- [Brownfield rules](#brownfield-rules)
- [Controlled exception schema](#controlled-exception-schema)

## Canonical placement

In a Resonance project, `.resonance/04_systems.md` holds two explicit layers in
one canonical artifact: the normative architecture constitution and the
descriptive system record. The constitution governs. The system record captures
technologies, topology, workflows, and evidence without turning every current
fact into a permanent constraint. Linked diagrams, ADRs, inventories, and operational
evidence are annexes. They may explain or prove a rule, but may not introduce,
override, or supersede a principle, quality requirement, boundary, canonical
owner, trust zone, contract, target, gate, or exception. Put every normative
rule in `04_systems.md` under a stable ID. On conflict, `04_systems.md` governs.

When an older `04_systems.md` uses the legacy inventory scaffold, upgrade it in
place. Preserve authored content, map it under Current system, add only missing
constitution sections, mark unproven claims `UNVERIFIED`, and keep the baseline
`PROPOSED` until a human approves it. Never overwrite or create a parallel file.

Outside Resonance, apply the same one-authority rule to the project's declared
canonical artifact. Do not impose the Resonance path.

## Required artifact

### Architecture constitution, normative

1. **Authority and scope**
   - purpose, audience, approval role or maintainer group, scope, exclusions, status, version
   - evidence sources and last verified revision
2. **System outcomes and quality attributes**
   - what the system must enable
   - ranked qualities with observable tests or thresholds
3. **Stable principles**
   - short rules with rationale, consequence, and verification method
   - principles describe direction, not current compliance
4. **Decision hierarchy, boundaries, and operating doctrine**
   - ranked trade-offs, trust zones, ownership, dependency and interface rules
   - failure, recovery, security, observability, deployment, and rollback rules
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

### System record, descriptive

1. **Current context and topology**
   - actors, providers, trust boundaries, internal subsystems, and dependencies
   - technologies, execution units, environments, deployment, and rollback path
2. **Current ownership and workflows**
   - canonical data owners, business-rule owners, state machines, and side effects
   - success, invalid, duplicate, concurrent, partial-failure, and recovery paths
3. **Evidence**
   - source paths, schemas, configuration, tests, runtime signals, and runbooks
   - known gaps marked `UNVERIFIED`

A technology in the system record is a current fact. It becomes an architecture
constraint only when the constitution gives it a stable rule, rationale, and
verification method.

## Derive principles from first principles

For each candidate rule, answer:

1. Which system outcome or required quality does it protect?
2. Which recurring failure does it prevent?
3. What concrete decision does it constrain?
4. How can a reviewer detect compliance or violation?
5. Does it stay useful across implementation changes?

Reject a principle when it is a technology preference, duplicates another rule,
cannot guide a decision, or has no verification method.

## Proportional depth

- Keep a small, local, reversible project on the lean current-state baseline.
  Current may equal target. Do not invent future architecture.
- Run `create` before approving the first change that creates a durable boundary
  or makes failure costly to reverse. Signals include canonical data ownership,
  authorization or trust zones, billing, multi-tenancy, async delivery, a
  critical provider, recovery behavior, a second deployable service, or a
  measurable scale or reliability target.
- Run `revise` only when approved intent, a required quality, stable rule,
  ownership, boundary, contract, or exception changes.
- Conforming implementation decisions may stay in annexed ADRs. Update the
  baseline version only when a normative fact changes or is clarified.

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
- approval role or maintainer group, plus approval evidence when active
- violated rule or boundary
- narrow scope
- reason the compliant path is not currently viable
- risk and blast radius
- accountable role, team, or maintainer group
- compensating controls
- evidence and monitoring
- review trigger
- removal condition
- linked replacement plan or decision, when one exists

A date can trigger review. It is not enough by itself as a removal condition.
An exception remains `PROPOSED` until the declared human approval role explicitly
accepts it. The skill may draft and review the exception but cannot accept debt on
that role's behalf.
Public artifacts contain no personal contact details. Keep private escalation
maps in the project's private operating system.
