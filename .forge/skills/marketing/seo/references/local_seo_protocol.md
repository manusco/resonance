# Local SEO Protocol

> For businesses with physical locations or service areas.

## Contents

- [1. Key Statistics (2026)](#1-key-statistics-2026)
- [2. Business Type Detection](#2-business-type-detection)
- [3. Industry Vertical Detection](#3-industry-vertical-detection)
- [4. Analysis Dimensions (6 Pillars)](#4-analysis-dimensions-6-pillars)
- [5. AI Impact on Local](#5-ai-impact-on-local)
- [6. Action Tiers](#6-action-tiers)

## 1. Key Statistics (2026)

| Metric | Value | Source |
|--------|-------|--------|
| GBP signals share of local pack weight | 32% | Whitespark 2026 |
| Proximity share of ranking variance | 55.2% | Search Atlas ML study |
| Review signals share (up from 16%) | ~20% | Whitespark 2026 |
| Google searches seeking local info | 46% | Industry data |
| Mobile "near me" → visit in 24h | 76% | Google |
| ChatGPT/AI usage for local recommendations | 45% (up from 6%) | BrightLocal LCRS 2026 |
| ChatGPT local conversion rate | 15.9% | Seer Interactive |
| Google organic local conversion rate | 1.76% | Seer Interactive |
| Local pack ads growth (Jan 2025→Jan 2026) | 1% → 22% | Sterling Sky |

---

## 2. Business Type Detection

Detect from page signals before analysis:

### Brick-and-Mortar
- Physical street address visible in content/footer
- Google Maps embed with pin/directions
- "Visit us at", "Located at", structured address in LocalBusiness schema

### Service Area Business (SAB)
- No visible physical address
- "Serving [city/region]", "We come to you", "Mobile [service]"
- `areaServed` in schema without `address.streetAddress`

### Hybrid
- Both physical address AND service area language present

**Impact**: SABs skip map verification and physical address consistency checks.

---

## 3. Industry Vertical Detection

| Vertical | Detection Signals |
|----------|------------------|
| **Restaurant** | /menu, reservations, cuisine types, "dine-in", "takeout" |
| **Healthcare** | Insurance accepted, appointments, NPI, HIPAA notice |
| **Legal** | Attorney, practice areas, bar admission, "free consultation" |
| **Home Services** | Service area, "free estimate", licensed/insured/bonded |
| **Real Estate** | MLS, properties, agent bio, brokerage, "open house" |
| **Automotive** | Inventory, VIN, test drive, dealership, service department |

---

## 4. Analysis Dimensions (6 Pillars)

### 4.1 GBP Signals (25%)
- Primary category is #1 local pack factor (Whitespark: score 193). Incorrect primary = #1 negative factor (score 176)
- Evidence of secondary categories (optimal: 4 additional, BrightLocal)
- Photos/video (45% more direction requests, Agency Jet)
- Q&A deprecated Dec 2025, replaced by Ask Maps Gemini AI → recreate as FAQ on website
- Business hours visibility (open at search time = higher ranking, factor #5)
- GBP link URL: Do NOT link to strongest page (Sterling Sky Diversity Update risks suppressing organic)

### 4.2 Reviews & Reputation (20%)
- Review velocity > total count. **18-day rule** (Sterling Sky): rankings cliff if no new reviews for 3 weeks
- Magic threshold: 10 reviews (Sterling Sky)
- 31% of consumers only use 4.5+ stars, 68% only use 4+ (BrightLocal 2026)
- 74% only care about reviews in last 3 months
- Consumers use average of 6 review sites (BrightLocal 2026)
- 88% would use business that responds to reviews (BrightLocal)
- **Review gating prohibited**: Pre-screening satisfaction before directing to review = Google fake engagement policy violation + FTC ($53,088/violation)

### 4.3 Local On-Page SEO (20%)
- Dedicated service pages = #1 local organic factor AND #2 AI visibility factor (Whitespark 2026)
- Title tag + H1 with city/service keywords
- NAP visible in HTML (footer, contact, header)
- Location page quality: >60-70% unique content minimum
- **Swap test**: If you can swap city name and content still works, it's a doorway page
- Embedded Google Map (lazy-load to mitigate speed impact)
- Click-to-call (`tel:` link) above fold
- Hub-and-spoke internal linking, every critical page within 3 clicks

### 4.4 NAP Consistency & Citations (15%)
- 3 of top 5 AI visibility factors are citation-related (Whitespark 2026)
- Compare NAP across: visible HTML, LocalBusiness JSON-LD, GBP data
- Tier 1 directories: Google, Yelp, BBB, Facebook
- Apple Business Connect (usage doubled to 27%, BrightLocal 2026)
- Bing Places (powers ChatGPT, Copilot, Alexa)
- Data aggregators: Data Axle, Foursquare, Neustar/TransUnion

### 4.5 Local Schema Markup (10%)
- Not a direct ranking factor (John Mueller), but enables rich results (43% CTR increase, Webstix)
- Required: `name`, `address` with PostalAddress
- Recommended: `geo` (5+ decimal places), `openingHoursSpecification`, `telephone`, `url`, `priceRange`, `image`, `aggregateRating`
- Use correct subtype (Restaurant, LegalService, MedicalClinic, AutoDealer — not generic LocalBusiness)
- Multi-location: each location page has own LocalBusiness with unique `@id`, linked via `branchOf`

### 4.6 Local Authority Signals (10%)
- Links: ~26% of local organic ranking (Whitespark 2026)
- "Best of" list placements = #1 AI visibility citation factor
- Chamber of Commerce (~80% more consumer visits, GlueUp)
- BBB (Google uses BBB for business verification)
- Brand mentions correlate 3x more strongly with AI visibility than backlinks (Ahrefs)

---

## 5. AI Impact on Local

- AI Overviews on up to 68% of local searches (Whitespark Q2 2025)
- ChatGPT does NOT access GBP directly — sources from Bing index, Yelp, TripAdvisor, BBB, Reddit
- AI-powered local packs (mobile US) show only 1-2 businesses, 32% fewer shown (Sterling Sky)
- Cross-reference `geo_protocol.md` for comprehensive AI visibility analysis

---

## 6. Action Tiers

### Quick Wins
1. Claim Apple Business Connect and Bing Places
2. Fix NAP discrepancies between page, schema, and GBP
3. Add LocalBusiness schema with correct industry subtype
4. Add `geo` coordinates with 5+ decimal precision
5. Ensure phone uses `tel:` link
6. Add city + service to title tag and H1

### Medium Effort
1. Create dedicated page per core service (#1 local organic factor)
2. Build review generation strategy with 18-day minimum cadence
3. Submit to three data aggregators
4. Claim industry-specific directory listings
5. Implement hub-and-spoke internal linking

### High Impact
1. Local digital PR targeting "best of" lists (#1 AI visibility factor)
2. Unique, non-swappable content for each location page (>60% unique)
3. Establish presence on platforms ChatGPT sources from (Yelp, TripAdvisor, BBB, Reddit)
4. Chamber of Commerce and BBB membership
5. Community involvement content
