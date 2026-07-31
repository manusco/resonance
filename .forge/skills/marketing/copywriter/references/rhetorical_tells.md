# Rhetorical Tells (the shape layer)

> **Objective**: Catch the sentence shapes that mark machine-written prose, the layer above the word Kill List.
> **The rule that governs this whole file**: a word tell is zero-tolerance, a figure tell is dose-dependent. One antithesis on a page is craft. An antithesis in every paragraph is the machine. Do not ban the figures. Ration them.

The word lists (`taboo_phrases`, `anti_slop`) fight vocabulary. Models already learned to drop "delve." What they kept is the architecture underneath: the pivot, the triad, the dramatic closer. A sentence can carry no banned word, run active and short, and still be unmistakably AI because of its shape. "This isn't about features. It's about trust." has zero banned words and would pass every word check while being the single loudest current-generation tell. This file is the referee for that.

## Contents

- [The dose principle](#the-dose-principle)
- [1. Corrective negation and antithesis](#1-corrective-negation-and-antithesis)
- [2. Landing sentences and setup or payoff](#2-landing-sentences-and-setup-or-payoff)
- [3. The rule of three](#3-the-rule-of-three)
- [4. Negative anaphora and parallelism](#4-negative-anaphora-and-parallelism)
- [5. Parallel skeletons](#5-parallel-skeletons)
- [6. Nominalization and stacked nouns](#6-nominalization-and-stacked-nouns)
- [7. Staccato runs](#7-staccato-runs)
- [8. Throat-clearing and performed enthusiasm](#8-throat-clearing-and-performed-enthusiasm)
- [The grill pass](#the-grill-pass)

## The dose principle

These figures are persuasion primitives, thousands of years old, and they work. Contrast, the triad, parallelism: a good writer reaches for one on purpose, when the moment earns it. The tell is not the figure. It is the frequency and the reflex. A model reaches for the pivot as its default sentence engine, so the pivots stack up until the page reads like a machine performing rhythm. Judge by dose and by intent, never by a blanket ban. Ban them outright and you get flat, gutless copy, which is its own kind of tell.

So every entry below gives the shape, why it reads as machine, and the dose rule for when it earns its place.

## 1. Corrective negation and antithesis

The shape: "It's not X. It's Y." "This isn't just a tool, it's a system." "Not because A, but because B."

Why it reads as machine: the model treats the pivot as punchy rhythm, so it reaches for it constantly, several times a page, whether or not there is a real belief to correct.

The dose rule: negate only a belief the reader actually holds. Myth-busting earns it, and so does a Sophistication-3 mechanism ("it is not your slow metabolism, it is a clogged receptor") because the reader really believes the wrong thing. Correcting a strawman nobody holds is decoration. If the reader would not nod at the "not X" half, cut the whole construction and state Y on its own.

## 2. Landing sentences and setup or payoff

The shape: a paragraph that builds, then drops a short dramatic closer. "And that changes everything." "That is the whole game."

Why it reads as machine: the model pins nearly every paragraph with one, and the rhythm turns into a metronome.

The dose rule: earn it, and rarely. A landing line lands only when the paragraph did real work and the line is not just a restatement of it. Perhaps one on a page. When every section ends on the same drumbeat, none of them does.

## 3. The rule of three

The shape: the triad. "Fast, simple, and secure." "We built it. We tested it. We shipped it." Adjectives stacked in threes.

What is fine: a factual list that happens to hold three items. What is the tell: the cadence, the drumroll used for effect, again and again down the page.

The dose rule: vary the count. Two items, or four, or one. When you do land on three, make each carry real content instead of three near-synonyms for the same idea.

## 4. Negative anaphora and parallelism

The shape: "No fluff. No filler. No fees." "It will not slow you down. It will not lock you in."

The dose rule: once, for a genuine set of real negatives, is fine. Repeated down the page as a rhythmic device, it is the machine. The correlative form, "not only X but also Y," almost never reads human; avoid it outright.

## 5. Parallel skeletons

The shape: three or more sentences inside one paragraph sharing the same grammatical frame.

The dose rule: no more than two sentences share a skeleton before you break it. Deliberate parallelism is real rhetoric. A paragraph built entirely on one frame is a template.

## 6. Nominalization and stacked nouns

Nominalization is a verb hiding as a noun. "The utilization of" for "using". "The implementation of" for "building". Find the buried verb and use it.

Stacked nouns are a pile of nouns worn as adjectives. "Next-generation cloud-native observability platform." Break it apart, or cut most of it. German suffers this worse; see `german_anti_slop` for Substantivketten and Nominalstil. The rule is the same in English.

## 7. Staccato runs

Short, punchy sentences are good, and burstiness is a law here (see `rubric` and `entropy_protocol`). The tell is the run: five short equal clauses in a row, the fake-punchy machine cadence. Land a longer sentence before the third short one, so the rhythm breathes instead of chopping.

## 8. Throat-clearing and performed enthusiasm

Throat-clearing is an opener that says nothing before the point. "It is worth noting that", "In a world where", "Let's face it". Cut to the point. The word-level openers live in `taboo_phrases`.

Performed enthusiasm is energy the writer does not feel. "We are SO excited." State the thing and let the reader feel it. See Trust Integrity: do not perform what you have not earned.

## The grill pass

This file is the checklist for the copywriter's Grill step (Draft, Edit, Humanize, Grill, Polish). On the near-final draft, read as an artifact rather than as its writer:

- Hunt each figure above. For every hit, decide whether it is the one earned instance or the reflex. If it is the reflex, rewrite it and state the point plainly.
- Every finding carries a proposed fix, never a bare complaint.
- Loop until the page reads like one person talking, with the figures rare and earned.

The deterministic checks (the copy-mode guard, the eval patterns) catch the mechanical surfaces such as "not only... but also" and the filler intensifiers. This pass catches everything that needs a reader's judgment.
