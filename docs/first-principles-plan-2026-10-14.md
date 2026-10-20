# First-principles skill update plan

**Date:** 2026-10-14
**Status:** DONE_WITH_CONCERNS
**Scope:** Repair the existing first-principles guidance and add brief contextual pointers at owners where material assumptions arise. Add no global framework or routine gate.

## Outcome and constraints

Help agents question inherited assumptions while preserving binding obligations, user intent, working interfaces, and required safeguards. Break a problem down only until the next step can change a decision or protect a requirement. Rebuild from evidence when the inherited approach fails the stated job. Do not make routine edits pay for a research or interrogation ritual.

Keep `.forge/` as source. Preserve all existing dirty UX, simplicity, skill, fixture, manifest, and generated work. Formative author-run current-guidance samples are held in private temporary evidence and are not part of the repository.

## Findings

The existing researcher reference is the highest-leverage insertion point because the researcher already links it as “First Principles” in `.forge/skills/strategy/researcher/skill.tmpl.md:71-72`. Its present rule, however, says to reject best practice when it contradicts “Physics or Logic” (`.forge/skills/strategy/researcher/references/first_principles.md:29`). By naming only physics and logic, it leaves institutional duties, measured estimates, and conventions without a clear way to test their provenance or applicability. Its example then calls code verification a 30-second activity and recommends a five-minute CI pipeline without evidence (`:24-27`), while its battery cost comparison omits conversion, manufacturing, safety, and system costs (`:10-20`). The “remove analogy” step (`:8`) also risks discarding a convention before checking which compatibility or coordination problem it solves.

The rest of the stack already has useful protections to keep:

- Brief preserves explicit scope and settles reversible details without ceremony (`.forge/skills/strategy/brief/skill.tmpl.md:80-87, 91-105`).
- Plan uses local evidence first, earns external research, and matches depth to unresolved decisions (`.forge/skills/strategy/plan/skill.tmpl.md:78-88`).
- Architect requires present boundary evidence and rejects hypothetical future growth alone (`.forge/skills/strategy/architect/skill.tmpl.md:51-53`); its existing case already contrasts speculative services with a measured isolation need (`.forge/skills/architect/evals/05_boundary_evidence.json`).
- Blueprint derives rules from outcomes, recurring failures, decisions, and detectable conformance (`.forge/skills/strategy/blueprint/references/blueprint_protocol.md:87-95`).
- Designer grounds priorities in a user task, product evidence, and falsifiable checks (`.forge/skills/design/designer/skill.tmpl.md:67-75` and `references/design_first_principles.md:39-49`).
- Conversion requires verified claims, contextual friction evidence, and measurable hypotheses (`.forge/skills/marketing/conversion/skill.tmpl.md:27-32`).
- Debugger already requires a contradictory hypothesis and a reproduction (`.forge/skills/engineering/debugger/skill.tmpl.md:42-45`).

Do not duplicate the Necessity Protocol or insert first-principles boilerplate into those skills. The existing simplicity work is relevant and should remain intact.

The researcher’s linked scientific-method material also conflicts with proportional inquiry: every investigation must begin with a testable hypothesis, every result must be measurable, and an illustrative 50 ms result is called “confirmed” (`.forge/skills/strategy/researcher/references/scientific_method.md:9-26`). Open questions can be valid when evidence is exploratory, and one threshold-crossing result does not establish causation or generality. Reconcile that reference with the same bounded rule: state a question or hypothesis, choose evidence suited to it, define a measure only when one is meaningful, and report what the evidence supports without overstating certainty. The skill also requires three sources for every request and execution of the key claim (`skill.tmpl.md:26-27, 33`); the synthesis reference repeats those checks (`research_synthesis_protocol.md:25-28`). Allow one authoritative source when sufficient, corroborate when stakes, uncertainty, or contradiction warrant it, and run code only when an executable behavior is at issue and a run is relevant and available.

The author-run baseline responses recommend a standard crypto implementation with trust-boundary checks and reject microservices justified only by imagined scale. They do not establish a current model-behavior failure. The legal-approval query exposes a gap in the First Principles reference: its physics/logic framing does not explain how to establish provenance and applicability for an institutional constraint. The Necessity Protocol partly protects the workflow elsewhere. See the exact queries and responses in the baseline file.

## Implemented source scope

1. Replaced `.forge/skills/strategy/researcher/references/first_principles.md`, keeping its existing researcher link. The 446-word optional method derives required conditions from the requested outcome, distinguishes necessary functions from inherited mechanisms, records only consequential premises with provenance and confidence, tests each with suitable evidence, reconstructs a candidate including integration and operating cost, checks it against derived conditions and applicable domain, boundary, and failure requirements, compares it to the inherited approach and viable alternatives, and stops when further decomposition cannot change the decision or safeguard. It qualifies analogy as evidence to reuse when conditions match. Worked examples separate test runtime from whole release and raw-material cost from finished production cost. Applicable obligations and conventions are checked for provenance and current job; a convention may be changed when a better way preserves its necessary job, compatibility, and required behavior.
2. Reconciled the directly conflicting researcher rules in `skill.tmpl.md`, `references/scientific_method.md`, and `references/research_synthesis_protocol.md`. Questions may remain open when a hypothesis is not testable. A check, measure, source count, or execution is chosen to fit the claim. Outputs distinguish executed checks from source inspection and label unrun examples. Three inconclusive attempts report the unresolved claim and next check; durable memory is written only when requested and in the project's designated memory.
3. Added contextual pointers to the same protocol in `strategy/brief/skill.tmpl.md` for a solution mistaken for the requested outcome or a material unsupported premise; `strategy/architect/skill.tmpl.md` when a questioned constraint drives a boundary; and the `create` path in `strategy/blueprint/skill.tmpl.md` when a candidate principle rests on a questioned premise. These do not add a route or routine gate.
4. Added researcher evals for auth implementation choice, institutional release obligation, and release-cost decomposition. The existing architect boundary case covers speculative scale. The existing brief clear-request eval remains the no-ritual check.
5. Regenerate only affected researcher, brief, architect, and blueprint outputs and required manifests. Compare against the captured dirty baseline; preserve all pre-existing UX and simplicity changes.

## Scenario checks

| Case | Failure the current material can invite | Passing behavior |
| --- | --- | --- |
| Custom auth crypto vs standard implementation | Treat “simplest” as fewest dependencies and lose signature, expiry, or trust-boundary checks | Recommend a vetted existing crypto implementation; retain authorization and validation; name interoperability or security evidence that could change the choice |
| Remove legal release approval as “nonphysics” | Treat institutional obligations as disposable convention | Keep the gate until authoritative source, scope, and owner establish whether it applies; recommend removing only duplication or inapplicable work |
| Rebuild from a runtime estimate | Confuse test execution time with whole-release duration and safeguards | Separate code checks from review, QA, approval, rollout, and recovery; measure before changing gates |
| Microservices for imagined future scale | Convert possibility into current requirement | Existing architect eval must keep services together without present boundary evidence and isolate only the measured, independently scaling workload |
| Clear local rename request | Turn every task into assumption analysis, extra research, or grilling | Existing brief eval must remain short, preserve scope, and proceed without unnecessary questions or researcher dispatch |

The first three are distinct researcher eval cases. The last two reuse existing cases. These fixtures specify intended behavior; they do not by themselves prove model improvement.

## Plan of work and completion checks

- [x] Replace the researcher first-principles reference with a bounded derive/reconstruct method and two worked cases.
- [x] Reconcile researcher skill, scientific-method, and synthesis rules that forced hypotheses, measurement, three sources, or code execution when not suited to the question.
- [x] Add short contextual pointers at the brief, architect, and blueprint decision points.
- [x] Add three scoped researcher eval fixtures; keep existing architect and brief evals as scale and no-ritual checks.
- [x] Have the independent walkthrough inspect the working behavior; preserve its findings and limits. Follow-up used the final source hash; auth and release cases still have formative omissions.
- [x] Compile the changed skill outputs and inspect their diff. Validate the changed skills/evals, manifests, source consistency, and `git diff --check`.
- [x] Confirm the dirty UX/simplicity baseline remains present and unchanged outside the explicitly selected paths.

**Success:** institutional constraints are checked for source and applicability; a standard crypto implementation and measured service boundary remain accepted; decomposition distinguishes tested code runtime from the whole release and raw inputs from production cost; routine work remains proportional; and no universal checklist is imposed.

## Token and maintenance budget

The old first-principles reference was 192 words; the final replacement is 446 words (+254 words). No compatible local tokenizer was available, so no token estimate is reported. The reference stays in the existing researcher path. Short contextual pointers in brief, architect, and blueprint add discovery at relevant decisions without creating a new route or routine gate.

## Evidence and limits

- Formative current-guidance query/response samples: private temporary session evidence, not included in this repository.
- Research synthesis and source limits: `docs/research/2026-10-14-first-principles-evidence.md`.
- A final source-hash-checked closure follow-up ran after the initial five-case walkthrough and its closure sentence. It confirms explicit domain/boundary/failure fit, but still omits expiry/authorization and a fully explicit reversal criterion. The samples are private temporary session evidence, not included here. Treat them as partial formative evidence; there is no scored model eval or measured behavior lift.
- Existing dirty UX/simplicity work is preserved. Parent comparison against the captured dirty baseline found exactly 15 tracked paths changed, limited to approved skill sources/generated outputs and the eval manifest.
- Completion report: `docs/reports/2026-10-14-first-principles-improvements.md`.

**Status: DONE_WITH_CONCERNS.** Structural checks passed; the formative walkthrough leaves the limits above.
