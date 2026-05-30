# Supply Chain Security Protocol (OWASP A03)

> "The attacker won't break your door; they'll poison your water supply."

## 1. Dependency Hygiene

**Before adding a package (`npm install x`):**
1.  **Age Check**: Is it < 1 month old? (Suspicious).
2.  **User Check**: Who maintains it? (Verified Org vs Random User).
3.  **Usage Check**: Downloads > 10k/week? (Safety in numbers).

## 2. The Lockfile Law

*   **Rule**: `package-lock.json` / `pnpm-lock.yaml` MUST be committed.
*   **CI Check**: `npm ci` (Clean Install) must be used in pipelines, NEVER `npm install`.
    *   `npm ci` respects the lockfile perfectly.
    *   `npm install` can update minor versions silently.

## 3. Secret Scanning (Pre-Commit)

**You must prevent secrets from entering git.**

*   **Banned Patterns**:
    *   `sk-` (Stripe/OpenAI keys).
    *   `ghp_` (GitHub Tokens).
    *   `-----BEGIN PRIVATE KEY-----` (RSA/PEM).

> ⚠️ **If a secret hits the remote repo, it is burned. Rotate it immediately.**

## 4. 3rd Party Scripts

*   **SRI (Subresource Integrity)**: External scripts (CDNs) MUST have an integrity hash.
    *   `<script src="..." integrity="sha384-..." crossorigin="anonymous">`
