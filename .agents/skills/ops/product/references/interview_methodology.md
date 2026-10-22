# Protocol: Iterative Interview Methodology

> **"You cannot ask good detailed questions about something you don't understand."**

## 1. The Core Philosophy
The interview process builds understanding progressively, from rough shape to a complete mental model. Each pass establishes the foundation for the next. Do not ask about edge cases before you understand the flow.

## 2. A 4-Pass Guide

Use the passes to uncover what this decision needs, not as a mandatory script. Scale depth to the consequence, reversibility, uncertainty, and cost of delay. A small reversible test may need only a brief problem and outcome check; a high-impact or hard-to-reverse commitment needs stronger evidence and fuller failure analysis.

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
*   **Checkpoint**: Important failure paths have a defined recovery strategy, or remain explicit assumptions with an owner and validation step.
*   **Questions**:
    *   "What happens if a dependency is unavailable?"
    *   "What if the input is malformed?"
    *   "How do we know if this is working in production (Observability)?"

## 3. Handle Uncertainty
*   Resolve ambiguity when it changes a consequential decision or creates material implementation risk.
*   If a decision is low-risk and reversible, choose a provisional default only when useful, and state what would change it.
*   If evidence is missing or the choice is premature, record the assumption, confidence, owner, and cheapest useful validation step. Do not turn an unknown into a requirement.

## 4. The Clarifying Question Test
Before handing work to engineering, distinguish blocking unknowns from details that can safely remain provisional. A blocking unknown needs an answer or an explicit validation gate; non-blocking uncertainty can remain documented with an owner and next step.
