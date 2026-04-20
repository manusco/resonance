# Verification Matrix

> "Works on my machine" is a fireable offense.

## 1. The Matrix

| Environment | Chrome | Firefox | Mobile (Sim) |
| :--- | :--- | :--- | :--- |
| **Local (Dev)** | Required | Optional | Required |
| **Preview (Vercel)** | Required | Required | Required |
| **Prod** | Smoke Test | Smoke Test | Smoke Test |

## 2. The Critical Path

Identify the "Money Flows".
1.  Sign Up.
2.  Checkout.
3.  Core Value Action (e.g., "Generate Image").

These flows MUST be verified on **Production** after every deploy.

## 3. The Evidence

*   **Screenshots**: "Here is the payment success screen on Mobile."
*   **Logs**: "Here is the Stripe 200 OK webhook."

> 🔴 **Rule**: No ticket is moved to "Done" without Proof of Verification (Screenshots/Logs).
