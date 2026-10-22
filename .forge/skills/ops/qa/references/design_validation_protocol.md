# Protocol: UI design validation

> **Objective**: Verify changed UI against applicable project intent and real rendered behavior.

## 1. Resolve the reference

Use the app's declared design source, then `.resonance/05_design.md`, then maintained local discovery. Discovery identifies evidence; it does not make a draft or exploration approved. Read only the rules and sources relevant to the changed UI.

## 2. Compare like with like

- Compare the changed screen or state with the approved default for its task family and a relevant sibling or reference.
- Use a comparable viewport and state. Check layout, content hierarchy, interaction, focus, and reachable states that the change affects.
- Follow explicit approved variant conditions. Do not infer a variant from the page name or register.
- A focused check is enough for routine reuse; do not require a full product inventory.
- Use a project-appropriate reference such as a maintained design file, implementation source, or sibling screen. Figma is optional.

## 3. Report evidence honestly

Cite the applicable rule, reference, viewport/state, and observed result. Missing rendered or comparison evidence means visual conformance is **unverified**. Source inspection alone cannot prove rendered consistency. A linked component or token file is the value owner, not approval for a material change to the approved treatment.

## 4. Report a mismatch

Name the component, expected approved pattern, actual behavior, and smallest correction. Preserve keyboard focus, accessibility, safety, and user data even when an approved rule conflicts; identify the conflict and do not claim conformance. Keep a material taste change proposed until authorized through existing project approval.
