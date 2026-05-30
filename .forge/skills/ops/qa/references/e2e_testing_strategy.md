# E2E Testing Strategy

> **Objective**: Verify critical paths without flakiness. "Test behavior, not implementation."

## 1. The Testing Pyramid API
- **Unit**: 70% (Jest/Vitest). Logic only. Fast.
- **Integration**: 20% (API Tests). Database + API.
- **E2E**: 10% (Playwright). Critical User Journeys only.

## 2. E2E Critical Paths
Only automate flows that directly impact revenue or core value:
1.  **Signup/Login**: Can users enter?
2.  **Checkout/Payment**: Can users pay?
3.  **Core Loop**: Can users do the "Main Thing"?

## 3. The "Reconnaissance-Then-Action" Pattern
When writing Playwright scripts for dynamic apps:
1.  **Wait**: `page.wait_for_load_state('networkidle')`.
2.  **Inspect**: Screenshot/Dump DOM to find robust selectors.
3.  **Act**: Interact with `data-testid` or robust text.

## 4. Anti-Flake Protocol
- ❌ **Fixed Waits**: `sleep(5000)` -> FAILS.
- ✅ **Smart Waits**: `waitForSelector`, `waitForResponse`.
- ❌ **XPath**: `div[3]/span[2]` -> FAILS on redesign.
- ✅ **Semantic**: `getByRole('button', name='Submit')`.
