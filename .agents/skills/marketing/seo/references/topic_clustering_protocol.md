# Topic Clustering Protocol - SERP-Overlap Methodology

> Group keywords by how Google actually ranks them, not by text similarity.

## Contents

- [1. Core Principle](#1-core-principle)
- [2. Seed Keyword Expansion](#2-seed-keyword-expansion)
- [3. SERP Overlap Clustering](#3-serp-overlap-clustering)
- [4. Intent Classification](#4-intent-classification)
- [5. Hub-and-Spoke Architecture](#5-hub-and-spoke-architecture)
- [6. Internal Link Matrix](#6-internal-link-matrix)
- [7. Cluster Scorecard](#7-cluster-scorecard)

## 1. Core Principle

SERP-overlap clustering groups keywords by shared top-10 results. If two keywords return the same URLs in Google's top 10, they belong on the same page. Text similarity is a weak proxy - SERP overlap is the ground truth.

---

## 2. Seed Keyword Expansion

Expand the seed keyword until the meaningful intent space is represented:

1. **Related searches** - Extract from SERP
2. **People Also Ask (PAA)** - Extract all visible questions
3. **Long-tail modifiers** - "best", "how to", "vs", "for beginners", "tools", "examples", "guide", "template", "mistakes", "checklist"
4. **Question mining** - who/what/when/where/why/how variants
5. **Intent modifiers** - "pricing", "review", "alternative", "comparison", "free", "top"

**Deduplication**: Normalize (lowercase, strip articles), remove exact duplicates.
Stop when another pass produces no material new intent, audience question, or decision criterion. Record the source and retrieval date because query sets and SERPs change.

---

## 3. SERP Overlap Clustering

For each candidate pair, search both keywords and count shared URLs in top 10 organic results (ignore ads, featured snippets, PAA):

Compare shared ranking URLs, result types, and dominant intent. Treat overlap as evidence, not a universal numeric boundary:

- Strong overlap with the same page job supports one target page.
- Partial overlap with related but distinct jobs supports separate, connected pages.
- Little overlap or different result types supports separate clusters or exclusion.
- Recheck ambiguous or high-value decisions across devices, locations, or dates when those factors matter.

**Efficiency**: Pre-group by intent before pairwise comparison, then spend manual review on ambiguous and high-value boundaries.

---

## 4. Intent Classification

| Intent | Signals | Include? |
|--------|---------|----------|
| Informational | how, what, why, guide, tutorial | Yes |
| Commercial | best, top, review, comparison, vs | Yes |
| Transactional | buy, price, discount, sign up | Yes |
| Navigational | brand names, login, specific products | No (exclude) |

Keywords can have mixed intent - classify by dominant intent.

---

## 5. Hub-and-Spoke Architecture

1. **Pillar job**: The broad user task that can route readers to its distinct subtopics.
2. **Cluster grouping**: One cluster per coherent page job and audience need.
3. **Spoke assignment**: Add a spoke only when it answers a distinct intent that the pillar should not absorb.
4. **Template selection by intent**:

| Intent Pattern | Template |
|---------------|----------|
| Informational (broad) | Ultimate guide |
| Informational (how) | How-to |
| Informational (list) | Listicle |
| Commercial (compare) | Comparison |
| Commercial (evaluate) | Review |
| Transactional | Landing page |

5. **Coverage test**: Each page is as long as its job requires and no longer.
6. **Cannibalization check**: Investigate pages competing for the same intent. Merge only when evidence shows one page can satisfy both jobs better.

---

## 6. Internal Link Matrix

| Link Type | Direction | Requirement |
|-----------|-----------|-------------|
| Spoke → Pillar | Mandatory | Every spoke |
| Pillar → Spoke | Mandatory | Every spoke |
| Spoke ↔ Spoke (same cluster) | Recommended when useful | Link where the reader needs the adjacent topic |
| Cross-cluster | Optional | Link only when the relationship is clear |

**Rules:**
- Give every indexable page a crawlable route from the site's information architecture.
- Anchor text: target keyword or close variant (never "click here")
- Link placement: within body content, not navigation/sidebar

---

## 7. Cluster Scorecard

| Metric | Target |
|--------|--------|
| Coverage | Material user intents have an owned page or an explicit exclusion |
| Link Purpose | Links reflect real relationships and next tasks |
| Orphan Pages | No intended indexable page lacks a crawlable route |
| Cannibalization | Suspected conflicts are measured and resolved |
| Pillar Links | Pillar and spokes connect where navigation requires it |
| Cross-Links | Added only when useful |
