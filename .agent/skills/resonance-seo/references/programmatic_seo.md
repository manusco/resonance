# Programmatic SEO Protocol

> "Write once. Publish 10,000 times."

## 1. The Data Source

You cannot write 10k pages. You need a Database.
*   **Example**: "Best Coffee in [City]".
*   **Data**: CSV with City Name, Population, Top 3 Shops, Lat/Long.

## 2. The Template (The Engine)

Do NOT use "Mad Libs" (e.g., "Welcome to [City], it is distinct.").
Use **Logic-Based Templates**.

```tsx
{city.population > 1000000 ? (
  <p>As a major metropolis, {city.name} offers...</p>
) : (
  <p>{city.name} is a hidden gem...</p>
)}
```

## 3. The Indexing Strategy

Do not dump 10k pages on Day 1. Google will flag you as spam.
1.  **Drip Feed**: Release 50 pages / day.
2.  **Internal Linking**: Create "Hub Pages" ("Best Coffee in California") that link to the "City Pages".
3.  **Canonical**: If data is thin, canonicalize to the State page.

> 🔴 **Rule**: If a user lands on a programmatic page and bounces immediately, you are burning your crawl budget. Value first.
