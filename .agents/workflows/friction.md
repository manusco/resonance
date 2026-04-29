---
description: Run the Friction Collider simulation to eliminate user resistance.
---

# The Friction Collider (/friction)

> **Objective**: Crash a specific User Persona into the interface to detect and eliminate resistance.

## 1. Setup: The Particles
**Define the input variables before running the simulation:**
*   **The Interface**: [URL or Content to Audit]
*   **The Goal**: [Single Desired Action, e.g., "Book Demo"]
*   **The Persona**: [Specific Archetype, e.g., "The Skeptical CTO" or "The Stressed Mom"]
*   **The Scope**: Single page OR Multi-step flow (see [Multi-Step Guidance](#multi-step-flows) below)

## 2. Run The Simulation (The 5 Sweeps)
*Execute the following simulation loop. Do not "review" the copy. BECOME the Persona.*

### Phase 1: Cognitive Force (The Brain)
> *Simulation State: You are tired, you have 15 tabs open, and you are looking for a reason to close this one.*
1.  Scan the headers. Do you understand **exactly** what the offer is in 3 seconds?
2.  Read the first paragraph. Did you have to re-read anything?
3.  Look for "Empty Calories" (words like: solution, seamless, robust, unlock).
4.  **Identify every moment you thought "Wait, what?"**

### Phase 2: Emotional Force (The Heart)
> *Simulation State: You are defensive. You hate being sold to. You smell manipulation.*
1.  Check the "Tone". Does it sound like a human or a marketer?
2.  Check the "Pressure". Is there fake urgency? (Countdowns, "Only 2 left").
3.  Check "Relevance". Does this feel like it was written *for you* or *for everyone*?
4.  **Identify every moment you felt "Ugh" or "Yeah right".**

### Phase 3: Visual Force (The Eyes)
> *Simulation State: You are scrolling fast on a phone. Your thumb is lazy.*
1.  Do the "Squint Test". Is the CTA the most obvious thing on the screen?
2.  Are the paragraphs huge walls of text? (Cognitive wall).
3.  Is the visual hierarchy leading your eye or confusing it?
4.  **Identify every moment your eye stopped flow.**

### Phase 4: Trust Force (The Gut)
> *Simulation State: You have been burned before.*
1.  Look for "Unearned Claims" (Best, #1, World-Class) without proof nearby.
2.  Look for "Generic Vibe" (Stock photos, template look).
3.  Look for "Pricing Games" (Hidden costs, "Contact for quote" on simple tools).
4.  Look for "Fabricated Evidence":
    *   Testimonial quotes with generic names and no verifiable source — **flag as invented**.
    *   Metrics without methodology or source ("500% faster", "10x ROI") — **flag as unverifiable**.
    *   Trust badges for certifications the company doesn't actually hold — **flag as fraudulent**.
    *   Screenshots or mockups that don't match the actual product UI — **flag as misleading**.
5.  **Identify every moment you thought "Is this real?" or "Prove it."**

### Phase 5: Product-Behavior Verification (The Truth)
> *Simulation State: You are a power user who has actually used the product. You read carefully.*
1.  Does every feature claim in the copy correspond to an actual, shipped product capability?
2.  Does the pricing/offer match the actual checkout flow? (No hidden fees, no bait-and-switch.)
3.  Do screenshots, mockups, or demo videos match the real UI? (No aspirational designs presented as current state.)
4.  Are testimonials attributable to real people with real affiliations?
5.  Does the "How It Works" section describe the actual product flow, or an idealized version?
6.  **Identify every moment you thought "Wait, the product doesn't actually do this."**

## 3. Multi-Step Flows

When the interface is a multi-step flow (checkout, onboarding, application form, wizard):

1.  **Run each step** as a separate simulation through all 5 sweeps.
2.  **Run transitions** as a 6th simulation:
    *   Are progress indicators clear and accurate?
    *   Can the user go back without losing data?
    *   Is state persisted if the user abandons and returns?
    *   Do error states on one step correctly prevent progression while preserving entered data?
3.  **The Abandonment Moments**: At which specific step does the user most likely think "This isn't worth it"? That is your highest-priority fix.

## 4. The Output: Release The Report
*Present the findings in the [Debris Field] format.*

### The Debris Field
| Force | The Snag (Specific Text/Element) | The Internal Monologue ("Quote") | The Smooth Slide (The Fix) |
| :--- | :--- | :--- | :--- |
| **Cognitive** | [Quote the text] | "I have to read this twice." | [Rewrite it simply] |
| **Emotional** | [Describe element] | "This feels manipulative." | [Human alternative] |
| **Visual** | [Describe layout issue] | "Where do I click?" | [Layout fix] |
| **Trust** | [Describe element] | "This looks fake." | [Specific proof element] |
| **Product-Behavior** | [Quote the claim] | "The product doesn't do this." | [Accurate description] |

### What's Working (Smooth Slides to Preserve)
> 🟢 **Rule**: Every friction report must also list what's working well. These elements must be **preserved** during optimization. Removing a working element to "fix" a friction point can cause regression.

| Element | Why It Works | Preserve? |
| :--- | :--- | :--- |
| [Quote or describe] | [Why it's effective] | ✅ Do not touch |

### Summary
*   **Total Snags Detected**: [Number]
*   **Total Smooth Slides (Working)**: [Number]
*   **Friction Score**: [High/Medium/Low]
*   **Critical Killers**: [The top 3 things that kill the sale immediately]
*   **Fabricated Claims**: [Count of invented quotes, unverifiable metrics, misleading screenshots]
*   **Product-Behavior Mismatches**: [Count of claims that don't match actual product]
