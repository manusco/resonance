# First-principles reasoning update

**Status: DONE_WITH_CONCERNS**
**Date:** 2026-10-14

## What changed

The researcher’s existing First Principles reference now gives an optional method for material decisions. It derives needed conditions from the requested outcome, separates necessary functions from inherited mechanisms, checks premise provenance and applicability, reconstructs a candidate with integration and operating costs, compares alternatives, and stops when further decomposition cannot change the decision or safeguard. It qualifies analogy as evidence to reuse when conditions match. Its examples separate code-check runtime from full release time and raw-material cost from finished-system cost.

The researcher’s linked skill, scientific-method, and synthesis guidance now accepts open questions when no testable hypothesis is available. It matches source count, measurement, and code execution to the claim. Reports distinguish execution from source inspection and mark unrun examples. After three inconclusive verification attempts, the researcher reports the blocker and next check; it writes durable memory only when requested and to the designated project memory.

Brief, architect, and blueprint now point to the same protocol at the decision points where a solution may be mistaken for a goal, a questioned constraint may drive an architecture boundary, or a questioned premise may underpin a principle. The pointers add no new route or routine gate.

Three researcher fixtures cover custom crypto versus an existing implementation, a legal release approval, and decomposition of release time. The existing architecture fixture covers speculative service boundaries; the existing brief fixture covers a clear local edit without extra ceremony.

## Evidence and limits

The author-run pre-change recommendations already handled the auth and speculative-scale cases well. They did not demonstrate a model failure. The legal-approval query exposed that the old reference named physics and logic but gave no method to establish institutional constraints' provenance and applicability. The old reference also used unsupported battery-cost and CI-runtime arithmetic as worked examples.

A review of five source-hash-checked synthetic walkthrough answers found that candidate reconstruction lacked an explicit closure check. The protocol gained one generic check against derived conditions and applicable domain, boundary, and failure requirements. The initial five answers predate that sentence. A source-hash-checked follow-up against the final reference explicitly checks domain, boundary, and failure fit in the auth case, but still does not name expiry or authorization. The release answer distinguishes the supplied 30-second runtime from other release stages and notes causal and safety limits, but leaves a fully explicit reversal criterion unstated. The runtime was supplied by the query, not independently measured. The samples are private temporary session evidence, not included here. This is partial formative evidence, not a scored eval or production evidence. No model lift claim is made.

The new first-principles reference is 446 words, up from 192, a 254-word increase. No compatible local tokenizer was available to measure token delta, so this report gives the exact word-count change and no token estimate.

## Verification

- `python3 .forge/validate_library.py`: PASS, 73 skills, 0 errors, 0 warnings.
- `python3 .forge/validate_skill.py --strict` on researcher, brief, architect, and blueprint: PASS, 0 errors and warnings for each.
- `python3 .forge/run_evals.py strategy/researcher --check`: PASS, 7 fixture structures, no model run.
- `python3 .forge/eval_integrity.py`: PASS, 467 oracle files, 0 problems.
- Forge dry runs for all four affected skills: PASS, generated outputs fresh.
- `python3 .forge/tests/run.py`: PASS, 324 tests, 1 skipped because PowerShell is unavailable.
- `git diff --check`: PASS.
- After the final generic closure sentence, researcher strict validation, its Forge dry run, and `git diff --check` passed again.

The parent agent compared the tracked changes with the captured session baseline: 15 expected paths changed, confined to the four owner skills and generated counterparts plus the eval manifest. Existing UX and simplicity edits remain intact. No version bump, commit, or release was made.
