# i18n Protocol (Global Scale)

> "If you hardcode english, you kill the product."

## 1. Key-Based Translation

Never write text literals in JSX/HTML.

**Bad:**
```tsx
<button>Save Changes</button>
```

**Elite:**
```tsx
<button>{t('actions.save_changes')}</button>
```

## 2. Pluralization & Interpretation

Don't do `count + " items"`. It breaks in Russian/Arabic.

**Bad:**
```tsx
<div>{count} Items</div>
```

**Elite:**
```tsx
// en.json: "item_count": "{count} item | {count} items"
<div>{t('item_count', { count })}</div>
```

## 3. Date & Number Formatting

Use `Intl` API. Never string concat.

*   ❌ `price + " USD"`
*   ✅ `new Intl.NumberFormat('en-US', { style: 'currency' }).format(price)`

> 🔴 **Rule**: If a string is visible to the user, it MUST come from a JSON file.
