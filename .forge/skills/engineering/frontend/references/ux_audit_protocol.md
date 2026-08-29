# UX Audit Protocol (Heuristics)

> "Don't make me think." - Steve Krug

## 1. The Interaction Cost

Minimize clicks.
*   **Rule**: 3 Clicks to Value.
*   **Audit**: Count the clicks for the critical path (e.g., Checkout). Can you remove one?

## 2. The Feedback Loop

Every action has a reaction.
*   **Click**: Does the button state change (Active/Loading)?
*   **Error**: Is the error message specific? ("Bad Request" vs "Email is invalid").
*   **Empty State**: When no data exists, do you guide the user?

## 3. Consistency

*   **Buttons**: Do primary buttons always look the same?
*   **Layout**: is the padding consistent?
*   **Language**: Do you mix "Sign In" and "Log In"? (Pick one).

## 4. The Attention Path

Before shipping UI, squint at the screen and name what the user sees first, second, and third. The implemented interface must preserve the intended job, not only match component props.

*   **Primary Lead**: The page title, key data, or primary action must lead the first glance.
*   **Action Priority**: Secondary and destructive actions must be visibly subordinate to the main action.
*   **Grouping**: Spacing must make relationships clear. Do not use boxes, borders, or separators to repair ambiguous proximity.
*   **Restraint**: Every border, shadow, background, icon, and decorative element must have a job.
*   **Shadow States**: Empty, loading, and error states must guide recovery or the next action.
*   **Access**: Contrast, focus-visible treatment, and keyboard order must be checked explicitly.

> 🔴 **Rule**: If the user has to guess what an icon means, add a label.
