# Site Authority Signals — Domain Trust, Age & PageRank

The leak confirmed Google maintains domain-level authority metrics. The `QualityNsrNsrData` module (58 fields) contains the core site-level signals, while `PerDocData` (230+ fields) holds PageRank variants and domain age data.

## QualityNsrNsrData — Site Quality Fields (Authority Subset)

| Field | Type | Description |
|---|---|---|
| `nsr` | number() | **Normalized Site Rank** — primary site quality score |
| `siteAuthority` | number() | **Confirmed domain authority metric** (Google denied this existed) |
| `siteQualityStddev` | number() | **Quality variance** — spread of page-level quality ratings |
| `smallPersonalSite` | number() | Small personal site classifier |
| `chromeInTotal` | number() | Chrome browser views for behavior tracking |

### siteAuthority — The Big Revelation
Confirms what Google publicly denied for years: a domain-level authority score exists and influences rankings. Present in both:
- `QualityNsrNsrData.siteAuthority` (site-level, type: number())
- `CompressedQualitySignals.siteAuthority` (compressed for Qstar scoring, type: integer())

Contributing factors include backlink profile, historical ranking performance, brand recognition, user engagement patterns, and content quality consistency.

### siteQualityStddev — Quality Consistency
Measures how consistent quality is across all pages on the site. A **narrow stddev** (consistent quality) is better than a wide one. Implications:
- A few excellent pages can't overcome many mediocre ones
- Removing low-quality pages improves the stddev
- Consistent editorial standards matter

## PerDocData — Domain Age & Sandbox

### hostAge — New Domain Sandbox
Confirms the "sandbox" for new domains. New sites face restricted ranking potential until trust signals accumulate over time.
- Low hostAge triggers conservative ranking treatment
- Rankings are suppressed (not blocked) for competitive queries
- The sandbox lifts gradually as trust signals accumulate (backlinks, content, entity recognition)

## Audit Checklist for Site Authority

- [ ] **siteAuthority indicators**: Diverse backlinks, brand recognition, entity presence
- [ ] **Domain age**: Established domain or new (potential sandbox)
- [ ] **NSR consistency**: Quality maintained across ALL pages (check siteQualityStddev)
- [ ] **Internal linking**: Clear hierarchy distributing PageRank effectively
- [ ] **Chrome/direct traffic**: chromeInTotal and directFrac indicate brand strength
