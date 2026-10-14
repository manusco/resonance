# First-principles reasoning: evidence and skill recommendations

**Question.** How should Resonance improve first-principles reasoning so agents challenge inherited assumptions without mistaking every non-physical constraint for disposable convention, or rebuilding a problem from scratch?

**Scope.** Research note for skill authors. It does not edit skills, generated files, or the public scaffold. The working hypothesis is that the current “reject best practice if it contradicts Physics or Logic” rule leaves important constraint types underspecified, while its unsupported CI-cost example can encourage false certainty. The rule does not literally say that only physical constraints are valid. Sources below include primary philosophical texts, a primary scientific-method essay, Shannon’s technical paper, and current government standards.

## Finding

Replace the physics-versus-culture dichotomy with a constraint ledger. An agent should classify each premise before challenging it, identify its evidence and owner, and test whether changing it preserves the requested outcome and safeguards. “First principles” is a way to expose dependencies, not proof that the agent has found an unquestionable foundation.

| Kind of premise | Example | How to challenge it | What can establish it |
|---|---|---|---|
| Mathematical or logical | An invariant, type rule, conservation relation | Check definitions, derivation, counterexample, or proof | Formal derivation or executable property |
| Physical or technical | Device limit, latency, capacity, platform behavior | Measure the actual environment; state model and tolerance | Reproducible measurement or authoritative platform specification |
| Empirical estimate | Conversion rate, workload, failure frequency | State uncertainty, sample, and an observation that would change the estimate | Data, experiment, operational history |
| Legal, contractual, or security | Data handling duty, customer promise, threat control | Find the governing source and responsible owner; test applicability and scope | Applicable law or signed terms; threat model and security standard/control |
| Convention or interface | API shape, workflow, file format, team practice | Find the coordination, compatibility, migration, or user cost it serves; trial a bounded change | Callers, dependency contracts, user evidence, migration/reversal plan |
| Preference or goal | Tone, workflow, quality target | Confirm whose preference it is and whether it is explicit; compare outcomes | User instruction or agreed product goal |

Do not treat these categories as a ranking. A convention may be cheap to change or may preserve compatibility with many users. A legal or security claim may be inapplicable, but an agent must establish that before dropping it. A physical limit can also be mismeasured or based on an incomplete model. Name the claim, its provenance, and confidence.

## What the sources support

- **First principles do not mean assumption-free reasoning.** In *Posterior Analytics* II.19 Aristotle describes primary premises as arising through perception, memory, repeated experience, and induction. This is a useful corrective to the idea that a reasoner can simply strip away tradition and reach pure certainty. (Primary text: [Aristotle, *Posterior Analytics*, II.19](https://classics.mit.edu/Aristotle/posterior.2.ii.html).)
- **Radical doubt is not a universal work procedure.** Descartes explicitly distinguishes his search for truth from practical action, where uncertain opinions may need to be adopted provisionally. His method is a targeted philosophical project, not a direction to suspend all working assumptions in ordinary tasks. (Primary text: [Descartes, *Discourse on the Method*, Part IV](https://www.gutenberg.org/files/59/59-h/59-h.htm).)
- **Verification requires attempts to find failure.** Feynman warns that a procedure can imitate scientific form while insulating its claim from adverse evidence. Popper’s “Conjectures and Refutations” likewise says tests should expose a claim to possible refutation, and notes that instruments may leave the result uncertain. These support predeclared counterevidence and honest confidence, not claims of certainty after a passing test. ([Feynman, “Cargo Cult Science”](https://calteches.library.caltech.edu/51/2/CargoCult.htm); [Popper, “Science: Conjectures and Refutation”](https://kpfu.ru/staff_files/F812164186/HISTORY_AND_PHILOSOPHY_OF_SCIENCE_COMMON_PROBLEMS.pdf), pp. 183–185.)
- **Formal truth is scoped to a model.** Shannon’s communication theory makes its chosen problem and assumptions explicit, then derives results within that model. This shows how powerful formal reasoning is when its boundary is stated; it does not turn an engineering abstraction into a universal account of user goals or organizational obligations. ([Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal* 27 (1948)](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb00917.x); [full text scan](https://www.cs.yale.edu/homes/yry/readings/general/shannon1948.pdf).)
- **Software safety constraints can be integrated rather than discarded as ceremony.** NIST’s SSDF describes security practices that can be added to different lifecycle models, to reduce vulnerabilities and mitigate exploitation impact. The standard supports checking the source, risk, and applicability of a practice, not reflexively removing it because it is not a law of physics. ([NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final).)
- **Obligations have distinct provenance.** For example, GDPR is a regulation with scope and applicability conditions, not a preference or a physical law. A skill should direct agents to identify the applicable provision and context, not announce generic compliance based on a vague “legal constraint.” ([Regulation (EU) 2016/679, official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj).)

These sources differ in purpose and authority. The philosophical texts clarify limits on the method; they do not validate a software workflow. NIST and EU law are operational sources in their domains. Shannon is a technical example of model-relative derivation. Treating these as the same kind of evidence would repeat the category error the method should prevent.

## Recommended mechanism for the skills

Use one compact sequence in the shared first-principles reference, then point appropriate build, plan, architecture, debugger, and design procedures to it rather than copying a new framework into each skill:

1. **State the requested outcome and boundary.** Record what must remain true, explicit preferences, non-goals, and safeguards. Don’t widen the task while decomposing it.
2. **List consequential premises with provenance.** For each, label it as mathematical/logical, physical/technical, empirical, legal/contractual/security, convention/interface, or preference/goal. Record evidence, owner, uncertainty, and the cost of being wrong. Skip trivial premises.
3. **Ask what would change the decision.** For each material premise, write one concrete observation, counterexample, governing source, or stakeholder answer that could overturn it. Challenge one-way doors more deeply than reversible choices.
4. **Separate decomposition from proof.** Break an outcome into required conditions only as far as needed to choose or implement a change. At each leaf, cite a derivation, observed result, governing source, explicit instruction, or named unresolved assumption. Stop when another layer would not change the decision or safeguard.
5. **Compare the smallest viable options.** Include the inherited practice and the smallest bounded alternative. Compare user outcome, risk/safeguard, compatibility and migration cost, and evidence needed. Do not assume removing a convention is cheaper than preserving it.
6. **Set a falsifiable check and reversal trigger.** State the expected result, how it will be observed, and what failure would cause the choice to be revised. Keep uncertain estimates marked as estimates. Use a reproduction or test where the claim concerns executable behavior.

**Bound the regress and avoid reinvention.** Treat verified platform behavior, applicable obligations, approved scope, and explicit user requirements as working premises with citations or pointers. This is a practical stopping rule, not a claim that they are metaphysically irreducible. Before replacing a convention, inspect its callers, consumers, migration path, and reason for existence. Change it only when the smallest test shows the requested outcome improves without violating a higher-priority condition.

**Suggested replacement for the current slogan:** “Challenge inherited practice by tracing its purpose and evidence. Keep mathematical and physical limits, empirically verify estimates, check legal/security duties for applicability, and test conventions against their compatibility and coordination costs. State uncertainty and a result that could change the decision.”

## Risks and limits

- A category checklist can become boilerplate. Require it only for material premises; use a short ledger, not a mandatory essay.
- “Falsifiable” does not mean every preference or legal interpretation can be tested like a physics hypothesis. Use the right challenge for the category: explicit owner/source, counterexample, experiment, or applicability review.
- Agents can misuse formal language to make guesses sound proven. Require provenance and confidence beside claims, and distinguish a proof within a model from evidence that the model fits the task.
- Deconstruction can expand scope or encourage replacement of established interfaces. Preserve the user’s outcome and safeguards, inspect consumers, and compare reversal costs before proposing change.
- This note does not assess the full skill library or the exact implementation cost of applying the mechanism to each skill. Skill owners should choose the smallest set of call sites after reviewing their own contracts.

## Sources

1. Aristotle, *Posterior Analytics*, Book II, Chapter 19, MIT Internet Classics Archive, translation by G. R. G. Mure. Primary text.
2. René Descartes, *Discourse on the Method*, Part IV, Project Gutenberg edition. Primary text.
3. Richard P. Feynman, “Cargo Cult Science,” Caltech commencement address (1974), Caltech Library. Primary text.
4. Karl Popper, “Science: Conjectures and Refutation,” lecture (1953), reproduced in source PDF. Primary text; hosted copy is not an official publisher site.
5. Claude E. Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal* 27 (1948), Wiley and Yale-hosted scan. Primary paper.
6. NIST, SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1* (2022). Official standard.
7. European Parliament and Council, Regulation (EU) 2016/679, official EUR-Lex text. Primary legal text.

**Status: DONE.** The evidence note is saved at `docs/research/2026-10-14-first-principles-evidence.md`. Seven primary/authoritative sources were consulted; claims and source limits are distinguished. No skill or generated file was edited. No tests apply to this research-only document.
