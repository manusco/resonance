# Static Analysis Strategy

Static analysis scales review, but it does not replace judgment. Its job is to discover surfaces, build candidate queues, and prove repeatable classes of bugs with the least expensive method that can support the claim.

## 1. Analysis Depth Ladder

Use the shallowest reliable layer. Escalate only when the claim requires it.

| Depth | Use | Limit |
| :--- | :--- | :--- |
| Token or regex | Literal secrets, simple config flags, obvious dangerous calls | No control flow, weak context. |
| Structured parser | JSON, YAML, HCL, Dockerfiles, lockfiles, workflow files | Good for config, weak for application semantics. |
| AST match | Entry points, API calls, decorators, imports, exports | Local syntax only unless summaries are added. |
| Intraprocedural flow | Local source-to-sink paths inside one function | Misses helper and policy boundaries. |
| Interprocedural summary | Shared auth, validation, data access, and framework wrappers | Slower, needs strong fixtures. |

A fixed line window is not proof of safety or risk. It is only a hint.

## 2. Rule Contract

Every custom rule should declare:

- rule ID and schema version,
- file and technology scope,
- sources, sinks, propagators, and sanitizers,
- safe variants and accepted exceptions,
- confidence level independent from severity,
- expected match location,
- positive fixtures,
- negative fixtures,
- suppression format with owner, reason, and expiry.

Generated rules are data, not trusted code. Validate them before use and bound file count, regex cost, candidate count, and collision behavior.

## 3. Discovery Is Not Confirmation

A rule can produce candidates. A finding needs evidence.

- An entry point without a guard is a candidate until the auth path is checked.
- A raw query API is a candidate until attacker control reaches it without safe binding.
- A secret-looking string is a candidate until it is classified as live, test, generated, or inert.
- A framework feature is a candidate until project config and middleware behavior are checked.

Severity answers: how bad if true? Confidence answers: how sure are we? Keep them separate.

## 4. Authorization Path Model

Model authorization as a path:

1. entry point,
2. identity extraction,
3. policy decision,
4. resource ownership,
5. action enforcement,
6. audit trail.

Do not treat a nearby `auth`, `user`, or `admin` token as proof. Do not treat a missing token as proof either. Follow the path.

## 5. Technology Scope

Detect technology at the package, service, or module level. Project-wide labels are scheduling hints, not correctness proof. Polyglot repositories need local scope so one framework's files do not trigger another framework's rules.

## 6. Fixture Standard

A useful rule has paired unsafe and safe fixtures:

- comments and strings that should not match,
- multiline calls,
- aliases and helper functions,
- CRLF and Windows paths,
- generated files and ignored paths,
- monorepo package boundaries,
- parser failures,
- safe framework variants,
- exact expected rule, source, sink, line, and confidence.

Tests that only assert `matches.length > 0` are not enough.

## 7. High-Value Pattern Classes

- Divergent parsing between layers.
- Unhandled failures in auth, validation, crypto, and persistence code.
- User-controlled input reaching SQL, shell, filesystem, template, redirect, deserialization, or network sinks.
- Authorization drift across route, policy, resource, and action layers.
- Tenant or ownership identifiers crossing trust boundaries.
- Unsafe defaults in framework routing, middleware, image fetching, server actions, internal headers, and public procedures.
- Secrets in source, logs, traces, fallback config, or generated artifacts.
- Infrastructure paths to public ingress, wildcard permissions, mutable dependencies, or missing encryption.
