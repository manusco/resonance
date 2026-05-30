# Content Quality Signals — Page Quality, Freshness, Tokens & Dates

Content quality in Google's ranking system is evaluated through multiple dedicated modules. The `QualityNsrPQData` module (19 fields) provides page-level quality scores including Google's internal code-named predictors. `QualityTimebasedSyntacticDate` (14 fields) handles date extraction and freshness. `PerDocData` contributes content-level signals like token analysis, originality, and spam detection.

## QualityNsrPQData — Page-Level Quality Scores

The dedicated page quality module. Contains Google's internal quality predictors, many named with food code names (CHARD, KETO, RHUBARB, TOFU).

| Field | Type | Description |
|---|---|---|
| `contentEffort` | number() | **Content effort score** — measures investment in content creation |
| `originalContentScore` | number() | **Content originality** — unique vs. duplicated/scraped |
| `vlq` | number() | **Very Low Quality** score at page level |
| `bodyWordsToTokensRatio` | number() | **Vocabulary diversity** — ratio of unique words to total tokens |
| `gibberishScore` | integer() | Non-sensical/auto-generated content detection |

### contentEffort — Editorial Investment
Measures the apparent effort invested in creating the content. Higher scores indicate:
- Original research, reporting, or analysis
- Detailed explanations with supporting evidence
- Custom illustrations, charts, or data visualizations
- Evidence of expert review or editorial process

### bodyWordsToTokensRatio — Vocabulary Diversity
One of the most actionable content signals. Measures the ratio of unique words to total tokens in the page body.
- **High ratio** (diverse vocabulary): Indicates substantive, well-written content with varied expression
- **Low ratio** (repetitive vocabulary): May indicate keyword stuffing, shallow content, or templated pages

## QualityTimebasedSyntacticDate — Date & Freshness

Google's date extraction module parses, validates, and scores content dates.

- **`trustSyntacticDateInRanking`**: Critical boolean. When `false`, the page receives no freshness benefit. Trust drops when dates conflict (URL vs Schema vs Byline).
- **`isHotdoc`**: Boolean flag for trending content (QDF activation).
- **`lastSignificantUpdate`**: Only substantial changes update this field. Cosmetic changes don't qualify.

## Audit Checklist for Content Quality

- [ ] **contentEffort**: Content demonstrates editorial investment (original research, detailed analysis, custom media)
- [ ] **OriginalContentScore**: Majority of content is unique, not scraped or syndicated
- [ ] **bodyWordsToTokensRatio**: Diverse vocabulary, not repetitive or keyword-stuffed
- [ ] **Date signals**: Publish date visible, consistent across all sources (URL, meta, byline, JSON-LD)
- [ ] **trustSyntacticDateInRanking**: No conflicting date signals that would break trust
- [ ] **lastSignificantUpdate**: Content has been meaningfully updated (not just cosmetic changes)
- [ ] **clutterScore**: Minimal ads, pop-ups, and non-content elements
- [ ] **vlq check**: No Very Low Quality flags at page or site level
