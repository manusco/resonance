# Topic Clustering Protocol — SERP-Overlap Methodology

> Group keywords by how Google actually ranks them, not by text similarity.

## 1. Core Principle

SERP-overlap clustering groups keywords by shared top-10 results. If two keywords return the same URLs in Google's top 10, they belong on the same page. Text similarity is a weak proxy — SERP overlap is the ground truth.

---

## 2. Seed Keyword Expansion

Expand the seed keyword into 30-50 variants:

1. **Related searches** — Extract from SERP
2. **People Also Ask (PAA)** — Extract all visible questions
3. **Long-tail modifiers** — "best", "how to", "vs", "for beginners", "tools", "examples", "guide", "template", "mistakes", "checklist"
4. **Question mining** — who/what/when/where/why/how variants
5. **Intent modifiers** — "pricing", "review", "alternative", "comparison", "free", "top"

**Deduplication**: Normalize (lowercase, strip articles), remove exact duplicates.
Target: 30-50 unique variants. Under 30 → run second pass with top PAA as seeds.

---

## 3. SERP Overlap Clustering

For each candidate pair, search both keywords and count shared URLs in top 10 organic results (ignore ads, featured snippets, PAA):

| Shared Results | Relationship | Action |
|---------------|-------------|--------|
| 7-10 | Same post | Merge into single target page |
| 4-6 | Same cluster | Group under same spoke cluster |
| 2-3 | Interlink | Place in adjacent clusters, add cross-links |
| 0-1 | Separate | Different clusters or exclude |

**Optimization**: Pre-group by intent to reduce comparisons. 40 keywords × full pairwise = 780 comparisons. Pre-group into 4 groups of ~10 = 4 × 45 = 180 comparisons.

---

## 4. Intent Classification

| Intent | Signals | Include? |
|--------|---------|----------|
| Informational | how, what, why, guide, tutorial | Yes |
| Commercial | best, top, review, comparison, vs | Yes |
| Transactional | buy, price, discount, sign up | Yes |
| Navigational | brand names, login, specific products | No (exclude) |

Keywords can have mixed intent — classify by dominant intent.

---

## 5. Hub-and-Spoke Architecture

1. **Pillar keyword**: Highest volume, broadest intent, most SERP overlap
2. **Cluster grouping**: 2-5 subtopic clusters per pillar
3. **Spoke assignment**: 2-4 posts per cluster
4. **Template selection by intent**:

| Intent Pattern | Template |
|---------------|----------|
| Informational (broad) | Ultimate guide |
| Informational (how) | How-to |
| Informational (list) | Listicle |
| Commercial (compare) | Comparison |
| Commercial (evaluate) | Review |
| Transactional | Landing page |

5. **Word count targets**: Pillar 2,500-4,000 words, spokes 1,200-1,800 words
6. **Cannibalization check**: No two posts share the same primary keyword. SERP overlap ≥7 → merge

---

## 6. Internal Link Matrix

| Link Type | Direction | Requirement |
|-----------|-----------|-------------|
| Spoke → Pillar | Mandatory | Every spoke |
| Pillar → Spoke | Mandatory | Every spoke |
| Spoke ↔ Spoke (same cluster) | Recommended | 2-3 links per post |
| Cross-cluster | Optional | 0-1 links per post |

**Rules:**
- Every post: minimum 3 incoming internal links
- No orphan pages (every post reachable from pillar in 2 clicks)
- Anchor text: target keyword or close variant (never "click here")
- Link placement: within body content, not navigation/sidebar

---

## 7. Cluster Scorecard

| Metric | Target |
|--------|--------|
| Coverage | 100% (posts written / planned) |
| Link Density | 3+ internal links per post |
| Orphan Pages | 0 |
| Cannibalization | 0 conflicts |
| Pillar Links | 100% bidirectional |
| Cross-Links | 80%+ implemented |
