# Protocol: GSC Intelligence & Search Intent Optimization

> **Status**: Core Implementation Standard
> **Objective**: Harness Google Search Console (GSC) data-via direct API access, UI analysis, or export-to move "Striking Distance" pages into Top 3 positions and secure AI citations.

## 0. GSC Evidence Preflight

GSC-backed recommendations start with the evidence boundary, not the fix.

1. Confirm the available source: API, UI evidence, export, or trusted report. Without live evidence, mark every GSC-dependent conclusion as unverified.
2. Record the exact property identity and distinguish URL-prefix from domain properties.
3. Capture retrieval time, timezone, reporting period, dimensions, filters, sorting, row limits, pagination, and whether the data is final, preliminary, or unknown.
4. Disclose truncation and never treat missing rows as zero.
5. Keep the audit read-only unless the user authorizes the exact account or sitemap mutation.

Every recommendation must name the observed evidence, the hypothesis, the smallest action that tests it, and a comparable follow-up window.

## 1. The "Striking Distance" Mine (Positions 8-20)

Top 1% experts don't focus on what's already winning; they focus on what's *almost* winning.

### Extraction Strategy
1.  **Filter**: Last 28-90 days.
2.  **Segment**: Find pages and queries close enough to their target result set that a focused change can be measured. Position bands are discovery filters, not guarantees.
3.  **Prioritize by opportunity**: Compare impressions, clicks, position, page job, business value, and the reliability of the sample.
4.  **Identify "Hidden" Queries**: Find queries that the page ranks for but are MISSING from the Title, H1, and First Paragraph.

### The Capture Loop
*   **Query Intent Mapping**: Don't just add keywords. Classify the GSC query as **Informational**, **Transactional**, or **Navigational**. Ensure the page's *Above-the-Fold* content matches the dominant intent.
    *   *Expert Move*: If a page ranks (Pos 12) for a "comparison" query but is a "product" page, restructure it into a comparison layout to satisfy the searcher's intent.
*   **Title/H1 Update**: Rewrite only when the verified query and dominant intent are a better description of the page's actual job. Keep titles readable and truthful.
*   **Contextual Injection**: Add a sub-heading (H2) specifically addressing the "Hidden" query if it's not adequately covered.

---

## 2. Entity Hardening (Internal Linking)

Internal links are the skeleton of **Model Trust**. They tell both Google and LLMs which nodes of information are authoritative.

### The Semantic Tightening Rule
*   **Relevance**: Add a link when it helps a reader or crawler discover a related page, understand the relationship, or complete the next task. Do not optimize to a density quota.
*   **Semantic Anchors**: Never use "click here." Use anchor text that describes the *Entity* of the target page (e.g., "how to optimize vector databases").
*   **Inbound Flow**: Find contextually related pages and add only the inbound links that fit their content and navigation job.

---

## 3. GEO Alignment (Answer Engine Optimization)

Once a page moves into the Top 10 via GSC tuning, it must be hardened for **AI Retrieval**.

### The Direct Answer Passage
*   **Placement**: Immediately following the `<h1>` or the relevant `<h2>`.
*   **Structure**: `[Question Rephrase] + [Direct Answer (Bold)] + [Nuance]`.
*   **Length**: As short as the complete, accurate answer allows. Do not pad or cut it to a fixed word count.
*   **Purpose**: Give readers and answer engines a self-contained passage whose claims remain clear outside the surrounding page.

---

## 4. Maintenance & Monitoring

### The CTR Lever (Snippet Engineering)
If CTR underperforms comparable queries, pages, devices, countries, or prior periods after position and SERP features are accounted for:
*   **Analyze the Snippet**: Is the meta description cut off? Does it lack a "Value Hook"?
*   **Check Schema Eligibility**: Use `schema_types_current.md`; recommend markup only when the page content and Google's current eligibility rules support it.
*   **Test the Title**: Make the value and page job clear without manufactured dates, numbers, or promises.

### The Decay & Freshness Audit
*   **Performance Change**: A downward trend is an observation, not a diagnosis. Check technical changes, indexing, SERP composition, demand, competitors, intent, and measurement comparability before proposing content decay.
*   **The Refresh Protocol**: Update only when evidence supports a freshness, accuracy, or completeness gap. Keep publish and modified dates honest. Use URL inspection to understand Google's indexed view, and request recrawl only when the user authorizes that exact action.

### The Link-to-Value Test
*   **Internal**: Link when the destination advances the reader's task or clarifies the site's information structure.
*   **External**: Cite the primary or best available source for material claims. Link count follows evidence needs, not word count.
