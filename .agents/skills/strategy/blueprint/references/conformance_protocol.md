# Conformance protocol

Use this protocol to check a proposed plan, implementation, PR, or release against
an approved architecture blueprint.

## Pin the baseline

Record the blueprint path, `APPROVED` status, version, approval evidence, and
last verified revision before tracing the change. Also record the checked
subject's path or identifier plus its exact commit, revision, or content digest.
If either artifact is missing, unapproved, or cannot be identified reproducibly,
stop and return `NEEDS_CONTEXT`; do not issue a conformance verdict. A verdict is
invalid after the checked subject changes.

In a Resonance project, derive normative rules only from
Part I of `.resonance/04_systems.md`. Part II and annexes provide evidence and
rationale. A current technology or topology fact is not a constraint unless
Part I gives it a stable normative rule. If Part II, an annex, ADR, plan, or
change introduces an architectural constraint that is absent from Part I,
return `NON_CONFORMING` until the same approved change updates the relevant
stable rule and architecture version.

## Trace the change

1. Identify the user-visible and operational outcomes.
2. List changed boundaries, dependencies, contracts, stores, trust zones, and
   external providers.
3. Trace each affected business decision, canonical write, state transition, and
   side effect to its accountable owner.
4. Walk success, empty, invalid, duplicate, concurrent, dependency-failure,
   partial-success, retry, and recovery paths where applicable.
5. Compare the evidence to the applicable blueprint rules, decisions, and active
   exceptions.
6. Check whether tests and runtime signals can prove the claimed behavior.

## Finding record

Each finding contains:

- violated rule or contract
- project-wide audit category
- evidence location
- observed behavior
- consequence and blast radius
- severity
- smallest safe correction
- required verification
- exception eligibility, if any

Use the project-wide seven-category taxonomy and P0-P3 severity ladder linked
from the skill. Do not create local categories, severity labels, or mappings.
Rank by user harm and system risk before maintainability or documentation drift.

## Verdicts

- `CONFORMING`: no unresolved violation. Verification evidence is sufficient.
- `CONFORMING_WITH_EXCEPTIONS`: every violation has an approved, active, scoped
  exception with recorded human approval evidence, and its controls are present.
  List all accepted debt.
- `NON_CONFORMING`: one or more violations lack an approved exception, a required
  invariant is unverified, or evidence is insufficient for the requested gate.

Never average findings into a passing score. One blocking boundary failure is a
non-conforming result.

## Lifecycle gates

- **Frame:** name affected boundaries, owners, decisions, and likely exceptions.
- **Plan:** show target alignment, transition state, compatibility, rollback, and
  verification.
- **Review:** compare the concrete diff and tests to the plan and blueprint.
- **Release:** prove deployment invariants, runtime configuration, recovery, and
  active exception controls.

Before `/build`, screen every approved plan for applicability. When the plan
touches a normative rule, required quality, owner, boundary, contract, trust
zone, failure or recovery path, deployment invariant, or active exception, run
the full plan gate and require a passing verdict. Otherwise record `not
applicable` with the reason and continue without manufacturing findings.

Only make a gate machine-blocking when the project defines a deterministic check
and explicitly adopts it. Otherwise return an advisory verdict with evidence.
Routine copy, styling, and local implementation changes that touch no applicable
architecture rule do not require a blueprint check.
