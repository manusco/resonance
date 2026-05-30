# Semantic HTML & JSON-LD Templates

> **Objective**: Improve Entity Density and Machine Readability.

## 1. JSON-LD Snippets

### Article (Blog Post)
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{TITLE}}",
  "image": "{{IMAGE_URL}}",
  "author": {
    "@type": "Person",
    "name": "{{AUTHOR_NAME}}"
  },
  "datePublished": "{{PUBLISH_DATE}}",
  "dateModified": "{{MODIFY_DATE}}"
}
</script>
```

### Product
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{{PRODUCT_NAME}}",
  "image": "{{IMAGE_URL}}",
  "description": "{{DESCRIPTION}}",
  "brand": {
    "@type": "Brand",
    "name": "{{BRAND}}"
  },
  "offers": {
    "@type": "Offer",
    "url": "{{URL}}",
    "priceCurrency": "USD",
    "price": "{{PRICE}}"
  }
}
</script>
```

## 2. Semantic Structure
**❌ Anti-Pattern**: `<div class="heading">`
**✅ Standard**:
```html
<article>
  <header>
    <h1>Main Title</h1>
    <p>By <a rel="author" href="/author">Name</a></p>
  </header>
  
  <section>
    <h2>Key Topic</h2>
    <p>Content...</p>
  </section>

  <aside>
    <h3>Related</h3>
    <ul>...</ul>
  </aside>
</article>
```
