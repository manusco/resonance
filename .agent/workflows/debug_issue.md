---
description: Identify Root Cause and fix bugs using the Scientific Method.
---

# Workflow: Debug Issue ("The Surgeon")

**Trigger**: User says "Bug found", "It's broken", or "Fix this".
**Context**: You need to fix a bug without breaking anything else.

## 1. The Setup (Isolation)
- [ ] **Stop**: Do not touch production code.
- [ ] **Check State**: Read `.resonance/01_state.md`.
- [ ] **Environment**: Ensure you are on a clean git branch `fix/[issue-id]`.

## 2. The Reproduction (The Scientist)
*Activate Skill*: `resonance-debugger`

- [ ] **Create Script**: Create `_repro_issue_[id].ts` (or equivalent).
- [ ] **Fail**: Run the script. It MUST fail. IF it passes, you have not reproduced the bug.
- [ ] **Commit**: `git commit -m "repro: add failing test case"`

## 3. The Diagnosis (The Detective)
*Activate Skill*: `resonance-debugger`

- [ ] **Hypothesize**: Write down 3 possible causes in `02_memory.md`.
- [ ] **Investigate**: Use `git bisect` if it's a regression. Use `console.log` tracing.
- [ ] **Locate**: Pinpoint the exact line and variable causing the issue.

## 4. The Fix (The Surgeon)
*Activate Skill*: `resonance-backend` / `resonance-frontend`

- [ ] **Implement**: Modify the code.
- [ ] **Verify**: Run `_repro.ts`. It MUST now pass.
- [ ] **Regression Test**: Run the full test suite. Make sure nothing else broke.

## 5. The Autopsy (Learning)
- [ ] **Clean**: Delete `_repro.ts` OR better, integrate it into `src/tests`.
- [ ] **Record**: Update `02_memory.md` with the Root Cause Analysis (RCA).
- [ ] **Push**: Submit PR.
