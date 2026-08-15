# Adoption Verdict Protocol: adopt, trial, hold, or reject

For a named external candidate ("should we adopt Biome?", "migrate to X?", "replace Y with Z?"). This forms a decisive, project-grounded verdict, not a neutral explainer. `ops/second-opinion` reviews a diff, `grill` stress-tests a plan you already mean to build, and an ADR records a choice after the fact; none of them forms the graded verdict on whether to take the thing on in the first place.

## The floor: earn the verdict against this project

Do not issue a verdict you did not earn against the project's own context. A web summary of the candidate is not a verdict. Read how this codebase would actually use it: the integration surface, what it replaces, the migration cost, the team's constraints. A verdict with no project grounding is an explainer wearing a verdict's clothes.

## Size the analysis by reversibility

The depth of the analysis is set by how hard the decision is to undo, not by how interesting the candidate is:

- **Two-way door** (cheap to reverse: a formatter, a lint rule, a dev dependency): decide fast, trial in a branch, move on. Over-analyzing a reversible call is its own waste.
- **One-way bounded** (reversible at a known, bounded cost: a testing library, a state manager): weigh the migration cost explicitly, and name the exit before you enter.
- **One-way high-stakes** (a database, a language, a core framework, an auth provider): full rigor. Failure modes, lock-in, the cost of being wrong, and one independent decision review through `ops/second-opinion --mode decision`.

## The verdict

State one of four, with the reason and the reversibility tier that sized the call:

- **Adopt**: take it on now. Name what it replaces and the migration path.
- **Trial**: adopt in a bounded scope with an exit criterion and a date to decide.
- **Hold**: not now, but not no. Name the signal that would change the answer.
- **Reject**: no. Name the disqualifier, so the question does not reopen without new evidence.
