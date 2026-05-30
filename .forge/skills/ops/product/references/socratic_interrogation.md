# Protocol: Socratic Interrogation

> **"Zero Guesswork is the law."**

## 1. The Trigger (When to run this)
**DO NOT run this if the user has provided a clear spec.**
Run this ONLY when:
1.  **Ambiguity**: The goal is clear ("Build a blog") but the details are missing ("What tech stack?").
2.  **Risk**: The request implies a high-cost reversible decision.
3.  **Conflict**: The request contradicts an existing system pattern.

## 2. In-Depth Interviewing (The Loop)
*Use the `AskUserQuestion` tool. Do not dump a list of questions. Ask one or two high-value questions at a time.*

### The 5 Whys (Root Cause)
*   "You asked for X. To ensure we solve the *real* problem, can you tell me the 'Why' behind this?"
*   "What is the expensive problem this solves?"

### The Edge Case Trap
*   "What happens if this fails?"
*   "How should this behave with 0 items? With 10,000 items?"
*   "What is the mobile experience?"

### The Tradeoff Slider
*   "We can optimize for **Speed of Delivery** (MVP) or **Scalability** (Robustness). Which is the priority now?"
*   "Do you prefer **Convention** (Standard UI) or **Novelty** (Unique Code)?"

### The Kill Assumption
*   "What if we *didn't* build this feature? What breaks?"

## 3. Output
Once you have clarity, proceed to **Deep Research**.
