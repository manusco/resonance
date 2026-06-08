# Voice Test Protocol — Validating the Compiled Profile

## Contents

- [Purpose](#purpose)
- [The Test](#the-test)
- [Common Failure Modes](#common-failure-modes)
- [Delivery Checklist](#delivery-checklist)

## Purpose

After the voice file is compiled, validate it before declaring done. A file that "looks right" is not verified. A file that produces output the subject recognizes as their own — that's verified.

The test prompts, evaluation criteria, and common failure modes differ by subject type.

---

## The Test

### Step 1 — Pick a Reference Prompt

Choose a prompt the subject has already answered in their own words. Use a type-appropriate prompt:

**Person:**
- A topic they covered during extraction: "Write a short take on [belief they shared]."
- A content type they produce: "Write the opening paragraph of a newsletter about [their topic]."
- A situation with a known right answer: "Write a reply declining a collaboration request."

**Brand:**
- A scenario the brand faces regularly: "Write a social post announcing [type of news the brand shares]."
- A customer touchpoint: "Write an email response to a customer who complained about [common issue]."
- A brand situation with clear standards: "Write the first paragraph of a blog post about [core topic]."

**Role/Character:**
- A character scenario from the extraction: "Write how [character] would explain [topic] to a novice."
- A pressure test: "Write how [character] responds to being told they're wrong about something."
- A consistency check: "Write [character] in a formal situation vs. a casual one."

### Step 2 — Run Two Sessions

**Session A — No profile:**
Open a blank session. Run the prompt with no context file. Save the output.

**Session B — With profile:**
Open a blank session. Paste the `<voice_profile>` as context. Run the exact same prompt. Save the output.

### Step 3 — Show Both to the Subject

Present Session A and Session B side by side. Ask:

1. "Which one sounds more like [you / us / the character]?"
2. "Point at the specific line in the wrong version that's most wrong."
3. "Is there anything in the right version that still doesn't sound right?"

### Step 4 — Evaluate

| Result | Action |
| :--- | :--- |
| Session B is clearly better | Profile is working. Deliver. |
| Sessions are indistinguishable | Profile isn't injecting enough signal. Identify the weakest section and run targeted follow-up. |
| Session B is worse | Profile has contradictory or noisy rules. Audit `<writing_laws>` and `<voice_fingerprint>` first. |
| Subject says "close, but..." | Ask them to name the gap. Patch only that section. No full rewrites. |

---

## Common Failure Modes

### Person

**"It sounds like a better version of me, not actually me."**
→ The file is preserving aspiration, not behavior. Check `<voice_fingerprint>` and `<signature_tells>`. Did any awkward phrases, "flaws," or quirks from the corpus get cut? Put them back.

**"It sounds too formal / too casual."**
→ Emotional temperature is off. Return to the corpus. Find 3 examples of the actual register. Update `<voice_fingerprint>` with specific behavioral evidence.

**"It doesn't refuse the right things."**
→ `<hard_refusals>` is under-specified. Return to the gap interview's Hard Refusals answers. Add specific examples in the `<never>` format.

**"Every sentence ends the same way."**
→ `<writing_laws>` are over-constraining rhythm. Add a `<productive_contradictions>` tension: "Writes in short punchy sentences AND occasionally lets a longer thought breathe. Preserve both."

---

### Brand

**"It sounds like our competitor."**
→ The `<voice_fingerprint>` captured generic industry voice, not brand-specific voice. Return to the corpus. Find what the brand does that competitors demonstrably don't. Update with that specificity.

**"It sounds like our mission statement, not how we actually write."**
→ The file contains aspirational brand values that didn't appear in the corpus. Audit `<identity_context>` and `<writing_laws>` for anything that can't be backed by a corpus quote. Cut it.

**"It's too cautious / too loud / too casual."**
→ The brand's actual temperature (from corpus) was overridden by self-described temperature. Return to corpus. Find the actual temperature. Trust it over the stated one.

**"It doesn't know how we talk to [specific audience]."**
→ The corpus was too homogeneous. The profile only captured one context. Request content from the missing audience context. Update `<communication_laws>` with the specific switch.

---

### Role / Character

**"The character sounds like a generic AI assistant."**
→ Generic AI voice bled through despite the profile. Audit `<voice_fingerprint>` for anything that's actually a default AI pattern rather than a character-specific pattern. Replace with character-specific observations.

**"The character would never say that."**
→ `<hard_refusals>` and `<character_limits>` are under-specified. Return to the Gap Track C Character Limits answers. Add specific `<never>` entries.

**"The character is inconsistent across situations."**
→ Context consistency rules weren't captured. Return to Gap Track C Context Consistency answers. Add specific `<communication_laws>` for each situation type.

---

## Delivery Checklist

- [ ] Test run on at least one reference prompt appropriate to subject type
- [ ] Subject confirmed "this sounds like [me / us / the character]" on Session B
- [ ] Voice file saved with the correct filename:
  - Person → `about-me.md`
  - Brand → `brand-voice.md`
  - Role/Character → `[name]-persona.md`
- [ ] Token count confirmed under 5,000
- [ ] Subject knows the file should be updated when their voice evolves (or the brand repositions, or the character is redesigned)
