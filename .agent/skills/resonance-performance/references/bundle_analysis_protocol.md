# Bundle Analysis Protocol

> "You are shipping code to a $50 Android phone on 3G."

## 1. The Visualizer

Don't guess what's big. Look at it.
*   **Tool**: `rollup-plugin-visualizer` or `@next/bundle-analyzer`.
*   **Action**: Generate `stats.html` on every build.

## 2. The Budget

Set a budget.
*   **Initial JS**: < 150KB (Gzipped).
*   **Total JS**: < 300KB (Gzipped).
*   **CI**: Fail if `main.js` exceeds budget.

## 3. The Tree Shaking Audit

*   **Check**: Are we importing all of `lodash`? (Use `lodash-es`).
*   **Check**: Are we importing all of `framer-motion`? (Use LazyMotion).
*   **Action**: Use `import { x } from 'pkg'` (Named Imports) everywhere.

> 🔴 **Rule**: If `node_modules` is 1GB, that's fine. If `dist/` is 10MB, you have a problem.
