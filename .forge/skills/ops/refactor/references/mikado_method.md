# Mikado Method Protocol

> "If you try to change everything at once, you will break everything at once."

## 1. The Core Concept

The Mikado Method allows you to make large-scale changes by "failing fast" and visualizing dependencies.

1.  **Set the Goal**: "Upgrade to Next.js 14".
2.  **Try it**: Just try to change it.
3.  **Fail**: It breaks. (e.g., "Link component invalid").
4.  **Draw the Dependency**: Write down "Fix Link Component" as a prerequisite.
5.  **Revert**: **CRITICAL**. Creating a clean slate.
6.  **Fix the Leaf**: Fix the "Link Component" first.
7.  **Retry**: Try the Goal again.

## 2. The Dependency Graph

*   **Goal**: Upgrade Next.js
    *   **Prereq 1**: Fix Link Component
        *   **Prereq 1.1**: Find all <a> tags.
    *   **Prereq 2**: Fix Image Component.

## 3. The Mandate

*   **Never "Push Through"**: If the detailed change fails tests, REVERT.
*   **Visualize**: Use a scratchpad to draw the tree.
*   **Commit Leafs**: Commit the small prerequisites as you fix them.

> 🔴 **Rule**: If your code doesn't compile for > 15 minutes, you are not doing Mikado. You are hacking. Revert.
