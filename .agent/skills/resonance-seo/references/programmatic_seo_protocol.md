# Protocol: Programmatic Content Architecture
> **Focus**: Engineering Scalable Content Systems (Programmatic SEO)
> **Resonance Phase**: Execution / Scale

## 1. System Overview
Programmatic SEO (pSEO) is **not** about "generating spam." It is the engineering practice of using **structured data** + **template engines** to solve long-tail search intent at scale.

**The Core Equation**:
`Unique Data Source` + `User Intent Template` + `Scalable Rendering` = `High-Value Page Instance`

## 2. The Architecture (The 12 Patterns)
Instead of "guessing" what to build, implement one of these proven architectural patterns.

### Type A: The Aggregators (Data-Heavy)
1.  **The Directory Engine** (`/directory/[category]`)
    *   *Input*: Structured database of tools, companies, or assets.
    *   *Value*: Filtering, sorting, and comparison logic that a human user cannot perform manually.
2.  **The Location Grid** (`/[service]/[city]`)
    *   *Input*: Geo-data, local pricing, regional regulations.
    *   *Value*: Hyper-local specificity. **Warning**: Do not just swap city names. Inject local data (weather, population, specific laws).
3.  **The Comparison Matrix** (`/compare/[x]-vs-[y]`)
    *   *Input*: Feature flags, pricing tiers, limiting specifications.
    *   *Value*: Unbiased side-by-side analysis. "Decision Support System" for the user.

### Type B: The Utilities (Function-Heavy)
4.  **The Conversion Engine** (`/convert/[from]-to-[to]`)
    *   *Input*: Mathematical formulas, exchange rates.
    *   *Value*: Instant utility. Lowest friction possible (no sign-ups).
5.  **The Template Factory** (`/templates/[type]`)
    *   *Input*: Downloadable assets (PDF, notion, figma).
    *   *Value*: "speed to zero-state" (solving the blank page problem).
6.  **The Integration Hub** (`/connect/[app]-to-[app]`)
    *   *Input*: API documentation, webhook triggers.
    *   *Value*: Explaining the *possibility space* of two tools working together.

### Type C: The Knowledge Graph (Information-Heavy)
7.  **The Glossary Graph** (`/learn/[term]`)
    *   *Input*: Definitions, related concepts, etymology.
    *   *Value*: Conceptual clarity and internal linking density.
8.  **The Curator** (`/best/[category]`)
    *   *Input*: Scored lists, weighted rankings.
    *   *Value*: Curation as a service. Saving the user research time.

## 3. Data Pipeline & Integrity
Garbage In, Garbage Out. Your pSEO system is only as good as your `Data Source`.

### Unacceptable Data Sources (The Spam Zone)
*   [ ] Public, commoditized data everyone else uses.
*   [ ] AI-hallucinated facts without verification.
*   [ ] Shallow Variable Swapping (e.g., only changing "New York" to "Boston").

### Elite Data Sources (The Moat)
*   [x] **Proprietary Telemetry**: Data your product generates (e.g., "Average typing speed of 1M users").
*   [x] **Aggregated API Synthesis**: Combining Weather API + Traffic API to create unique insights.
*   [x] **User Generated Graphs**: Reviews, comments, and community submissions.

## 4. Engineering Quality Assurance (QA)
Treat pSEO pages like code. They need unit tests.

### Thin Content Detector
Before deploying 1,000 pages, run this audit on a sample size (n=10):
1.  **Uniqueness Ratio**: Is >40% of the DOM unique to this specific URL (vs the template)?
2.  **Intent Match**: Does the page actually *solve* the `[query]`?
    *   *Bad*: A page for "Plumbers in NYC" that lists no plumbers.
    *   *Good*: A page with a verified list of 20 NYC plumbers with licenses.

## 5. URL & Routing Strategy
*   **Subfolders > Subdomains**: Keep equity on the root domain (`example.com/templates/` not `templates.example.com`).
*   **Clean Slugs**: `/compare/linear-vs-jira` (No query params for indexable pages).
*   **Breadcrumb Logic**: Ensure the parent category is navigable.

## 6. Implementation Checklist
- [ ] **Data Model**: Defined schema for the entity (e.g., `City`, `Tool`, `Integration`).
- [ ] **Template**: Built high-performance component (React/Astro/Liquid).
- [ ] **Internal Linking**: "Hub and Spoke" connectivity established.
- [ ] **Sitemap Partitioning**: Split XML sitemaps if >10k URLs (`sitemap-locations.xml`).
- [ ] **Indexer Strategy**: Slow roll-out to prevent "Crawl Budget" exhaustion.
