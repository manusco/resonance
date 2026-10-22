# Protocol: project-owned design values

> **Objective**: Keep shared UI values at the source that already owns them.

Use the project's existing theme, tokens, component API, or platform value owner when one applies. Add a semantic token when multiple current callers need the same meaning or an existing contract requires it. A three-layer token system, CSS variables, or a theme provider is not a universal prerequisite.

Do not copy values into a second source of truth. A linked value file does not approve a material change to the treatment recorded in the project design contract; assess that change against the approved intent and existing authorization. For native UI, use the project's native value owner and platform conventions without CSS tooling.
