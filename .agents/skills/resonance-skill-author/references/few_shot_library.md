# Few-Shot Library Protocol

> "Examples are worth 1000 instructions."

## 1. The Definition

**Zero-Shot**: "Write a poem." (Unpredictable).
**Few-Shot**: "Here are 3 poems I like. Write one like this." (Predictable).

## 2. The Pattern

When building an Agent or a Tool, you MUST provide at least 3 examples of "Input -> Output".

### Example (SQL Generator)

**Instruction**: Convert English to SQL.

**Example 1:**
Input: "Show me users who signed up yesterday."
Output: `SELECT * FROM users WHERE signup_date = DATE('now', '-1 day');`

**Example 2:**
Input: "Count pro users."
Output: `SELECT count(*) FROM users WHERE plan = 'pro';`

**Input:**
[User Query]

## 3. The Mandate

*   **Complex Tasks**: 3+ Examples.
*   **Style Matching**: 5+ Examples.

> 🔴 **Rule**: If the model fails, don't write more instructions. Write more examples.
