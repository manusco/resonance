# Workflow: Quality Assurance ("The Shield")

**Primary Roles**: `qa`, `security`, `performance`
**Goal**: **Prove the system is broken.** (If you fail to break it, it is ready).
**Output**: A Validation Report confirming reliability.

---

## 1. Trigger
User says: "Test this", "Release candidate", or "Audit project".

## 2. Phase 1: The Offensive (Role: `qa`)
Don't test the happy path. Attack the system.

1.  **Edge Cases**: Input `null`, `undefined`, emojis, huge strings.
2.  **Race Conditions**: Click buttons twice.
3.  **Mobile Check**: Resize window to 320px. Does it explode?

## 3. Phase 2: The Trap (Role: `security`)
Run a STRIDE check.

1.  **Access Control**: Can User A invoke User B's endpoint?
2.  **Injection**: Can I put SQL in the search bar?
3.  **Secrets**: Grep for "sk-", "api_key" in the codebase.

## 4. Phase 3: The Stopwatch (Role: `performance`)
1.  **Core Web Vitals**: Run Lighthouse. LCP < 2.5s?
2.  **Queries**: Check logs for N+1 queries.

## 5. Artifact Generation
Create a report.

**Template:**
```markdown
# QA Report: [Version/Feature]

## 1. Destructive Testing
- [x] Null Inputs: Handled gracefully.
- [x] Network Disconnect: Showed "Offline" toast.

## 2. Security Audit
- [x] No secrets in build.
- [x] Auth enforced on all endpoints.

## 3. Performance
- LCP: 1.2s (Pass)
- API Latency: 45ms (Pass)

**Verdict**: READY FOR PRODUCTION.
```
