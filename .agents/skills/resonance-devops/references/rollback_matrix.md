# Emergency Response (Rollback Matrix)

> "Panic is not a strategy. Have a button."

## 1. The 5-Step Response

**When Production is Down:**

1.  **ACK**: Acknowledge the alert. "I am investigating." (Stop others from panicking).
2.  **ROLLBACK**: Do not debug forward. **Revert to the last known good commit immediately.**
    *   `vercel rollback`
    *   `fly releases rollback`
3.  **STABILIZE**: Verify the rollback fixed the immediate symptom.
4.  **INVESTIGATE**: Now (and only now) look at logs in Staging.
5.  **RCA**: Write the Root Cause Analysis (5 Whys).

## 2. Classification

| Severity | Definition | Response Time |
| :--- | :--- | :--- |
| **Sev-1 (Critical)** | Data Loss, Auth Broken, Site Down. | **Immediate (Wake up)**. |
| **Sev-2 (High)** | Major feature broken (Checkout). | **< 1 Hour**. |
| **Sev-3 (Medium)** | Minor glitch, UI bug. | **Next Business Day**. |

> 🔴 **Rule**: Never debug on Production. Rollback Level 1 -> Debug Level 4.
