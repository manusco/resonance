# Testing Pyramid Protocol (Agent Edition)

> "Unit tests prove the code works. E2E tests prove the product works."

## 1. The Strategy (Inverted)

For AI Agents and Web Apps, we invert the traditional pyramid slightly.

1.  **E2E (End-to-End)**: **30%**. (Crucial).
    *   Simulate a REAL user flow (Login -> Buy -> Logout).
    *   If this fails, nothing else matters.
    *   Tool: Playwright.
2.  **Integration**: **50%**. (The Sweet Spot).
    *   Test the API + Database + AI Model.
    *   Mock ONLY external SaaS (Stripe/SendGrid).
    *   Do NOT mock the DB (Use a test container).
3.  **Unit**: **20%**. (Utility only).
    *   Test complex pure functions (Pricing logic, Parsers).
    *   Do NOT write unit tests for simple React components.

## 2. The Mandate

*   **No Mocks for Core Logic**: If you mock the Database, you are testing your imagination, not the system.
*   **Test Behavior, Not Implementation**:
    *   ❌ Test: `expect(div.className).toBe('red')`
    *   ✅ Test: `expect(screen.getByText('Error')).toBeVisible()`

> 🔴 **Rule**: If you delete a test and the app still breaks in production, that test was worthless.
