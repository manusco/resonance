# CORS Policy Protocol

> "The bouncer at the door."

## 1. The Whitelist

Never use `Access-Control-Allow-Origin: *`.

**Dev:**
*   `localhost:3000`

**Prod:**
*   `https://app.example.com`

## 2. The Preflight (OPTIONS)

Browsers send an `OPTIONS` request before a `POST`.
*   You must handle `OPTIONS` with `204 No Content`.
*   You must set `Access-Control-Max-Age` to cache the preflight (e.g., 86400s) to save latency.

## 3. Credentials

If you use Cookies (HttpOnly), you MUST set:
*   `Access-Control-Allow-Credentials: true`

> 🔴 **Rule**: If your API is public, use a Gateway / API Key. Do not open CORS globally.
