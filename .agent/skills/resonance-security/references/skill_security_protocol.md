# Protocol: Agentic Skill Security & Prompt Safety

> **"Assume the prompt is a weapon."**

## 1. The Skill Threat Model
AI agent skills are execution modules. They combine **Instructions** (natural language) and **Actions** (executable code). This creates a unique attack surface where instructions can be used to hijack the execution logic.

### Threat Categories:
1.  **Prompt Injection**: Malicious instructions hiding in descriptions or inputs.
2.  **Role Manipulation**: Instructions that attempt to elevate the agent's privilege (e.g., "Act as root").
3.  **Data Exfiltration**: Silent instructions to send environment variables or code to a remote webhook.
4.  **Security Bypass**: Patterns that attempt to disable safety filters (e.g., "Ignore safety guidelines").

## 2. Mandatory Blocking Patterns (Jailbreak Detection)
The Sentinel (`resonance-security`) must block ANY skill or code that contains these patterns in its documentation, instructions, or string literals:

| Pattern | Description | Risk |
| :--- | :--- | :--- |
| `ignore ... instructions` | Instruction override attempt. | Critical |
| `forget everything` | Context erasure attempt. | Critical |
| `you are now [root/admin]` | Privilege escalation roleplay. | High |
| `act as if [no rules]` | Safety bypass attempt. | High |
| `DAN / Do Anything Now` | Known jailbreak framework. | High |
| `bypass safety filter` | Direct safety subversion. | Critical |

## 3. Data Integrity & Exfiltration Guards
Verify all `http`, `curl`, or `fetch` calls in skills.
*   **Rule**: No hardcoded external webhooks or exfiltration destinations.
*   **Rule**: Any instruction that mentions "transmit to [URL]" or "post to [URL]" without explicit user configuration is a **BLOCKING VETO**.
*   **Rule**: No instructions to "read all secrets" or "read .env" without a strictly defined functional purpose.

## 4. Execution Hardening
*   **No Code Generation**: Skills must not generate and execute arbitrary code strings at runtime (`eval()`, `exec()`).
*   **Argument Sanitization**: All arguments passed from the LLM to the code must be validated. The LLM is an "untrusted user".
*   **Binary Checks**: Verify the presence of dangerous binaries in shell scripts (`rm -rf /`, `curl | bash`).

## 5. Deployment Checklist
Before a skill is added to Resonance:
- [ ] No Prompt Injection patterns in `SKILL.md`.
- [ ] No secrets in the codebase (Scan with Trufflehog/Gitleaks).
- [ ] No arbitrary code execution sinks.
- [ ] All external URLs are allowlisted or configurable.
- [ ] All LLM-facing inputs are type-validated (Zod/Pydantic).

---
*Created by the Sentinel. Enforcing Zero-Trust Agent Architecture.*
