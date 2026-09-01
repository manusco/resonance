# Necessity Protocol

Use this after understanding the requested behavior and the real execution path. It reduces ownership surface. It is not code golf.

## Order

Stop at the first option that fully satisfies the requirement:

1. **Delete or decline.** If the behavior is dead, duplicated, or speculative, remove it or do not build it.
2. **Reuse the codebase.** Prefer an existing helper, type, component, or established pattern.
3. **Use the language runtime.** Prefer the standard library over local machinery.
4. **Use the native platform.** Prefer browser, database, operating-system, or framework primitives over custom code.
5. **Use an installed dependency.** Reuse a dependency already owned by the project when it fits without an adapter layer.
6. **Write the smallest local implementation.** Add only the code required by current behavior and known edge cases.

Search before deciding. Trace callers and data flow. A tiny patch at the wrong layer creates more work than a slightly larger fix at the shared cause.

## Valid cuts

- Dead code, unused flags, unreachable branches, and duplicated implementations.
- Single-use factories, interfaces with one implementation, pass-through wrappers, and configuration no caller changes.
- New dependencies that duplicate the standard library, native platform, framework, or an installed package.
- Helpers and files that add indirection without enforcing a contract or centralizing truth.
- Speculative extension points with no current caller or approved requirement.

## Protected behavior

Never remove or weaken these to make a diff smaller:

- Trust-boundary validation and authorization.
- Error handling that prevents corruption or data loss.
- Accessibility and required fallbacks.
- Observability needed to operate or recover the system.
- Tests that prove non-trivial logic or a known regression.
- Explicit user scope and approved architecture rules.

## Evidence

For each proposed cut, state:

- The exact file or symbol.
- What can disappear.
- What existing capability replaces it, or `nothing` for dead code.
- Which behavior check proves the cut is safe.

Do not optimize for line count. Optimize for fewer concepts, dependencies, branches, files, and owners while preserving required behavior. If the current implementation is already the smallest safe one, leave it alone.
