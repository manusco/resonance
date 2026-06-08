# Universal Audit Directives

> **Purpose**: These 8 directives are constitutional rules for every Resonance agent that produces reports, writes tests, or modifies code. They override stylistic preference whenever there is a conflict.

## Contents

- [1. Authorization Directive](#1-authorization-directive)
- [2. Verification Directive](#2-verification-directive)
- [3. Product Integrity Directive](#3-product-integrity-directive)
- [4. Environment Robustness Directive](#4-environment-robustness-directive)
- [5. Report Prioritization Directive](#5-report-prioritization-directive)
- [6. Copy/Trust Directive](#6-copytrust-directive)
- [7. Refactor Directive](#7-refactor-directive)
- [8. Test Quality Directive](#8-test-quality-directive)

---

## 1. Authorization Directive

**Rule**: Model identity and permissions separately. Roles describe *who* a user is. Capabilities describe *what* a user can access.

**Example**: Instead of `if (user.role === 'editor')` scattered across routes, policies, and templates, define a capability like `can('publish-articles')` and check it once per layer.

**Anti-Pattern**: Role checks (`isAdmin()`, `hasRole('manager')`) used directly as permission logic in 30+ locations. This is permission-model drift — when you add a new role, you must find and update every check.

**Deliverable**: When auditing authorization, produce a **Capability Matrix**:

| Capability | Admin | Editor | Viewer | Enforced At |
|:---|:---|:---|:---|:---|
| View dashboard | ✅ | ✅ | ✅ | Route, Policy |
| Edit articles | ✅ | ✅ | ❌ | Policy, Resource |
| Delete users | ✅ | ❌ | ❌ | Route only ⚠️ |

---

## 2. Verification Directive

**Rule**: Do not accept "tests pass" as sufficient verification. Check whether critical success paths, failure paths, unauthorized paths, malformed-data paths, and environment-sensitive paths are all covered.

**Example**: A checkout flow has 15 tests — all for happy path. Zero tests for: expired card, network timeout, duplicate submission, unauthorized user accessing another user's cart. The suite is green. The system is unsafe.

**Anti-Pattern**: Treating test coverage percentage as proof of safety. 95% coverage can still miss the one path that handles payment failure.

---

## 3. Product Integrity Directive

**Rule**: Do not recommend changing user-facing behavior, copy, labels, or flow solely to satisfy stale tests or architectural preference. If product intent and tests diverge, flag the divergence explicitly.

**Example**: A test asserts the submit button says "Sign Up." The product team changed it to "Get Started" last sprint. The test fails. The correct action is to **update the test**, not revert the button text.

**Anti-Pattern**: Changing production copy to make a test pass without checking whether the copy change was intentional.

---

## 4. Environment Robustness Directive

**Rule**: Assume preview, staging, and production environments may have partial schema, legacy data, or incomplete records. Audit code paths for graceful degradation under imperfect conditions.

**Example**: A feature uses a `settings` JSON column added in migration #47. Preview hasn't run that migration. The feature crashes with `Column not found`. The code should check for the column's existence or handle `null` gracefully.

**Anti-Pattern**: "Works on my machine" as a defense. If the code doesn't handle a missing optional dependency, it's not environment-robust.

**Checklist**:
- [ ] What happens if an optional table/column is missing?
- [ ] What happens if a config value is unset or empty?
- [ ] What happens if production data has legacy/null values where code expects a value?
- [ ] What happens if a background job's prerequisite data is only partially available?
- [ ] What happens if the user record is unusual but technically valid?

---

## 5. Report Prioritization Directive

**Rule**: Rank findings by user harm and system risk first, then by maintainability, then by style. Never lead with formatting or architectural commentary when auth, crash, or data-flow risks exist.

**Example**: A report has 3 findings: (1) SQL injection in search endpoint, (2) God class in UserService, (3) inconsistent indentation. The report must lead with #1. If it leads with #2 or #3, it is a weak report.

**Anti-Pattern**: Reports that spend 2 pages on "clean architecture" recommendations while a broken auth check sits in a footnote.

---

## 6. Copy/Trust Directive

**Rule**: Reject fabricated quotes, unsupported testimonials, invented metrics, and promises not backed by actual product behavior. Prefer concrete, verifiable statements over persuasive filler.

**Example**:
- ❌ `"This changed my life" — Sarah K., CEO` (unverifiable, possibly fabricated)
- ✅ `"Reduced our deploy time from 45 minutes to 3 minutes" — Sarah Kim, CTO at Acme (case study link)`

**Anti-Pattern**: Generating social proof to fill a template. If the proof doesn't exist, leave the section empty and note it as a gap — don't invent it.

**What To Flag**:
- Fabricated testimonial quotes with generic names
- Metrics without source or methodology ("500% faster")
- Trust badges for certifications the company doesn't hold
- Screenshots that don't match the actual product UI
- Feature claims for capabilities that aren't implemented

---

## 7. Refactor Directive

**Rule**: Every refactor must identify the exact unsafe business rule or drift risk it addresses. Prefer the smallest extraction that creates a single source of truth. Avoid abstraction-first recommendations.

**Example**:
- ❌ "This is a God class. Extract services." (What breaks? Why now?)
- ✅ "Subscription billing logic is duplicated in `PaymentController` (line 45) and `WebhookHandler` (line 112). When pricing tiers change, one will be missed. Extract to `BillingCalculator`."

**Anti-Pattern**: Recommending strategy patterns, abstract factories, or DTO layers for code that has a single consumer and no proven variation need.

**Safe Sequence**:
1. Lock current behavior with tests
2. Extract duplicated truth into a single source
3. Centralize access/permission rules
4. Split overloaded responsibilities
5. Format and style cleanup **last**

---

## 8. Test Quality Directive

**Rule**: Prefer assertions against visible behavior, state transitions, session/auth state, and persisted data. Avoid overfitting tests to implementation details or raw template output unless the source itself is the invariant being guarded.

**Example**:
- ❌ `expect(wrapper.html()).toContain('<div class="btn-primary">')` — Breaks on any CSS change
- ✅ `expect(screen.getByRole('button', { name: 'Submit' })).toBeEnabled()` — Tests user-visible behavior

**Anti-Pattern**: Snapshot tests on entire rendered components. They break on every visual change and train developers to blindly update snapshots.

**Assertion Hierarchy** (prefer higher levels):
1. **Behavior**: "User clicks Submit → order is created in DB → confirmation page appears"
2. **Visible State**: "Error message 'Invalid email' is visible after submitting empty form"
3. **Data State**: "Session contains `user_id` after successful login"
4. **Redirect Contract**: "POST /login with valid creds → 302 to /dashboard"
5. **Rendered Output**: "Page contains text 'Welcome back'" (acceptable for content verification)
6. **Source Template**: Raw HTML/template assertions (use only when template structure itself is the invariant)

> See also: `ops/qa/references/assertion_layers.md` for framework-specific assertion examples.
