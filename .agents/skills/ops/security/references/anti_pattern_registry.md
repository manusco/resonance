# Security Anti-Pattern Registry

This registry defines patterns that deserve immediate scrutiny in code review. A registry match creates a blocker only when evidence shows reachability, unsafe configuration, or exposed sensitive assets. Keep severity and confidence separate.

## Blocking Patterns

### 1. Dependency Confusion and Slopsquatting

**Risk**: A package name is mistyped, invented, abandoned, newly claimed, or controlled by the wrong publisher.

**Review target**:

- new dependency,
- changed package manager registry,
- install script,
- package with low reputation or recent ownership change,
- lockfile drift that does not match the manifest.

**Evidence gate**: verify existence, publisher, maintenance, install scripts, version pinning, transitive risk, and whether the package is actually needed.

### 2. Unsafe HTML Rendering

**Risk**: Attacker-controlled content reaches HTML, Markdown, SVG, rich text, or template rendering without escaping or sanitization.

**Evidence gate**: prove input control, rendering path, missing sanitizer or unsafe sanitizer config, and browser execution impact.

### 3. Hardcoded Secrets

**Risk**: API keys, tokens, certificates, private URLs, or credentials enter source, logs, generated artifacts, or examples that users may copy.

**Evidence gate**: classify as live, test, placeholder, generated, or inert. Live or credible credentials block. Do not log partial credential fingerprints.

### 4. Injection Into Privileged Interpreters

**Risk**: User input reaches SQL, shell, NoSQL, LDAP, template, GraphQL, or command interpreters without safe binding.

**Evidence gate**: show source, propagation, sink, missing binding or validation, and affected data or command authority.

### 5. Authorization Bypass

**Risk**: A sensitive action relies on client state, navigation hiding, middleware-only checks, scattered roles, or missing ownership checks.

**Evidence gate**: walk entry point, identity extraction, policy decision, resource ownership, action enforcement, and audit trail.

### 6. Missing Boundary Validation

**Risk**: External input crosses into persistence, business logic, filesystem, queue, AI prompt, or network request without schema validation and normalization.

**Evidence gate**: name the boundary, accepted shape, rejected shape, downstream assumption, and failure mode.

### 7. Unsafe Process Execution

**Risk**: User-controlled values reach process execution, shell mode, script arguments, working directory, environment, or path lookup.

**Evidence gate**: prove control of command, argument, environment, path, or current directory. Prefer argument arrays and fixed executables.

### 8. Abuse Without Rate or Cost Controls

**Risk**: Public or tenant-facing routes allow expensive work, credential checks, model calls, exports, search, or writes without budget limits.

**Evidence gate**: show actor, operation, cost driver, missing quota, and impact on availability or spend.

### 9. Excessive Data Exposure

**Risk**: Internal entities, debug payloads, traces, model prompts, logs, or generated reports expose sensitive fields.

**Evidence gate**: identify sensitive field, response or artifact path, audience, retention, and whether an allowlist exists.

### 10. Unsafe File Handling

**Risk**: Uploads, archives, generated files, symlinks, or paths can escape intended boundaries or execute active content.

**Evidence gate**: prove path control, type confusion, archive traversal, symlink boundary crossing, executable handling, or missing content validation.

### 11. Prompt and Tool Boundary Injection

**Risk**: Untrusted text changes agent instructions, tool selection, credentials handling, or output validation.

**Evidence gate**: show untrusted content entering privileged prompt context, tool arguments, policy decisions, or parser-sensitive output. Prompt separation alone is not a sufficient defense.

## Review Rule

A match is a candidate. A blocker needs evidence. When evidence is incomplete, mark the item as uncertain, name the missing check, and do not present it as proven.
