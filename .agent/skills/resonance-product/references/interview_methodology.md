# Protocol: Iterative Interview Methodology

> **"You cannot ask good detailed questions about something you don't understand."**

## 1. The Core Philosophy
The interview process builds understanding progressively, from rough shape to a complete mental model. Each pass establishes the foundation for the next. Do not ask about edge cases before you understand the flow.

## 2. The 4-Pass Methodology

### Pass 1: The Shape (Establish the Rough Goal)
*   **Purpose**: Understand WHAT we're building and WHY.
*   **Checkpoint**: You must be able to state the feature's soul in one sentence.
*   **Questions**:
    *   "In one sentence, what is this feature?"
    *   "What problem does this solve?"
    *   "Who or what uses this?"
    *   "What is explicitly OUT of scope?"

### Pass 2: The Flow (Establish the End-to-End Process)
*   **Purpose**: Understand HOW it works at a flowchart/sequence level.
*   **Checkpoint**: You can draw a mental (or ASCII) flowchart of the major stages.
*   **Questions**:
    *   "Walk me through this end-to-end. What's the trigger?"
    *   "And then what happens next?"
    *   "Where does this split into different paths?"
    *   "Where does it end?"

### Pass 3: The Detail (Flesh Out Each Stage)
*   **Purpose**: For EACH stage in Pass 2, gather exact specs.
*   **Checkpoint**: You know the inputs, outputs, and business logic for every node.
*   **Questions**:
    *   "What data does this stage need as input?"
    *   "What are the specific validation rules here?"
    *   "Does this touch persistent storage or external APIs?"

### Pass 4: The Completeness (Edge Cases & Resilience)
*   **Purpose**: Ensure the system is robust and failure-aware.
*   **Checkpoint**: Every failure path has a defined recovery strategy. No "TBD" allowed.
*   **Questions**:
    *   "What happens if a dependency is unavailable?"
    *   "What if the input is malformed?"
    *   "How do we know if this is working in production (Observability)?"

## 3. Decision Forcing (The "No TBD" Rule)
*   **Ambiguity is a bug**. If the user says "it depends," force a default.
*   **Default Selection**: "Let's pick a default. What should it be? Under what circumstances would someone change it?"
*   **Guess and Verify**: "What's your best guess? We can mark it as an assumption for now."

## 4. The Clarifying Question Test
Before finishing, read your internal notes. **If a developer would have to ask a clarifying question to implement this, the interview has failed.**

---
*Created by the Product agent. Enforcing the Outstanding Skills Standard.*
