# CI Test Runner Protocol

> "If it's not in CI, it's not tested."

## 1. The Pyramid Execution

Run fast tests first. Fail fast.
1.  **Stage 1: Unit Tests** (Jest). Matches `*.test.ts`. (Time: < 1min).
2.  **Stage 2: Integration Tests** (API). (Time: < 5min).
3.  **Stage 3: E2E Tests** (Playwright). (Time: < 15min).

## 2. The Flake Detector

Flaky tests are worse than no tests.
*   **Retries**: `retries: 2` (Allow 2 retries).
*   **Quarantine**: If it fails 3 times, move it to `skipped` and file a High Priority Bug.

## 3. The Artifacts

When a test fails, you need evidence.
*   **Video**: Record the run.
*   **Trace**: Capture the network stack.
*   **Upload**: Save traces to S3/GitHub Artifacts for debugging.

> 🔴 **Rule**: Never merge a PR with a "skipped" test without a ticket number attached.
