# Protocol: GSC Intelligence and Search Intent Optimization

> **Status**: Core Implementation Standard
> **Objective**: Use Google Search Console (GSC) data from direct API access, UI analysis, or exports to find evidence-backed search opportunities, move "Striking Distance" pages toward Top 3 positions, and improve AI citation readiness.

## Contents

- [0. GSC Evidence Preflight](#0-gsc-evidence-preflight)
- [1. The "Striking Distance" Mine (Positions 8-20)](#1-the-striking-distance-mine-positions-8-20)
- [2. Entity Hardening (Internal Linking)](#2-entity-hardening-internal-linking)
- [3. GEO Alignment (Answer Engine Optimization)](#3-geo-alignment-answer-engine-optimization)
- [4. Maintenance and Monitoring](#4-maintenance-and-monitoring)

## 0. GSC Evidence Preflight

GSC-backed recommendations must start with the evidence boundary, not the fix.
Before diagnosing a ranking, CTR, indexing, sitemap, or cannibalization issue,
record:

1. **Access and capability**: Confirm the available GSC source, such as API,
   UI screenshot, CSV export, or a trusted report. If live access is unavailable,
   continue with on-page analysis and mark every GSC-dependent conclusion as
   unverified.
2. **Exact property identity**: Use the exact GSC property string supplied by
   the source. Distinguish URL-prefix properties from domain properties. If the
   site has multiple plausible properties, ask before comparing or prescribing.
3. **Retrieval metadata**: Capture retrieval time, timezone, reporting period,
   dimensions, filters, row limits, sorting, pagination status, and whether the
   data is final, preliminary, or unknown. Retrieval time is not data freshness.
4. **Completeness limits**: Pagination, row limits, and sampled exports can hide
   long-tail rows. Disclose truncation. Do not treat missing rows as zero.
5. **Action authority**: Keep audits read-only unless the user explicitly
   authorizes the exact account or sitemap mutation. A tool's write capability
   is not approval to use it.

### Evidence-to-Recommendation Loop

Every GSC-backed recommendation needs:

- **Observed evidence**: Query, page, date range, device, country, index verdict,
  sitemap status, or other concrete signal.
- **Hypothesis**: The user problem the evidence suggests, such as intent
  mismatch, weak snippet, crawl block, canonical conflict, or content decay.
- **Action**: The smallest change likely to test the hypothesis.
- **Follow-up window**: A comparable period to check after the change. Prefer
  finalized data for before/after comparisons. If preliminary data is used, label
  it clearly.

## 1. The "Striking Distance" Mine (Positions 8-20)

Top 1% experts don't focus on what's already winning; they focus on what's *almost* winning.

### Extraction Strategy
1. **Filter**: Last 28-90 days, with property, country, device, and data-state
   metadata recorded.
2. **Sort**: Average Position between 8 and 20.
3. **Prioritize by impressions**: High impressions at Position 12 indicate
   latent demand, but verify the row set is complete enough for the decision.
4. **Identify "hidden" queries**: Find queries that the page ranks for but are
   missing from the Title, H1, and first paragraph.

### The Capture Loop

* **Query Intent Mapping**: Do not just add keywords. Classify the GSC query as
  **Informational**, **Transactional**, or **Navigational**. Ensure the
  above-the-fold content matches the dominant intent.
  * **Expert Move**: If a page ranks around Position 12 for a comparison query
    but is a product page, restructure it into a comparison layout to satisfy the
    searcher's intent.
* **Title/H1 Update**: Inject the high-impression query directly into the Title
  and H1 only when the query matches the page's true job.
* **Contextual Injection**: Add a sub-heading (H2) specifically addressing the
  hidden query if it is not adequately covered.

---

## 2. Entity Hardening (Internal Linking)

Internal links are the skeleton of **Model Trust**. They tell both Google and LLMs which nodes of information are authoritative.

### The Semantic Tightening Rule
* **Density**: Target ~1 internal link per 50-75 words.
* **Semantic Anchors**: Never use "click here." Use anchor text that describes
  the *Entity* of the target page, such as "how to optimize vector databases".
* **Inbound Flow**: Scrape the site for all pages semantically related to your
  "Striking Distance" page. Point 3-5 new internal links from these related
  pages back to the target.

---

## 3. GEO Alignment (Answer Engine Optimization)

Once a page moves into the Top 10 via GSC tuning, it must be hardened for **AI Retrieval**.

### The 50-Word Direct Answer
* **Placement**: Immediately following the `<h1>` or the relevant `<h2>`.
* **Structure**: `[Question Rephrase] + [Direct Answer (Bold)] + [Nuance]`.
* **Length**: 40-60 words.
* **Purpose**: This is the primary extraction point for ChatGPT, Perplexity, and
  Google AI Overviews.

---

## 4. Maintenance and Monitoring

### The CTR Lever (Snippet Engineering)
If impressions are high but CTR is < 2% in the Top 5:

* **Analyze the snippet**: Is the meta description cut off? Does it fail to
  match the searcher's immediate job?
* **Add schema**: Ensure eligible schema is present to clarify the result and
  expand the SERP footprint.
* **Title psychology**: Use specific numbers or useful freshness signals only
  when they are truthful and match the page.

### The Decay & Freshness Audit
* **Performance decay**: If a page with high historical impressions shows a
  downward trend in average position over 6 months, it may be suffering from
  **Content Decay**. Check technical changes, SERP changes, and demand changes
  before assuming stale content is the cause.
* **Refresh protocol**: Update the page with current, useful material only when
  the evidence supports a freshness or completeness gap. Keep publish and
  modified dates honest. Use URL inspection to understand Google's indexed view,
  and request recrawl only when the user has authorized that exact action.

### The Link-to-Value Ratio
* **Internal**: 1 per 50 words when the links help users move to related value.
* **External**: 1 per 150 words when citations strengthen the claim.
