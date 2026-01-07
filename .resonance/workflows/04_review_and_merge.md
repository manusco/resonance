# Workflow: Review & Merge ("The Gatekeeper")

**Primary Roles**: `reviewer`, `qa`
**Goal**: Ensure code meets **Google Engineering Standards** before merging.
**Output**: A Merged PR or a "Request for Changes".

---

## 1. Trigger
User says: "Review this", "Can I merge?", or "Check my code".

## 2. Phase 1: The Automaton Check (Role: `qa`)
Before looking at semantics, check syntax and safety.

1.  **Lint**: `npm run lint` (Must pass).
2.  **Types**: `tsc --noEmit` (Must pass).
3.  **Tests**: `npm test` (Must pass).
4.  **Security**: `npm audit` (No criticals).

## 3. Phase 2: The Semantic Review (Role: `reviewer`)
Read the code *as if you have to maintain it forever*.

### Checklist:
*   [ ] **Correctness**: Does it actually solve the User Story?
*   [ ] **Readability**: Are variable names descriptive? (No `data`, `item`, `x`).
*   [ ] **Complexity**: Are functions < 20 lines? Are there deep nestings?
*   [ ] **Architecture**: Does it violate boundaries? (e.g., UI touching DB).

## 4. Phase 3: The Merge
If all pass:
1.  **Squash & Merge**: One commit per feature.
2.  **Clean Up**: Delete feature branch.
3.  **Update State**: Mark task as `[x]` in `task.md` or `implementation_plan.md`.

## 5. Artifact Generation
(Optional) **Review Note** in `02_memory.md` if a major anti-pattern was caught.

**Template:**
```markdown
# Code Review: [Feature]
**Status**: APPROVED / BLOCKED

**Findings**:
- ✅ Logic isolated in `UseCases`.
- ❌ Security risk in SQL concatenation (See `security.md`).
```
