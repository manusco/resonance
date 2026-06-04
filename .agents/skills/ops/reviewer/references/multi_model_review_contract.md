# Multi-Model Review Contract

> **Goal**: Define the discipline for structured closeout reviews that use a second model (or second pass) to validate code before commit or ship. This is a review contract, not a review tool. It governs how you interpret, verify, and act on structured review output.

## When to Use

- After non-trivial code edits, before final commit or ship.
- When a second-model review pass is explicitly requested.
- When reviewing a local branch or PR branch after fixes.
- As a final closeout check before merging to main.

## The Contract

### 1. Advisory, Not Authoritative

Treat all review output as advisory. Never blindly apply findings. Every finding must be verified by reading the actual code path and adjacent files. A review that recommends a change you apply without understanding is a review you wasted.

### 2. Verify Every Finding

Before accepting a finding:
- Read the real code path the finding references.
- Read adjacent files that interact with the flagged code.
- Read dependency docs, source code, or type definitions when the finding depends on external behavior.
- If you cannot reproduce or verify the concern, reject the finding with a brief reason.

### 3. Reject Aggressively

Reject findings that are:
- **Speculative risks**: "This could theoretically fail if..." without a concrete scenario.
- **Unrealistic edge cases**: Conditions that cannot occur in the current architecture.
- **Broad rewrites**: Suggestions to restructure code that is not part of the current change scope.
- **Over-complications**: Fixes that add more complexity than the bug they address.

The bar for acceptance: "Does this finding describe a real bug, a concrete security risk, or a clear maintainability regression in the code I just changed?"

### 4. Scope to Ownership Boundaries

When an accepted finding reveals a bug class or repeated pattern:
- Inspect the current PR scope for sibling instances of the same bug class.
- Fix the scoped bug class at once when practical.
- Stop at touched surfaces and ownership boundaries. Do not chase the pattern into unrelated code.
- If the bug class extends beyond the current scope, note it as a follow-up, not an in-scope fix.

### 5. Rerun After Fixes

If a review-triggered fix changes code:
1. Rerun focused tests on the changed code.
2. Rerun the structured review on the updated code.
3. Repeat until the review returns no accepted/actionable findings.

Do not skip the rerun. A fix that introduces a new issue is worse than the original finding.

### 6. Security Findings — Concrete Only

Security perspective is always included in a structured review, but it must not cripple legitimate functionality.

Report security findings only when:
- The change creates a concrete, actionable risk (not a theoretical one).
- The change removes an existing safety check.
- The change exposes data that was previously protected.

Do not flag every missing input validation as a security finding. Focus on changes that actually move the security boundary.

### 7. No Nested Reviews

Do not invoke a second reviewer, a reviewer panel, or a built-in review command from inside a review pass. The structured review is:
1. One bundle of changes.
2. One selected review engine.
3. One structured result.
4. One verification pass by the primary agent.

Multi-reviewer panels are opt-in only. Use them when explicitly requested or when risk justifies the extra cost. The primary agent still verifies every accepted finding.

### 8. Completion Criteria

Stop reviewing when:
- The structured review exits successfully with no accepted/actionable findings.
- All accepted findings have been fixed and the rerun is clean.

Do not run an extra review pass just to get a "clean" output, a second opinion, or clearer closeout wording. A successful exit with no actionable findings IS the clean result.

### 9. Rejection Documentation

When rejecting a finding as intentional or not worth fixing:
- Add a brief inline code comment only if it explains a real invariant or ownership decision that future reviewers would need to understand.
- Do not add comments just to document that a review ran. The review output itself is the documentation.

---

## Review Output Interpretation

| Review Output | Interpretation | Action |
|:---|:---|:---|
| Finding references code you changed | Verify against actual code path | Accept or reject with reason |
| Finding references code you did not change | Out of scope | Reject, note as follow-up if valid |
| Finding depends on external behavior | Read dependency docs/types | Accept only if dependency behavior is confirmed |
| Finding is a style preference | Not a bug, not a risk | Reject unless it matches project conventions |
| Finding suggests a broad refactor | Scope exceeds the current change | Reject, log as tech debt if warranted |
| No findings returned | Review is complete | Stop. Do not rerun for a "better" result. |

---

## Patience Protocol

Structured reviews on large bundles can take up to 30 minutes. During a review:
- Treat heartbeat lines (`review still running: ... elapsed=... pid=...`) as healthy progress, not a hang.
- Do not kill a review because it has been quiet for 2-5 minutes.
- Inspect the process only after: missing multiple expected heartbeats, exceeding the 30-minute window, or an obviously failed subprocess.
- Prefer letting the review finish over restarting. Restarted reviews waste the compute already invested.
