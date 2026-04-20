# SEO Schema Markup (JSON-LD)

> "Speak Google's Native Language."

## 1. The Strategy

Google doesn't read your HTML. It reads your JSON-LD.

## 2. The Must-Haves

1.  **Organization**: (Logo, Social Profiles).
2.  **BreadcrumbList**: (Site Structure).
3.  **Article**: (Blog Posts - Author, Date, Headline).
4.  **Product**: (Price, Availability, Review Rating).

## 3. The Implementation

Place this in the `<head>`:

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Resonance Framework",
  "offers": {
    "@type": "Offer",
    "price": "0.00",
    "priceCurrency": "USD"
  }
}
</script>
```

> 🔴 **Rule**: Validate with Google Rich Results Test before shipping.
