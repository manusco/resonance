# Extraction Protocol — Observe, Confirm, Fill

## Contents

- [The Method](#the-method)
- [Stage 0 — Identify Subject Type](#stage-0--identify-subject-type)
- [Stage 1 — Corpus Intake & Analysis](#stage-1--corpus-intake--analysis)
- [Stage 2 — Gap Interview](#stage-2--gap-interview)
- [No-Corpus Fallback](#no-corpus-fallback)
- [What to Track Throughout](#what-to-track-throughout)

## The Method

Text is ground truth. What someone says about how they sound is opinion. Start with the text.

The extraction runs in two stages:
1. **Corpus Analysis** — Read their writing. Extract observable behavioral patterns. Present them as hypotheses with evidence.
2. **Gap Interview** — Ask only about what text cannot reveal: beliefs/positioning, refusals, red flags, decision rules.

The gap interview has three distinct tracks depending on subject type. Run only the track that matches.

---

## Stage 0 — Identify Subject Type

This is the first question you ask. Everything else depends on it.

> "Before we start — are we capturing a **personal voice** (an individual's writing style), a **brand voice** (a company or product's communication), or a **character/persona** (a designed role, fictional character, or AI personality)?"

| Subject Type | Corpus Source | Output File |
| :--- | :--- | :--- |
| **Person** | Personal writing: emails, posts, essays, messages | `about-me.md` |
| **Brand** | Brand content: website, social, emails, pitch decks, press, ads | `brand-voice.md` |
| **Role/Character** | Character artifacts: scripts, example conversations, character notes, reference archetypes | `[name]-persona.md` |

If ambiguous (e.g. "my startup's voice but it's really just me"), default to **Brand**. Note in the compiled file that the brand voice is founder-driven.

---

## Stage 1 — Corpus Intake & Analysis

### Step 1: Request the Corpus

Use the type-appropriate ask:

**Person:**
> "Before I ask you anything, I want to read your writing. Share 2–5 pieces — different contexts if you have them. Could be emails, posts, essays, Slack messages, anything you've actually written. No minimum length."

**Brand:**
> "Before I ask anything, I want to read the brand's actual content. Share 2–5 pieces across different contexts — website copy, a social post, a customer email, a pitch deck slide, a press quote. The more contexts the better."

**Role/Character:**
> "Before I ask anything, share 2–5 examples of this character in action — scripts, example conversations, reference material, anything that shows how they're supposed to sound. Include edge cases or 'wrong' examples if you have them; those are useful too."

If there is nothing to share, go to the **No-Corpus Fallback** at the bottom of this document.

### Step 2: Read Everything

Read all pieces silently using the **Text Analysis Dimensions** as your lens. Scan all 12 dimensions. Do not ask questions yet.

> See also: `ops/voice/references/text_analysis_dimensions.md` for all 12 dimensions with examples.

For **Brand** corpora: pay extra attention to pronoun stance (we/you/they), formality register across contexts, and vocabulary the brand appears to own vs. avoid.

For **Role/Character** corpora: pay extra attention to consistency across situations, how the character handles being challenged, and any apparent "rules" embedded in the examples.

### Step 3: Build the Fingerprint Report

Surface 8–12 specific, falsifiable observations. Each must:
- Name the dimension
- State the observed behavior
- Cite a quote from the corpus as evidence

**Format:**
> "[Dimension]: [Behavioral statement]. Evidence: '[quote].' Is this deliberate, or does it surprise you?"

**Quality gate**: If an observation could describe 40% of writers or brands, cut it. Only keep what's distinctive.

### Step 4: Present Hypotheses — One at a Time

Present each observation individually. Wait for response before the next. Track:
- **Confirm** → Lock it in.
- **Deny** ("that piece is unusual") → Note the exception, ask what typical looks like.
- **Refine** ("yes, but only for [audience/context]") → Capture the condition.
- **Surprise** ("I didn't realize we did that") → Unconscious tell. Mark it. Highest-signal data point.

Push back on vague responses:
- "I guess that's right" → "Show me another example from a different piece."
- Blanket denial → "Here's a second instance. Is this also an exception?"

---

## Stage 2 — Gap Interview

After hypotheses are confirmed or denied, shift to the Gap Interview. Ask only what text cannot reveal.

**One question at a time. Follow threads. Cut questions that are redundant given what you already know.**

---

### Gap Track A — Person

**Beliefs & Contrarian Takes**
What careful writing hides:
- "What do most people in your field believe that you think is wrong?"
- "What would you defend in an argument even if it made people uncomfortable?"
- "What's a common piece of advice you find lazy or inaccurate?"

**Hard Refusals**
The personal fence around the voice:
- "What topic or angle would you never write about, regardless of who asked?"
- "Is there a format or structure you refuse to use?"
- "What would make you decline a writing project entirely?"

**Red Flags**
How they detect bullshit — shapes editorial judgment:
- "What makes you immediately distrust a piece of writing?"
- "What signals that someone doesn't actually know their subject?"
- "What phrase, when you read it, makes you close the tab?"

**Context Switches**
How voice shifts — the corpus may show only one context:
- "How does your writing change when you're angry vs. when you're explaining something patiently?"
- "Do you write differently for email vs. public posts? Describe the difference."
- "What does writing for yourself look like vs. writing for an audience?"

**Decision Rules**
How they judge quality:
- "What makes something worth saying?"
- "What's your test for whether a piece of writing is done?"
- "How do you know when something sounds wrong, even when you can't explain why?"

**Coverage Checklist — Person:**
- [ ] 2–3 specific contrarian beliefs confirmed
- [ ] 3+ specific hard refusals confirmed (topics, formats, situations)
- [ ] 2–3 specific red flag phrases or patterns named
- [ ] Context switches captured if corpus shows only one register
- [ ] Quality decision rules captured
- [ ] All 12 fingerprint dimensions confirmed or noted

---

### Gap Track B — Brand

**Positioning Beliefs**
What the brand actually stands for vs. what competitors also claim:
- "What does [Brand] believe that your competitors don't say publicly — or say but don't mean?"
- "What do you stand for that you rarely say explicitly in your marketing?"
- "What industry belief or convention does [Brand] reject?"

**Brand Safety Refusals**
The hard lines around the brand voice:
- "What would you never publish under the [Brand] name, regardless of context?"
- "Are there content categories, tones, or formats that are off-limits?"
- "What would make you pull a piece of content that was already live?"

**Competitor Red Flags**
How they detect weak brand communication — shapes quality judgment:
- "Show me a competitor's copy that makes you cringe. What's wrong with it specifically?"
- "What does 'off-brand' look like for [Brand]? Give me an example."
- "What phrase or pattern, when you see it in the market, signals lazy brand thinking?"

**Audience & Context Switches**
How the brand voice shifts — the corpus may show only one audience:
- "How does the brand voice shift when talking to [audience A] vs. [audience B]?"
- "What changes in tone or vocabulary when you're in crisis mode vs. growth mode?"
- "How does the voice differ between a sales email and a press release? Between social and a CEO letter?"

**Brand Decision Rules**
Who decides if something is on-brand and how:
- "Who is the internal arbiter of 'does this sound like us?' What's their gut test?"
- "What's the difference between a piece that's acceptable and a piece that's genuinely on-brand?"
- "What would a customer say about [Brand]'s voice if they had to describe it to someone unfamiliar?"

**Coverage Checklist — Brand:**
- [ ] 2–3 specific positioning beliefs confirmed (not generic values)
- [ ] 3+ specific brand safety refusals confirmed
- [ ] 2–3 specific competitor red flags or off-brand patterns named
- [ ] Audience/context switches captured across at least 2 contexts
- [ ] Brand quality decision rules captured
- [ ] All 12 fingerprint dimensions confirmed or noted

---

### Gap Track C — Role / Character

**Character Worldview**
What the character believes — shapes how they speak and judge:
- "What does this character believe that most people around them don't?"
- "What is this character right about that others underestimate?"
- "What does this character find genuinely stupid or frustrating?"

**Character Limits**
What breaks the character:
- "What would this character never say, regardless of how the user prompts them?"
- "What behavior or tone would immediately break the illusion for someone familiar with this character?"
- "Is there a situation where the character would refuse to engage? What does that refusal look like?"

**Character Reactions**
How the character behaves under pressure — the corpus rarely shows this:
- "How does this character respond when they're wrong?"
- "How do they handle being challenged or pushed back on?"
- "What does this character sound like when they're genuinely excited vs. skeptical?"

**Context Consistency**
How the character maintains voice across situations:
- "How does the character's voice shift in a formal vs. casual situation?"
- "How do they adjust for an expert vs. a novice audience without losing character?"
- "Are there any situations where you'd expect them to sound different? How?"

**Character Rules**
The quality standard for staying in character:
- "If someone handed you a script for this character and it felt 'off', what would be wrong with it?"
- "What's the one thing that makes this character feel real vs. performative?"
- "What's the easiest mistake an AI would make when imitating this character?"

**Coverage Checklist — Role/Character:**
- [ ] 2–3 specific worldview beliefs confirmed
- [ ] 3+ specific character limits/refusals confirmed
- [ ] Character reactions under pressure captured (wrong, challenged, excited, skeptical)
- [ ] Context consistency rules captured
- [ ] Quality standard for staying in character captured
- [ ] All 12 fingerprint dimensions confirmed or noted

---

## No-Corpus Fallback

If the subject has nothing to share, use the type-appropriate fallback:

**Person — Option A (preferred):**
> "No problem. Write me three sentences right now: a cold email declining a meeting, a reply to someone who gave you advice you disagreed with, and the first line of something you actually care about. Don't overthink it."
Three sentences across three situations. Analyze those, then run Gap Track A.

**Person — Option B (if they resist):**
Run Gap Track A only. Add: "Give me a sentence you've written that sounds exactly like you." / "Give me something you'd rewrite now." / "What's a word you use too much? One you'd never use?"

**Brand — Option A (preferred):**
> "No problem. Send me three pieces of copy that already exist: one customer-facing sentence from your website, one recent social post, and one internal communication (email, Slack, memo). Those three already reveal a lot."

**Brand — Option B (if nothing exists — new brand):**
This is a brand voice creation, not extraction. Switch method: ask about aspirational voice, reference brands they admire and why, reference brands they'd never want to sound like and why. Flag in compiled file: `<corpus_quality>New brand. No published content analyzed. Voice profile based on aspirational positioning — validate against first published content.</corpus_quality>`

**Role/Character — Option A (preferred):**
> "No problem. Write me three lines this character would say in three situations: turning someone down, explaining something complex to a novice, and reacting to being wrong. Don't overthink it."

**Role/Character — Option B:**
Run Gap Track C directly. The character definition is largely intentional — self-description is more reliable for designed characters than for humans.

---

## What to Track Throughout

Across all subject types, maintain a running note of:
- **Recurring patterns** — same behavior across multiple pieces or answers
- **Productive contradictions** — corpus says X, subject describes Y — preserve both
- **Unconscious tells** — things they didn't know they did (or the brand does) — highest-signal data points

These feed directly into `<productive_contradictions>` and `<signature_tells>` in the compiled file.
