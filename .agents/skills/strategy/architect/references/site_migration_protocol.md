# Site Migration Protocol

> **Objective**: A gold-standard, technology-agnostic playbook for migrating any existing site or application into a new architecture.
> **Philosophy**: We do not port blindly. We audit first, design deliberately, migrate surgically, and verify obsessively.
> **Prime Directive**: Nothing is deleted or replaced without a documented justification. Preserving business value is always the priority.

## Contents

- [0. The Migrator's Mindset](#0-the-migrators-mindset)
- [Phase 0: Discovery & Audit](#phase-0-discovery--audit)
- [Phase 1: Domain Model Design](#phase-1-domain-model-design)
- [Phase 2: Architecture Design](#phase-2-architecture-design)
- [Phase 3: Data Migration Strategy](#phase-3-data-migration-strategy)
- [Phase 4: Testing Requirements](#phase-4-testing-requirements)
- [Phase 5: UX Migration Rules](#phase-5-ux-migration-rules)
- [Phase 6: Implementation Sequence](#phase-6-implementation-sequence)
- [Phase 7: Quality Gates](#phase-7-quality-gates)
- [Phase 8: Agent Behavior Rules](#phase-8-agent-behavior-rules)
- [Phase 9: Documentation Deliverables](#phase-9-documentation-deliverables)
- [Appendix A: Common Migration Anti-Patterns](#appendix-a-common-migration-anti-patterns)
- [Appendix B: Pre-Migration Checklist](#appendix-b-pre-migration-checklist)
- [Appendix C: Pre-Launch Checklist](#appendix-c-pre-launch-checklist)

---

## 0. The Migrator's Mindset

Before writing a single file, internalize these rules:

| Law | Statement |
| :--- | :--- |
| **Understand Before You Rewrite** | The old system is a behavioral reference, not a target. It encodes years of business decisions. Read it like archaeology. |
| **No Blind Ports** | Do not translate old files 1:1 into the new stack. Understand what each piece *does*, then design it correctly for the new context. |
| **No Accidental Deletions** | A field, route, or behavior is only removed after it is confirmed dead — via business review, not by assumption. |
| **New Architecture, Preserved Intent** | The data model changes. The business rules do not. Separate the two. |
| **Migrate in Slices, Not in One Shot** | Break the migration into independently shippable phases. Each phase must be verifiable on its own. |
| **Dry Run is Mandatory** | Any data transformation runs in dry-run mode first. No production data is mutated until the report is reviewed. |

---

## Phase 0: Discovery & Audit

> **Rule**: Do not start building until these documents exist.

### 0.1 Product Summary

Produce a plain-English document answering:

- What does the application do?
- Who are the user types? (public, authenticated, roles)
- What are the main workflows, start to finish?
- What does an admin manage?
- What external systems does it integrate with? (email, payments, storage, APIs)
- What are the high-traffic and high-stakes paths?

### 0.2 Current Data Model

For every data entity in the old system:

- [ ] Name and purpose
- [ ] All fields, with types and nullability
- [ ] Required vs optional fields
- [ ] Relationships (one-to-many, many-to-many, polymorphic)
- [ ] Status/enum fields and their full set of values
- [ ] Indexes and uniqueness constraints
- [ ] Validation rules (where enforced and how)
- [ ] Implicit business rules buried in code (controllers, hooks, middleware, jobs, etc.)
- [ ] Soft-delete behavior, if any
- [ ] Audit/timestamps fields

### 0.3 Workflow Map

For every user-facing and admin workflow:

- [ ] Entry point (URL, trigger, event)
- [ ] Step-by-step flow
- [ ] Branching conditions (status gates, role checks, conditional fields)
- [ ] Exit points (success, failure, abandoned)
- [ ] What state changes in the database on each transition
- [ ] What side effects fire (emails, webhooks, jobs, logs)

### 0.4 Risk Report

Before designing anything, identify and classify risk:

| Risk Category | Questions to Answer |
| :--- | :--- |
| **Fragile Code** | What is held together with duct tape? What breaks if touched? |
| **Unclear Logic** | What parts have no tests, no comments, and no obvious owner? |
| **Duplicated Rules** | Where is the same validation or permission check in multiple places? |
| **Dead Code** | What routes, models, or features appear unused? Flag — do not delete yet. |
| **Manual Product Decisions** | Which behaviors require a product decision before redesigning? |
| **Data Quality** | Are there orphaned records, inconsistent states, or nulls in required fields? |
| **Hidden Dependencies** | What external systems does the old app touch that the new one must replicate or replace? |

**Output**: A `RISK_REPORT.md` that classifies every finding as P0 (blocker), P1 (high), P2 (medium), or P3 (low).

---

## Phase 1: Domain Model Design

> **Rule**: Design the new domain model before creating any screens or routes.

### 1.1 Entity Definition

For each entity in the new system, define:

```
Entity: [Name]
Purpose: [One sentence — what does this record represent?]
Fields:
  - name: [field_name]
    type: [String | Integer | Boolean | Date | Enum | Relation]
    required: [yes/no]
    notes: [validation rules, constraints, business meaning]
Relationships:
  - [entity] has many [entity] via [field]
  - [entity] belongs to [entity] via [field]
Status Enum: [list all valid states]
Access Rules:
  - [role] can [create | read | update | delete] when [condition]
Indexes / Uniqueness:
  - [field or compound] must be unique
Timestamps: [created_at, updated_at, deleted_at if soft-deleted]
Test Cases: [key scenarios to verify]
```

### 1.2 Status Machines

Every entity with a `status` field must have an explicit state machine:

- List all valid states
- List all valid transitions (`draft → submitted`, not `draft → accepted`)
- Name the function that performs each transition
- Specify who (which role) is allowed to trigger each transition
- Define what side effects fire on each transition

> **Anti-pattern**: Scattered `status = "x"` assignments throughout the codebase. Every status change must go through a named domain function.

### 1.3 Field Disposition Map

For every field in the old system, make an explicit decision:

| Old Field | New Field | Action | Justification |
| :--- | :--- | :--- | :--- |
| `user_name` | `name` | Rename | Cleaner language |
| `application_type` | `type` | Preserve | Same semantics |
| `old_flag` | — | **Delete** | Confirmed unused by [person] on [date] |
| `status` | `status` | Redesign | New enum with explicit state machine |
| `created_at` | `createdAt` | Rename | Convention change |

> ⚠️ **Rule**: A field is only deleted when its absence is explicitly approved. "It looks unused" is not sufficient. Search the old codebase, check the UI, and confirm with a stakeholder.

### 1.4 Role & Permission Matrix

Define all roles and their permissions before writing any code:

| Role | Resource | Create | Read | Update | Delete | Condition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Public | Application | ✅ | Own only | Draft only | ❌ | — |
| Admin | Application | ✅ | All | All | Soft only | Authenticated |

---

## Phase 2: Architecture Design

> **Rule**: Agree on architecture before starting implementation. Record decisions in ADRs.

### 2.1 Layered Structure

Use a clear, separated layer structure. The exact directory names adapt to the tech stack, but the layers must be present:

```
[project root]/
  [presentation layer]     ← UI components, pages, templates
  [API/route layer]        ← Thin handlers. No business logic here.
  [domain layer]           ← Business logic, state transitions, rules
  [data layer]             ← Collections, models, schemas, migrations
  [infrastructure layer]   ← Email, storage, auth, external APIs
  [shared/lib]             ← Validation, types, constants, utilities
  [tests]                  ← Unit, integration, E2E
```

### 2.2 Architecture Rules (Non-Negotiable)

1. Business logic lives in the **domain layer**, not in UI components or route handlers.
2. Route/API handlers are thin wrappers around domain functions.
3. Validation schemas are defined once and reused across domain and API layers.
4. Access control functions are **named**, **tested**, and **reused** — never inlined.
5. Status transitions go through **explicit named functions**. No direct field assignments from arbitrary locations.
6. Do not mix unrelated business concerns into lifecycle hooks (e.g., ORM hooks).
7. All important status transitions must be tested.
8. No secrets in code. All environment configuration goes through validated env schema.

### 2.3 Architecture Decision Records

Write an ADR for every significant choice:

- **Stack selection**: Why this framework/language/DB?
- **Data layer**: Why this ORM / schema approach?
- **Auth strategy**: Why this auth mechanism?
- **Deployment target**: Why this infra (Docker, serverless, VPS)?
- **Testing approach**: Why this test runner / E2E tool?

> See also: `strategy/architect/references/adr_protocol.md` for a full ADR template.

---

## Phase 3: Data Migration Strategy

> **Rule**: No production data is mutated without a dry-run report reviewed and approved.

### 3.1 Migration Script Requirements

Every migration script must:

- [ ] Read from the old data source (export, CSV, JSON, direct DB connection)
- [ ] Validate each record against the new schema before inserting
- [ ] Track per-record disposition: `migrated | skipped | error`
- [ ] Produce a migration report (see 3.2)
- [ ] Support a `--dry-run` flag that reads and validates without writing
- [ ] Be idempotent: running it twice must not create duplicates
- [ ] Preserve old IDs in a `legacyId` / `sourceId` field for traceability
- [ ] Log validation errors with enough context to fix the source data

### 3.2 Migration Report Format

After every run (dry or live), produce:

```
Migration Report — [timestamp]
Source: [old system name / export file]
Target: [new system name / collection]
Mode: [DRY RUN | LIVE]

Summary:
  Total records read:       [n]
  Successfully migrated:    [n]
  Skipped (intentional):    [n]  ← with reason codes
  Errors:                   [n]  ← with field-level details
  Warnings:                 [n]  ← suspicious but not blocking

Detail:
  [record_id]: ERROR — field [x] failed validation: [reason]
  [record_id]: SKIPPED — reason: [deleted/duplicate/out_of_scope]
  [record_id]: WARNING — field [x] is null; defaulted to [y]

Missing Relationships:
  [n] records reference [entity_id] that does not exist in new system

Data Quality Issues:
  [description of any systemic data quality problem found]
```

### 3.3 Migration Safety Rules

- **Do not migrate everything at once.** Migrate one entity / collection at a time. Verify before proceeding.
- **Keep old IDs.** Store the original ID in `legacyId`. This enables debugging and rollback mapping.
- **Do not assume data is clean.** Old systems accumulate garbage. Validate every field.
- **Do not delete source data.** The old database is read-only during migration. Never modify it.
- **Establish a freeze point.** Agree on a date/time when the old system stops accepting new data. Migrate after that point.
- **Test with a subset first.** Run the migration script on 10% of records before full execution.
- **Confirm relationships survive.** Check that all foreign key references resolve in the new system.

---

## Phase 4: Testing Requirements

> **Rule**: No feature is complete without tests, validation, access control, and error states.

### 4.1 Test Pyramid

```
       [ E2E ]            ← Critical user flows, happy paths + key failure cases
     [ Integration ]      ← Collection/model behavior, role-based access, status transitions
   [ Unit ]               ← Pure logic: validation, state machines, calculations, access helpers
```

### 4.2 Mandatory Test Coverage

**Unit tests** must cover:
- Every status transition rule (valid transitions pass, invalid transitions throw)
- Every access control function (correct role → allowed, wrong role → denied)
- Every validation helper
- Every calculation / scoring function

**Integration tests** must cover:
- Creating and submitting each entity type
- Each role's access to each collection
- Admin actions (accept, reject, assign, invite, etc.)

**E2E tests** must cover at minimum:
- The primary public-facing happy path (submit a form, receive confirmation)
- Admin login and primary admin action (review, approve, reject)
- Unauthorized user cannot reach protected areas
- Form validation errors render correctly
- Required field omission blocks submission

### 4.3 Test Infrastructure Requirements

- [ ] Separate test database / environment
- [ ] Deterministic seed data (same data every run)
- [ ] Factory/builder functions for all major entities
- [ ] Tests must be runnable with a single command
- [ ] CI-equivalent local check script that runs: typecheck → lint → unit → integration → build

---

## Phase 5: UX Migration Rules

> **Rule**: Do not copy the old UI. Redesign it correctly for the new stack and users.

### 5.1 Identify User Segments

For each user type, define:
- Their entry point
- Their primary goal
- Their frustration points in the old system
- The mental model they bring

### 5.2 UX Quality Gates

**Applicant/Public-facing UI:**
- [ ] Clear entry point — user knows immediately what to do
- [ ] Multi-step forms show progress
- [ ] Draft save where the form is long or the session could be lost
- [ ] Review step before final submission
- [ ] Confirmation screen after submission
- [ ] Status visibility — user can check where their submission stands
- [ ] Friendly, specific error messages — not generic "Invalid input"
- [ ] Mobile-first or at minimum mobile-tested

**Admin/Internal-facing UI:**
- [ ] Dense, efficient — admin users value speed over beauty
- [ ] Filterable lists (by status, date, assignee, score)
- [ ] Inline status badges that match the domain status enum exactly
- [ ] Bulk actions where appropriate
- [ ] Internal notes / audit trail visible
- [ ] Decision actions (approve, reject, request more info) prominent and labeled clearly
- [ ] Confirmation dialogs for irreversible actions

### 5.3 States That Must Be Handled

Every page that fetches data must handle all four states:

| State | What to Show |
| :--- | :--- |
| Loading | Skeleton, spinner, or progressive render |
| Empty | Helpful empty-state message, not a blank page |
| Error | Clear error message + retry action |
| Success | The actual content |

---

## Phase 6: Implementation Sequence

Follow this order. Do not skip phases. Each phase must be verified before proceeding.

```
1. Project setup & tooling
   ├── Framework scaffold
   ├── Environment variable validation
   ├── Linting + formatting + typechecking (if typed language)
   ├── Containerization / deployment config
   └── CI-equivalent local check script

2. Auth & access foundation
   ├── User model
   ├── Roles definition
   ├── Access control helpers
   ├── Seed: admin user
   └── Tests: role-based access

3. Core domain model
   ├── Primary entities (collections / models / schemas)
   ├── Status enums and constants
   ├── Relationship wiring
   └── Tests: CRUD + access per role

4. Domain logic
   ├── Named domain functions for each workflow
   ├── Status transition functions
   ├── Validation functions (shared)
   └── Tests: each function's happy path + failure cases

5. Public UI
   ├── Entry / landing page
   ├── Primary public flow (application, registration, etc.)
   ├── Confirmation screen
   └── Applicant status dashboard (if applicable)

6. Admin UI
   ├── List view with filters
   ├── Detail view
   ├── Action panel (approve / reject / assign / invite)
   ├── Notes / audit trail
   └── Batch actions

7. Migration tooling
   ├── Field mapping spec
   ├── Migration script (dry-run capable)
   ├── Validation logic
   └── Migration report generator

8. Hardening
   ├── E2E tests for all critical flows
   ├── Error pages (404, 500, auth failure)
   ├── Empty states
   ├── Logging / observability
   ├── Security review
   └── Deployment rehearsal
```

---

## Phase 7: Quality Gates

Run before every merge / deploy:

```
[typecheck]  → Zero type errors
[lint]       → Zero lint violations
[format]     → Code style consistent
[unit]       → All unit tests pass
[integration]→ All integration tests pass
[build]      → Production build succeeds
[e2e]        → Critical E2E flows pass (run on CI)
```

> A feature is not done unless all gates pass. "It works on my machine" is not done.

---

## Phase 8: Agent Behavior Rules

These rules govern how a coding agent executes a migration task.

1. **Never make broad rewrites without explaining the intended change first.** Present the plan. Wait for review.
2. **Prefer small, reviewable changes.** One entity / one workflow at a time.
3. **Do not invent business requirements.** If the old system's intent is unclear, flag it in `ASSUMPTIONS.md` and continue with a documented assumption.
4. **Do not leave TODO comments** unless they are also tracked in a `TODO.md` with context and priority.
5. **Do not suppress type errors** or disable linting rules to make checks pass.
6. **Do not disable tests** to make the suite pass.
7. **Do not skip access control.** Every route and every action must have explicit role enforcement.
8. **Do not put secrets in code.** All credentials and keys go through environment configuration.
9. **Do not put business logic in UI components.** Components handle presentation only.
10. **Do not add dependencies without a reason.** Document the reason.
11. **Do not optimize prematurely.** Make it correct first.
12. **Do not delete a field, route, or feature** without explicit stakeholder confirmation and a documented reason.
13. **Every generated file has a clear, singular purpose.**
14. **Every status transition is tested.**
15. **Every public form has validation and all four states** (loading, empty, error, success).

---

## Phase 9: Documentation Deliverables

By the end of the migration, the following documents must exist:

| File | Contents |
| :--- | :--- |
| `docs/migration/01-product-summary.md` | What the old system did; user types; key workflows |
| `docs/migration/02-current-data-model.md` | All entities, fields, relationships, enums from old system |
| `docs/migration/03-workflow-map.md` | Step-by-step flows for every user journey |
| `docs/migration/04-business-rules.md` | Extracted business rules from controllers/hooks/policies/jobs |
| `docs/migration/05-risk-report.md` | Fragile parts, unclear logic, duplications, dead code |
| `docs/migration/06-field-disposition.md` | Preserve / rename / merge / split / delete decisions for every field |
| `docs/migration/07-new-domain-model.md` | The clean entity design for the new system |
| `docs/migration/08-migration-plan.md` | Phased implementation plan |
| `docs/migration/09-migration-report.md` | Output from the data migration run (dry + live) |
| `ASSUMPTIONS.md` | Every assumption made when the old behavior was ambiguous |
| `docs/adr/` | One ADR per major architectural decision |

---

## Appendix A: Common Migration Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
| :--- | :--- | :--- |
| **1:1 file porting** | Preserves old architecture's problems | Audit intent → design correctly |
| **Migrating all data at once** | One error blocks everything | Migrate entity by entity |
| **Deleting fields by assumption** | Loses data that may matter | Field disposition review with stakeholder sign-off |
| **Skipping dry run** | Corrupts production data | Always dry-run first, review the report |
| **Inlining status changes** | Creates scattered state mutation | Named domain functions for all transitions |
| **Permission checks in UI** | Bypassable, inconsistent | Access control in the data/API layer, always |
| **Copying old tests verbatim** | Tests the old behavior, not the new model | Rewrite tests from the new domain model |
| **Migrating dead features** | Pays technical debt forward | Confirm before migrating; discard if truly dead |
| **No rollback plan** | Irreversible mistakes | Keep old system live until new system is verified |

---

## Appendix B: Pre-Migration Checklist

Complete before writing a single file in the new system:

- [ ] Product summary documented
- [ ] All entities, fields, and relationships catalogued
- [ ] Every workflow mapped end-to-end
- [ ] Business rules extracted from code and documented
- [ ] Risk report complete and reviewed
- [ ] Field disposition decisions made and recorded
- [ ] Role and permission matrix defined
- [ ] New domain model designed
- [ ] Architecture decisions recorded (ADRs)
- [ ] Stack selection justified
- [ ] Test strategy defined
- [ ] Migration script approach agreed
- [ ] "Freeze point" for old system agreed with stakeholders
- [ ] Rollback plan documented

---

## Appendix C: Pre-Launch Checklist

Complete before switching traffic to the new system:

- [ ] All quality gates pass (typecheck, lint, test, build)
- [ ] E2E tests pass for all critical flows
- [ ] Data migration dry-run reviewed and approved
- [ ] Data migration live run report reviewed and approved
- [ ] All migrated records spot-checked by a human reviewer
- [ ] Admin users can log in and perform all primary actions
- [ ] Public flows tested end-to-end in staging
- [ ] Error pages exist (404, 500, auth failure)
- [ ] Environment variables validated at startup (app refuses to start with missing config)
- [ ] Secrets confirmed not in source code
- [ ] Old system is in read-only / maintenance mode before go-live
- [ ] Rollback procedure tested
- [ ] Monitoring / alerting active
- [ ] DNS / traffic cutover plan documented
