# Automated Scanning Protocol

> "Software rots. Dependencies age. Automate the watch."

## 1. The Dependency Sentinel

Dependencies are your biggest attack surface.
*   **Action**: `npm audit --audit-level=high` in CI.
*   **Tool**: Snyk / Dependabot.
*   **Policy**: If a `High` severity vulnarability is found, the build BREAKS.

## 2. The Secret Scanner

Access keys belong in Vaults, not Git.
*   **Tool**: `trufflehog` or `git-secrets`.
*   **Pre-Commit**: Scan the stagged files. If a key pattern (e.g., `sk_live_...`) is found, REJECT the commit.

## 3. The Container Scan

Docker images have layers. Layers have OS vulnerabilities.
*   **Tool**: Trivy.
*   **Command**: `trivy image my-app:latest`.

> 🔴 **Rule**: A "Critical" vulnerability means Stop The Line. No features until it's patched.
