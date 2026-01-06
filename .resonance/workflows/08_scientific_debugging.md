# Workflow: Scientific Debugging ("The Lab")

**Primary Role**: `debugger` (Elite Debugger)
**Goal**: Fix bugs using evidence, not guesses. Stop "Vibe Coding".
**Constraint**: You MUST create a reproduction script before fixing anything.

## 1. Trigger
User says: "Fix this error", "It's broken", "Debug this", or "Investigation needed".

## 2. The Golden Rule
**"If you can't reproduce it, you can't fix it."**
Do not touch the production code until you have a failing test case in your hand.

## 3. The Protocol

### Phase 1: Isolation (The Trap)
Before reading the code, write a script that proves the bug exists.
1.  **Analyze the Report**: What input caused the crash?
2.  **Create Repro**: Create `repro_bug.ts` (or .py/.sh) that attempts to trigger the error.
3.  **Run Repro**:
    *   If it passes (no error): **STOP**. You don't understand the bug. Re-read logs.
    *   If it fails (error reproduces): **PROCEED**. You have trapped the bug.

### Phase 2: Root Cause Analysis (The Why)
Don't just patch the symptom. Find the cause.
*   **Trace**: Use `console.log` or a debugger to trace the data flow in the `repro`.
*   **Hypothesis**: "I think X is null because Y failed."
*   **Verify**: Prove your hypothesis.

### Phase 3: The Surgery (The Fix)
Apply the minimal effective change.
*   **Constraint**: Do not refactor unrelated code.
*   **Constraint**: Do not change code style.
*   **Action**: Edit the source file.

### Phase 4: Verification (The Proof)
1.  **Run Repro**: It should now **PASS**.
2.  **Run Regression**: Run `npm test` to ensure you didn't break anything else.

### Phase 5: Cleanup
1.  Delete `repro_bug.ts`.
2.  (Optional) Convert `repro_bug.ts` into a permanent test case in the test suite.

## 4. Artifact Generation
Draft a "Post-Mortem" entry for `docs/bugs/BUG-[date].md` (or just log to `02_memory.md`).

**Template:**
```markdown
# Bug Fix: [Title]
**Date**: [YYYY-MM-DD]
**Root Cause**: [Why it happened]
**The Fix**: [What we changed]
**Prevention**: [How to stop it happening again]
```

## 5. Next Steps
Ask the user: "Bug fixed and verified. Tests passed. Should I **commit the fix**?"
