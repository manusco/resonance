# 04 Systems: Architecture Constitution and System Record

> **Authority:** `.resonance/04_systems.md` is the sole normative architecture
> baseline for a Resonance project. It contains two distinct layers in one
> place: the architecture constitution states what must remain true, and the
> system record states what currently exists. Linked ADRs, diagrams,
> inventories, and runbooks are supporting evidence. They may not introduce,
> override, or supersede a principle, quality requirement, boundary, owner,
> contract, gate, target, or exception.

- **Status:** PROPOSED
- **Architecture version:** [Version]
- **Approval role or maintainer group:** [Role or group, no personal contact details]
- **Approval evidence:** [PR, decision ID, signed record, or UNAPPROVED]
- **Last verified repository revision:** [Commit, tag, or UNVERIFIED]
- **Scope:** [Systems and decisions governed here]
- **Exclusions:** [Explicitly out of scope]

## How to use this file

- Read **Part I** as law. Normative statements use `must`, `must not`, or a
  stable `SYS-###` rule. A slogan, preference, or undocumented convention is
  not an architecture rule.
- Read **Part II** as evidence. It records technologies, deployment topology,
  providers, workflows, and known gaps. A current implementation fact becomes
  mandatory only when Part I names it as a rule.
- When reality violates Part I, do not rewrite the rule to make the code pass.
  Record the gap or a proposed exception, then choose whether to correct the
  system or approve a constitution change.
- Before every `/build`, screen the approved plan against the conformance
  triggers in Section 10. If a trigger applies, run `/blueprint check` against
  the approved architecture version before writing code. If no trigger applies,
  record that the architecture gate is not applicable and continue.
- Run `/blueprint create` before approving the first change that creates a
  durable boundary or makes failure costly to reverse. Triggers include
  canonical data ownership, authorization or trust zones, billing,
  multi-tenancy, async delivery, a critical external provider, recovery
  behavior, a second deployable service, or a measurable scale or reliability
  target.

Delete prompts that do not apply, but do not omit a material concern. Mark an
unknown fact `UNVERIFIED` and an undecided rule `UNRESOLVED`. Never invent a
target, threshold, or requirement to fill the template.

# Part I: Architecture constitution

This part defines the durable principles and constraints used to judge plans,
changes, and releases. Keep it technology-independent unless a technology
choice is itself an approved, decision-relevant constraint.

## 1. Purpose, outcomes, and non-goals

- **System purpose:** [Why this system exists]
- **Primary users or dependants:** [Roles or systems, not personal details]
- **Required outcomes:**
  1. [Observable outcome]
- **Non-goals:**
  - [Outcome or capability this architecture does not optimize for]
### Hard constraints

| Rule ID | Constraint | Why it is binding | Accountable role or group | Verification |
| :--- | :--- | :--- | :--- | :--- |
| SYS-### | [Regulatory, contractual, operational, budget, or compatibility constraint] | [Source of authority] | [Role or group] | [Evidence] |

## 2. Decision hierarchy and trade-offs

Rank the concerns that resolve architecture conflicts. A lower-ranked concern
does not defeat a higher-ranked one without an approved exception. Do not copy a
generic ranking when the product requires a different one.

| Rule ID | Rank | Concern | Decision rule | Accountable role or group | Evidence that justifies an exception |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SYS-### | 1 | [Concern] | [What wins when concerns conflict] | [Role or group] | [Required evidence] |

## 3. Principles and invariants

A principle must protect an outcome, constrain a real decision, survive an
implementation change, and be testable by a reviewer. Put implementation
preferences and local coding rules elsewhere.

| Rule ID | Normative rule | Outcome or failure protected | Scope | Accountable role or group | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SYS-001 | [The system must or must not...] | [Why this rule exists] | [Where it applies] | [Role or group] | [How a change proves conformance] |

## 4. Required qualities and budgets

Record only qualities that can change an architecture decision. Give each one an
observable threshold, test, or budget. Use `UNRESOLVED` when the project has not
approved a value and `NOT_APPLICABLE` with a reason when a concern does not
apply.

| Rule ID | Quality or budget | Required level and operating conditions | Accountable role or group | Measurement and evidence | Failure response |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SYS-### | [Availability, latency, capacity, durability, recovery, privacy, accessibility, cost, or another material quality] | [Threshold and conditions] | [Role or group] | [Test, metric, or inspection] | [Degrade, block, recover, or escalate] |

## 5. Boundaries, ownership, and dependency rules

### Trust and authorization boundaries

| Rule ID | Boundary or trust zone | Allowed entry | Forbidden crossing | Accountable role or group | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SYS-### | [Boundary] | [Authenticated and authorized path] | [What must never cross] | [Role or group] | [Test or control] |

### Canonical data and business-rule ownership

| Rule ID | Data, decision, transition, or side effect | Canonical owner | Allowed writers or initiators | Read or notification contract | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SYS-### | [Owned concern] | [Subsystem or role] | [Named operations] | [Contract] | [Test or evidence] |

### Dependency and interface rules

| Rule ID | Caller -> owner | Named operation or contract | Compatibility rule | Failure semantics | Accountable role or group | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SYS-### | [Boundary crossing] | [Operation, event, or schema] | [Versioning or migration rule] | [Timeout, retry, rejection, or partial success] | [Role or group] | [Contract test or evidence] |

## 6. Failure, recovery, security, and operational doctrine

State the system-wide rules that implementations must preserve. Every material
rule needs a stable ID, accountable role or group, and verification. Delete an
inapplicable row only after recording why the concern does not apply.

| Rule ID | Concern | Normative rule | Accountable role or group | Verification |
| :--- | :--- | :--- | :--- | :--- |
| SYS-### | Success and failure semantics | [Define acceptance, partial success, business completion, and failure] | [Role or group] | [Test or evidence] |
| SYS-### | Idempotency and concurrency | [Define duplicate, replay, ordering, and conflict behavior] | [Role or group] | [Test or evidence] |
| SYS-### | Timeout, retry, and reconciliation | [Define retry ownership, limits, backoff, and repair] | [Role or group] | [Test or evidence] |
| SYS-### | Degraded operation | [Define what remains available and what fails closed] | [Role or group] | [Test or evidence] |
| SYS-### | Data protection | [Define classification, retention, deletion, encryption, and secret boundaries] | [Role or group] | [Control or evidence] |
| SYS-### | Auditability and observability | [Define durable decision evidence and runtime signals] | [Role or group] | [Signal or inspection] |
| SYS-### | Recovery and continuity | [Define backup, restore, RPO, RTO, and recovery proof] | [Role or group] | [Exercise or evidence] |
| SYS-### | Deployment and rollback | [Define compatibility, migration, release, and rollback invariants] | [Role or group] | [Deployment proof] |

## 7. Approved target and evolution doctrine

- **Current state equals approved target:** Yes | No | UNRESOLVED
- **Target summary:** [The smallest approved architectural direction, or current state]
- **Evolution rules:** [How change stays reversible, compatible, and observable]

Do not design speculative future machinery. When current and target differ,
record only evidenced gaps and the smallest safe transitions.

| Gap | Violated or target rule IDs | Keep / constrain / migrate / replace / remove | Smallest safe transition | Verification and rollback |
| :--- | :--- | :--- | :--- | :--- |
| [Gap] | [SYS-IDs] | [Disposition] | [Reversible slice] | [Proof and rollback] |

# Part II: System record

This part describes the system that exists at the verified revision. Facts here
do not become policy by repetition. Cite source paths, schemas, configuration,
tests, runtime evidence, or operator procedures. Mark gaps `UNVERIFIED`.

## 8. Current system map

### Five-minute orientation

- **System context view:** [Inline context/container view or annex path, with
  actors, system boundary, deployable units, stores, and external providers]
- **One-paragraph system summary:** [How the parts work together and where the
  highest-risk boundary sits]

### Domain vocabulary

When domain terms cross subsystem or team boundaries, add a bounded-context map
to the context view and state which context owns each meaning.

| Term | Exact meaning in this system | Canonical owner or source | Common ambiguity to avoid |
| :--- | :--- | :--- | :--- |
| [Term] | [Meaning] | [Owner, schema, or rule] | [What this term does not mean] |

### Context and external systems

| External system or actor | Purpose | Data exchanged | Trust or authentication boundary | Failure dependency | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [System or role] | [Purpose] | [Data] | [Boundary] | [Effect of failure] | [Source or runtime evidence] |

### Internal subsystems and technology

| Subsystem | Responsibility | Technology | Deployed or executed as | Source or configuration | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Subsystem] | [Owned responsibility] | [Runtime, framework, or store] | [Process, service, job, library, or client] | [Path] | [Dependencies] |

### Deployment and environments

| Environment | Runtime and region | Entry points | Configuration and secrets | Data stores | Release and rollback path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Environment] | [Runtime fact] | [Ingress] | [Mechanism, no secret values] | [Stores] | [Procedure] |

### Current data and business-rule ownership

| Data, decision, transition, or side effect | Current owner | Write path | Readers or consumers | Persistence or delivery guarantee | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Owned concern] | [Subsystem] | [Operation] | [Consumers] | [Guarantee] | [Schema, code, test, or runtime evidence] |

## 9. Critical workflows and failure paths

For each material workflow, trace the user or system trigger through the
canonical decision, writes, side effects, and observable completion. Keep
provider acceptance, queueing, delivery, settlement, and business completion as
separate facts unless the contract proves they are the same.

### [Workflow name]

1. **Trigger:** [Actor, precondition, and entry point]
2. **Decision owner:** [Subsystem and named operation]
3. **State changes:** [Canonical writes and transitions]
4. **Side effects:** [Events, messages, provider calls, or user-visible effects]
5. **Completion evidence:** [What proves business completion]
6. **Invalid or unauthorized path:** [Rejection behavior]
7. **Duplicate or concurrent path:** [Conflict and idempotency behavior]
8. **Dependency or partial-failure path:** [Timeout, retry, compensation, and reconciliation]
9. **Recovery path:** [Operator or automated repair and proof]

## 10. Decisions, exceptions, conformance, and evidence

### Constitution-changing decisions

- [Decision ID, affected rule IDs, status, approval evidence, and supersession]

Implementation decisions that conform to this constitution may stay in linked
ADRs. A decision that changes or clarifies a principle, quality requirement,
boundary, canonical owner, trust zone, cross-system contract, target, gate, or
exception must update this file and its architecture version in the same
approved change.

### Active exceptions

| Exception | Violated rule | Scope and risk | Accountable role or group | Controls and monitoring | Review trigger | Removal condition | Status and approval evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [EXC-ID] | [SYS-ID] | [Scope and blast radius] | [Role or group] | [Controls] | [Evidence-based trigger] | [Exit condition] | PROPOSED |

An exception remains `PROPOSED` until the declared human approval role or group
accepts it and records approval evidence. An agent may draft or review an
exception. It may not accept architecture debt on that role's behalf.

### Conformance triggers

Screen every approved implementation plan before `/build`. Run a full
`/blueprint check` when the plan, diff, PR, or release changes or depends on:

- a `SYS-###` rule or required quality;
- canonical data or business-rule ownership;
- a trust zone, authorization path, privacy boundary, or retention rule;
- a cross-system contract, provider, event, queue, or side effect;
- a state transition, failure semantic, retry, reconciliation, or recovery path;
- deployment topology, migration compatibility, rollback, scale, reliability,
  or an active exception.

Routine copy, styling, tests that preserve behavior, and local implementation
changes need only the applicability screen. Record `not applicable` with the
reason instead of manufacturing a conformance review.

### Annex index

| Path | Non-normative purpose | Last verified revision | Related rule IDs |
| :--- | :--- | :--- | :--- |
| [Path] | [Evidence, diagram, inventory, ADR, or rationale] | [Revision] | [SYS-IDs] |

### Evidence gaps

- [UNVERIFIED fact, risk created by uncertainty, and evidence needed]

### Change policy

- **Who may approve revisions:** [Role or maintainer group]
- **What records valid approval evidence:** [Repository-visible mechanism]
- **What requires an architecture version update:** [Normative changes]
- **Evidence required to approve a principle change:** [Evidence]
- **Review cadence or event trigger:** [Trigger based on system change or risk]
