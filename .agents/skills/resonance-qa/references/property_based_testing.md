# Property Based Testing Protocol (Fuzzing)

> "Don't test x + y = z. Test that addition is commutative."

## 1. The Concept

Instead of "Input: 2, Output: 4", generate 1,000 random inputs.
*   **Invariant**: A property that is always true.
*   **Example**: `reverse(reverse(list)) === list`.

## 2. The Tool (Fast-Check)

```typescript
import fc from 'fast-check';

test('sort should sort', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = sort(arr);
      // Property 1: Same length
      expect(sorted).toHaveLength(arr.length);
      // Property 2: Ordered
      for (let i = 0; i < sorted.length - 1; i++) {
        expect(sorted[i]).toBeLessThanOrEqual(sorted[i + 1]);
      }
    })
  );
});
```

## 3. The Use Case

*   **Parsers**: JSON, CSV, Markdown.
*   **Calculators**: Tax logic, Pricing engines.
*   **Date Math**: The ultimate edge case generator.

> 🔴 **Rule**: If your function takes a User Input string, you MUST fuzz it with Emojis and Null bytes.
