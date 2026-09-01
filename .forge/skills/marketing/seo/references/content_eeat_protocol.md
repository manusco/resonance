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

## 2. Content Tests

### Page Job and Coverage

Do not prescribe a minimum word count. Define what the page must help its audience understand or do, then test whether it:

- answers the dominant intent without filler;
- covers the material questions and decision criteria for that page type;
- distinguishes itself from overlapping pages with real information, experience, or utility;
- supports factual claims with primary or best available sources;
- gives the next useful action or route when the task continues elsewhere.

Length follows the work. A short page can be complete, and a long page can still be thin.

### Readability
- Match vocabulary and sentence structure to the intended audience.
- Break sections where the subject or reader task changes.
- Use lists, tables, examples, or diagrams only when they make the information easier to use.

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
- **Pattern Fatigue Check**: Vary structure when the content calls for it. Do not insert decorative breaks to satisfy a quota.

### Multimedia
- Relevant images with proper alt text
- Videos where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### Internal Linking
- Add relevant links when they improve discovery, supply needed context, or advance the reader's next task.
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

### AI Pattern Fatigue Check
1. **Format Fit**: Use the structure best suited to the information instead of repeating one template across pages.
2. **Natural Rhythm**: Rewrite mechanical repetition that makes the text harder to read.
3. **Voice Fit**: Keep one appropriate voice for the audience. Do not force tone shifts as a detection tactic.

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
- Entity clarity through consistent names and, when eligible, structured data supported by the visible page content and `schema_types_current.md`

> **Helpful content:** Treat helpfulness as an ongoing quality standard, not as a single classifier to game. The actionable rule is stable: make content for people, show real experience, and avoid search-engine-first filler.

---

## 5. Content Freshness

- Publication date visible
- Last updated date if content has been revised
- Review fast-changing topics on a cadence justified by their subject and risk, not a universal age cutoff.
- Keep URL, structured data, metadata, byline, publication, and modified dates truthful and mutually consistent.

---

## 6. E-E-A-T Scoring Output

| Factor | Score | Key Signals |
|--------|-------|-------------|
| Experience | XX/25 | ... |
| Expertise | XX/25 | ... |
| Authoritativeness | XX/25 | ... |
| Trustworthiness | XX/25 | ... |

**AI Citation Readiness: XX/100**
