# Search Experience Optimization (SXO) Protocol

> Why well-optimized pages still fail to rank: the page-type mismatch problem.

## 1. Core Insight

A page can score 95/100 on technical SEO and still fail to rank because it is the **wrong page type** for the keyword. If Google shows 8 product pages and 2 comparison pages for your keyword, your blog post will never break through — regardless of optimization.

SXO bridges SEO (what Google rewards) and UX (what users need).

---

## 2. SERP Backwards Analysis

Read the SERP *before* optimizing. For the target keyword:

1. **Classify top 10 results** by page type:
   - Product page, comparison, how-to, listicle, tool/calculator, landing page, blog post, video, forum
2. **Determine SERP consensus**:
   - >60% one type = strong consensus
   - 40-60% = mixed signals
   - <40% = fragmented (opportunity for differentiation)
3. **Record SERP features**: Featured snippet format, PAA questions, ads, related searches, AI Overview, Knowledge panel

---

## 3. Page-Type Mismatch Detection

| Your Page Type | SERP Expects | Severity | Action |
|----------------|-------------|----------|--------|
| Blog Post | Product Pages | CRITICAL | Create dedicated product page |
| Blog Post | Comparison | HIGH | Restructure as comparison with matrix |
| Product | Informational | HIGH | Add educational content layer |
| Landing Page | Tool/Calculator | HIGH | Build interactive component |
| Service Page | Local Results | MEDIUM | Add location signals + local schema |
| Type match | — | ALIGNED | Focus on depth and UX |

---

## 4. User Story Derivation

From SERP signals, derive user stories:

- **PAA questions** → knowledge gaps and concerns
- **Ad copy themes** → commercial triggers and value propositions
- **Related searches** → search journey (what comes before/after)
- **Featured snippet format** → expected answer structure
- **AI Overview** → what Google considers the definitive answer

**Template:**
```
As a [persona from signal],
I want to [goal from query intent],
because [driver from ad copy / PAA tone],
but I'm blocked by [barrier from PAA / related searches].
```

Generate 3-5 user stories covering primary intent angles.

---

## 5. Gap Analysis (7 Dimensions)

| Dimension | What to Compare | Max Score |
|-----------|----------------|-----------|
| Page Type | Target type vs SERP dominant type | 15 |
| Content Depth | Word count, heading depth, topic coverage | 15 |
| UX Signals | CTA clarity, above-fold content, mobile layout | 15 |
| Schema Markup | Present vs expected structured data | 15 |
| Media Richness | Images, video, interactive elements vs norm | 15 |
| Authority Signals | E-E-A-T markers, social proof, credentials | 15 |
| Freshness | Last updated, date signals, recency | 10 |

**Total: 0-100 SXO Gap Score** (lower = larger gap, higher = better alignment)

---

## 6. Persona-Based Scoring

1. Derive 4-7 personas from SERP intent signals
2. Score target page per persona on 4 dimensions (25 pts each):
   - **Relevance**: Does the page address this persona's need?
   - **Clarity**: Can this persona find their answer within 10 seconds?
   - **Trust**: Are there adequate trust signals?
   - **Action**: Is there a clear next step?
3. Sort recommendations by weakest persona first (biggest opportunity)

---

## 7. SXO vs SEO Health Score

These are **separate** scores:
- **SEO Health Score** = technical compliance (crawlability, speed, schema)
- **SXO Gap Score** = alignment between page and SERP expectations
- A page can score 95 SEO + 30 SXO = technically perfect but strategically misaligned
- Report both scores together when available

---

## 8. Cross-Skill References

| Finding | Hand Off To |
|---------|-------------|
| E-E-A-T gaps | Content quality audit (`content_eeat_protocol.md`) |
| Missing schema | Schema assessment (`schema_types_current.md`) |
| Local intent | Local SEO analysis (`local_seo_protocol.md`) |
| Content depth gaps | Deep page analysis |
| Image/media gaps | Image optimization |
