# Strategy: Static Analysis (SAST)
> **Objective**: Scale security review beyond human speed using Automated Reasoning.
> **Philosophy**: "If a pattern causes a bug once, write a rule to catch it forever."

## 1. The Tooling Hierarchy
Use the right tool for the depth of analysis.

| Tool | Depth | Speed | Use Case |
| :--- | :--- | :--- | :--- |
| **Semgrep** | Superficial (Regex+) | Instant | Linting, Simple Pattern Matching (`exec(user_input)`). |
| **CodeQL** | Deep (Data Flow) | Slow | Interprocedural Taint Analysis, Complex Logic bugs. |

---

## 2. High-Value Pattern Classes

### A. Divergent Representations
*Parsing inconsistencies between layers.*
*   **Scenario**: A WAF parses a URL one way, the Backend parses it another.
*   **Query Goal**: Identify where input is parsed multiple times by different libraries.

### B. Unhandled Error Flows
*Silent failures in security critical code.*
*   **Query Goal**: Find functions calling `auth_check()` but ignoring the return value.
*   **Pattern**: `call = auth_check(); if (call) { ... }` (Good) vs `auth_check(); do_thing();` (Bad).

### C. Tainted Loop Conditions
*Memory corruption via user-controlled loops.*
*   **Query Goal**: Find `for (i=0; i < user_input; i++)`.

---

## 3. The "False Positive" Rule
*   If a rule generates > 20% false positives, **disable it** or **refine it**.
*   Alert fatigue is a security vulnerability.
*   **Pipeline Strategy**:
    *   **Blocker**: High Confidence, High Severity (SQLi, Hardcoded Secrets).
    *   **Warning**: Medium Confidence (Logic smells).
    *   **Audit**: Low Confidence (Manual review queue).
