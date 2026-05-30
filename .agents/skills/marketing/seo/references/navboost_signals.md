# NavBoost Signals — Click & User Interaction Data

NavBoost is the most significant ranking system revealed in the 2024 Google leak. It is a "Twiddler" — a re-ranking function that adjusts results after Google's primary ranking algorithm (Ascorer) has produced initial rankings. NavBoost uses aggregated click data from Chrome and Google Search over a rolling 13-month window.

## QualityNavboostCrapsCrapsClickSignals — Complete Field Reference

The core NavBoost click signal module. CRAPS = **C**lick, **R**ank, **A**nd **P**osition **S**ignals. Active since 2005.

| Field | Type | Description |
|---|---|---|
| `clicks` | float() | Total clicks on the result |
| `goodClicks` | float() | **Positive engagement clicks** — user found what they needed |
| `badClicks` | float() | **Negative clicks** — quick return to SERP (pogo-sticking) |
| `lastLongestClicks` | float() | **Last click in session + longest dwell time** — strongest positive signal |
| `impressions` | float() | Total SERP impressions |
| `unicornClicks` | float() | Clicks from "Unicorn" user subset (quality-filtered panel) |

## Signal Deep Dives

### goodClicks — The Positive Signal
Indicators that trigger goodClicks classification:
- Long dwell time on the page
- No return to search results
- Continued browsing on the same site
- Task completion signals

### badClicks — The Demotion Signal
A high badClicks ratio actively demotes a page. Indicators:
- Quick back-button clicks (short dwell time)
- Immediately clicking a different search result
- Returning to SERP within seconds

### lastLongestClicks — The Strongest Signal
The most powerful positive signal in NavBoost. Tracks which result was the **last click** in a search session AND had the **longest dwell time**.

**Optimization**:
- Create comprehensive, definitive content that ends the search journey
- Cover the topic thoroughly enough that users don't need other results
- Include supporting media (images, videos, tables) that extend engagement

## Audit Checklist for Click Optimization

- [ ] **Title tag**: Accurately reflects content, compelling enough to earn clicks
- [ ] **Meta description**: Sets correct expectations, includes value proposition
- [ ] **Page speed**: Loads fast enough to prevent impatient back-button clicks
- [ ] **Above-the-fold content**: Immediately relevant to the target query
- [ ] **Content completeness**: Comprehensive enough to be the lastLongestClick
- [ ] **Intent match**: Content format matches search intent
