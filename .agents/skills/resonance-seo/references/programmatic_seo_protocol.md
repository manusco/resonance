# Protocol: Programmatic Content Architecture (100k+ Scale)
> **Objective**: Engineer a programmatic SEO system capable of scaling to 100,000+ unique, high-value pages without triggering "Thin Content" penalties.

## 1. The Core Philosophy
Scale is not about **copy-paste**. Scale is about **rendering**.
We treat SEO pages as **application states**, not static markdown files.

**The Equation:**
`Structured Data` + `Intent-Matched Logic` + `Incremental Rendering` = `Platinum Scale`

---

## 2. Infrastructure & Scalability
Running 100k pages requires engineering, not just content writing.

### A. Rendering Strategy (ISR > SSR > Static)
*   **Best Practice**: Use **Incremental Static Regeneration (ISR)**.
    *   *Why*: Building 100k static pages takes hours. SSR is too slow (TTFB). ISR builds on demand and caches.
*   **Stale-While-Revalidate**: Serve stale content while fetching dynamic updates in the background.

### B. Sitemap Partitioning (The 50k Rule)
Google has a hard limit of 50,000 URLs per sitemap.
*   **Pattern**: `sitemap-index.xml` pointing to:
    *   `sitemap-products-001.xml` (Page 0-49,999)
    *   `sitemap-products-002.xml` (Page 50,000+)
    *   `sitemap-articles.xml`

### C. Performance (Core Web Vitals)
*   **Image Optimization**: Programmatic images must be compressed at the source or via edge functions (Cloudinary/Next/Image).
*   **Bundle Size**: Do NOT load heavy interactivity (React Hydration) on purely informational pSEO pages. Use "Islands Architecture" or plain HTML where possible.

---

## 3. The "Anti-Thin" Content Layer
To survive the "Helpful Content Update", pages must be >40% unique.

### Variable Swapping vs. Logic Injection
*   ❌ **Bad (Variable Swapping)**:
    *   "Best Plumbers in **Austin**" -> "Best Plumbers in **Boston**"
    *   *Result*: Deindexed (Duplicate Content).
*   ✅ **Good (Logic Injection)**:
    *   **Austin Page**: "Austin has **hard water**, so standard heaters fail faster. Here are 3 plumbers specializing in **water softening**."
    *   **Boston Page**: "Boston has **older pipes** (pre-1950). Here are 3 plumbers specializing in **lead pipe replacement**."
    *   *Mechanism*: `if (city.water_hardness > 7) { renderSoftenerAdvice() }`

---

## 4. Metadata Engineering (The Head)
Dynamic metadata must be programmatic, not static.

### Dynamic Title Logic
```typescript
const generateTitle = (data: CityData) => {
  if (data.population > 1000000) {
     return `Top 10 Rated Plumbers in ${data.city} (24/7 Emergency Services)`;
  }
  return `Best Local Plumbers near ${data.city} | Verified Reviews`;
}
```

### Canonical Strategy
*   **Self-Referencing**: Every pSEO page must point to itself.
*   **Consolidation**: If "New York" and "NYC" pages exist, choose ONE as canonical to prevent cannibalization.

### Structured Data (Schema.org)
Every page MUST have specific JSON-LD injection:
1.  **BreadcrumbList**: Critical for structure. `Home > Services > [State] > [City]`.
2.  **Dataset / Table**: If showing data rows.
3.  **FAQPage**: Generated from unique data (e.g., "How much does a plumber cost in [City]?").
4.  **LocalBusiness**: If displaying a specific entity.

---

## 5. Hub & Spoke Internal Linking
Isolate authority flow to prevent "orphans".

**The Topology:**
*   **Hub (State Page)**: Links to top 20 Cities.
*   **Spoke (City Page)**: Links back to State, and to "Nearby Cities" (neighbors).
    *   *Algorithm*: `SELECT * FROM cities WHERE distance < 50km LIMIT 5`.
*   **Cross-Link**: "Related Services in [City]" (e.g., Plumber links to Electrician in Austin).

---

## 6. Implementation Checklist
- [ ] **Data Source**: Validated JSON/CSV with high uniqueness factors.
- [ ] **Routing**: Clean slugs (`/service/city`) without query params.
- [ ] **Templates**: specialized layouts for different data types.
- [ ] **Metadata**: Dynamic factories for Titles and OG Images.
- [ ] **Sitemaps**: Split logic implemented.
- [ ] **Performance**: Lighthouse score > 90 on template sample.
