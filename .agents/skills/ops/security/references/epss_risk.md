# Risk Prioritization (EPSS Protocol)

> "Not all CVSS 9.0s are equal. If it's not exploitable, it's noise."

## 1. The Decision Matrix

**Use EPSS (Exploit Prediction Scoring System) alongside CVSS.**

| Scenario | EPSS Score | CVSS Score | Action |
| :--- | :--- | :--- | :--- |
| **The Emergency** | **> 0.1 (10%)** | Any | **FIX IMMEDIATELY**. Attack is likely. |
| **The Bomb** | < 0.01 | > 9.0 (Critical) | **Fix Next**. High impact, low probability. |
| **The Noise** | < 0.01 | < 7.0 (Medium) | **Backlog**. Low risk. |

> 🔴 **Rule**: A High CVSS with Low EPSS is a lower priority than a Medium CVSS with High EPSS.

## 2. Red Team Prioritization

When simulating attacks, focus on:
1.  **RCE (Remote Code Execution)**: Always P0.
2.  **Auth Bypass**: Always P0.
3.  **Data Exfiltration**: P1.
4.  **XSS (Reflected)**: P2 (Requires user interaction).

## 3. The "False Positive" Protocol

If you mark a finding as "False Positive", you must prove:
1.  **Unreachable Code**: "This function is never called."
2.  **Mitigating Control**: "WAF blocks this pattern."
3.  **Sandbox**: "Execution is isolated."
