# Regex Wizardry Protocol

> "Some people have a problem and think 'I know, I'll use regex.' Now they have two problems."

## 1. The Named Capture Group
Stop using `$1`, `$2`. It's fragile.

**Bad:**
```javascript
const match = str.match(/(\d{4})-(\d{2})/);
const year = match[1];
```

**Elite:**
```javascript
const match = str.match(/(?<year>\d{4})-(?<month>\d{2})/);
const { year, month } = match.groups;
```

## 2. The Lookarounds (Zero-Width Assertions)
Match something *only if* it is followed by something else.

*   `(?=...)`: Positive Lookahead. "Must be followed by".
*   `(?!...)`: Negative Lookahead. "Must NOT be followed by".
    *   *Example*: Match `foo` only if NOT followed by `bar`: `foo(?!bar)`.

## 3. The Flags

*   `g`: Global (All matches).
*   `i`: Case Insensitive.
*   `m`: Multiline (`^` matches start of line, not just start of string).
*   `s`: Dotall (`.` matches newlines).

> 🔴 **Rule**: If your regex is longer than 20 chars, comment it or split it.
