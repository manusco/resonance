# JWT Hardening Protocol

> **Objective**: Secure JSON Web Token implementation against leakage, replay, and forgery.

## 1. Core Implementation Rules

### ❌ NEVER
- Store sensitive data (PII, passwords) in the JWT payload.
- Use weak secrets or default keys.
- Store JWTs in `localStorage` (XSS vulnerability).
- Allow "none" algorithm.

### ✅ ALWAYS
- Sign with strong secrets (min 256-bit).
- Use `HttpOnly; Secure; SameSite=Strict` cookies.
- Set short expiration for Access Tokens (e.g., 15-60 min).
- Use Refresh Tokens for long-lived sessions.

---

## 2. Secure Implementation Pattern

### Generating Tokens
```typescript
const accessToken = jwt.sign(
  { userId: user.id, role: user.role }, // Minimal payload
  process.env.JWT_SECRET,
  { 
    expiresIn: '15m', 
    algorithm: 'HS256',
    issuer: 'resonance-auth',
    audience: 'resonance-api'
  }
);
```

### Refresh Token Rotation
1.  **Issue**: Generate random opaque string (or long-lived JWT) as Refresh Token.
2.  **Store**: Hash it (bcrypt/argon2) and store in DB `refresh_tokens` table.
3.  **Rotate**: On use, delete the old Refresh Token and issue a new one. This detects token theft (if potential thief tries to use old one, invalidate all).

---

## 3. Storage Strategy

| Storage | Security | Recommendation |
| :--- | :--- | :--- |
| **LocalStorage** | 🔴 Low (XSS) | **NEVER** for sensitive apps. |
| **SessionStorage** | 🔴 Low (XSS) | **NEVER** for sensitive apps. |
| **Cookie (HttpOnly)** | 🟢 High (CSRF needed) | **PREFERRED**. Immune to XSS. |

**Cookie Configuration:**
```javascript
res.cookie('access_token', token, {
  httpOnly: true,    // Prevent JS access
  secure: true,      // HTTPS only
  sameSite: 'strict',// CSRF protection
  maxAge: 15 * 60 * 1000 // 15 mins
});
```

---

## 4. Verification Checklist

- [ ] Secret is loaded from env var (not hardcoded).
- [ ] Algorithm is explicitly set (no `none`).
- [ ] Expiration (`exp`) is verified.
- [ ] Issuer (`iss`) and Audience (`aud`) are verified.
- [ ] Token is revoked/blacklisted on logout (requires stateful check or short expiry).
