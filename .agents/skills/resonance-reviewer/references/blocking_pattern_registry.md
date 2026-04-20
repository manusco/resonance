# Blocking Pattern Registry

> "Usage of these patterns triggers an immediate 'Request Changes'."

## 1. Consoling
*   `console.log` in production code. (Use Logger).

## 2. The "Any" Type
*   `any` in TypeScript. (Use `unknown` or Generic).

## 3. The Ghost Code
*   Commented out blocks of code. (Delete it. Git has history).

## 4. The Magic Number
*   `if (status === 4)` -> `if (status === STATUS.READY)`.

## 5. The Hardcoded Secret
*   API Keys in code. (Revoke immediately).

> 🔴 **Rule**: These are non-negotiable. Do not argue. Fix them.
