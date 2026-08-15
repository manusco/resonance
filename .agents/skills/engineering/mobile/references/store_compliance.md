# Store Compliance Checklist (Pre-Flight)

> Rejection is expensive. Check these before submission.

## Source Card

- Primary source: https://developer.apple.com/app-store/review/guidelines/
- Secondary source: https://support.google.com/googleplay/android-developer/answer/14151465
- Verified: 2026-08-15
- Scope: Apple App Store review and Google Play testing requirements.
- Review trigger: store submission, paid digital-goods change, account-system change, or store policy update.

## 1. Apple App Store

*   [ ] **Login**: If you support Google/FB Login, you **MUST** support "Sign in with Apple".
*   [ ] **Account Deletion**: User must be able to delete account *inside the app*.
*   [ ] **Permissions**: Info.plist strings (Camera, Location) must explain *why*. "We need location" -> REJECTED. "We need location to show local maps" -> ACCEPTED.
*   [ ] **UGC**: If users post content, you need: Block User, Report Content, EULA.
*   [ ] **Payments**: Digital goods and external-link rules depend on storefront, app category, entitlement, and current Apple policy. Check the current guideline before promising a payment path.

## 2. Google Play Store

*   [ ] **Data Safety**: Form must match your manifest permissions exactly.
*   [ ] **Target API**: Must target the latest Android SDK version (Update every year).
*   [ ] **Testing**: New personal developer accounts must satisfy the current Google Play closed-testing requirement before production access. As verified on 2026-08-15, Google states 12 testers for at least 14 days for the qualifying flow; confirm before submission.

## 3. Metadata Assets

*   [ ] **Screenshots**: Must show the *app*, not just marketing art.
*   [ ] **Privacy Policy**: Link must be active and accessible.
