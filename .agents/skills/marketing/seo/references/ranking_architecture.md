# Ranking Architecture — CompositeDoc, Ascorer, Twiddlers & Index Tiers

The leak reveals Google's multi-stage ranking architecture through its data structures. `CompositeDoc` (44 fields) is the master container that aggregates all signals for a document. `CompressedQualitySignals` (38 fields) serves as a pre-computed "cheat sheet" for rapid scoring. The pipeline flows from indexing through Ascorer (primary ranking) to Twiddlers (re-ranking) to diversity constraints.

## The Ranking Pipeline

```
Crawl → Index → [CompositeDoc assembled] → Retrieval → Ascorer → Twiddlers → Diversity → Final SERP
```

### Stage 1: Crawl & Index
- Googlebot crawls pages and stores content
- Content is parsed; attributes are extracted into module fields
- Entity recognition, date extraction, quality flags are computed
- Links are processed; link graph is updated
- `CompositeDoc` is assembled with all signal modules
- `CompressedQualitySignals` is generated from source modules
- Version history is updated (last 20 changes tracked)

### Stage 2: Retrieval
- For a given query, candidate pages are retrieved from the index
- `scaledSelectionTierRank` determines which index tier the page is in
- Hundreds to thousands of candidates are selected
- Initial filtering removes obviously irrelevant results

### Stage 3: Ascorer (Primary Ranking)
The main ranking algorithm. Evaluates pages using signals from `CompositeDoc`:

**Per-document signals** (from CompositeDoc, computed at index time):
- PageRank variants from `PerDocData`
- Content quality from `QualityNsrPQData`
- Site quality from `QualityNsrNsrData`
- Entity signals from `RepositoryWebrefEntityJoin`
- Link profile from `IndexingDocjoinerAnchorStatistics`

### Stage 4: Twiddlers (Re-ranking)
Post-Ascorer functions that re-order results. They use `CompressedQualitySignals` for rapid access:

**NavBoost Twiddler** — Most powerful re-ranker
- Uses aggregated click data over 13-month rolling window
- Can significantly override Ascorer rankings
- Details: See `navboost_signals.md`

**QualityBoost Twiddler** — Content quality adjustments
- Uses `pandaDemotion`, `babyPandaDemotion`, `lowQuality`
- Uses `authorityPromotion`, `unauthoritativeScore`
- Can demote low-quality sites even with relevant content
- Can boost high-quality sites for competitive queries

**RealTimeBoost Twiddler** — Freshness adjustments
- Activated when query triggers QDF
- Uses `isHotdoc` and date signals
- Provides temporary ranking boost for fresh content

### Stage 5: Diversity Constraints
Final adjustments to ensure result variety:
- **Host diversity**: Limits results from a single domain (typically 2-3 per SERP page)
- **Content type diversity**: Mixes articles, videos, images, tools
- **Source diversity**: Includes different source types (news, blogs, forums)
- **Intent diversity**: For ambiguous queries, serves results for multiple intents

## CompressedQualitySignals — The Scoring Cheat Sheet

The `CompressedQualitySignals` module (38 fields) is a critical architectural revelation. It contains **pre-computed, compressed** versions of quality signals from multiple source modules, stored for rapid access during ranking.

**Demotions:**
- `pandaDemotion` (integer) — Panda content quality penalty
- `babyPandaDemotion` (integer) — Lighter Panda penalty
- `navDemotion` (integer) — Doorway/navigation page penalty
- `scamness` (integer, 0-1023) — Scam likelihood

**NavBoost (CRAPS):**
- `crapsNewUrlSignals` (String.t) — Compressed URL-level click data
- `crapsNewHostSignals` (String.t) — Compressed host-level click data

## Diagnosis Checklist

- [ ] **CompositeDoc completeness**: Page has signals present across all major modules
- [ ] **No demotion flags**: Clean CompressedQualitySignals (no Panda, EMD, nav, anchor demotions)
- [ ] **authorityPromotion active**: Positive authority boost present
- [ ] **NavBoost health**: Sufficient click data, positive goodClicks/badClicks ratio
- [ ] **Multi-stage optimization**: Strong signals at Ascorer level AND Twiddler level
