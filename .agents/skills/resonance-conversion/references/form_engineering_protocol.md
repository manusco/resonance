# Protocol: Form Friction Engineering
> **Focus**: Data Capture Optimization
> **Resonance Phase**: Conversion / Activation

## 1. The Field Cost Axiom
Every field you add reduces conversion rate by ~3-5%.
*   **Law**: Only ask for what is mathematically necessary to permit the next step.

## 2. Multi-Step Form Patterns

### The Slippery Slope (Progressive Disclosure)
Break complex forms into steps. Each step deepens commitment.

**Step 1: Low Friction (The Handshake)**
- Fields: Email Address ONLY.
- Psychology: "That was easy." Commitment & Consistency bias activated.

**Step 2: Enrichment (The Detail)**
- Fields: Name, Password.
- Psychology: "I'm already committed." Sunk cost kicks in.

**Step 3: Qualification (The Ask)**
- Fields: Company Size, Role.
- Logic: Use Clearbit/Apollo API to auto-fill this instead of asking.

### When to Use Multi-Step
- **Use**: 5+ fields, qualification data needed, complex data capture.
- **Don't use**: Simple signup (email + password), newsletter subscribe, contact forms.

### Progress Indicators
- Show step count: "Step 2 of 3" — Zeigarnik Effect pulls completion.
- Use progress bar, not dots — bars show momentum.
- **Never lie about step count** — trust destruction if "Step 3 of 3" reveals Step 4.

## 3. Conditional Logic
Show fields only when relevant. Every hidden field is friction removed.

| Trigger | Show Field | Example |
|---------|-----------|---------|
| Role = "Developer" | "Tech stack" dropdown | Qualify without asking everyone |
| Company size > 50 | "Department" field | Only relevant for enterprise |
| Country ≠ US | "VAT number" | Tax compliance without universal friction |
| "Other" selected | Free-text input | Don't show unless needed |

**Rule**: If a field applies to <50% of users, make it conditional.

## 4. UX Micro-Interactions
- **Labels**: Top-aligned (mobile friendly), not left-aligned.
- **Inline Validation**: Specific errors ("Missing '@'") not generic ("Error").
- **Action-Oriented Buttons**: "Create Account" > "Submit".
- **Success States**: Micro-animation on valid input (green check, subtle border change).

## 5. Mobile Form Physics
- **Input Types**: Use `type="email"` and `type="tel"` to trigger the correct native keyboard.
- **Auto-Capitalization**: Turn OFF for email/username fields.
- **Hit Area**: Minimum 44px height for touch targets.
- **Field Ordering**: Most critical field first. On mobile, every scroll is a dropout.
- **Sticky CTA**: Keep submit button visible during scroll on long forms.

## 6. Conversion Killers (Audit Checklist)
1. **The Captcha**: Use invisible reCAPTCHA v3. Do not make humans identify crosswalks.
2. **Phone Number**: Do not ask unless you *will* call them within 5 minutes.
3. **"Confirm Password"**: Delete it. Use an "Eye" toggle to show password instead.
4. **Reset Button**: Remove it. No one wants to clear the form.
5. **Required Asterisks Everywhere**: If most fields are required, mark optional ones instead.
6. **Address Fields Before Need**: Don't ask for shipping address at signup.

## 7. Trust Injection
Place these *inside* or *immediately below* the form container:
- "No Credit Card Required"
- "10,000+ Designers Joined"
- Lock Icon (Security theater, but effective)
- "We'll never share your email" (below email field, not in footer)

## 8. Post-Submit
- Immediate visual confirmation (not just a page redirect).
- "Check your email" with preview of what they'll receive.
- Auto-focus next action if multi-step ("Step 2" loads instantly, no page reload).
