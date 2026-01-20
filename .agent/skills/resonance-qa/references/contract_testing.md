# Contract Testing Protocol (Pact)

> "End-to-End tests are slow. Mocks are lies. Contract Tests are the truth."

## 1. The Consumer-Driven Contract

1.  **Consumer (Frontend)** defines what it needs: "I need `id` and `name`."
2.  **Provider (Backend)** verifies it can deliver: "I verify against the contract."

## 2. The Pact Flow

```typescript
// Consumer Test
provider.addInteraction({
  state: 'user exists',
  uponReceiving: 'a request for user',
  withRequest: { method: 'GET', path: '/user/1' },
  willRespondWith: { status: 200, body: { id: 1, name: 'Alice' } }
});
```

## 3. The Broker

Store contracts in a central "Pact Broker".
*   If Frontend changes requirement -> CI fails.
*   If Backend deletes field -> CI fails.
*   **No Integration Environment needed.**

> 🔴 **Rule**: Do not write E2E tests for schema validation. Use Contracts.
