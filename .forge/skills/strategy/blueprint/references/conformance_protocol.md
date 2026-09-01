# Conformance protocol

Use this protocol to check a proposed plan, implementation, PR, or release against
an approved architecture blueprint.

## Trace the change

1. Identify the user-visible and operational outcomes.
2. List changed boundaries, dependencies, contracts, stores, trust zones, and
   external providers.
3. Trace each affected business decision, canonical write, state transition, and
   side effect to its named owner.
4. Walk success, empty, invalid, duplicate, concurrent, dependency-failure,
   partial-success, retry, and recovery paths where applicable.
5. Compare the evidence to the applicable blueprint rules, decisions, and active
   exceptions.
6. Check whether tests and runtime signals can prove the claimed behavior.

## Finding record

Each finding contains:

- violated rule or contract
- evidence location
- observed behavior
- consequence and blast radius
- severity
- smallest safe correction
- required verification
- exception eligibility, if any

Rank severity by consequence:

- **BLOCKER:** breaks a protected boundary or invariant and can cause unauthorized
  access, data loss, incorrect irreversible action, unsafe deployment, or loss of
  recovery.
- **HIGH:** creates duplicated authority, hidden coupling, ambiguous state, or a
  material failure path likely to spread.
- **MEDIUM:** increases change cost or weakens verification within a bounded area.
- **LOW:** local drift with limited consequence and a clear correction.

## Verdicts

- `CONFORMING`: no unresolved violation. Verification evidence is sufficient.
- `CONFORMING_WITH_EXCEPTIONS`: every violation has an approved, active, scoped
  exception and its controls are present. List all accepted debt.
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

Only make a gate machine-blocking when the project defines a deterministic check
and explicitly adopts it. Otherwise return an advisory verdict with evidence.
