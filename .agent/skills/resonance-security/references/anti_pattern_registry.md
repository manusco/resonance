# Security Anti-Pattern Registry ("The Hunter's Guide")

> **Origin**: Adapted from [Arcanum-Sec](https://github.com/Arcanum-Sec/sec-context).
> **Mandate**: `resonance-security` must BLOCK any code matching these patterns.

## 🔴 Critical Blocking Registry (The Top 10)

These patterns have a high probability of appearing in AI-generated code. They are strictly forbidden.

### 1. Slopsquatting (Dependency Hallucination)
*   **The Risk**: AI invents packages like `html-sanitizer-plus` that don't exist. Attackers register them with malware.
*   **bad**: `import { sanitize } from "non-existent-lib";`
*   **Good**: Verification. `npm view non-existent-lib` before approving.
*   **Rule**: **NEVER** approve an import without verifying existence and reputation (Stars > 500, Maintenance < 6mo).

### 2. XSS (Direct String Concatenation)
*   **The Risk**: AI loves `"<div>" + input + "</div>"`. This fails 86% of the time.
*   **Bad**: `return "<h1>" + user.name + "</h1>";`
*   **Good**: `return <h1>{user.name}</h1>;` (JSX escapes automatically).
*   **Rule**: **No string concatenation** for HTML/SQL/Shell.

### 3. Hardcoded Secrets (The "Quick Fix")
*   **The Risk**: `const API_KEY = "sk-..."` for testing.
*   **Bad**: Providing a "placeholder" key that gets committed.
*   **Good**: `process.env.API_KEY`.
*   **Rule**: **0 Tolerance**. Use `.env.example` for templates.

### 4. SQL Injection (f-strings/template literals)
*   **The Risk**: `const query = \`SELECT * FROM users WHERE id = ${id}\`;`
*   **Bad**: Interpolating variables directly into query strings.
*   **Good**: `db.query('SELECT * FROM users WHERE id = $1', [id])`
*   **Rule**: All DB queries **MUST** use parameterized binding.

### 5. Authentication Bypass (The Logic Flaw)
*   **The Risk**: Checks that look correct but fail. `if (user.isAdmin)` (client-side verification).
*   **Bad**: Trusting frontend state for admin actions.
*   **Good**: `if (!ctx.session.user.claims.includes('admin')) throw Forbidden;`
*   **Rule**: Auth checks **MUST** happen on the server/middleware.

### 6. Missing Input Validation (The Root Cause)
*   **The Risk**: Assuming `req.body.age` is a number.
*   **Bad**: `const age = req.body.age;` (Could be an object/array causing NoSQLi).
*   **Good**: `const { age } = z.object({ age: z.number() }).parse(req.body);`
*   **Rule**: **All inputs** (API, CLI, File) must be passed through Zod/Pydantic schemas.

### 7. Command Injection (Shell Execution)
*   **The Risk**: `exec("git checkout " + branch)`
*   **Bad**: Passing user input to `exec` or `spawn` with shell: true.
*   **Good**: `spawn('git', ['checkout', branch], { shell: false })`
*   **Rule**: Avoid `child_process.exec`. Use `spawn` with argument arrays.

### 8. Missing Rate Limiting (DOS Vector)
*   **The Risk**: Public APIs allowing valid but infinite requests.
*   **Bad**: No `ThrottlerGuard` on public endpoints.
*   **Good**: Limits per IP/User (e.g., 100 req/min).
*   **Rule**: All public routes **MUST** have rate limiting.

### 9. Excessive Data Exposure (DTO Leak)
*   **The Risk**: `return user;` (Dumps `password_hash`, `email`, `history`).
*   **Bad**: Returning a raw ORM entity.
*   **Good**: `return new UserResponseDto(user);` (Allowlist fields).
*   **Rule**: Never return internal entities. Map to Response DTOs.

### 10. Unrestricted File Upload (RCE)
*   **The Risk**: Accepting `.php` or `.exe` files.
*   **Bad**: Trusting `file.mimetype`.
*   **Good**: Re-encoding images or validating "Magic Numbers" (File Signatures).
*   **Rule**: Strict Allowlist on file extensions + Virus Scan (if possible) + Rename on disk.
