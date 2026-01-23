# Verified Security Checklist

> **Purpose**: A mandatory verification list for all code reviews and architectural decisions.
> **Philosophy**: "Safe by Default". If it's not explicitly verified, it's insecure.

## 1. Secrets Management

### ❌ NEVER Do This
```typescript
const apiKey = "sk-proj-xxxxx"  // Hardcoded secret
const dbPassword = "password123" // In source code
```

### ✅ ALWAYS Do This
```typescript
const apiKey = process.env.OPENAI_API_KEY
if (!apiKey) throw new Error('OPENAI_API_KEY not configured')
```

### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords.
- [ ] All secrets loaded via `process.env` (or `unifiedConfig`).
- [ ] `.env` files are in `.gitignore`.
- [ ] Secrets are injected at runtime (e.g., Vercel/Railway env vars).

---

## 2. Input Validation (Zero Trust)

### ❌ NEVER Assume Valid Input
```typescript
// Dangerous: passing raw input to DB
db.users.create(req.body)
```

### ✅ ALWAYS Validate Borders
```typescript
import { z } from 'zod'
const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0)
})
const validated = UserSchema.parse(req.body)
```

### Verification Steps
- [ ] All external inputs (API body, query params) verified with Zod schemas.
- [ ] File uploads restricted by size (e.g., 5MB) and strictly checked types.
- [ ] Whitelist validation used (allow "a,b,c", not "block x,y,z").

---

## 3. SQL Injection Prevention

### ❌ NEVER Concatenate SQL
```typescript
const query = `SELECT * FROM users WHERE email = '${userEmail}'` // VULNERABLE
```

### ✅ ALWAYS Use Parameterized Queries
```typescript
// Safe - parameterized query
await db.query('SELECT * FROM users WHERE email = $1', [userEmail])
// Safe - ORM
await prisma.user.findUnique({ where: { email } })
```

### Verification Steps
- [ ] No string concatenation in SQL queries.
- [ ] Primitives mapped to parameters ($1, $2) or ORM methods used.

---

## 4. Authentication & Authorization

### ❌ NEVER Store Tokens in LocalStorage
LocalStorage is vulnerable to XSS.

### ✅ ALWAYS Use HttpOnly Cookies
```typescript
res.setHeader('Set-Cookie', `token=${token}; HttpOnly; Secure; SameSite=Strict`)
```

### Verification Steps
- [ ] Tokens stored in `HttpOnly` Secure cookies.
- [ ] Authorization checks performed server-side for *every* sensitive action.
- [ ] Row Level Security (RLS) enabled for Supabase/Postgres.

---

## 5. XSS & CSRF Prevention

### ❌ NEVER Render Raw HTML
```jsx
<div dangerouslySetInnerHTML={{ __html: userContent }} /> // VULNERABLE
```

### ✅ ALWAYS Sanitize
```typescript
import DOMPurify from 'isomorphic-dompurify'
const clean = DOMPurify.sanitize(userContent)
// Then it is safe to render 'clean'
```

### Verification Steps
- [ ] User-provided HTML sanitized with DOMPurify.
- [ ] Content Security Policy (CSP) headers configured.
- [ ] CSRF tokens used for state-changing operations (if not using SameSite=Strict).

---

## 6. Rate Limiting

### Verification Steps
- [ ] Global rate limit enabled (e.g., 100 req/15min).
- [ ] Distinct strict rate limits for Auth endpoints (Login/Register).
- [ ] Expensive endpoints (e.g., AI generation) have tighter limits.

---

## 7. Dependencies

### Verification Steps
- [ ] `npm audit` returns clean.
- [ ] No unused dependencies.
- [ ] Lockfiles (`package-lock.json`) committed.
