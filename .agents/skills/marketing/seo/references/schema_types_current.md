# Schema Types — Current Status (April 2026)

> Which Schema.org types to use, which are restricted, which are deprecated.

## ACTIVE (Recommend Freely)

### Core Business
- `Organization`, `LocalBusiness` (+ subtypes), `Service`

### Software & Products
- `SoftwareApplication`, `WebApplication`, `Product` (with Certification markup as of April 2025), `ProductGroup`, `Offer`

### Content
- `Article`, `BlogPosting`, `NewsArticle`, `DiscussionForumPosting`
- `Review`, `AggregateRating`

### Navigation & Structure
- `BreadcrumbList`, `WebSite`, `WebPage`

### People & Entities
- `Person`, `ProfilePage`, `ContactPage`

### Media
- `VideoObject`, `ImageObject`, `BroadcastEvent`, `Clip`, `SeekToAction`

### Other Active Types
- `Event`, `JobPosting`, `Course`, `SoftwareSourceCode`

---

## RESTRICTED (Only for Specific Sites)

| Type | Restriction | Date |
|------|-------------|------|
| **FAQPage** | Google rich results: government and healthcare sites ONLY | August 2023 |

**Guidance for FAQPage:**
- Existing FAQPage on commercial sites → Flag as Info priority (not Critical), noting AI/LLM citation benefit still exists
- Adding new FAQPage to commercial sites → Not recommended for Google benefit
- FAQ content itself is still valuable for AI citability — just don't expect Google rich results

---

## DEPRECATED (Never Recommend)

| Type | Status | Date |
|------|--------|------|
| **HowTo** | Rich results removed | September 2023 |
| **SpecialAnnouncement** | Deprecated | July 31, 2025 |
| **CourseInfo** | Retired from rich results | June 2025 |
| **EstimatedSalary** | Retired from rich results | June 2025 |
| **LearningVideo** | Retired from rich results | June 2025 |
| **ClaimReview** | Retired from rich results | June 2025 |
| **VehicleListing** | Retired from rich results | June 2025 |
| **Practice Problem** | Retired from rich results | Late 2025 |
| **Dataset** | Retired from rich results | Late 2025 |

---

## Implementation Notes

### JSON-LD and JavaScript Rendering (December 2025)

Per Google's JS SEO guidance update: structured data injected via JavaScript may face delayed processing. For time-sensitive markup (especially Product, Offer), include JSON-LD in the initial server-rendered HTML.

### Graph Connectivity

The power of schema comes from **nesting** and **referencing** via `@id`:

**Weak** (disconnected nodes):
- A `Product` schema floating alone
- An `Organization` schema floating alone

**Strong** (connected graph):
- `Product` → `brand` → `Organization` (via `@id`)
- `Article` → `author` → `Person` → `worksFor` → `Organization`

### Validation Pipeline

1. Ensure valid JSON syntax (no trailing commas)
2. Validate with Google Rich Results Test
3. Monitor Search Console "Enhancements" tab for regression alerts
