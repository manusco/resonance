# Destructive Testing Protocol (Chaos)

> "The system will fail. The only question is when."

## 1. The Attack Vectors

Do not just test the "Happy Path". You must actively try to destroy the app.

1.  **The Double Click**: Click the "Submit" button 10 times rapidly. Does it charge 10 times?
2.  **The Network Cut**: Submit a form, then kill the wifi (Simulate offline). Does it recover?
3.  **The Input Fuzz**: Paste 10,000 emojis into the "Name" field. Does the DB crash?
4.  **The Race Condition**: Open the page in two tabs. Update tab A. What happens in Tab B?

## 2. The Mandate

**For every Feature PR:**
*   You MUST run at least one destructive test.
*   Document it in the PR: "Tested Double-Click on Payment: Handled correctly (Disabled button)."

> 🔴 **Rule**: If you can break it in 5 seconds, the user will break it in 1.
