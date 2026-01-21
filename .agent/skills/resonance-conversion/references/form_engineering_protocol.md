# Protocol: Form Friction Engineering
> **Focus**: Data Capture Optimization
> **Resonance Phase**: Conversion / Activation

## 1. The Field Cost Axiom
Every field you add reduces conversion rate by $X\%$.
*   **Law**: Only ask for what is mathematically necessary to permit the next step.

## 2. Optimization Pattern: The "Slippery Slope"

### Step 1: Low Friction (The Handshake)
*   **Fields**: Email Address ONLY.
*   **Psychology**: "That was easy."

### Step 2: Enrichment (The Detail)
*   **Fields**: Name, Password.
*   **Psychology**: "I'm already committed."

### Step 3: Qualification (The Ask)
*   **Fields**: Company Size, Role.
*   **Logic**: Use Clearbit/Apollo API to auto-fill this instead of asking.

## 3. UX Micro-Interactions
*   **Labels**: Top-aligned (Mobile friendly) not Left-aligned.
*   **Inline Validation**: specific errors ("Missing '@'") not generic ("Error").
*   **Action-Oriented Buttons**: "Create Account" > "Submit".

## 4. Mobile Form Physics
*   **Input Types**: Use `type="email"` and `type="tel"` to trigger the correct native keyboard.
*   **Auto-Capitalization**: Turn OFF for email/username fields.
*   **Hit Area**: Minimum 44px height for touch targets.

## 5. Conversion Killers (Audit Checklist)
1.  **The Captcha**: Use invisible reCAPTCHA v3. Do not make humans identify crosswalks.
2.  **Phone Number**: Do not ask unless you *will* call them within 5 minutes.
3.  **"Confirm Password"**: Delete it. Use an "Eye" toggle to show password instead.
4.  **Reset Button**: Remove it. No one wants to clear the form.

## 6. Trust Injection
Place these *inside* or *immediately below* the form container:
*   "No Credit Card Required"
*   "10,000+ Designers Joined"
*   Lock Icon (Security theater, but effective)
