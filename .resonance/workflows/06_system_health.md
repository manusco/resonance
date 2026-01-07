# Workflow: System Health ("The Doctor")

**Primary Roles**: `architect`, `devops`
**Goal**: Holistic deep-dive for stability, currency, and excellence.
**Output**: `docs/reports/HEALTH-[date].md` with actionable Scores.

---

## 1. Trigger
User says: "System Check", "Run diagnostics", or "Health check".

## 2. Phase 1: The Vital Signs (Automated)
Don't guess. Measure.

1.  **Dependencies**: `npm audit` (Security), `npm outdated` (Freshness).
2.  **Lint/Test**: `npm run lint && npm test` (Hygiene).
3.  **Build**: `npm run build` (Integrity).
4.  **Database**: Check migration status (Consistency).

## 3. Phase 2: The Physical (Manual Deep Dive)
Iterate through the layers.

### Layer 1: Foundation (Architect)
*   **Circular Deps**: Is the graph clean?
*   **File Structure**: Are we following DDD? (No "utils" junk drawers).
*   **Code Duplication**: "Rule of Three" violations.

### Layer 2: Logic (Backend/DB)
*   **N+1 Queries**: Inspect logs/code.
*   **Error Handling**: Are we swallowing errors or logging them?

### Layer 3: Surface (Frontend)
*   **Console Errors**: Is the browser shouting at us?
*   **Responsiveness**: Does it break on mobile?

## 4. Phase 3: The Diagnosis (Synthesis)
Assign a **Health Score (0-100)** based on:
*   **Stability** (Tests/Types pass): 40 pts.
*   **Security** (Audit clean): 30 pts.
*   **Maintainability** (Lint/Duplication): 20 pts.
*   **Freshness** (Deps up to date): 10 pts.

## 5. Artifact Generation
Create `docs/reports/HEALTH-[YYYY-MM-DD].md`.

**Template:**
```markdown
# Health Report: [Date]

## 🩺 Logic Vital Signs
**Score**: 85/100 (B+)
- ✅ Build passes.
- ✅ Tests pass (95% coverage).
- ⚠️ Found 3 high-severity vulns (See Security).

## 🔍 Deep Dive Findings
### Critical (Fix NOW)
1. **Security**: Hardcoded API key in `utils/api.ts`.
2. **Database**: Missing index on `orders.user_id`.

### Warnings (Fix Soon)
1. **Frontend**: `Header` component is 400 lines (Split it).
2. **Deps**: `react` is 2 major versions behind.

## ℞ Prescription
- [ ] Run `05_qa.md` to fix Security.
- [ ] Schedule refactor for Header.
```

## 6. Stability Protocol
If Score < 50: **Code Freeze**. No new features until score > 80.
If Score > 90: **Shipping Mode**. Go fast.
