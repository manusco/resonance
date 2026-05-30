# CSP Headers Protocol (Content Security Policy)

> "Whitelisting is safer than Blacklisting."

## 1. The Policy

You must define exactly where assets can load from.
`default-src 'self'` is the baseline.

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'self' https://analytics.google.com;
  img-src 'self' https://cdn.example.com data:;
  style-src 'self' 'unsafe-inline';
  object-src 'none';
  frame-ancestors 'none';
```

## 2. Nonce-Based CSP (Strict)

For inline scripts, use a cryptographic nonce.
1.  Server generates nonce: `abcd123`
2.  Header: `script-src 'nonce-abcd123'`
3.  HTML: `<script nonce="abcd123">...`
*   **Result**: Attacker injected `<script>` tags (XSS) will fail to execute.

## 3. Reporting

`Content-Security-Policy-Report-Only`
*   Use this to test your policy in production without breaking the app.
*   Send violations to Sentry.

> 🔴 **Rule**: `script-src 'unsafe-inline'` sans nonce is forbidden.
