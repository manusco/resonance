# Protocol: Property Based Testing (PBT)
> **Objective**: Find bugs you didn't think to write tests for.
> **Philosophy**: "Don't test `2 + 2 = 4`. Test `a + b = b + a`."

## 1. The Core Properties (The Invariants)
Instead of testing example values, test the *laws* of your function.

| Property | Formula | Use Case |
| :--- | :--- | :--- |
| **Roundtrip** | `decode(encode(x)) == x` | Serialization, Parser, Database Store/Load. |
| **Idempotence** | `f(f(x)) == f(x)` | Formatters, Normalizers, Sorting. |
| **Invariant** | `balance_before == balance_after` | Money transfer (Total system state constant). |
| **Inverse** | `decrypt(encrypt(x)) == x` | Compression, Cryptography. |
| **Oracle** | `fast_algo(x) == slow_algo(x)` | Optimization refactors. |

---

## 2. When to PBT (The Signal)
*   **Do PBT if**:
    *   You are writing a Parser / Serializer.
    *   The input space is infinite (Strings, Integers).
    *   You have "Business Laws" (e.g., "User account can never be negative").
*   **Skip PBT if**:
    *   It's a simple CRUD operation.
    *   There is no clear invariant (UI Rendering).

## 3. The Fuzzing Mindset
PBT tools (FastCheck, Hypothesis) generate "Nasty Inputs":
*   `null`, `undefined`
*   `""` (Empty String)
*   `"      "` (Whitespace)
*   `MAX_INT`, `MIN_INT`, `0`, `-1`
*   `💩` (Emoji/Unicode)

*If your code crashes on emoji, it fails the PBT.*
