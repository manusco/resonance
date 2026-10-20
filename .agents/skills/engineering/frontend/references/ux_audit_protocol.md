# UX Audit Protocol (Heuristics)

> "Don't make me think." - Steve Krug

## 1. The Interaction Cost

Minimize clicks.
*   **Audit**: Trace the critical task path. Remove steps only when the task remains understandable, safe, and recoverable; there is no universal click quota.

## 2. The Feedback Loop

Every action has a reaction.
*   **Click**: Does the button state change (Active/Loading)?
*   **Error**: Is the error message specific? ("Bad Request" vs "Email is invalid").
*   **Empty State**: When no data exists, do you guide the user?

## 3. Consistency

*   **Buttons**: Do primary buttons always look the same?
*   **Layout**: is the padding consistent?
*   **Language**: Do you mix "Sign In" and "Log In"? (Pick one).

## 4. The Task Path

Before shipping UI, squint at the screen and name what the user sees first, second, and third. The implemented interface must preserve the intended job, not only match component props.

*   **Task lead**: Make the status, information, and action needed for the next consequential task easy to find. Support multiple peer actions when the workflow has legitimate branches.
*   **Action priority**: Set hierarchy from task frequency, consequence, and reversibility. Keep destructive scope and consequence clear, with a safe exit or confirmation when justified.
*   **Responsive content**: At 320 CSS px and supported zoom, preserve ordinary content flow and task actions. Keep genuine table comparison operable, even if its own region needs horizontal inspection.
*   **Forms and overlays**: Preserve entered data on failure. Choose inline, modal, nonmodal, or route behavior from interruption, reference needs, task length, and viewport.
*   **Grouping**: Spacing must make relationships clear. Do not use boxes, borders, or separators to repair ambiguous proximity.
*   **Restraint**: Every border, shadow, background, icon, and decorative element must have a job.
*   **Shadow States**: Empty, loading, and error states must guide recovery or the next action.
*   **Access**: Contrast, focus-visible treatment, and keyboard order must be checked explicitly.

> 🔴 **Rule**: If the user has to guess what an icon means, add a label.
