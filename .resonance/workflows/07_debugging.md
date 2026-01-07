# Workflow: Scientific Debugging ("The Surgeon")

**Primary Roles**: `debugger`
**Goal**: Identify Root Cause and fix it without regression.
**Output**: `_repro.ts` script and a fix.

---

## 1. Trigger
User says: "Bug found", "It's broken", or "Fix this error".

## 2. Phase 1: The Reproduction (Role: `debugger`)
**CRITICAL**: Do not touch production code until you have a failing script.

1.  **Isolate**: Create `_repro_issue_[id].ts`.
2.  **Simulate**: Mock the conditions (inputs, state).
3.  **Assert**: The script MUST fail. If it passes, you haven't found the bug.

## 3. Phase 2: The Diagnosis
Use the Scientific Method.

1.  **Hypothesis**: "I think the cache is stale."
2.  **Test**: Disable cache. Run repro. Does it pass?
3.  **Refine**: If no, new hypothesis.

## 4. Phase 3: The Fix & Verify
1.  **Implement Fix**: Change the code.
2.  **Verify**: Run `_repro.ts`. It should now PASS.
3.  **Regression Test**: Add this scenario to the permanent test suite.

## 5. Artifact Generation
Log the RCA in `02_memory.md`.

**Template:**
```markdown
# Incident: [Issue Name]
**Root Cause**: [Explanation]
**Fix**: [Explanation]
**Prevention**: Added `tests/security/issue_101.test.ts` to CI.
```
