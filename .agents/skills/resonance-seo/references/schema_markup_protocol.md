# Protocol: Semantic Data Engineering (Schema Markup)
> **Focus**: Graph Implementation & Structured Data
> **Resonance Phase**: Optimization

## 1. The Semantic Web Philosophy
Schema Markup (JSON-LD) is not just "SEO sprinkles." It is **Semantic Engineering**. It translates your messy HTML DOM into a rigorous **Knowledge Graph** that machines (Google, LLMs, Agents) can understand deterministically.

**Goal**: Move from "Probabilistic Parsing" (Google guessing your content) to "Deterministic Understanding" (You telling Google what it is).

## 2. The Core Entity Graph
Do not implement schema randomly. Build a graph.

### The "Identity" Node (`Organization`)
*   **Context**: The root of your graph. Who owns this digital space?
*   **Critical Properties**: `name`, `url`, `logo`, `sameAs` (Social Proof).
*   **Resonance Standard**: Always link this `Organization` as the `publisher` or `author` of other nodes.

### The "Item" Node (`Product` / `SoftwareApplication`)
*   **Context**: What are you selling or providing?
*   **Critical Properties**:
    *   `offers` (Price, Currency, Availability).
    *   `aggregateRating` (Social Proof data).
    *   `applicationCategory` (For SaaS).

### The "Knowledge" Node (`Article` / `BlogPosting`)
*   **Context**: Informational assets.
*   **Critical Properties**: `headline`, `datePublished` (Freshness), `author` (E-E-A-T).

## 3. Engineering Implementation (JSON-LD)
We strictly use **JSON-LD** (JavaScript Object Notation for Linked Data).

### Pattern: The React/Next.js Injection
Don't write strings manually. Use a typed object.

```typescript
// Define the Schema Type (e.g. using 'schema-dts')
const schema: WithContext<Product> = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: product.title,
  description: product.description,
  offers: {
    '@type': 'Offer',
    price: product.price,
    priceCurrency: 'USD',
    availability: 'https://schema.org/InStock'
  }
};

// Injection
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
/>
```

## 4. The Graph Connectivity
The power comes from **nesting** or **referencing** via `@id`.

**The Unconnected (Weak)**:
*   A `Product` schema floating alone.
*   An `Organization` schema floating alone.

**The Graph (Strong)**:
*   `Product` has a `brand` property referencing the `Organization` `@id`.
*   `Article` has an `author` property referencing a `Person` `@id`, who worksFor the `Organization`.

## 5. Verification Pipeline
Do not deploy invalid JSON. It breaks the parser.

1.  **Linter**: Ensure valid JSON syntax (no trailing commas).
2.  **Schema Validator**: Use Google's [Rich Results Test](https://search.google.com/test/rich-results) or [Schema.org Validator](https://validator.schema.org/).
3.  **Search Console**: Monitor "Enhancements" tab for regression alerts.

## 6. Advanced Playbooks

### The FAQ Interceptor
Use `FAQPage` schema on landing pages to occupy more vertical pixels in SERPs.
*   *Requirement*: The content must legally be visible on the page (no hidden FAQs).

### The Breadcrumb Trail
Use `BreadcrumbList` to force Google to display your site structure (`Home > Features > Analytics`) instead of a raw URL.

### The Local Nexus
For physical locations, `LocalBusiness` is mandatory. Embed `geo` (Lat/Long) and `openingHoursSpecification`.
