# Verified Security Checklist

Use this checklist for code reviews and architecture decisions. It is not a substitute for threat modeling. Every checked item needs evidence from code, configuration, tests, or runtime behavior.

## 1. Secrets

- [ ] No live secrets, private keys, tokens, certificates, or credentials in source, logs, examples, generated artifacts, or committed config.
- [ ] Secret examples use inert placeholders and cannot be mistaken for real credentials.
- [ ] Runtime secrets are loaded from approved secret storage or environment injection.
- [ ] Review output records whether secrets are configured, not their values or partial fingerprints.

## 2. Input Boundaries

- [ ] Every external boundary has schema validation: API body, query params, headers, files, CLI args, webhooks, queue messages, and AI/tool input.
- [ ] Validation uses allowlists and normalization before business logic.
- [ ] Rejected input has a safe error path and does not leak internals.
- [ ] File uploads enforce size, content type, magic bytes, storage path, and execution behavior.

## 3. Injection Sinks

- [ ] SQL and NoSQL paths use parameter binding or safe query builders.
- [ ] Shell execution uses fixed executables and argument arrays, not shell string composition.
- [ ] Template, HTML, Markdown, SVG, and rich-text rendering escape or sanitize untrusted content.
- [ ] Redirects, outbound fetches, filesystem paths, and deserialization have explicit allowlists.

## 4. Authentication and Authorization

- [ ] Sensitive actions are enforced server-side.
- [ ] Authorization is checked across route, policy, resource, and action layers.
- [ ] Ownership and tenant boundaries are explicit.
- [ ] Middleware, menu visibility, and client checks are not treated as sufficient by themselves.
- [ ] Capability changes include regression tests for allowed and denied actors.

## 5. Browser and Session Safety

- [ ] Session cookies are HttpOnly, Secure, SameSite-aware, scoped, and rotated where needed.
- [ ] CSP, CORS, and CSRF defenses match the application flow.
- [ ] Unsafe HTML APIs, postMessage handlers, and third-party embeds have explicit trust boundaries.

## 6. Abuse and Availability

- [ ] Public and tenant-facing expensive operations have rate, cost, and concurrency limits.
- [ ] AI calls, exports, search, upload, login, and webhook endpoints have tighter controls.
- [ ] Error handling avoids retry storms and user-controlled amplification.

## 7. Dependencies and Build Chain

- [ ] New packages are verified for name, publisher, maintenance, install scripts, and necessity.
- [ ] Lockfiles match manifests and are committed where the ecosystem expects them.
- [ ] CI actions and build images are pinned or otherwise controlled.
- [ ] Untrusted code paths do not receive secrets during install, build, or test.

## 8. Evidence and Coverage

- [ ] Every scoped target has clean, candidate, finding, rejected, fixed, skipped, or incomplete status.
- [ ] Findings include input, path, missing guard, impact, severity, confidence, fix, and verification command.
- [ ] Scanner hits are not filed as final findings without confirmation.
- [ ] Incomplete coverage is reported explicitly.
