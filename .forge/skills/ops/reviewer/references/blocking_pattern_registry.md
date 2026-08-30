# Blocking Pattern Registry

> "Usage of these patterns triggers an immediate 'Request Changes'."

## 1. Consoling
*   `console.log` in production code. (Use Logger).

## 2. The "Any" Type
*   `any` in TypeScript. (Use `unknown` or Generic).

## 3. Type Evidence Erasure
*   A precise value widened to `unknown`, `object`, `{}`, or
    `Record<string, unknown>` and later recovered with `as`. Preserve inference,
    use `satisfies`, or parse untrusted input once at the boundary.

## 4. The Ghost Code
*   Commented out blocks of code. (Delete it. Git has history).

## 5. The Magic Number
*   `if (status === 4)` -> `if (status === STATUS.READY)`.

## 6. The Hardcoded Secret
*   API Keys in code. (Revoke immediately).

> 🔴 **Rule**: These are non-negotiable. Do not argue. Fix them.
