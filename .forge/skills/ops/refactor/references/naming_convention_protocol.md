# Protocol: Naming Conventions (The Decision Tree)
> **Objective**: Eliminate cognitive load by enforcing consistent naming patterns.
> **Philosophy**: "If I have to guess what type a variable is, the name is wrong."

## 1. The Decision Tree
Run this mental check for *every* name you write.

```text
Is it a boolean?
├─ Yes → Use is/has/can/should prefix (e.g., isValid, hasPermission)
└─ No → Is it a function?
    ├─ Yes → Use verb phrase (action) (e.g., getUser, calculateTotal)
    └─ No → Is it a class/interface?
        ├─ Yes → Use Noun + PascalCase (e.g., UserProfile, PaymentService)
        └─ No → Is it a constant?
            ├─ Yes → Use UPPER_SNAKE_CASE (e.g., MAX_RETRY_COUNT)
            └─ No → Use descriptive noun + camelCase (e.g., userList)
```

---

## 2. The Rules (Strict)

### A. Booleans
*   ❌ `valid`, `check`, `done` (Ambiguous)
*   ✅ `isValid`, `shouldCheck`, `isDone` (Explicit State)

### B. Functions
*   ❌ `process(data)` (Vague)
*   ✅ `processPayment(transaction)` (Specific)
*   **Pattern**: `verb` + `noun` (Action + Object)

### C. Collections
*   ❌ `list`, `data`, `items`
*   ✅ `users`, `activeProjects`, `menuItems`
*   **Tip**: Plural nouns for arrays.

### D. Magic Numbers/Strings
*   ❌ `if (status === 2) ...`
*   ✅ `const STATUS_ACTIVE = 2; if (status === STATUS_ACTIVE) ...`

---

## 3. Anti-Patterns (The "Slop" List)
1.  **Abbreviations**: `usr`, `idx`, `cnt`. (Use `user`, `index`, `count`).
2.  **Types in Names**: `userString`, `accountArray`. (Redundant in TS).
3.  **Utility/Manager/Helper**: `UserManager`. (God object warning. Use `UserAuthenticator` or `UserRepository`).
