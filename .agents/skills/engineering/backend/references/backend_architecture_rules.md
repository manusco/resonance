# Backend Architecture Rules

> **Objective**: Maintain a clean, scalable, and verifiable backend structure. "Routes Route, Controllers Control."

## 1. The 7 Golden Rules

### 1. Routes Only Route
**❌ Anti-Pattern**: Business logic in route definitions.
**✅ Standard**: Routes purely delegate to Controllers.
```typescript
// Good
router.post('/users', (req, res) => userController.create(req, res));
```

### 2. Controllers Control (BaseController)
**❌ Anti-Pattern**: Ad-hoc error handling in every function.
**✅ Standard**: All controllers extend `BaseController` for consistent responses and error boundary handling.

### 3. Service Layer Isolation
**❌ Anti-Pattern**: Controllers access the Database directly.
**✅ Standard**: Controllers call Services. Services call Repositories.
*   *Flow*: `Request -> Controller -> Service -> Repository -> DB`.

### 4. Configuration Purity
**❌ Anti-Pattern**: Using `process.env.DB_HOST` scattered in code.
**✅ Standard**: Use `unifiedConfig` singleton. Validation happens at startup.

### 5. Input Boundaries (Zod)
**❌ Anti-Pattern**: Manually checking `if (req.body.email)`.
**✅ Standard**: Zod schemas for ALL inputs (Body, Query, Params).
```typescript
const payload = CreateUserSchema.parse(req.body); // Auto-throws 400 on fail
```

### 6. Observability First
**❌ Anti-Pattern**: `console.log('error', err)`.
**✅ Standard**: Errors go to Sentry (or Logger). Metrics go to Prometheus/Datadog.

### 7. Repository Pattern
**❌ Anti-Pattern**: Complex Prisma queries inside Services.
**✅ Standard**: Encapsulate DB logic in Repositories. Makes services testable (mockable repositories).
