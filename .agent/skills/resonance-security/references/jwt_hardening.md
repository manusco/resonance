# JWT Hardening Protocol

> "A token is a key. Treats it like one."

## 1. Storage (The Holy War)

**Where do I store the Access Token?**

1.  **LocalStorage**: ❌ **BANNED**. (Vulnerable to XSS).
2.  **Cookie (HttpOnly)**: ✅ **REQUIRED**. (Immune to XSS).

## 2. The Rotation Dance (Refresh Tokens)

Access Tokens should live for **15 minutes**.
Refresh Tokens should live for **7 days**.

**The Flow:**
1.  Client: "My Access Token expired (401)."
2.  Client: "Here is my Refresh Token (Cookie)."
3.  Server: "Verify Refresh Token. Is it revoked in Redis?"
4.  Server: "Here is a new Access Token."

## 3. The Algorithm

*   **HS256**: Symmetric. (Fast). Only if you control Auth + Resource Server.
*   **RS256**: Asymmetric. (Robust). Use if Auth and API are separate.

> 🔴 **Rule**: Never allow `alg: "none"`.
