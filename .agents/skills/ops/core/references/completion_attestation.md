# Completion Attestation

> **Purpose**: Replace vague "DONE" status with structured evidence. A staff engineer wouldn't accept "Looks good" — they'd ask "Show me the test output."

## When to Use

| Context | Required? |
|:---|:---|
| `/refactor` | ✅ **Required** — Refactors have the highest regression risk |
| `/audit` | ✅ **Required** — Audits must prove coverage, not just list findings |
| `/debug` | ✅ **Required** — Must prove root cause and fix |
| `/test` | ✅ **Required** — Must show what was verified |
| `/build` (feature work) | 📋 Recommended — Helps catch scope drift |
| `/design` | 📋 Recommended |

## The Template

```markdown
## Completion Attestation

**Status**: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

### What Changed
- [List files and functions modified, with one-line description of each change]

### Blast Radius
- [What could break from this change? Name the specific pages, flows, or features affected]
- [If the blast radius is "nothing beyond this file," say so explicitly]

### Verification Evidence
- [Exact commands run and their output summary]
- [Test names that passed/failed]
- [Screenshots if UI was affected]
- [Manual verification steps taken]

### Do Not Change (Preserved Behavior)
- [User-facing behavior that was intentionally kept unchanged]
- [Copy/labels/flow that must not regress]
- [Tests that were updated to match current product intent, with rationale]

### Concerns
- [Side effects or technical debt introduced]
- [Known limitations of this change]
- [Things that should be monitored after deployment]
```

## Status Definitions

| Status | Meaning | Required Evidence |
|:---|:---|:---|
| **DONE** | All steps complete. Verified. | Full attestation with verification evidence |
| **DONE_WITH_CONCERNS** | Completed, but list potential side effects | Full attestation + explicit concern list |
| **BLOCKED** | Cannot proceed | What was tried, what failed, what is needed |
| **NEEDS_CONTEXT** | Missing information to proceed | What exactly is missing, who can provide it |

## Anti-Patterns

- ❌ "DONE" with no verification evidence
- ❌ "Tests pass" without listing which tests
- ❌ Claiming blast radius is zero without checking consumers
- ❌ Omitting the "Do Not Change" section because "nothing changed" (say that explicitly)
