# Sharp Edges Protocol

A sharp edge is an API, configuration, workflow, or default where the easy path leads to an insecure outcome. The goal is not to shame the caller. The goal is to make unsafe use hard to express.

## 1. Core Question

If a capable developer is tired, rushed, and missing context, will the design still guide them toward safe behavior?

If not, treat it as a sharp edge.

## 2. Common Sharp Edges

### Configuration Cliffs

One value disables a critical control: certificate verification, auth enforcement, encryption, sandboxing, tenant isolation, logging, or rate limits.

**Fix**: reject dangerous values at startup, require explicit unsafe mode names, and keep unsafe modes out of production config.

### Primitive Instead of Semantic Types

Raw strings, booleans, and maps hide security meaning: `isAdmin`, `key`, `token`, `path`, `redirect`, `algorithm`, `timeout`.

**Fix**: use typed values, enums, branded types, and constructors that validate invariants.

### Caller-Controlled Security Decisions

The caller chooses algorithms, trust modes, redirect targets, policy names, roles, tenant IDs, or sandbox escape flags.

**Fix**: make policy server-owned. Let callers request intent, not decide enforcement.

### Framework Trust Boundaries

Framework conveniences can hide entry points: catch-all routes, server actions, public procedures, middleware-only auth, internal headers, image fetchers, webhooks, and background jobs.

**Fix**: document each entry point, identity source, policy layer, resource ownership check, and action boundary.

### Generated and Agentic Workflows

Generated rules, prompts, reports, and fixtures can be treated as trusted because they look structured.

**Fix**: validate generated data, cap execution, isolate untrusted input, and require evidence before promotion.

## 3. Severity Matrix

| Severity | Criteria | Response |
| :--- | :--- | :--- |
| Critical | Unsafe default exposes secrets, remote execution, auth bypass, or cross-tenant data. | Block and redesign. |
| High | Security can be disabled accidentally or by ordinary configuration. | Require safer API or production guard. |
| Medium | Ambiguous behavior can produce unsafe use. | Rename, type, validate, or document with tests. |
| Low | Confusing but unlikely to create material harm. | Improve naming or examples. |

## 4. Evidence

A sharp-edge finding should name:

- the easy path,
- the unsafe outcome,
- the affected asset,
- the safer default,
- the migration cost,
- the test or validation that prevents regression.
