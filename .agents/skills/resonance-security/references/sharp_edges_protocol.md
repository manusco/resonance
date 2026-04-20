# Protocol: Sharp Edges (Footgun Detection)
> **Objective**: Identify API designs where the "Easy Path" leads to insecurity.
> **Philosophy**: "The Pit of Success" - Secure usage should be the path of least resistance.

## 1. The Core Question
When auditing an API or Configuration Schema, ask:
*   *"If a developer is tired, rushing, and hasn't read the docs, will they use this securely?"*

If the answer is **NO**, it is a Sharp Edge.

---

## 2. The Rogue's Gallery (Common Footguns)

### A. Configuration Cliffs
*One wrong setting causes catastrophic failure.*
*   ❌ `verify_ssl: false` (Silent acceptance of insecure connections).
*   ❌ `timeout: 0` (Does this mean "Immediate" or "Infinite"? Ambiguity is fatal).
*   **Fix**: Validate config at startup. Reject dangerous values. Fail hard.

### B. Primitives vs Semantics
*Exposing raw bytes invites type confusion.*
*   ❌ `function encrypt(data: string, key: string)` (Strings are untyped).
*   ✅ `function encrypt(data: Plaintext, key: EncryptionKey)` (Types enforce safety).

### C. The "Algo" Parameter
*Letting the caller choose the algorithm.*
*   ❌ `jwt.verify(token, secret, { alg: 'HS256' })` (Caller controls security).
*   ✅ `jwt.verify(token, secret)` (Library enforces strongest available).

---

## 3. Threat Modeling the Developer
We assume three types of users:
1.  **The Scoundrel**: Actively malicious. Can they disable security via config?
2.  **The Lazy Developer**: Copy-pastes the first StackOverflow answer. Is that answer secure?
3.  **The Confused Developer**: Swaps parameters. Does the type system catch it?

## 4. Severity Matrix

| Severity | Criteria | Example |
| :--- | :--- | :--- |
| **Critical** | Default is insecure. | `password_hash` defaulting to MD5. |
| **High** | Easy to disable security. | `allow_unauthorized: true` flag exists. |
| **Medium** | Ambiguous behavior. | Negative timeouts. |
