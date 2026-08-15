# Content Quality & E-E-A-T Protocol

> Source-grounded content-quality guidance. Do not treat leaked field names, word counts, or readability formulas as ranking factors.

## Source Card

- Primary source: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Secondary source: https://developers.google.com/search/blog/2023/02/google-search-and-ai-content
- Verified: 2026-08-15
- Scope: Google Search guidance on helpful, reliable, people-first content and AI-assisted content.
- Review trigger: Google Search Central updates helpful content, spam policy, or quality rater guidance.

## Contents

- [1. E-E-A-T Framework](#1-e-e-a-t-framework)
- [2. Content Metrics](#2-content-metrics)
- [3. AI Content Assessment](#3-ai-content-assessment)
- [4. AI Citation Readiness (GEO Signals)](#4-ai-citation-readiness-geo-signals)
- [5. Content Freshness](#5-content-freshness)
- [6. E-E-A-T Scoring Output](#6-e-e-a-t-scoring-output)

## 1. E-E-A-T Framework

### Experience (First-Hand Signals)
- Original research, case studies, before/after results
- Personal anecdotes, process documentation
- Unique data, proprietary insights
- Photos/videos from direct experience

### Expertise
- Author credentials, certifications, bio
- Professional background relevant to topic
- Technical depth appropriate for audience
- Accurate, well-sourced claims

### Authoritativeness
- External citations and backlinks from authoritative sources
- Brand mentions and industry recognition
- Published in recognized outlets
- Cited by other experts

### Trustworthiness
- Contact information, physical address
- Privacy policy, terms of service
- Customer testimonials and reviews
- Date stamps, transparent corrections
- Secure site (HTTPS)

---

## 2. Content Metrics

### Word Count by Page Type

| Page Type | Minimum | Unique Content % |
|-----------|---------|-----------------|
| Homepage | 500 | 100% |
| Service / Feature page | 800 | 100% |
| Blog post | 1,500 | 100% |
| Product page | 300+ (400+ for complex) | 80%+ |
| Location page (primary) | 600 | 60%+ |
| Location page (secondary) | 500 | 40%+ |

> **Important**: These are topical coverage floors, not targets. Google has confirmed word count is NOT a direct ranking factor. A 500-word page that thoroughly answers the query will outrank a 2,000-word page that doesn't. Use these as guidelines for adequate coverage depth.

### Readability
- Flesch Reading Ease: Target 60-70 for general audience
- Sentence length: Average 15-20 words
- Paragraph length: 2-4 sentences

> **Note**: Flesch Reading Ease is a useful proxy for content accessibility but is NOT a direct ranking factor (John Mueller confirmed). Yoast deprioritized Flesch scores in v19.3. Use as a content quality indicator, not an SEO metric.

### Keyword Optimization
- Primary topic appears naturally in title, H1, and early context when it helps the reader.
- Semantic variations are present because the topic is covered well, not because a density target was met.
- No keyword stuffing. Do not cite leaked metric names as if they were a public scoring API.

### Content Structure
- Logical heading hierarchy (H1→H2→H3)
- Scannable sections with descriptive headings
- Bullet/numbered lists where appropriate
- Table of contents for long-form content
- **AI Pattern Fatigue Check**: No more than 2 paragraphs without a visual break (list, table, quote, image)

### Multimedia
- Relevant images with proper alt text
- Videos where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### Internal Linking
- 3-5 relevant internal links per 1,000 words (density: ~1 per 50-75 words)
- Descriptive anchor text (never "click here")
- Links to related content
- No orphan pages

---

## 3. AI Content Assessment

Google says automation is not banned by itself. The failure is content made primarily to manipulate ranking, or content that lacks originality, accuracy, usefulness, or human accountability.

### Acceptable AI Content
- Demonstrates genuine E-E-A-T
- Provides unique value
- Has human oversight and editing
- Contains original insights

### Low-Quality AI Content Markers
- Generic phrasing, lack of specificity
- No original insight
- Repetitive structure across pages
- No author attribution
- Factual inaccuracies

### AI Pattern Fatigue (Entropy Check)
1. **Format Variance**: No more than 2 paragraphs without a visual break
2. **Rhythm Variance**: Sentences must vary in length. 3 sentences with identical structure = fail
3. **Tone Modulation**: Shift between technical and conversational at least once per 500 words

---

## 4. AI Citation Readiness (GEO Signals)

Optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews):

- Clear, quotable statements with statistics/facts
- Structured data (especially for data points)
- Strong heading hierarchy (H1→H2→H3)
- Answer-first formatting for key questions
- Tables and lists for comparative data
- Clear attribution and source citations
- Topical authority through content clusters, not isolated pages
- Entity clarity via Organization, Person schema

> **Helpful content:** Treat helpfulness as an ongoing quality standard, not as a single classifier to game. The actionable rule is stable: make content for people, show real experience, and avoid search-engine-first filler.

---

## 5. Content Freshness

- Publication date visible
- Last updated date if content has been revised
- Flag content older than 12 months without update for fast-changing topics
- Date signals must be consistent across URL, Schema, meta, and byline (inconsistency breaks `trustSyntacticDateInRanking` - see `content_quality_signals.md`)

---

## 6. E-E-A-T Scoring Output

| Factor | Score | Key Signals |
|--------|-------|-------------|
| Experience | XX/25 | ... |
| Expertise | XX/25 | ... |
| Authoritativeness | XX/25 | ... |
| Trustworthiness | XX/25 | ... |

**AI Citation Readiness: XX/100**
