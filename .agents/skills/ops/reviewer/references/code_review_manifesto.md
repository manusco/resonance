# Code Review Manifesto Protocol

> "Code is a liability. Review is the asset."

## 1. The Tone (Empathy)
Review the code, not the person.
*   ❌ "You broke the build."
*   ✅ "This change breaks the build."
*   ❌ "Why did you do this?"
*   ✅ "Can you explain the reasoning here?"

## 2. The Nitpick vs The Blocker
Distinguish clearly.
*   **[Nit]**: "Rename var `x` to `index`." (Non-blocking).
*   **[Block]**: "This introduces an N+1 query." (Blocking).

## 3. The "Why"
Always explain *why* you are requesting a change.
*   ❌ "Change this loop."
*   ✅ "Change this loop to a map because it reduces mutation."

> 🔴 **Rule**: If you block a PR, you must suggest a path to resolution.
