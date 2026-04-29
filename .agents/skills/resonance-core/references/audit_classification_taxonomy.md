# Audit Classification Taxonomy

> **Purpose**: Every audit, review, and report in Resonance uses this taxonomy. It ensures findings are classified by *what they affect*, then ranked by *how much harm they cause*.

## 1. The 7-Category Taxonomy

Every finding belongs to exactly one category. Categories are ordered by risk priority — address earlier categories before later ones.

### A. Product Correctness

Does the system behave according to intended user-facing rules?

| Signal | Example |
|:---|:---|
| Wrong access for the wrong user type | An "editor" can delete users |
| Wrong redirect behavior | Login redirects to 404 instead of dashboard |
| Invalid workflow sequencing | Payment collected before terms accepted |
| Stale tests forcing product regressions | Test asserts old copy, dev changes product to match |
| Interface copy mismatching behavior | Button says "Free Trial" but triggers paid checkout |

### B. Runtime Safety

Can the system crash, corrupt state, or expose wrong data under normal or edge-case operation?

| Signal | Example |
|:---|:---|
| Login crashes on malformed session | `null.user_id` when cookie is stale |
| Missing-schema crashes | Migration not run on preview; query hits nonexistent table |
| Unhandled null/undefined paths | Profile page crashes when user has no avatar |
| Hidden data-shape assumptions | Code assumes `settings` is always an object, but legacy rows store `null` |
| Bad fallback behavior | Error handler shows raw stack trace to user |

### C. Authorization Integrity

Are identity and permissions modeled clearly and enforced consistently across all layers?

| Signal | Example |
|:---|:---|
| Role labels used as permission checks | `if (user.role === 'admin')` scattered across 30 files |
| Inconsistent access logic | Route allows access, but policy blocks it (or vice versa) |
| Inherited privileges are implicit | "Managers" inherit "Editor" permissions by convention, not code |
| Restricted users seeing forbidden sections | Menu hidden, but direct URL access works |
| Navigation treated as authorization | Hiding a sidebar link but not protecting the route/resource |

**The 6-Layer Authorization Model:**

Every authorization finding must specify *which layer* is affected:

1. **Menu/Navigation Visibility** — Can the user *see* the link?
2. **Page/View Access** — Can the user *load* the page?
3. **Route Access** — Does the HTTP route allow the request?
4. **Policy Enforcement** — Does the domain policy authorize the action?
5. **Resource Access** — Can the user read/write this specific record?
6. **Action/Button Availability** — Can the user *trigger* this specific operation?

> 🔴 **Rule**: A finding at one layer does NOT imply coverage at other layers. Audit each independently.

### D. Data Integrity

Is the same business rule, mapping, or transformation implemented in exactly one place?

| Signal | Example |
|:---|:---|
| Duplicated persistence mapping | Same field mapped in Eloquent model AND raw SQL query |
| Parallel transformation logic | Price calculation in both frontend JS and backend PHP |
| Same domain rule in multiple layers | "Active subscription" defined differently in policy vs. view vs. API |
| Silent drift risk | Adding a new field requires changes in 4 files; one will be missed |

### E. Environment Robustness

Does the system assume ideal conditions that may not exist on preview, staging, or production?

| Signal | Example |
|:---|:---|
| Optional tables may be missing | Migration not yet run on preview environment |
| Production data differs from test fixtures | Legacy user records have `null` where tests assume a value |
| Preview data is incomplete | Seed data only covers happy path; edge users don't exist |
| Deploy environment differs from local | Local uses SQLite, production uses Postgres (query syntax diverges) |
| Config assumes specific OS/path | Hardcoded `/tmp/` path fails on Windows |

### F. Verification Quality

Do tests actually cover critical behavior and failure modes?

| Signal | Example |
|:---|:---|
| Green suite but missing critical path tests | No test for "what happens when payment fails" |
| Tests check implementation, not behavior | Asserts internal method was called, not that user sees confirmation |
| Stale tests encode old product decisions | Test asserts "Sign Up" button text, but product changed to "Get Started" |
| Error handlers are untested | `catch` block exists but no test exercises it |
| Assertions are too weak | `expect(response.status).toBe(200)` without checking body/redirect/state |

### G. Maintainability

Structural quality that affects the team's ability to change the code safely. **Address only after A–F are clear.**

| Signal | Example |
|:---|:---|
| High cyclomatic complexity | 200-line method with 8 nested conditionals |
| Mixed responsibilities | Controller handles validation, business logic, AND formatting |
| Poor naming | `handleStuff()`, `data2`, `processIt()` |
| Dead code | Unused imports, commented-out blocks, unreachable branches |
| Style inconsistency | Tabs in one file, spaces in another |

---

## 2. Severity Ranking (P0–P3)

Within each category, rank findings by harm potential:

### P0 — Critical (Stop-Ship)

The system is actively broken, insecure, or corrupting data.

- Auth bypass (any user can access admin)
- Data leak (PII exposed to wrong user)
- Corruption risk (concurrent writes with no locking)
- Crash on critical path (login, checkout, signup)
- Broken deployment safety (no rollback possible)

### P1 — High (Fix Before Next Release)

The system works but has dangerous ambiguity or missing safety nets.

- Authorization model is inconsistent across layers
- Duplicated business rule that can silently drift when fields are added
- Critical workflow has zero test coverage
- Unsupported product claims with business/legal risk
- Environment-sensitive crash (works locally, fails on staging)

### P2 — Medium (Fix Within Sprint)

The system is safe but harder to maintain or slower than it should be.

- Complexity hotspot (high cyclomatic complexity in critical path)
- Brittle tests (pass today, break on unrelated changes)
- Heavy coupling between unrelated modules
- Avoidable performance overhead (N+1 queries, full table scans)

### P3 — Low (Backlog)

Quality issues that don't affect users or safety.

- Style drift (inconsistent formatting)
- Minor naming improvements
- Low-impact code organization
- Documentation gaps in non-critical areas

> 🔴 **Rule**: A report that leads with P3 findings while P0 or P1 findings exist is a **weak report**. Always rank by harm, not by how impressive the finding sounds.

---

## 3. Standard Report Template

Every audit-type report should output findings in this structure:

```markdown
## 1. Behavioral Risks (Product Correctness)
What user-visible or workflow-critical behavior is wrong or fragile?

## 2. Authorization Risks
Where identity and access are mixed, duplicated, or inconsistently enforced.

## 3. Data Truth Risks
Where mappings, transformations, or rules are duplicated across layers.

## 4. Environment Risks
What assumptions may fail outside ideal local development conditions.

## 5. Verification Gaps
What critical paths or failure paths are currently untested.

## 6. Performance Risks
What structurally slows down the user experience.

## 7. Maintainability Risks
What complexity or coupling should be simplified — after behavior is safe.

## 8. Do Not Change
Explicit list of user-facing behavior, copy, and flow that must not be altered
without explicit approval. Prevents regression from overzealous fixing.

## 9. Recommended Sequence
A safe order of operations:
1. Reproduce the issue
2. Lock current behavior with tests
3. Centralize duplicated truth
4. Simplify boundaries
5. Run full verification
6. Style/formatting cleanup last
```

---

## 4. Required Questions

Every report must answer these questions. If the answer is "Not applicable," say so explicitly — do not skip silently.

### Product
- What intended behavior must not change?
- Are any failing tests stale relative to current product truth?
- Did anyone change copy/flow just to satisfy tests?

### Auth / Access
- Who is allowed to do what?
- Where is that encoded? (Route? Policy? Template? Database?)
- Is the rule explicit or inferred from a role label?
- Is the rule enforced consistently across all 6 layers?

### Data
- Where is the single source of truth for each business rule?
- Is any mapping, validation, or transformation duplicated?
- What breaks if a new field is added tomorrow?

### Environment
- What assumptions exist about schema, config, or data shape?
- What happens if those assumptions are false?
- Has this been tested on a non-local environment?

### Tests
- What critical behavior is not covered?
- What failure path is not covered?
- Which assertions are too implementation-specific to survive a refactor?

### UX / Copy
- Is the visible experience correct and consistent?
- Are there unsupported claims or fabricated attributions?
- Is wording promising functionality the product does not actually support?

---

## 5. Report Anti-Patterns

A strong report **never** does these things:

| Anti-Pattern | Why It's Wrong |
|:---|:---|
| Vague "God class" rhetoric without naming the business consequence | Doesn't tell the reader what actually breaks |
| Generic SOLID/DRY preaching without a concrete risk | Academic, not actionable |
| Style issues ranked above runtime or access issues | Wrong priority; undermines trust in the report |
| Recommending abstractions before naming the current failure mode | Solving a problem that hasn't been proven to exist |
| Conflating menu visibility with authorization | Navigation is not security |
| Assuming green tests means the system is safe | Tests can be incomplete, stale, or wrong |
| Assuming failing tests means the product is wrong | Sometimes the test is stale |
| Suggesting copy that introduces unsupported claims | Trading one problem for another |
| Praising "consistency" when it flattens a stronger interface | Consistency for its own sake can reduce quality |
| Using adjectives instead of evidence | "Robust auth" vs "Auth checked at route, policy, and resource layers" |
