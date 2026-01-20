# Cognitive Complexity Limits

> "If it fits in your head, it fits in the codebase."

## 1. The Limits

*   **Function Length**: < 50 lines.
*   **Line Length**: < 100 chars (Prettier default).
*   **Cyclomatic Complexity**: < 10. (If > 10, split function).

## 2. The Nesting Limit
Maximum 3 levels of indentation.
```javascript
if (a) {
  if (b) {
    if (c) {
      // STOP using Guard Clauses.
    }
  }
}
```

## 3. The Parameter Limit
Maximum 3 arguments per function.
*   If > 3, use an Object (DTO).
*   `function createUser(name, email, age, role, active)` -> `function createUser({ name, email, ... })`

> 🔴 **Rule**: If I have to scroll vertically to see the end of the function, refactor it.
