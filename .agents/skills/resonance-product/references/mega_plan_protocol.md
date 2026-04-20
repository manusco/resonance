# Mega Plan Protocol: Scope & Vision

> **Source**: Integration of the gstack `/plan-ceo-review` framework.
> **Objective**: Rethink the problem, find the 10-star product, challenge premises, and explicitly define the scope mode before writing technical specs.

## 1. Premise Challenge
Before accepting any request, challenge the premise:
1. Is this the right problem to solve? Could a different framing yield a dramatically simpler or more impactful solution?
2. What is the actual user/business outcome? Is the plan the most direct path to that outcome, or is it solving a proxy problem?
3. What would happen if we did nothing?

## 2. Dream State Mapping
Map the trajectory of the feature:
```
[CURRENT STATE] ---> [THIS PLAN'S DELTA] ---> [12-MONTH IDEAL STATE]
```
Ensure the current plan moves *toward* the 12-month ideal, not away from it.

## 3. The 3 Scope Modes
Never passively accept the scope. Pick one of the three postures:

### A. SCOPE EXPANSION (Build the Cathedral)
*   **When to use**: Greenfield features, core product value, user explicitly wants ambition.
*   **Action**: Push scope UP. Ask "what would make this 10x better for 2x the effort?"
*   **Requirements**:
    *   **10x Check**: Define the wildly ambitious version.
    *   **Platonic Ideal**: Define the perfect user experience if engineering constraints didn't exist.
    *   **Delight Opps**: Find 3-5 small features (<30 mins) that show high craftsmanship.

### B. HOLD SCOPE (Maximum Rigor)
*   **When to use**: Bug fixes, refactors, standard feature additions.
*   **Action**: Accept the scope boundaries, but make the execution bulletproof.
*   **Requirements**:
    *   **Complexity Check**: Can we achieve the same goal with fewer files/classes?
    *   **Temporal Interrogation**: What ambiguities will the implementer hit in Hour 1 vs Hour 6? Solve them *now*.

### C. SCOPE REDUCTION (The Surgeon)
*   **When to use**: Massive PRs, overly complex proposals, "nice-to-have" sprawling requests.
*   **Action**: Strip the plan to its absolute essentials. Cut ruthlessly.
*   **Requirements**:
    *   **Ruthless Cut**: What is the absolute bare minimum that ships value? Defer everything else.

## 4. Execution Rule
**Once a mode is chosen, COMMIT.** Do not silently drift. If EXPANSION is chosen, do not argue for less work later. If REDUCTION is chosen, do not sneak scope back in.
