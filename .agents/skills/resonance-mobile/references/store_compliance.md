# Store Compliance Checklist (Pre-Flight)

> Rejection is expensive. Check these before submission.

## 1. Apple App Store (The Strict One)

*   [ ] **Login**: If you support Google/FB Login, you **MUST** support "Sign in with Apple".
*   [ ] **Account Deletion**: User must be able to delete account *inside the app*.
*   [ ] **Permissions**: Info.plist strings (Camera, Location) must explain *why*. "We need location" -> REJECTED. "We need location to show local maps" -> ACCEPTED.
*   [ ] **UGC**: If users post content, you need: Block User, Report Content, EULA.
*   [ ] **Payments**: Digital goods must use IAP. No external links to stripe.

## 2. Google Play Store (The Robot One)

*   [ ] **Data Safety**: Form must match your manifest permissions exactly.
*   [ ] **Target API**: Must target the latest Android SDK version (Update every year).
*   [ ] **Testing**: Must run Closed Testing with 20 testers for 14 days (New accounts).

## 3. Metadata Assets

*   [ ] **Screenshots**: Must show the *app*, not just marketing art.
*   [ ] **Privacy Policy**: Link must be active and accessible.
