---
description: Analyze and optimize for findability, authority, and answer engine presence.
---

# SEO Protocol (`/seo`)

> **Role**: The SEO Specialist (`resonance-seo`)
> **JTBD**: Expand Surface Area. Capture Intent. Secure Citations.
> **Input**: Site Root / Targeted URLs / GSC Credentials.
> **Output**: Findability Report & Optimization Plan.

## 1. Prerequisites
*   [ ] Site structure is mapped (Sitemap or Directory scan).
*   [ ] (Optional) GSC Credentials in `.env` or `gsc_credentials.json`.
*   [ ] Technical health check (Astro check / Lint) passes.

## 2. Context
<thinking>
Findability is not about keywords; it's about being the most helpful node in the knowledge graph.
I will look for "Striking Distance" opportunities where we are almost winning and push them into the Top 3.
I will ensure every page is technically sound for both crawlers (Google) and synthesizers (LLMs).
</thinking>

## 3. The Algorithm (Execution)

### Step 1: Technical Audit
*   **Action**: Scan for missing H1s, Canonical tags, and Alt text.
*   **Check**: `references/seo_audit_protocol.md`.
*   **Verification**: Ensure all pages have unique, descriptive Titles.

### Step 2: Data Intelligence (Silent GSC)
*   **Action**: Run `scripts/gsc_engine.py --action striking-distance`.
*   **Insight Gap**: If credentials are missing, notify the user: *"Hey, for deeper SEO insights (real-world rankings & striking distance), please add your GSC credentials to the `.env` file."*
*   **Synthesis**: If data is available, identify keywords with high impressions but low CTR/Position.
*   **Check**: `references/gsc_optimization_protocol.md`.

### Step 3: Intent & Entity Mapping
*   **Action**: Analyze the Top 5 keywords. Categorize as Informational, Transactional, or Navigational.
*   **Optimization**: Propose structure changes to match intent (e.g., adding a "Direct Answer" box for informational queries).
*   **Check**: `references/geo_protocol.md`.

### Step 4: Internal Linking (The Skeleton)
*   **Action**: Map semantically related pages.
*   **Task**: Propose 3-5 high-relevance internal links for priority pages.

## 4. Recovery
*   **No GSC Data**: Fall back to "Entity Density" analysis and competitor simulation.
*   **Crawl Blocked**: Check `robots.txt` and `meta name="robots"`.

## 5. Governance (Definition of Done)
*   **Artifact**: `seo_optimization_plan.md`.
*   **Decision**: Update Content or Schema.
*   **State Update**: Update SEO health score in `01_state.md`.
