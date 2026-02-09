# Protocol: Documentation Quality Gate

> **Status**: Core Implementation Standard
> **Objective**: Eliminate ambiguity and ensure 100% self-sufficiency in technical documentation.

## 1. The Clarifying Question Rule
**If a reader must ask a clarifying question, the documentation has failed.**
Every sentence should pass this test: "Could someone unfamiliar with this system execute or understand this without asking me anything?"

### Quality Markers:
*   **Executable State**: Every command or code snippet must be runnable. No placeholders like `/* logic here */`.
*   **No Assumed Knowledge**: Project-specific terms (e.g., "The Harvester") must be defined inline or linked.
*   **Realistic Examples**: Use actual file paths and table names. Avoid `foo/bar` or `example.com`.
*   **Self-Sufficiency**: The reader should not need to consult the source code to understand the documentation.

## 2. Forbidden Forbidden Phrases (Auto-Fail)
Presence of these phrases marks the document as **Draft/Incomplete**:
*   **Tier 1**: TBD, TODO, FIXME, "Coming soon".
*   **Tier 2**: "Simply", "Just", "Obviously", "Trivially". (Avoid false simplicity).
*   **Tier 3**: "Appropriately", "As needed", "When applicable". (Be specific).
*   **Tier 4**: "Check the code", "Refer to documentation". (Provide the context or link specifically).

## 3. Mandatory Context for Code
Every code block must include:
1.  **Language Tag**: For syntax highlighting.
2.  **File Path**: As a comment in the first line.
3.  **Executable Surroundings**: Imports and context required to run/compile.

## 4. The Self-Verification Protocol
Before finalizing, perform these tests:
1.  **The New Developer Test**: Can a stranger follow this without talking to you?
2.  **The Execution Test**: Copy-paste the commands. Do they work exactly as written?
3.  **The Link Test**: Do all internal/external links resolve?

---
*Created by the Librarian. Enforcing the Outstanding Skills Standard.*
