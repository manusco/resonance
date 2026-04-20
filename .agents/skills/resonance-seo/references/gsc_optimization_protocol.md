# Protocol: GSC Intelligence & Search Intent Optimization

> **Status**: Core Implementation Standard
> **Objective**: Harness Google Search Console (GSC) data—via direct API access, UI analysis, or export—to move "Striking Distance" pages into Top 3 positions and secure AI citations.

## 1. The "Striking Distance" Mine (Positions 8-20)

Top 1% experts don't focus on what's already winning; they focus on what's *almost* winning.

### Extraction Strategy
1.  **Filter**: Last 28-90 days.
2.  **Sort**: Average Position between 8 and 20.
3.  **Prioritize by Impressions**: High impressions at Position 12 indicate massive latent demand.
4.  **Identify "Hidden" Queries**: Find queries that the page ranks for but are MISSING from the Title, H1, and First Paragraph.

### The Capture Loop
*   **Query Intent Mapping**: Don't just add keywords. Classify the GSC query as **Informational**, **Transactional**, or **Navigational**. Ensure the page's *Above-the-Fold* content matches the dominant intent.
    *   *Expert Move*: If a page ranks (Pos 12) for a "comparison" query but is a "product" page, restructure it into a comparison layout to satisfy the searcher's intent.
*   **Title/H1 Update**: Inject the high-impression query directly into the Title and H1.
*   **Contextual Injection**: Add a sub-heading (H2) specifically addressing the "Hidden" query if it's not adequately covered.

---

## 2. Entity Hardening (Internal Linking)

Internal links are the skeleton of **Model Trust**. They tell both Google and LLMs which nodes of information are authoritative.

### The Semantic Tightening Rule
*   **Density**: Target ~1 internal link per 50-75 words.
*   **Semantic Anchors**: Never use "click here." Use anchor text that describes the *Entity* of the target page (e.g., "how to optimize vector databases").
*   **Inbound Flow**: Scrape the site for all pages semantically related to your "Striking Distance" page. Point 3-5 new internal links from these related pages back to the target.

---

## 3. GEO Alignment (Answer Engine Optimization)

Once a page moves into the Top 10 via GSC tuning, it must be hardened for **AI Retrieval**.

### The 50-Word Direct Answer
*   **Placement**: Immediately following the `<h1>` or the relevant `<h2>`.
*   **Structure**: `[Question Rephrase] + [Direct Answer (Bold)] + [Nuance]`.
*   **Length**: 40-60 words.
*   **Purpose**: This is the primary extraction point for ChatGPT, Perplexity, and Google AI Overviews.

---

## 4. Maintenance & Monitoring

### The CTR Lever (Snippet Engineering)
If impressions are high but CTR is < 2% in the Top 5:
*   **Analyze the Snippet**: Is the meta description cut off? Does it lack a "Value Hook"?
*   **Add Schema**: Ensure FAQ or Review schema is present to expand the SERP footprint.
*   **Title Psychology**: Use brackets `[2026 Updated]` or specific numbers `7 Best...` to increase the visual salience of the link.

### The Decay & Freshness Audit
*   **Performance Decay**: If a page with high historitcal impressions shows a downward trend in average position over 6 months, it is suffering from **Content Decay**.
*   **The Refresh Protocol**: Update with 3-5 new paragraphs of current data, refresh the publish date, and re-index via GSC API/UI immediately.

### The Link-to-Value Ratio
*   **Internal**: 1 per 50 words (Distribute authority).
*   **External**: 1 per 150 words (Contextual citations to high-authority nodes).

---
*Created by the SEO & Research agents. Enforcing the Outstanding Skills Standard.*
